# Pace narration for follow-along: insert silence between STE sentences, align
# caption words to the exact STE script text. Reads raw TTS from .media/voice-raw.
import json, re, wave, difflib
TARGET = {1:6.0, 2:6.5, 3:6.5, 4:5.0, 5:8.0, 6:15.0, 7:17.5, 8:18.0, 9:6.0, 10:5.0}
LEAD, MAX_GAP = 0.3, 1.6
import array as _arr
_peak = max(max(abs(x) for x in _arr.array('h', wave.open('.media/voice-raw/%02d.wav' % n).readframes(10**8))) for n in range(1, 11))
GAIN = 0.708 * 32767 / _peak   # all lines peak at -3 dBFS, same gain for every frame
NUM = {'1':'one','2':'two','3':'three','4':'four','8':'eight'}
sb = open('STORYBOARD.md').read()
vo = {int(n): t for n, t in re.findall(r'## Frame (\d+) .*?- voiceover: "(.*?)"', sb, re.S)}
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
meta = json.load(open('.media/voice-raw/audio_meta.raw.json')); eng = json.load(open('audio_engine_meta.json'))
for v in meta['voices']:
    f = v['frame']; S = vo[f].split()
    units = []
    for w in v['words']:
        t = w['text']; n = norm(t)
        if t.endswith('%'):
            mid = (w['start'] + w['end']) / 2
            units += [(norm(t[:-1]), w['start'], mid), ('percent', mid, w['end'])]
        else:
            units.append((NUM.get(n, n), w['start'], w['end']))
    Sn = [norm(s) for s in S]; Wn = [u[0] for u in units]
    times = [None] * len(S)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, Sn, Wn, autojunk=False).get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1): times[i1 + k] = units[j1 + k][1:]
        elif op in ('replace', 'insert'):
            if j2 > j1: a, b = units[j1][1], units[j2 - 1][2]
            else:
                a = units[j1 - 1][2] if j1 > 0 else 0.0
                b = units[j1][1] if j1 < len(units) else a + 0.3
            n = i2 - i1
            for k in range(n): times[i1 + k] = (a + (b - a) * k / n, a + (b - a) * (k + 1) / n)
    # sentence cut points
    cuts = [(times[i][1] + times[i + 1][0]) / 2 for i in range(len(S) - 1) if S[i][-1] in '.:']
    src = wave.open('.media/voice-raw/%02d.wav' % f); p = src.getparams(); fr = p.framerate
    raw = src.readframes(p.nframes); src.close(); D = p.nframes / fr
    extra = max(0.0, TARGET[f] - D - LEAD)
    tail = min(0.8, extra) if cuts else extra
    gap = min(MAX_GAP, (extra - tail) / len(cuts)) if cuts else 0.0
    tail = max(0.0, extra - gap * len(cuts))
    import array, math
    smp = array.array('h', raw)
    smp = array.array('h', [int(x * GAIN) for x in smp])
    # find the real pause at each sentence break: the longest silent run (10 ms frames,
    # mean |x| < 150) between the start of the word before and the end of the word after
    STEP = int(0.01 * fr)
    def silent_run(t0, t1):
        a0, a1 = int(t0 * fr), int(t1 * fr)
        best = None; run = None
        for k in range(a0, a1, STEP):
            e = sum(abs(smp[j]) for j in range(k, min(k + STEP, len(smp)))) / STEP
            if e < 300 * GAIN:
                run = (run[0], k + STEP) if run else (k, k + STEP)
                if best is None or run[1] - run[0] > best[1] - best[0]: best = run
            else:
                run = None
        return best if best and best[1] - best[0] >= int(0.15 * fr) else None
    cut_i = []
    for i in [i for i in range(len(S) - 1) if S[i][-1] in '.:']:
        r = silent_run(times[i][0], times[i + 1][1])
        if not r:
            print('   frame', f, 'no pause after', S[i], '- no gap here'); continue
        c = (r[0] + r[1]) // 2; cut_i.append(c)
        # snap caption timing to the real pause
        times[i] = (times[i][0], min(times[i][1], r[0] / fr))
        times[i + 1] = (max(times[i + 1][0], r[1] / fr), max(times[i + 1][1], r[1] / fr + 0.05))
    cuts = [ci / fr for ci in cut_i]
    if cuts:
        tail = min(0.8, extra); gap = min(MAX_GAP, (extra - tail) / len(cuts)); tail = max(0.0, extra - gap * len(cuts))
    else:
        gap, tail = 0.0, extra
    FADE = int(0.015 * fr)
    def fade(seg, fin, fout):
        seg = array.array('h', seg); n = len(seg)
        for j in range(min(FADE, n)):
            g = 0.5 - 0.5 * math.cos(math.pi * j / FADE)
            if fin: seg[j] = int(seg[j] * g)
            if fout: seg[n - 1 - j] = int(seg[n - 1 - j] * g)
        return seg
    sil = lambda s: array.array('h', [0]) * int(round(s * fr))
    edges = [0] + cut_i + [len(smp)]
    out = sil(LEAD)
    for k in range(len(edges) - 1):
        seg = fade(smp[edges[k]:edges[k + 1]], k > 0, k < len(edges) - 2)
        out += seg
        out += sil(gap if k < len(edges) - 2 else tail)
    out = out.tobytes()
    w = wave.open('assets/voice/%02d.wav' % f, 'wb'); w.setparams(p); w.writeframes(out); w.close()
    def shift(t):
        return t + LEAD + gap * sum(1 for c in cuts if t > c)
    v['words'] = [{'id': 'w%d' % k, 'text': S[k], 'start': round(shift(a), 3), 'end': round(shift(b), 3)} for k, (a, b) in enumerate(times)]
    v['duration_s'] = round(len(out) / 2 / fr, 3)
    for ev in eng['voices']:
        if int(ev['id']) == f: ev['words'] = v['words']; ev['duration_s'] = v['duration_s']
    print(f, 'raw %.2f -> %.2f' % (D, v['duration_s']), 'gaps %d x %.2f' % (len(cuts), gap), 'tail %.2f' % tail)
# caption override (user, frame 10): the last caption is only the URL (title already says "Make your zine."), no trailing period
for v in meta['voices']:
    if v['frame'] == 10:
        v['words'] = [w for w in v['words'] if w['text'] not in ('Make', 'your', 'zine', 'at')]
        for w in v['words']:
            if w['text'] == 'zine.imurph.com.': w['text'] = 'zine.imurph.com'
        for ev in eng['voices']:
            if int(ev['id']) == 10: ev['words'] = v['words']
# keep the sound bed: the raw copy predates the MusicGen track
meta['bgm'] = {'path': 'assets/bgm/track.wav', 'volume': 0.12, 'query': None, 'duration_s': 93.5}
meta['bgm_pending'] = False
eng['bgm'] = {'path': 'assets/bgm/track.wav', 'volume': 0.12, 'mode': 'detached-seed-loop', 'duration_s': 93.5}
eng['bgm_pending'] = False
eng['total_duration_s'] = round(sum(v['duration_s'] for v in meta['voices']), 3)
json.dump(meta, open('audio_meta.json', 'w'), indent=2); json.dump(eng, open('audio_engine_meta.json', 'w'), indent=2)
print('total', eng['total_duration_s'])
