#!/usr/bin/env python3
"""Generate compositions/frames/NN-*.html for "How to make a zine".

One generator so the sheet, task card and paper components are identical in
every frame. Each output is a standalone <template> sub-composition (fonts,
styles, GSAP load and one paused timeline inside the template). The token "§"
is replaced with the frame's class/id prefix (e.g. "f06-").
Coordinates are px on a 1920x1080 canvas; content stays above y=896 (captions).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "compositions", "frames")
os.makedirs(OUT, exist_ok=True)

sb = open(os.path.join(ROOT, "STORYBOARD.md")).read()
DUR = {int(n): float(d) for n, d in re.findall(r"## Frame (\d+) .*?- duration: ([\d.]+)s", sb, re.S)}

FONTS = """
@font-face{font-family:'Newsreader';font-style:normal;font-weight:400;src:url('assets/fonts/Newsreader-normal-400.woff2') format('woff2');}
@font-face{font-family:'Newsreader';font-style:normal;font-weight:600;src:url('assets/fonts/Newsreader-normal-600.woff2') format('woff2');}
@font-face{font-family:'Newsreader';font-style:italic;font-weight:400;src:url('assets/fonts/Newsreader-italic-400.woff2') format('woff2');}
@font-face{font-family:'Public Sans';font-style:normal;font-weight:400;src:url('assets/fonts/PublicSans-normal-400.woff2') format('woff2');}
@font-face{font-family:'Public Sans';font-style:normal;font-weight:600;src:url('assets/fonts/PublicSans-normal-600.woff2') format('woff2');}
@font-face{font-family:'Public Sans';font-style:normal;font-weight:700;src:url('assets/fonts/PublicSans-normal-700.woff2') format('woff2');}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;src:url('assets/fonts/IBMPlexMono-normal-400.woff2') format('woff2');}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:600;src:url('assets/fonts/IBMPlexMono-normal-600.woff2') format('woff2');}
"""

BASE_CSS = """
#root{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;font-family:'Public Sans',sans-serif;color:#17221d;}
.§bg{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#f3f0e9;}
.§a{position:absolute;}
.§kick{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:24px;letter-spacing:.16em;text-transform:uppercase;color:#b8501f;}
.§kick-m{color:#5a655f;}
.§disp{font-family:'Newsreader',serif;font-weight:400;letter-spacing:-.022em;line-height:1.02;margin:0;}
.§mono{font-family:'IBM Plex Mono',monospace;}
.§paper{background:#ffffff;}
.§shadow{box-shadow:0 2px 6px rgba(23,34,29,.08),0 23px 50px -19px rgba(23,34,29,.32);}
.§p3d{transform-style:preserve-3d;}
.§face{position:absolute;left:0;top:0;width:100%;height:100%;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#fff;}
.§grid{position:absolute;left:0;top:0;width:100%;height:100%;display:grid;}
.§cellp{position:relative;display:flex;align-items:center;justify-content:center;font-family:'Newsreader',serif;color:#17221d;}
.§up > *{transform:rotate(180deg);}
.§shade{position:absolute;left:0;top:0;width:100%;height:100%;background:#17221d;opacity:0;}
.§task{position:absolute;background:#fdfaf4;border:1.5px solid #ddd8cd;border-radius:17px;box-shadow:0 19px 46px -27px rgba(23,34,29,.38);overflow:hidden;}
.§task-hd{padding:21px 29px 17px;border-bottom:1.5px solid #ddd8cd;}
.§task-hd span{display:block;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px;letter-spacing:.16em;color:#b8501f;}
.§task-hd h3{margin:4px 0 0;font-family:'Newsreader',serif;font-weight:600;font-size:40px;letter-spacing:-.01em;line-height:1.1;}
.§task ol{margin:0;padding:17px 29px 19px 63px;display:grid;gap:5px;font-size:21px;line-height:1.3;color:#5a655f;}
.§task li{padding:3px 10px;margin-left:-10px;border-radius:8px;background:rgba(251,230,218,0);}
.§task li::marker{font-family:'IBM Plex Mono',monospace;font-size:18px;color:#5a655f;}
.§notice{margin:0 29px 17px;padding:14px 19px;border-radius:13px;font-size:21px;line-height:1.3;}
.§notice b{display:block;font-family:'IBM Plex Mono',monospace;font-size:17px;letter-spacing:.16em;margin-bottom:2px;}
.§caution{background:#fbf0d2;border:1.5px solid #e2bb5c;color:#7f5600;}
.§note{background:#fbe6da;border:1.5px solid #f1c9b1;color:#17221d;}
.§note b{color:#ae4c1d;}
"""

def wrap(fid, n, css, body, js):
    p = "f%02d-" % n
    dur = DUR[n]
    html = f"""<template>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>{FONTS}{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{fid}" data-width="1920" data-height="1080" data-duration="{dur}">
    <div id="§ground" class="§bg clip" data-start="0" data-duration="{dur}" data-track-index="0"></div>
{body}
  </div>
  <script>
  (function () {{
    var D = {dur};
    var q = function (s) {{ return document.querySelector('[data-composition-id="{fid}"] ' + s); }};
    var qa = function (s) {{ return Array.prototype.slice.call(document.querySelectorAll('[data-composition-id="{fid}"] ' + s)); }};
    var tl = gsap.timeline({{ paused: true }});
    // Step-card highlighter: each entry [stepIds[], time]; the previous active rows go "past".
    function steps(seq) {{
      var prev = [];
      seq.forEach(function (e) {{
        var t = e[1];
        prev.forEach(function (id) {{
          tl.fromTo(q('#§' + id), {{ backgroundColor: 'rgba(251,230,218,1)', color: '#17221d' }},
            {{ backgroundColor: 'rgba(251,230,218,0)', color: '#6f7572', duration: 0.3, ease: 'power2.out', immediateRender: false }}, t);
        }});
        e[0].forEach(function (id) {{
          tl.fromTo(q('#§' + id), {{ backgroundColor: 'rgba(251,230,218,0)', color: '#5a655f' }},
            {{ backgroundColor: 'rgba(251,230,218,1)', color: '#17221d', duration: 0.3, ease: 'power2.out' }}, t);
        }});
        prev = e[0];
      }});
    }}
{js}
    tl.set({{}}, {{}}, D);
    window.__timelines = window.__timelines || {{}};
    window.__timelines["{fid}"] = tl;
  }})();
  </script>
</template>
"""
    html = html.replace("§", p)
    open(os.path.join(OUT, fid + ".html"), "w").write(html)
    print("wrote", fid, dur)

# ---------- shared components ----------
TOP = ["5", "4", "3", "2"]
BOT = ["6", "7", "8", "1"]

def panels(nums_top, nums_bot, size, faint=False, labels=False, extra=None):
    """8-panel grid with dashed guides. Top row upside down."""
    op = "opacity:.28;" if faint else ""
    cells = []
    for i, n in enumerate(nums_top + nums_bot):
        top = i < 4
        bd = []
        if i % 4 != 3: bd.append("border-right:3px dashed #b4b4b4")
        if top: bd.append("border-bottom:3px dashed #b4b4b4")
        lab = ""
        if labels and n in ("8", "1"):
            lab = f'<small class="§mono" style="display:block;font-size:{int(size*0.42)}px;color:#6a6a6a;letter-spacing:.04em;text-align:center">{"BACK" if n=="8" else "FRONT"}</small>'
        content = (extra or {}).get(n, f'<span style="{op}">{n}{lab}</span>' if not lab else f'<span style="{op};text-align:center">{n}{lab}</span>')
        cells.append(f'<div class="§cellp {"§up" if top else ""}" style="{";".join(bd)};font-size:{size}px">{content}</div>')
    return '<div class="§grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,1fr)">' + "".join(cells) + "</div>"

def task_card(idp, label, title, items, caution_before=None, note=None, start=1, style="", fs=21):
    """items: list of step strings. caution_before: 1-based step number the CAUTION precedes."""
    html = [f'<div class="§task" id="§{idp}card" style="{style}"><div class="§task-hd"><span>{label}</span><h3>{title}</h3></div>']
    def ol(a, b):
        lis = "".join(f'<li id="§{idp}s{k}">{items[k-1]}</li>' for k in range(a, b + 1))
        return f'<ol start="{a}" style="font-size:{fs}px">{lis}</ol>' if a <= b else ""
    if caution_before:
        html.append(ol(1, caution_before - 1))
        html.append(f'<p class="§notice §caution" id="§{idp}caution"><b>CAUTION</b>Do not cut past the first vertical fold line. If the cut is too long, the zine will come apart.</p>')
        html.append(ol(caution_before, len(items)).replace("<ol ", '<ol style="padding-top:0" ', 1).replace('style="padding-top:0" start', 'start'))
    else:
        html.append(ol(1, len(items)))
    if note:
        html.append(f'<p class="§notice §note"><b>NOTE</b>{note}</p>')
    html.append("</div>")
    return "".join(html)

def book(style, title="My first zine", arch=True):
    a = '<div class="§a" style="left:26px;right:26px;bottom:28px;height:96px;border:2.5px solid #17221d;border-radius:50% 50% 0 0/60% 60% 0 0;opacity:.5"></div>' if arch else ""
    return (f'<div class="§a §paper" style="{style};border-left:10px solid #ece7dc;padding:31px 25px;'
            f'box-shadow:12px 17px 35px -19px rgba(23,34,29,.45)">'
            f'<div class="§kick §kick-m" style="font-size:15px">Page 1 · Front</div>'
            f'<div class="§disp" style="font-size:46px;margin-top:19px">{title.replace(" zine","<br>zine") if title=="My first zine" else title}</div>{a}</div>')

# ======================================================================
# 01 — hook: a flat sheet folds into a small book
# ======================================================================
def f01():
    W, H = 576, 445
    L, T = 118, 214
    body = f"""
    <div class="§a" id="§ghost" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;transform:rotate(-4deg);transform-origin:504px 111px;opacity:0">
      <div class="§a §paper §shadow" style="left:0;top:0;width:100%;height:100%">{panels(['']*4, ['']*4, 20)}</div>
    </div>
    <div class="§a" id="§arrow" style="left:733px;top:406px;font-family:'IBM Plex Mono';font-size:58px;color:#d86b3c;opacity:0">→</div>
    <div class="§a" id="§sheetw" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;perspective:2400px">
      <!-- A: full sheet, bottom row folds up -->
      <div class="§a §p3d" id="§A" data-layout-allow-overlap style="left:0;top:0;width:{W}px;height:{H}px">
        <div class="§a §paper §shadow" style="left:0;top:0;width:{W}px;height:{H//2}px">{panels(['']*4, [], 20).replace('repeat(2,1fr)','1fr')}</div>
        <div class="§a §p3d" id="§Aflap" data-layout-allow-overlap style="left:0;top:{H//2}px;width:{W}px;height:{H - H//2}px;transform-origin:50% 0%">
          <div class="§face">{panels([], ['']*4, 20).replace('repeat(2,1fr)','1fr')}<div class="§shade" id="§Ashade"></div></div>
          <div class="§face" style="transform:rotateX(180deg)"></div>
        </div>
      </div>
      <!-- B: top half, left two columns fold right -->
      <div class="§a §p3d" id="§B" data-layout-allow-overlap style="left:0;top:0;width:{W}px;height:{H//2}px;opacity:0">
        <div class="§a §paper §shadow" style="left:{W//2}px;top:0;width:{W//2}px;height:{H//2}px"></div>
        <div class="§a §p3d" id="§Bflap" data-layout-allow-overlap style="left:0;top:0;width:{W//2}px;height:{H//2}px;transform-origin:100% 50%">
          <div class="§face"><div class="§shade" id="§Bshade"></div></div><div class="§face" style="transform:rotateY(180deg)"></div>
        </div>
      </div>
      <!-- C: last fold, column 3 onto column 4 -> one panel -->
      <div class="§a §p3d" id="§C" data-layout-allow-overlap style="left:{W//2}px;top:0;width:{W//2}px;height:{H//2}px;opacity:0">
        <div class="§a §paper §shadow" style="left:{W//4}px;top:0;width:{W//4}px;height:{H//2}px"></div>
        <div class="§a §p3d" id="§Cflap" data-layout-allow-overlap style="left:0;top:0;width:{W//4}px;height:{H//2}px;transform-origin:100% 50%">
          <div class="§face"><div class="§shade" id="§Cshade"></div></div><div class="§face" style="transform:rotateY(180deg)"></div>
        </div>
      </div>
    </div>
    {book("left:848px;top:157px;width:288px;height:442px;opacity:0", ).replace('class="§a §paper"', 'id="§book" class="§a §paper"', 1)}
    <div class="§a" style="left:1226px;top:166px;width:614px">
      <div class="§kick" id="§kick"><span class="§w">One sheet</span> <span class="§w">· One cut</span> <span class="§w">· Eight pages</span></div>
      <h2 class="§disp" style="font-size:123px;margin-top:23px"><span id="§t1" style="display:block">How to make</span><span id="§t2" style="display:block">a zine</span></h2>
    </div>"""
    css = ".§w{display:inline-block}"
    # panel (col 4, top half) local centre = (504,111); book centre = (992,378); sheet centre-of-origin screen = (118+504, 214+111)
    js = """
    // Scene 1: sheet settles
    tl.fromTo(q('#§sheetw'), {transformOrigin:'504px 111px', y:-40, opacity:0, rotation:-4}, {transformOrigin:'504px 111px', y:0, opacity:1, rotation:-4, duration:0.9, ease:'power3.out'}, 0.1);
    // Scene 2: folds
    tl.fromTo(q('#§ghost'), {opacity:0}, {opacity:0.35, duration:0.4, ease:'power2.out'}, 1.35);
    tl.fromTo(q('#§Aflap'), {rotationX:0}, {rotationX:180, duration:0.6, ease:'power2.inOut'}, 1.4);
    tl.fromTo(q('#§Ashade'), {opacity:0}, {opacity:0.14, duration:0.3, ease:'power1.in'}, 1.4);
    tl.set(q('#§A'), {opacity:0}, 2.02); tl.set(q('#§B'), {opacity:1}, 2.02);
    tl.fromTo(q('#§Bflap'), {rotationY:0}, {rotationY:180, duration:0.5, ease:'power2.inOut'}, 2.05);
    tl.fromTo(q('#§Bshade'), {opacity:0}, {opacity:0.14, duration:0.25, ease:'power1.in'}, 2.05);
    tl.set(q('#§B'), {opacity:0}, 2.57); tl.set(q('#§C'), {opacity:1}, 2.57);
    tl.fromTo(q('#§Cflap'), {rotationY:0}, {rotationY:180, duration:0.45, ease:'power2.inOut'}, 2.6);
    tl.fromTo(q('#§Cshade'), {opacity:0}, {opacity:0.14, duration:0.22, ease:'power1.in'}, 2.6);
    // the single panel lifts into the standing book
    tl.fromTo(q('#§sheetw'), {transformOrigin:'504px 111px', x:0, y:0, scale:1, rotation:-4},
      {transformOrigin:'504px 111px', x:370, y:53, scale:2, rotation:0, duration:0.6, ease:'power3.inOut', immediateRender:false}, 3.08);
    tl.fromTo(q('#§book'), {opacity:0}, {opacity:1, duration:0.3, ease:'power1.out'}, 3.5);
    tl.fromTo(q('#§sheetw'), {opacity:1}, {opacity:0, duration:0.2, ease:'none', immediateRender:false}, 3.62);
    // Scene 3: arrow + kicker
    tl.fromTo(q('#§arrow'), {opacity:0, x:-16}, {opacity:1, x:0, duration:0.5, ease:'power3.out'}, 3.5);
    tl.fromTo(qa('.§w'), {opacity:0, y:10}, {opacity:1, y:0, duration:0.45, ease:'power3.out', stagger:0.14}, 3.7);
    // Scene 4: title on "zine"
    tl.fromTo(q('#§t1'), {opacity:0, y:46}, {opacity:1, y:0, duration:0.7, ease:'power3.out'}, 4.45);
    tl.fromTo(q('#§t2'), {opacity:0, y:46}, {opacity:1, y:0, duration:0.7, ease:'power3.out'}, 4.6);
"""
    wrap("01-hook", 1, css, body, js)

# ======================================================================
# 02 — the procedure: four tiles
# ======================================================================
def f02():
    x0, w, gap, top, h = 80, 417, 31, 168, 518
    def tile(i, num, glyph, word):
        x = x0 + i * (w + gap)
        return (f'<div class="§a §tile" id="§tile{i}" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px">'
                f'<div class="§mono" style="font-size:23px;color:#5a655f">{num}</div>'
                f'<div style="margin:46px 0;height:211px;display:flex;align-items:center;position:relative">{glyph}</div>'
                f'<div class="§disp" style="font-size:84px">{word}</div></div>')
    g_type = ('<div style="display:grid;gap:17px;width:100%">'
              '<i id="§l1" style="display:block;height:27px;width:80%;background:#ddd8cd;border-radius:6px;transform-origin:0 50%"></i>'
              '<i id="§l2" style="display:block;height:27px;width:60%;background:#ddd8cd;border-radius:6px;transform-origin:0 50%"></i>'
              '<i id="§l3" style="display:block;height:27px;width:70%;background:#e2703f;border-radius:6px;transform-origin:0 50%"></i></div>')
    g_print = ('<div style="width:250px;height:193px;overflow:hidden;position:relative">'
               '<div id="§psheet" style="position:absolute;left:0;top:0;width:250px;height:193px;background:#fff;border:2px solid #ddd8cd;box-shadow:0 8px 15px -8px rgba(0,0,0,.3)"></div></div>')
    g_cut = ('<div id="§cline" style="width:250px;height:9px;background:#e2703f;transform-origin:0 50%"></div>'
             '<span id="§sc" style="font-size:69px;margin-left:8px;color:#17221d;display:inline-block">✂</span>')
    g_fold = ('<div style="perspective:900px"><div id="§fbook" style="width:127px;height:192px;background:#fff;border-left:10px solid #ece7dc;'
              'box-shadow:6px 8px 15px -8px rgba(0,0,0,.35);transform-origin:0 50%"></div></div>')
    body = f"""
    <div class="§a §kick" id="§kick" style="left:80px;top:80px">The procedure</div>
    {tile(0,'01',g_type,'Type')}
    {tile(1,'02',g_print,'Print')}
    {tile(2,'03',g_cut,'Cut <span id="§once" class="§mono" style="font-size:29px;color:#b8501f;letter-spacing:.04em">1 time</span>')}
    {tile(3,'04',g_fold,'Fold')}
    <div class="§a" id="§need" style="left:80px;top:812px;font-size:28px;color:#5a655f"><span class="§kick §kick-m" style="font-size:20px;margin-right:19px">Necessary</span>A printer · US Letter paper · Scissors</div>"""
    css = ".§tile{background:#fdfaf4;border:1.5px solid #ddd8cd;border-radius:17px;padding:35px;box-shadow:0 19px 46px -30px rgba(23,34,29,.3)}"
    js = """
    tl.fromTo(q('#§kick'), {opacity:0, y:8}, {opacity:1, y:0, duration:0.5, ease:'power3.out'}, 0.05);
    function rise(id, t) { tl.fromTo(q(id), {opacity:0, y:60}, {opacity:1, y:0, duration:0.6, ease:'power3.out'}, t); }
    rise('#§tile0', 0.25);
    tl.fromTo([q('#§l1'), q('#§l2'), q('#§l3')], {scaleX:0}, {scaleX:1, duration:0.45, ease:'power3.out', stagger:0.15}, 0.55);
    rise('#§tile1', 1.25);
    tl.fromTo(q('#§psheet'), {yPercent:-100}, {yPercent:0, duration:0.6, ease:'power2.inOut'}, 1.5);
    rise('#§tile2', 3.95);
    tl.fromTo(q('#§cline'), {scaleX:0}, {scaleX:1, duration:0.5, ease:'power2.inOut'}, 4.15);
    tl.fromTo(q('#§sc'), {x:-258, opacity:0}, {x:0, opacity:1, duration:0.5, ease:'power2.inOut'}, 4.15);
    tl.fromTo(q('#§once'), {opacity:0}, {opacity:1, duration:0.35, ease:'power1.out'}, 4.5);
    rise('#§tile3', 4.85);
    tl.fromTo(q('#§fbook'), {rotationY:-70}, {rotationY:0, duration:0.6, ease:'power3.out'}, 5.05);
    tl.fromTo(q('#§need'), {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, ease:'power3.out'}, 5.5);
"""
    wrap("02-procedure", 2, css, body, js)

# ======================================================================
# 03 — type your pages: form ↔ sheet preview live sync
# ======================================================================
def f03():
    fld = "border:2px solid #ddd8cd;border-radius:10px;padding:12px 15px;font-size:27px;background:#fff;height:58px;line-height:32px;white-space:nowrap;overflow:hidden"
    body = f"""
    <div class="§a" id="§form" style="left:80px;top:80px;width:691px;height:790px;background:#fdfaf4;border:1.5px solid #ddd8cd;border-radius:17px;padding:27px 31px">
      <div style="display:flex;justify-content:space-between;align-items:center;height:36px">
        <span class="§kick §kick-m" style="font-size:19px">Your pages</span>
        <span class="§mono" id="§url" style="font-size:21px;color:#b8501f;background:#fbe6da;padding:5px 14px;border-radius:99px;border:2px solid rgba(226,112,63,0)">zine.imurph.com</span>
      </div>
      <div style="margin-top:27px;display:grid;gap:19px">
        <div><div class="§mono" style="font-size:18px;color:#5a655f">Page 1 · Front cover</div><div id="§f1" style="{fld};margin-top:6px"><span id="§f1t"></span><span id="§c1" style="color:#e2703f;opacity:0">|</span></div></div>
        <div><div class="§mono" style="font-size:18px;color:#5a655f">Page 2</div><div id="§f2" style="{fld};margin-top:6px"><span id="§f2t"></span><span id="§c2" style="color:#e2703f;opacity:0">|</span></div></div>
        <div><div class="§mono" style="font-size:18px;color:#5a655f">Page 3</div><div style="{fld};margin-top:6px"></div></div>
        <div><div class="§mono" style="font-size:18px;color:#5a655f">Page 4</div><div style="{fld};margin-top:6px"></div></div>
        <div class="§mono" style="font-size:18px;color:#5a655f">… Page 8 · Back cover</div>
      </div>
    </div>
    <div class="§a §paper §shadow" id="§sheet" style="left:1034px;top:99px;width:806px;height:623px">
      {panels(TOP, BOT, 31, faint=True, extra={
        '2': '<span id="§p2" style="font-size:27px;text-align:center;line-height:1.15"><span id="§p2t"></span></span>',
        '1': '<span id="§p1" style="font-size:31px;text-align:center;line-height:1.1"><span id="§p1t"></span></span>'})}
      <div class="§a" id="§o1" style="left:604px;top:311px;width:202px;height:312px;box-shadow:inset 0 0 0 6px #e2703f;opacity:0"></div>
      <div class="§a" id="§o2" style="left:604px;top:0;width:202px;height:311px;box-shadow:inset 0 0 0 6px #e2703f;opacity:0"></div>
    </div>
    <div class="§a" id="§hint" style="left:1034px;top:812px;width:806px;text-align:right;font-size:24px;color:#5a655f">To draw a page by hand, do not type on it.</div>"""
    js = """
    // Scene 2: URL chip on "zine.imurph.com"
    tl.fromTo(q('#§url'), {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.45, ease:'power3.out'}, 0.7);
    tl.fromTo(q('#§url'), {borderColor:'rgba(226,112,63,0)'}, {borderColor:'rgba(226,112,63,1)', duration:0.3, ease:'power1.out'}, 1.15);
    tl.fromTo(q('#§url'), {borderColor:'rgba(226,112,63,1)'}, {borderColor:'rgba(226,112,63,0)', duration:0.6, ease:'power1.in', immediateRender:false}, 1.6);
    // typing helper: field + mirrored panel share one proxy (control-target-sync)
    function type(txt, fieldEl, panelEl, panelHtml, t, dur) {
      var o = {n:0};
      tl.fromTo(o, {n:0}, {n:txt.length, duration:dur, ease:'none', onUpdate:function(){
        var k = Math.round(o.n); fieldEl.textContent = txt.slice(0,k);
        panelEl.innerHTML = panelHtml(txt.slice(0,k)); }}, t);
    }
    tl.fromTo(q('#§f1'), {borderColor:'#ddd8cd'}, {borderColor:'#e2703f', duration:0.2}, 3.85);
    tl.fromTo(q('#§c1'), {opacity:0}, {opacity:1, duration:0.05}, 3.85);
    tl.fromTo(q('#§o1'), {opacity:0}, {opacity:1, duration:0.25, ease:'power1.out'}, 3.85);
    type('My first zine', q('#§f1t'), q('#§p1t'), function(s){ return s.replace('first ', 'first<br>'); }, 3.95, 1.0);
    tl.fromTo(q('#§f1'), {borderColor:'#e2703f'}, {borderColor:'#ddd8cd', duration:0.2, immediateRender:false}, 5.0);
    tl.fromTo(q('#§c1'), {opacity:1}, {opacity:0, duration:0.05, immediateRender:false}, 5.0);
    tl.fromTo(q('#§o1'), {opacity:1}, {opacity:0, duration:0.25, immediateRender:false}, 5.0);
    tl.fromTo(q('#§f2'), {borderColor:'#ddd8cd'}, {borderColor:'#e2703f', duration:0.2}, 5.0);
    tl.fromTo(q('#§c2'), {opacity:0}, {opacity:1, duration:0.05}, 5.0);
    tl.fromTo(q('#§o2'), {opacity:0}, {opacity:1, duration:0.25, ease:'power1.out'}, 5.0);
    type('One sheet. One cut.', q('#§f2t'), q('#§p2t'), function(s){ return s.replace('. ', '.<br>'); }, 5.05, 0.95);
    tl.fromTo(q('#§hint'), {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, ease:'power3.out'}, 5.4);
"""
    wrap("03-type-pages", 3, "", body, js)

# ======================================================================
# 04 — top row upside down
# ======================================================================
def f04():
    W, H = 960, 742
    L, T = 480, 106
    cells = []
    for i, n in enumerate(TOP + BOT):
        top = i < 4
        bd = []
        if i % 4 != 3: bd.append("border-right:3px dashed #b4b4b4")
        if top: bd.append("border-bottom:3px dashed #b4b4b4")
        lab = f'<small class="§mono" style="display:block;font-size:22px;color:#6a6a6a;letter-spacing:.04em">{"BACK" if n=="8" else "FRONT"}</small>' if n in ("8","1") else ""
        idn = f' id="§n{n}"' if top else ""
        cells.append(f'<div class="§cellp" style="{";".join(bd)};font-size:69px"><span{idn} style="display:inline-block;text-align:center">{n}{lab}</span></div>')
    grid = '<div class="§grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,1fr)">' + "".join(cells) + "</div>"
    body = f"""
    <div class="§a §paper §shadow" id="§sheet" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px">{grid}</div>
    <div class="§a" id="§tag" style="left:80px;top:138px;width:269px">
      <div class="§kick" style="line-height:1.5">Top row prints upside down</div>
      <div class="§mono" id="§rot" style="font-size:58px;color:#e2703f;margin-top:12px;display:inline-block">↻</div>
    </div>
    <div class="§a" id="§ok" style="left:1571px;top:690px;width:269px;text-align:right"><div class="§disp" style="font-size:65px;font-style:italic">This is correct.</div></div>"""
    js = """
    tl.fromTo(q('#§sheet'), {scale:0.94, opacity:0.6}, {scale:1, opacity:1, duration:0.5, ease:'power3.out'}, 0);
    tl.fromTo(q('#§tag'), {opacity:0, x:-14}, {opacity:1, x:0, duration:0.5, ease:'power3.out'}, 0.5);
    tl.fromTo(q('#§rot'), {rotation:0}, {rotation:360, duration:1.6, ease:'power2.inOut'}, 0.6);
    ['2','3','4','5'].forEach(function(n, i){
      tl.fromTo(q('#§n'+n), {rotation:0}, {rotation:180, duration:0.55, ease:'power3.inOut'}, 0.75 + i*0.33);
    });
    tl.fromTo(q('#§ok'), {opacity:0, y:16}, {opacity:1, y:0, duration:0.6, ease:'power3.out'}, 3.6);
"""
    wrap("04-sheet-layout", 4, "", body, js)

# ======================================================================
# 05 — print settings
# ======================================================================
def f05():
    rows = [("Paper", "US Letter", 2.4), ("Orientation", "Landscape", 1.5), ("Scale", "100% (Actual size)", 3.8), ("Margins", "None", 5.3)]
    rh = []
    for i, (k, v, _) in enumerate(rows):
        bb = "border-bottom:1.5px solid #ddd8cd;" if i < 3 else ""
        rh.append(f'<div style="display:flex;justify-content:space-between;padding:12px 0;{bb}"><span style="color:#5a655f">{k}</span>'
                  f'<b id="§v{i}" style="font-weight:600;color:#5a655f">{v} <span id="§k{i}" style="color:#949189">✓</span></b></div>')
    card = (f'<div class="§task" style="left:80px;top:80px;width:730px"><div class="§task-hd"><span>PRINT SETTINGS</span><h3>Print the sheet</h3></div>'
            f'<div style="padding:19px 29px 25px;display:grid;gap:4px;font-size:30px">{"".join(rh)}</div></div>')
    W, H = 672, 519
    body = f"""
    {card}
    <div class="§a" id="§keys" style="left:80px;top:842px;font-size:22px;color:#5a655f" ><span class="§mono">⌘ P (Mac) · Ctrl P (Windows)</span></div>
    <div class="§a" style="left:1032px;top:111px;width:{W}px;height:{H+30}px;overflow:hidden">
      <div class="§a §paper §shadow" id="§sheet" style="left:0;top:0;width:{W}px;height:{H}px">{panels(TOP, BOT, 46)}</div>
    </div>
    <div class="§a" style="left:992px;top:80px;width:768px;height:61px;background:#17221d;border-radius:15px"></div>"""
    js = "\n".join(
        f"    tl.fromTo(q('#§k{i}'), {{color:'#949189'}}, {{color:'#c8602f', duration:0.3, ease:'power1.out'}}, {t});\n"
        f"    tl.fromTo(q('#§v{i}'), {{color:'#5a655f'}}, {{color:'#17221d', duration:0.3, ease:'power1.out'}}, {t});"
        for i, (_, _, t) in enumerate(rows))
    js += """
    tl.fromTo(q('#§sheet'), {y:-560}, {y:0, duration:1.5, ease:'power2.inOut'}, 5.8);
    tl.fromTo(q('#§keys'), {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, ease:'power3.out'}, 6.4);
"""
    wrap("05-print", 5, "", body, js)

# ======================================================================
# fold-able sheet (frames 6, 7): A = bottom-row flap, B = left-half flap,
# B2 = column-3 flap. Faces carry faint panel numbers.
# ======================================================================
def fold_sheet(W, H, faint=True, with_c=True):
    half = H // 2
    hw = W // 2
    qw = W // 4
    def rowgrid(nums, up):
        cells = []
        for i, n in enumerate(nums):
            bd = ""
            cells.append(f'<div class="§cellp {"§up" if up else ""}" style="font-size:{int(H*0.075)}px"><span style="opacity:.25">{n}</span></div>')
        return f'<div class="§grid" style="grid-template-columns:repeat({len(nums)},1fr);grid-template-rows:1fr">' + "".join(cells) + "</div>"
    a = f"""
      <div class="§a §p3d" id="§A" data-layout-allow-overlap style="left:0;top:0;width:{W}px;height:{H}px">
        <div class="§a §paper §shadow" style="left:0;top:0;width:{W}px;height:{half}px">{rowgrid(TOP, True)}</div>
        <div class="§a §p3d" id="§Aflap" data-layout-allow-overlap style="left:0;top:{half}px;width:{W}px;height:{H-half}px;transform-origin:50% 0%">
          <div class="§face" style="box-shadow:0 23px 50px -19px rgba(23,34,29,.32)"><div class="§a" id="§Afront" style="left:0;top:0;width:100%;height:100%">{rowgrid(BOT, False)}</div><div class="§shade" id="§Ashade"></div></div>
          <div class="§face" style="transform:rotateX(180deg)"></div>
        </div>
      </div>
      <div class="§a §p3d" id="§B" data-layout-allow-overlap style="left:0;top:0;width:{W}px;height:{H}px;opacity:0">
        <div class="§a §paper §shadow" style="left:{hw}px;top:0;width:{W-hw}px;height:{H}px">
          <div class="§a" style="left:0;top:0;width:100%;height:{half}px">{rowgrid(TOP[2:], True)}</div>
          <div class="§a" style="left:0;top:{half}px;width:100%;height:{H-half}px">{rowgrid(BOT[2:], False)}</div>
        </div>
        <div class="§a §p3d" id="§Bflap" data-layout-allow-overlap style="left:0;top:0;width:{hw}px;height:{H}px;transform-origin:100% 50%">
          <div class="§face" style="box-shadow:0 23px 50px -19px rgba(23,34,29,.32)"><div class="§a" id="§Bfront" style="left:0;top:0;width:100%;height:100%">
            <div class="§a" style="left:0;top:0;width:100%;height:{half}px">{rowgrid(TOP[:2], True)}</div>
            <div class="§a" style="left:0;top:{half}px;width:100%;height:{H-half}px">{rowgrid(BOT[:2], False)}</div></div>
            <div class="§shade" id="§Bshade"></div></div>
          <div class="§face" style="transform:rotateY(180deg)"></div>
        </div>
      </div>"""
    c = f"""
      <div class="§a §p3d" id="§C" data-layout-allow-overlap style="left:{hw}px;top:0;width:{W-hw}px;height:{H}px;opacity:0">
        <div class="§a §paper §shadow" style="left:{qw}px;top:0;width:{W-hw-qw}px;height:{H}px"></div>
        <div class="§a §p3d" id="§Cflap" data-layout-allow-overlap style="left:0;top:0;width:{qw}px;height:{H}px;transform-origin:100% 50%">
          <div class="§face"><div class="§shade" id="§Cshade"></div></div><div class="§face" style="transform:rotateY(180deg)"></div>
        </div>
      </div>""" if with_c else ""
    return a + c

def lines_overlay(W, H, ids):
    """Dashed fold lines drawn over the open sheet."""
    out = []
    if "h" in ids:
        out.append(f'<div class="§a" id="§lh" style="left:0;top:{H//2-1}px;width:{W}px;border-top:3px dashed #b4b4b4;opacity:0"></div>')
    for k, frac in (("v1", .25), ("v2", .5), ("v3", .75)):
        if k in ids:
            out.append(f'<div class="§a" id="§l{k}" style="left:{int(W*frac)-1}px;top:0;height:{H}px;border-left:3px dashed #b4b4b4;opacity:0"></div>')
    return "".join(out)

# ======================================================================
# 06 — Task 1: make the fold lines
# ======================================================================
TASK1 = ["Put the sheet flat, with the printed side up.",
         "Turn the sheet so that the long edges are at the top and the bottom.",
         "Fold the bottom edge up to the top edge.",
         "Push your thumbnail along the fold.",
         "Open the sheet.",
         "Fold the left edge to the right edge.",
         "Fold the sheet in half again. Put the folded edge on the open edges.",
         "Push your thumbnail along each fold.",
         "Open the sheet fully.",
         "Make sure that you have 8 equal panels, in 2 rows of 4."]

def f06():
    W, H = 768, 593
    L, T = 80, 280
    mini = lambda i, w, h, edge, lab, x: (
        f'<div class="§a" id="§m{i}" style="left:{x}px;top:{238 - h - 36}px;text-align:center">'
        f'<div style="width:{w}px;height:{h}px;background:#fff;box-shadow:0 8px 15px -8px rgba(0,0,0,.3);{edge}:4px solid #ddd8cd" id="§me{i}"></div>'
        f'<div class="§mono" id="§ml{i}" style="font-size:17px;color:#9aa29e;margin-top:10px;white-space:nowrap">{lab}</div></div>')
    outl = "".join(
        f'<div class="§a §po" style="left:{int(W/4*(k%4))}px;top:{int(H/2*(k//4))}px;width:{int(W/4)}px;height:{int(H/2)}px;box-shadow:inset 0 0 0 5px rgba(226,112,63,.75);opacity:0"></div>'
        for k in range(8))
    body = f"""
    {mini(1, 192, 74, 'border-top', 'bottom → top', 80)}
    {mini(2, 96, 148, 'border-left', 'left → right', 330)}
    {mini(3, 48, 148, 'border-left', 'again', 520)}
    <div class="§a" id="§sheetw" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;perspective:2600px">
      {fold_sheet(W, H)}
      {lines_overlay(W, H, ("h","v1","v2","v3"))}
      <div class="§a" id="§creaseH" style="left:-14px;top:-14px;width:28px;height:28px;border-radius:50%;background:rgba(226,112,63,.55);opacity:0"></div>
      <div class="§a" id="§creaseV" style="left:{3*W//4-14}px;top:-14px;width:28px;height:28px;border-radius:50%;background:rgba(226,112,63,.55);opacity:0"></div>
      {outl}
    </div>
    <div class="§a" id="§tag" style="left:{L+W+29}px;top:{T+H-110}px;font-family:'IBM Plex Mono';font-size:20px;color:#b44e1e;line-height:1.4">8 equal<br>panels<br>2 rows of 4</div>
    {task_card('', 'TASK 1', 'Make the fold lines', TASK1, style='left:1110px;top:80px;width:730px', fs=19.5)}"""
    js = f"""
    var W={W}, H={H};
    tl.fromTo(q('#§sheetw'), {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.6, ease:'power3.out'}}, 0.05);
    tl.fromTo([q('#§m1'),q('#§m2'),q('#§m3')], {{opacity:0}}, {{opacity:1, duration:0.4, stagger:0.08, ease:'power1.out'}}, 0.2);
    function lightMini(i, t) {{
      tl.fromTo(q('#§me'+i), {{borderColor:'#ddd8cd'}}, {{borderColor:'#e2703f', duration:0.3}}, t);
      tl.fromTo(q('#§ml'+i), {{color:'#9aa29e'}}, {{color:'#17221d', duration:0.3}}, t);
    }}
    steps([[['s1','s2'],0.5],[['s3'],3.0],[['s4'],4.3],[['s5'],5.5],[['s6'],7.1],[['s7'],8.3],[['s8'],9.3],[['s9'],10.5],[['s10'],12.1]]);
    // fold 1: bottom edge to top edge
    lightMini(1, 3.0);
    tl.fromTo(q('#§Aflap'), {{rotationX:0}}, {{rotationX:180, duration:1.0, ease:'power2.inOut'}}, 3.1);
    tl.fromTo(q('#§Ashade'), {{opacity:0}}, {{opacity:0.14, duration:0.5, ease:'power1.in'}}, 3.1);
    tl.set(q('#§Afront'), {{opacity:0}}, 3.6); tl.set(q('#§Afront'), {{opacity:1}}, 5.9);
    // thumbnail along the fold (folded edge is the centre line)
    tl.fromTo(q('#§creaseH'), {{opacity:0, x:0, y:H/2}}, {{opacity:1, duration:0.15}}, 4.3);
    tl.fromTo(q('#§creaseH'), {{x:0}}, {{x:W, duration:0.65, ease:'power2.inOut', immediateRender:false}}, 4.3);
    tl.fromTo(q('#§creaseH'), {{opacity:1}}, {{opacity:0, duration:0.15, immediateRender:false}}, 4.95);
    // open
    tl.fromTo(q('#§Aflap'), {{rotationX:180}}, {{rotationX:0, duration:0.8, ease:'power2.inOut', immediateRender:false}}, 5.5);
    tl.fromTo(q('#§Ashade'), {{opacity:0.14}}, {{opacity:0, duration:0.6, immediateRender:false}}, 5.6);
    tl.fromTo(q('#§lh'), {{opacity:0}}, {{opacity:1, duration:0.3}}, 6.2);
    // fold 2: left edge to right edge, then in half again
    tl.fromTo(q('#§lh'), {{opacity:1}}, {{opacity:0, duration:0.15, immediateRender:false}}, 6.95);
    tl.set(q('#§A'), {{opacity:0}}, 7.1); tl.set(q('#§B'), {{opacity:1}}, 7.1);
    lightMini(2, 7.1);
    tl.fromTo(q('#§Bflap'), {{rotationY:0}}, {{rotationY:180, duration:0.8, ease:'power2.inOut'}}, 7.15);
    tl.fromTo(q('#§Bshade'), {{opacity:0}}, {{opacity:0.14, duration:0.4, ease:'power1.in'}}, 7.15);
    tl.set(q('#§Bfront'), {{opacity:0}}, 7.55); tl.set(q('#§Bfront'), {{opacity:1}}, 11.26);
    tl.set(q('#§B'), {{opacity:0}}, 8.0); tl.set(q('#§C'), {{opacity:1}}, 8.0);
    lightMini(3, 8.3);
    tl.fromTo(q('#§Cflap'), {{rotationY:0}}, {{rotationY:180, duration:0.75, ease:'power2.inOut'}}, 8.3);
    tl.fromTo(q('#§Cshade'), {{opacity:0}}, {{opacity:0.14, duration:0.35, ease:'power1.in'}}, 8.3);
    tl.fromTo(q('#§creaseV'), {{opacity:0, y:0}}, {{opacity:1, duration:0.12}}, 9.3);
    tl.fromTo(q('#§creaseV'), {{y:0}}, {{y:H, duration:0.6, ease:'power2.inOut', immediateRender:false}}, 9.3);
    tl.fromTo(q('#§creaseV'), {{opacity:1}}, {{opacity:0, duration:0.12, immediateRender:false}}, 9.9);
    // open fully
    tl.fromTo(q('#§Cflap'), {{rotationY:180}}, {{rotationY:0, duration:0.45, ease:'power2.inOut', immediateRender:false}}, 10.5);
    tl.fromTo(q('#§Cshade'), {{opacity:0.14}}, {{opacity:0, duration:0.4, immediateRender:false}}, 10.5);
    tl.set(q('#§C'), {{opacity:0}}, 10.96); tl.set(q('#§B'), {{opacity:1}}, 10.96);
    tl.fromTo(q('#§Bflap'), {{rotationY:180}}, {{rotationY:0, duration:0.6, ease:'power2.inOut', immediateRender:false}}, 10.96);
    tl.fromTo(q('#§Bshade'), {{opacity:0.14}}, {{opacity:0, duration:0.5, immediateRender:false}}, 10.96);
    tl.fromTo([q('#§lh'),q('#§lv1'),q('#§lv2'),q('#§lv3')], {{opacity:0}}, {{opacity:1, duration:0.35, stagger:0.06, immediateRender:false}}, 11.6);
    // eight equal panels
    tl.fromTo(qa('.§po'), {{opacity:0}}, {{opacity:1, duration:0.25, stagger:0.07, ease:'power1.out'}}, 13.2);
    tl.fromTo(q('#§tag'), {{opacity:0, x:-12}}, {{opacity:1, x:0, duration:0.5, ease:'power3.out'}}, 13.4);
"""
    wrap("06-task1-fold-lines", 6, "", body, js)

# ======================================================================
# 07 — Task 2: cut the slot (CAUTION before step 3)
# ======================================================================
TASK2 = ["Fold the sheet so that the left edge touches the right edge.",
         "Hold the sheet with the folded edge on the left.",
         "Cut along the horizontal fold line from the folded edge.",
         "Stop the cut at the first vertical fold line. The cut is 2.75 in (70 mm) long.",
         "Open the sheet.",
         "Make sure that the slot is on the cut line between the 2 center panels of each row."]

def f07():
    W, H = 906, 700
    L, T = 157, 119
    hw = W // 2
    body = f"""
    <div class="§a" id="§sheetw" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;perspective:2600px">
      <div id="§sheetin" data-layout-allow-overlap class="§a" style="left:0;top:0;width:{W}px;height:{H}px">
        {fold_sheet(W, H, with_c=False)}
        {lines_overlay(W, H, ("h","v1","v2","v3"))}
      </div>
      <!-- marks on the folded half (right half before the slide) -->
      <div class="§a" id="§half" data-layout-allow-overlap style="left:{hw}px;top:0;width:{W-hw}px;height:{H}px;opacity:0">
        <div class="§a" style="left:0;top:0;width:7px;height:{H}px;background:#17221d"></div>
        <div class="§a" id="§stop" style="left:{hw//2-1}px;top:0;height:{H}px;border-left:3px dashed #b4b4b4"></div>
        <div class="§a" style="left:{hw//2}px;right:0;top:{H//2-1}px;border-top:3px dashed #b4b4b4"></div>
        <div class="§a" style="left:7px;width:{hw//2-7}px;top:{H//2-1}px;border-top:3px dashed #b4b4b4"></div>
        <div class="§a" id="§cut" style="left:0;width:{hw//2}px;top:{H//2-4}px;height:8px;background:#e2703f;transform-origin:0 50%"></div>
        <div class="§a" id="§sc" style="left:-22px;top:{H//2-38}px;font-size:50px;color:#17221d;opacity:0">✂</div>
        <div class="§a §mono" id="§dim" style="left:0;width:{hw//2}px;top:{H//2+27}px;text-align:center;font-size:20px;color:#b8501f;opacity:0">├ 2.75 in (70 mm) ┤</div>
      </div>
    </div>
    <div class="§a §mono" id="§lab1" style="left:{L-7}px;top:{T-42}px;font-size:18px;color:#5a655f;opacity:0">folded edge</div>
    <div class="§a §mono" id="§lab2" style="left:{L+hw//2-150}px;width:300px;text-align:center;top:{T+H+14}px;font-size:18px;color:#5a655f;opacity:0">first vertical fold line</div>
    {task_card('', 'TASK 2', 'Cut the slot', TASK2, caution_before=3, style='left:1072px;top:80px;width:768px', fs=21)}"""
    js = f"""
    var hw={hw};
    tl.fromTo(q('#§sheetw'), {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.6, ease:'power3.out'}}, 0.05);
    tl.fromTo([q('#§lh'),q('#§lv1'),q('#§lv2'),q('#§lv3')], {{opacity:0}}, {{opacity:1, duration:0.4}}, 0.3);
    tl.set(q('#§A'), {{opacity:0}}, 0); tl.set(q('#§B'), {{opacity:1}}, 0);
    steps([[['s1'],2.8],[['s2'],4.2],[[],5.8],[['s3'],13.6],[['s4'],16.3]]);
    // fold the left half onto the right half
    tl.fromTo([q('#§lh'),q('#§lv1'),q('#§lv2'),q('#§lv3')], {{opacity:1}}, {{opacity:0, duration:0.2, immediateRender:false}}, 2.85);
    tl.fromTo(q('#§Bflap'), {{rotationY:0}}, {{rotationY:180, duration:1.0, ease:'power2.inOut'}}, 2.9);
    tl.fromTo(q('#§Bshade'), {{opacity:0}}, {{opacity:0.14, duration:0.5, ease:'power1.in'}}, 2.9);
    tl.set(q('#§Bfront'), {{opacity:0}}, 3.4);
    tl.fromTo(q('#§half'), {{opacity:0}}, {{opacity:1, duration:0.3}}, 3.95);
    tl.fromTo(q('#§cut'), {{scaleX:0}}, {{scaleX:0, duration:0.01}}, 0);
    // slide so the folded edge is on the left
    tl.fromTo(q('#§sheetw'), {{x:0}}, {{x:-hw, duration:1.0, ease:'power3.inOut', immediateRender:false}}, 4.2);
    tl.fromTo([q('#§lab1'), q('#§lab2')], {{opacity:0}}, {{opacity:1, duration:0.45, stagger:0.2}}, 5.0);
    // CAUTION: lift, pulse once, hold still
    tl.fromTo(q('#§caution'), {{boxShadow:'0 0 0 0 rgba(226,187,92,0)'}}, {{boxShadow:'0 0 0 9px rgba(226,187,92,.55)', duration:0.35, ease:'power2.out'}}, 5.8);
    tl.fromTo(q('#§caution'), {{boxShadow:'0 0 0 9px rgba(226,187,92,.55)'}}, {{boxShadow:'0 0 0 2px rgba(226,187,92,.35)', duration:0.6, ease:'power2.in', immediateRender:false}}, 6.2);
    tl.fromTo(q('#§stop'), {{borderLeftColor:'#b4b4b4'}}, {{borderLeftColor:'#e2703f', duration:0.4}}, 8.3);
    tl.fromTo(q('#§lab2'), {{color:'#5a655f'}}, {{color:'#b8501f', duration:0.4}}, 8.3);
    // the cut: from the folded edge, stop hard at the first vertical fold line
    tl.fromTo(q('#§sc'), {{opacity:0}}, {{opacity:1, duration:0.2}}, 13.5);
    tl.fromTo(q('#§cut'), {{scaleX:0}}, {{scaleX:1, duration:2.5, ease:'expo.inOut', immediateRender:false}}, 13.7);
    tl.fromTo(q('#§sc'), {{x:0}}, {{x:hw/2, duration:2.5, ease:'expo.inOut'}}, 13.7);
    tl.fromTo(q('#§dim'), {{opacity:0, y:-6}}, {{opacity:1, y:0, duration:0.45, ease:'power3.out'}}, 16.25);
"""
    wrap("07-task2-cut", 7, "", body, js)

# ======================================================================
# 08 — Task 3: fold the zine (large "+" hero)
# ======================================================================
TASK3 = ["Fold the top row back, behind the bottom row.",
         "Make sure that you can see the front cover and pages 6, 7, and 8.",
         "Hold the left end and the right end of the sheet.",
         "Push the two ends slowly toward the center. The slot opens into a diamond shape.",
         'Continue to push until the sheet makes a "+" shape.',
         "Fold the 4 arms together to close the zine like a book.",
         "Put the front cover on the outer side.",
         "Push along the spine to make the folds flat.",
         "Make sure that the pages are in the sequence 1 to 8."]

def f08():
    W, H = 760, 587
    L, T = 160, 120
    half = H // 2
    # plus geometry (sketch v2): box 595, arms 154 wide
    PX, PY, PS, AW = 292, 80, 595, 154
    a0 = (PS - AW) // 2
    def row(nums, up, faint=True):
        cells = "".join(f'<div class="§cellp {"§up" if up else ""}" style="font-size:42px;{"border-right:3px dashed #b4b4b4" if i<3 else ""}"><span style="opacity:{.3 if faint else 1}">{n}</span></div>' for i, n in enumerate(nums))
        return f'<div class="§grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:1fr">{cells}</div>'
    arm_num = lambda n, c: f'<div class="§a" style="left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-family:Newsreader;font-size:46px;color:{c}">{n}</div>'
    body = f"""
    <div class="§a" id="§sheetw" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;perspective:2600px">
      <div class="§a §p3d" id="§topflap" style="left:0;top:0;width:{W}px;height:{half}px;transform-origin:50% 100%">
        <div class="§face" style="border-bottom:3px dashed #b4b4b4">{row(TOP, True)}</div>
      </div>
      <div class="§a §paper §shadow" id="§strip" style="left:0;top:{half}px;width:{W}px;height:{H-half}px">{row(BOT, False)}
        <div class="§a" id="§diamond" style="left:{W//2-95}px;top:-30px;width:190px;height:60px;background:#f3f0e9;clip-path:polygon(0 50%,50% 0,100% 50%,50% 100%);transform:scale(0)"></div>
      </div>
      <div class="§a" id="§slot" style="left:{W//4}px;top:{half-2}px;width:{W//2}px;height:4px;background:#17221d"></div>
      <div class="§a §mono" id="§pl" style="left:-56px;top:{half+ (H-half)//2 - 30}px;font-size:50px;color:#e2703f;opacity:0">→</div>
      <div class="§a §mono" id="§pr" style="left:{W+12}px;top:{half+ (H-half)//2 - 30}px;font-size:50px;color:#e2703f;opacity:0">←</div>
    </div>
    <div class="§a" id="§plus" style="left:{PX}px;top:{PY}px;width:{PS}px;height:{PS}px;perspective:2400px">
      <div class="§a §paper §shadow" id="§armT" style="left:{a0}px;top:0;width:{AW}px;height:{a0}px;transform-origin:50% 100%">{arm_num('4','#c9c4b8')}</div>
      <div class="§a §paper §shadow" id="§armB" style="left:{a0}px;top:{a0+AW}px;width:{AW}px;height:{a0}px;transform-origin:50% 0%">{arm_num('1','#17221d')}</div>
      <div class="§a §paper §shadow" id="§armL" style="left:0;top:{a0}px;width:{a0}px;height:{AW}px;transform-origin:100% 50%">{arm_num('6','#c9c4b8')}</div>
      <div class="§a §paper §shadow" id="§armR" style="left:{a0+AW}px;top:{a0}px;width:{a0}px;height:{AW}px;transform-origin:0% 50%">{arm_num('8','#c9c4b8')}</div>
      <div class="§a §paper" id="§ctr" style="left:{a0}px;top:{a0}px;width:{AW}px;height:{AW}px"></div>
      <div class="§a" id="§ctro" style="left:{a0}px;top:{a0}px;width:{AW}px;height:{AW}px;border:5px solid #e2703f"></div>
      <div class="§a §mono" id="§plabel" style="left:0;top:0;font-size:27px;font-weight:600;color:#b8501f">"+" shape</div>
      <div class="§a §mono" id="§qa" style="left:-65px;top:{a0+AW//2-32}px;font-size:50px;color:#e2703f">→</div>
      <div class="§a §mono" id="§qb" style="left:{PS+16}px;top:{a0+AW//2-32}px;font-size:50px;color:#e2703f">←</div>
      <div class="§a §paper" id="§closed" style="left:{(PS-200)//2}px;top:{(PS-310)//2}px;width:200px;height:310px;border-left:10px solid #ece7dc;box-shadow:8px 12px 26px -12px rgba(23,34,29,.45);padding:23px 19px">
        <div class="§kick §kick-m" style="font-size:12px">Page 1 · Front</div><div class="§disp" style="font-size:34px;margin-top:14px">My first<br>zine</div></div>
      <div class="§a §mono" id="§zlabel" style="left:0;top:0;font-size:27px;font-weight:600;color:#b8501f">zine</div>
    </div>
    <div class="§a" id="§tdia" style="left:80px;top:745px;text-align:center;font-family:'IBM Plex Mono';font-size:19px;color:#5a655f">
      <div style="width:250px;height:96px;background:#fff;box-shadow:0 10px 19px -8px rgba(0,0,0,.3);position:relative"><div style="position:absolute;left:28%;right:28%;top:50%;height:50px;margin-top:-25px;background:#f3f0e9;clip-path:polygon(0 50%,50% 0,100% 50%,50% 100%)"></div></div>
      <div style="margin-top:12px">1 · diamond</div></div>
    <div class="§a" id="§tbook" style="left:925px;top:657px;text-align:center;font-family:'IBM Plex Mono';font-size:19px;color:#5a655f">
      <div style="width:123px;height:184px;background:#fff;border-left:10px solid #ece7dc;box-shadow:8px 12px 23px -10px rgba(0,0,0,.35)"></div>
      <div style="margin-top:12px">3 · book</div></div>
    {task_card('', 'TASK 3', 'Fold the zine', TASK3, style='left:1110px;top:80px;width:730px', fs=19.5)}"""
    js = """
    tl.fromTo(q('#§sheetw'), {opacity:0, y:24}, {opacity:1, y:0, duration:0.6, ease:'power3.out'}, 0.05);
    tl.fromTo([q('#§plus'), q('#§closed'), q('#§zlabel'), q('#§tdia'), q('#§tbook')], {opacity:0}, {opacity:0, duration:0.01}, 0);
    steps([[['s1'],3.3],[['s2'],4.6],[['s3'],6.2],[['s4'],7.4],[['s5'],12.2],[['s6'],14.2],[['s7'],15.7],[['s8'],16.2],[['s9'],16.7]]);
    // top row back, behind the bottom row
    tl.fromTo(q('#§topflap'), {rotationX:0, opacity:1}, {rotationX:88, duration:0.9, ease:'power2.in'}, 3.4);
    tl.set(q('#§topflap'), {opacity:0}, 4.3);
    tl.fromTo(q('#§slot'), {opacity:1}, {opacity:0, duration:0.2, immediateRender:false}, 4.3);
    // hold the ends, push to the centre
    tl.fromTo([q('#§pl'), q('#§pr')], {opacity:0}, {opacity:1, duration:0.35}, 6.2);
    tl.fromTo(q('#§strip'), {scaleX:1}, {scaleX:0.72, duration:1.8, ease:'power2.inOut'}, 7.4);
    tl.fromTo(q('#§pl'), {x:0}, {x:106, duration:1.8, ease:'power2.inOut'}, 7.4);
    tl.fromTo(q('#§pr'), {x:0}, {x:-106, duration:1.8, ease:'power2.inOut'}, 7.4);
    // slot opens into a diamond
    tl.fromTo(q('#§diamond'), {scale:0}, {scale:1, duration:1.0, ease:'power3.out', immediateRender:false}, 10.5);
    tl.fromTo(q('#§tdia'), {opacity:0, y:10}, {opacity:0.85, y:0, duration:0.5, ease:'power3.out', immediateRender:false}, 11.6);
    // ...then into the plus shape (hero)
    tl.fromTo(q('#§sheetw'), {opacity:1, scale:1}, {opacity:0, scale:0.6, duration:0.6, ease:'power2.in', immediateRender:false}, 12.2);
    tl.fromTo(q('#§plus'), {opacity:0}, {opacity:1, duration:0.3, immediateRender:false}, 12.35);
    tl.fromTo([q('#§ctr'), q('#§ctro')], {scale:0.4}, {scale:1, duration:0.5, ease:'power3.out'}, 12.35);
    tl.fromTo([q('#§armT'), q('#§armB')], {scaleY:0}, {scaleY:1, duration:0.6, ease:'power3.out'}, 12.5);
    tl.fromTo([q('#§armL'), q('#§armR')], {scaleX:0}, {scaleX:1, duration:0.6, ease:'power3.out'}, 12.5);
    tl.fromTo(q('#§plabel'), {opacity:0, y:8}, {opacity:1, y:0, duration:0.4, ease:'power3.out'}, 13.0);
    tl.fromTo([q('#§qa'), q('#§qb')], {opacity:0}, {opacity:1, duration:0.35}, 13.1);
    // fold the four arms together -> book
    tl.fromTo([q('#§qa'), q('#§qb'), q('#§plabel')], {opacity:1}, {opacity:0, duration:0.25, immediateRender:false}, 14.2);
    tl.fromTo(q('#§armL'), {rotationY:0}, {rotationY:178, duration:0.7, ease:'power2.inOut'}, 14.3);
    tl.fromTo(q('#§armR'), {rotationY:0}, {rotationY:-178, duration:0.7, ease:'power2.inOut'}, 14.45);
    tl.fromTo(q('#§armT'), {rotationX:0}, {rotationX:-178, duration:0.7, ease:'power2.inOut'}, 14.6);
    tl.fromTo(q('#§armB'), {rotationX:0}, {rotationX:178, duration:0.7, ease:'power2.inOut'}, 14.75);
    tl.fromTo(q('#§ctro'), {opacity:1}, {opacity:0, duration:0.3, immediateRender:false}, 15.2);
    tl.fromTo(q('#§closed'), {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.6, ease:'power3.out', immediateRender:false}, 15.4);
    tl.fromTo([q('#§armL'),q('#§armR'),q('#§armT'),q('#§armB'),q('#§ctr')], {opacity:1}, {opacity:0, duration:0.3, immediateRender:false}, 15.45);
    tl.fromTo(q('#§zlabel'), {opacity:0}, {opacity:1, duration:0.4, immediateRender:false}, 15.8);
    tl.fromTo(q('#§tbook'), {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, ease:'power3.out', immediateRender:false}, 16.6);
"""
    wrap("08-task3-fold-zine", 8, "", body, js)

# ======================================================================
# 09 — check the zine: pages turn 1 -> 8
# ======================================================================
def f09():
    L, T, W, H = 157, 99, 653, 461
    pw = W // 2
    def page(n, side):
        num_pos = "left:31px" if side == "L" else "right:31px"
        if n == 1:
            inner = '<div class="§kick §kick-m" style="font-size:13px">Page 1 · Front</div><div class="§disp" style="font-size:38px;margin-top:12px">My first<br>zine</div>'
        elif n == 4:
            inner = '<div class="§disp" style="font-size:38px">One sheet.<br>One cut.</div>'
        elif n == 5:
            inner = '<div style="font-size:27px;line-height:1.4;color:#5a655f">Fold edge to edge.</div>'
        elif n == 8:
            inner = '<div class="§kick §kick-m" style="font-size:13px">Page 8 · Back</div>'
        else:
            inner = ('<i style="display:block;height:14px;width:80%;background:#ece7dc;border-radius:4px"></i>'
                     '<i style="display:block;height:14px;width:62%;background:#ece7dc;border-radius:4px;margin-top:12px"></i>'
                     '<i style="display:block;height:14px;width:70%;background:#ece7dc;border-radius:4px;margin-top:12px"></i>')
        return (f'<div style="position:absolute;left:0;top:0;width:100%;height:100%;padding:31px">{inner}'
                f'<span class="§mono" style="position:absolute;bottom:19px;{num_pos};font-size:19px;color:#5a655f">{n}</span></div>')
    # spread states: (left, right)
    states = [(None, 1), (2, 3), (4, 5), (6, 7), (8, None)]
    statics = []
    for n in range(1, 9):
        side = "R" if n in (1, 3, 5, 7) else "L"
        x = pw if side == "R" else 0
        bd = "border-right:2px solid #e6e1d6;" if side == "L" else ""
        statics.append(f'<div class="§a §paper §shadow" id="§pg{n}" data-layout-allow-overlap style="left:{x}px;top:0;width:{pw}px;height:{H}px;{bd}opacity:0">{page(n, side)}</div>')
    flaps = []
    for k in range(4):
        front = states[k][1]; back = states[k + 1][0]
        flaps.append(f'<div class="§a §p3d" id="§flap{k}" data-layout-allow-overlap style="left:{pw}px;top:0;width:{pw}px;height:{H}px;transform-origin:0% 50%;opacity:0">'
                     f'<div class="§face">{page(front, "R")}</div>'
                     f'<div class="§face" style="transform:rotateY(180deg);border-right:2px solid #e6e1d6">{page(back, "L")}</div></div>')
    digits = "".join(f'<span id="§d{n}" style="color:#ddd8cd">{n}</span>{" " if n < 8 else ""}' for n in range(1, 9))
    body = f"""
    <div class="§a" id="§book" style="left:{L}px;top:{T}px;width:{W}px;height:{H}px;perspective:2600px">
      {''.join(statics)}{''.join(flaps)}
    </div>
    <div class="§a" style="left:1149px;top:99px;width:691px">
      <div class="§kick §kick-m" id="§ck">Page sequence</div>
      <div class="§mono" style="font-size:58px;margin-top:12px;letter-spacing:.05em;white-space:pre">{digits}</div>
      <p class="§notice §note" id="§note" style="margin:46px 0 0;font-size:26px"><b>NOTE</b>To make more copies, copy the flat sheet before you cut it.</p>
    </div>"""
    turns = [0.4, 1.05, 1.7, 2.35]
    js = """
    var turns = %s;
    tl.fromTo(q('#§ck'), {opacity:0}, {opacity:1, duration:0.4}, 0.05);
    tl.fromTo(q('#§book'), {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5, ease:'power3.out'}, 0.0);
    tl.set(q('#§pg1'), {opacity:1}, 0);
    tl.fromTo(q('#§d1'), {color:'#ddd8cd'}, {color:'#17221d', duration:0.25}, 0.3);
    var st = [[null,1],[2,3],[4,5],[6,7],[8,null]];
    turns.forEach(function(t, k){
      var cur = st[k], nxt = st[k+1];
      var f = q('#§flap'+k);
      tl.set(f, {opacity:1}, t);
      tl.set(q('#§pg'+cur[1]), {opacity:0}, t);
      if (nxt[1]) tl.set(q('#§pg'+nxt[1]), {opacity:1}, t);
      tl.fromTo(f, {rotationY:0}, {rotationY:-180, duration:0.55, ease:'power2.inOut'}, t);
      tl.set(f, {opacity:0}, t + 0.56);
      if (cur[0]) tl.set(q('#§pg'+cur[0]), {opacity:0}, t + 0.56);
      tl.set(q('#§pg'+nxt[0]), {opacity:1}, t + 0.56);
      [nxt[0], nxt[1]].forEach(function(n){ if (n) tl.fromTo(q('#§d'+n), {color:'#ddd8cd'}, {color:'#17221d', duration:0.25}, t + 0.5); });
    });
    tl.fromTo(q('#§note'), {opacity:0, y:16}, {opacity:1, y:0, duration:0.6, ease:'power3.out'}, 4.5);
""" % json.dumps(turns)
    wrap("09-check", 9, "", body, js)

# ======================================================================
# 10 — CTA
# ======================================================================
def f10():
    url = "zine.imurph.com"
    body = f"""
    {book("left:195px;top:99px;width:288px;height:442px", arch=False).replace('class="§a §paper"', 'id="§book" class="§a §paper"', 1)}
    <div class="§a" style="left:656px;top:147px;width:1184px">
      <h2 class="§disp" id="§title" style="font-size:134px">Make your zine.</h2>
      <div class="§mono" style="font-size:65px;margin-top:27px;color:#e2703f;height:80px"><span id="§url"></span></div>
      <div class="§mono" id="§recap" style="margin-top:58px;font-size:22px;letter-spacing:.14em;color:#5a655f;text-transform:uppercase">Type · Print · Cut · Fold</div>
    </div>"""
    js = """
    tl.fromTo(q('#§book'), {opacity:0, rotation:-3, y:20}, {opacity:1, rotation:-3, y:0, duration:0.6, ease:'power3.out'}, 0.0);
    tl.fromTo(q('#§title'), {opacity:0, y:40}, {opacity:1, y:0, duration:0.7, ease:'power3.out'}, 0.25);
    var u = %s, o = {n:0}, el = q('#§url');
    tl.fromTo(o, {n:0}, {n:u.length, duration:0.9, ease:'none', onUpdate:function(){ el.textContent = u.slice(0, Math.round(o.n)); }}, 1.4);
    tl.fromTo(q('#§recap'), {opacity:0}, {opacity:1, duration:0.6, ease:'power1.out'}, 3.0);
""" % json.dumps(url)
    wrap("10-cta", 10, "", body, js)

for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10):
    fn()
