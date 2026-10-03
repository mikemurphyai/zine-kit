import re
s=open('STORYBOARD.md').read()
VD='''## Locked

- Layout locked at storyboard v2 (user, 2026-10-03). Workers dress the confirmed sketch at `storyboard.html#frame-NN`; they never redraw it.

## Video direction

- **Palette (frame.md roles):** ground `cream` #f3f0e9 on every frame; cards `surface` #fdfaf4 with 1px `line` #ddd8cd border and 14px radius; diagram sheet `paper` #ffffff with a soft card shadow; text `ink` #17221d / `muted` #5a655f; the ONE voltage per frame is `coral` #e2703f (cut line, active step, URL, current-panel outline) with `tile-strong` #b8501f for kickers; CAUTION uses `caution` #7f5600 on `caution-bg` #fbf0d2 with `caution-line` #e2bb5c; NOTE and active-step highlight use `accent-soft` #fbe6da. Fold lines are dashed #b4b4b4.
- **Type:** Newsreader display (sentence case, 400, negative tracking; 600 only for task-card titles, as in the kit); Public Sans for steps, labels, body; IBM Plex Mono for kickers (uppercase, tracked), numbers, dimensions, URL.
- **Motion grammar:** smooth long-tail settles (`power3.out` default, `expo.out` for fast arrivals); no overshoot, no bounce anywhere. Every reveal lands on the voiceover word that names it (word times are in audio_meta.json); nothing enters before its cue. Paper moves like paper: folds are 3D rotations about the fold line (`rotateX` for bottom→top, `rotateY` for left→right) with `transform-origin` on the fold, a slight shadow darkening on the moving flap, `power2.inOut` so the flap accelerates and lands. Task-card step highlight moves row to row in step with the VO, the earlier steps dim to muted.
- **Spine:** the white sheet. It is the hero object from frame 3 to frame 8 (preview → large sheet → printed → folded → cut → "+"), and the closed book bookends it (frames 1, 9, 10). Keep its proportions (11:8.5, panels 2.75:4.25) exact everywhere.
- **Held frames:** frame 4 ends on a still "This is correct." (the breather before the procedure); frame 7 holds still for a beat after the CAUTION before the cut draws; frame 10 holds to the end. During holds only subtle jitter is allowed, and in this video prefer complete stillness.
- **Caption keep-out:** bottom 17% (y > 896px) is reserved for captions; all content sits above it.
- **Negative list:** no glow, no gradients, no bokeh, no drop-shadow heavier than the kit's card shadow, no hands or photos, no cursor except the form's text caret, no navy code surface, no ✱ mark, no slideshow (front-load then freeze), no screensaver (independent floating), no lazy breathing, no back-half pan/push, no new words on task cards (copy the kit verbatim, CAUTION before step 3).

## Frame 1 —'''
s=s.replace('\n## Frame 1 —','\n'+VD,1)

SHOT={
1:'''- blueprint: compose
- focal: the white sheet that folds into a small book
- roles: sheet/book = foreground subject · kicker + serif title = supporting · cream ground = background
- sfx: none

Scene 1 (0.0–1.4s): a flat white sheet (8 faint dashed panels, 11:8.5) settles onto the cream ground left-of-center, ~40% of frame width, tilted −4°; entrance is a short drop + settle (power3). Asymmetric 60/40: sheet left, empty right waiting.
Scene 2 (1.4–3.4s): on "eight pages… one sheet", the sheet folds: bottom row rotates up onto the top (rotateX about the center fold), then folds in half twice left→right (rotateY), shrinking into a single panel; the folded panel stands up into the closed book (front cover "My first zine" in Newsreader, Page 1 · Front mono label) at the sketch position.
Scene 3 (3.4–4.5s): the coral arrow and the ghost of the flat sheet remain dim at left (opacity ~35%) as in the sketch; the mono kicker "ONE SHEET · ONE CUT · EIGHT PAGES" writes in at right (per-word staggered reveal → dynamic-content-sequencing).
Scene 4 (4.5–6.0s): on "zine", the title "How to make a zine" rises in by line (waterfall-entry, smooth) at display scale; hold still.''',
2:'''- blueprint: grid-card-assemble (Adapt)
- focal: four step tiles Type · Print · Cut · Fold
- roles: tiles = foreground subject · "THE PROCEDURE" kicker + Necessary line = supporting · cream ground = background
- sfx: none

Adapt: keep the staggered self-assemble into a row; each tile arrives on its own VO word instead of one cascade.
Scene 1 (0.0–0.6s): kicker "THE PROCEDURE" fades up top-left.
Scene 2 (0.3–1.4s): on "Type", tile 01 rises in (power3) and its three text lines draw left→right, the last one coral.
Scene 3 (1.9–2.6s): on "Print", tile 02 rises in; its small white sheet slides down into place.
Scene 4 (3.6–4.4s): on "Cut", tile 03 rises in; the coral line draws left→right and the scissors land at its end; "1 time" mono tag appears.
Scene 5 (5.2–5.9s): on "Fold", tile 04 rises in; the small book swings closed (rotateY) on its spine.
Scene 6 (5.6–6.5s): the "NECESSARY · A printer · US Letter paper · Scissors" line fades up bottom-left; hold.''',
3:'''- blueprint: panel-edit-live-sync (Adapt)
- focal: the live coupling — form field text → sheet panel
- roles: kit form card (left) = foreground subject · sheet preview (right) = foreground target · URL chip + hand-drawn hint = supporting · cream = background
- sfx: none

Adapt: keep the bound-pair signature (edit here, it changes there in the same beat); the "control" is a typed text field, not a slider.
Scene 1 (0.0–0.7s): the form card and the empty sheet preview are in place at sketch positions (they arrived with the push-slide); the URL chip "zine.imurph.com" is hidden.
Scene 2 (0.7–2.8s): on "zine.imurph.com", the URL chip pops in coral-soft at the card's top-right (smooth scale 0.9→1), then a brief coral outline pulse on the chip.
Scene 3 (3.9–5.3s): on "Type", "My first zine" types into the Page 1 field with a caret (type-on with caret → discrete-text-sequence + context-sensitive-cursor); the SAME characters appear in panel 1 (bottom-right) which gets the coral active outline (control-target-sync).
Scene 4 (5.0–6.2s): on "form", Page 2 types "One sheet. One cut." and the text appears upside down in panel 2 (top row, far right); active outline moves to panel 2. The hint "To draw a page by hand, do not type on it." fades up bottom-right. Hold.''',
4:'''- blueprint: compose
- focal: the large sheet with panel numbers
- roles: sheet = foreground subject (~52% width, centered) · "TOP ROW PRINTS UPSIDE DOWN" kicker + ↻ = supporting · "This is correct." = supporting payoff · cream = background
- sfx: none

Scene 1 (0.0–0.5s): the large sheet is centered (arrives via zoom-through); all 8 numbers upright: 5 4 3 2 / 6 7 8 BACK 1 FRONT.
Scene 2 (0.5–2.2s): on "top row… upside down", the kicker writes in upper-left with the coral ↻, and the four top-row numbers rotate 180° one after another, right to left (2, 3, 4, 5), each a smooth power3 turn.
Scene 3 (3.6–5.0s): on "correct", "This is correct." sets in Newsreader italic lower-right (fade + small rise); then everything holds completely still (held frame).''',
5:'''- blueprint: grid-card-assemble (Adapt)
- focal: print-settings card with four rows
- roles: settings card (left) = foreground subject · printer slot + emerging sheet (right) = foreground payoff · shortcut line = supporting · cream = background
- sfx: none

Adapt: the "list that accumulates" is the four settings checking on in VO order; the payoff is the sheet leaving the printer.
Scene 1 (0.0–0.6s): settings card (title "Print the sheet", kicker "PRINT SETTINGS") and the dark printer slot are in place; all four rows show values with grey checks.
Scene 2 (1.5–5.6s): each row's check turns coral and its value goes bold on its VO word: "landscape" (1.5) → Orientation, "US Letter" (2.4) → Paper, "100 percent" (3.8) → Scale, "no margins" (5.3) → Margins.
Scene 3 (5.8–7.4s): the sheet slides down out of the printer slot (clip reveal from the slot edge, power2.inOut), its top row upside down, as in the sketch; the "⌘ P (Mac) · Ctrl P (Windows)" line fades up bottom-left. Hold.''',
6:'''- blueprint: compose
- focal: the sheet folding into fold lines
- roles: sheet diagram (left, ~45% width) = foreground subject · TASK 1 card (right, verbatim kit text, 10 steps) = supporting rail · fold-state labels + "8 equal panels / 2 rows of 4" tag = supporting · cream = background
- sfx: none

Layout: asymmetric 55/45 — diagram left, task card right (card is present from the push-slide with all steps muted).
Scene 1 (0.0–1.5s): on "Task one", the card header TASK 1 / "Make the fold lines" brightens; the printed sheet lies flat at left, printed side up, panel numbers faint; steps 1–2 highlight briefly together.
Scene 2 (3.3–5.0s): on "Fold the bottom edge", step 3 highlights; the bottom row rotates up onto the top row (rotateX about the horizontal center line); step 4 highlights as a thumbnail-crease line sweeps along the fold.
Scene 3 (5.8–6.6s): on "Open", step 5 highlights; the flap rotates back down, leaving a dashed horizontal fold line.
Scene 4 (7.3–9.8s): on "Fold the sheet in half two times", steps 6–7 highlight; the left half rotates over onto the right (rotateY about the center vertical), then the folded stack folds in half again (rotateY about its new center); step 8 crease sweep.
Scene 5 (10.6–11.6s): on "Open", step 9 highlights; both folds rotate back open, leaving dashed vertical lines at the quarters and center.
Scene 6 (12.1–15.0s): on "eight equal panels", step 10 highlights coral-soft; the 8 panels flash a soft coral outline one by one in reading order (fast stagger) and the mono tag "8 equal panels · 2 rows of 4" appears; hold.''',
7:'''- blueprint: compose
- focal: the coral cut line that stops at the first vertical fold
- roles: folded half-sheet (left) = foreground subject · TASK 2 card with CAUTION before step 3 (right, verbatim) = supporting rail · dimension "2.75 in (70 mm)", "folded edge", "first vertical fold line" labels = supporting · cream = background
- sfx: none

Layout: asymmetric 50/50 — diagram left, card right.
Scene 1 (0.0–2.6s): on "Task two… Cut the slot", card header brightens; the opened sheet (8 panels, dashed fold lines) lies at left.
Scene 2 (2.7–5.6s): on "Fold the sheet in half", steps 1–2 highlight; the left half rotates over onto the right (rotateY), then the folded sheet slides so the folded edge is on the left (bold ink edge) — the sketch pose. Labels "folded edge" and "first vertical fold line" fade in.
Scene 3 (6.0–12.9s): on "Caution", the yellow CAUTION notice lifts to full strength (others dim) and its border pulses once; the first vertical fold line on the diagram turns coral-dashed as a stop marker on "first vertical fold line" (8.4). Then everything holds still through "the zine will come apart" (held beat).
Scene 4 (13.6–17.5s): on "Cut along", step 3 highlights; the coral cut line draws from the folded edge along the horizontal fold (svg-path-draw) with the scissors riding its head, and stops hard at the first vertical fold line (expo.out arrival, no overshoot); the dimension tag "├ 2.75 in (70 mm) ┤" fades in under it; step 4 highlights. Hold.''',
8:'''- blueprint: compose
- focal: the large "+" shape
- roles: "+" (center-left, ~31cqw square, same scale as sheets in frames 4–7) = foreground subject · diamond (lower-left) and book (lower-right) thumbnails = supporting before/after · TASK 3 card (right, verbatim, 9 steps) = supporting rail · push arrows = supporting · cream = background
- sfx: none

Layout: asymmetric 55/45 per confirmed sketch v2 — hero "+" left-center, card right.
Scene 1 (0.0–3.2s): on "Task three… Fold the zine", card header brightens; at the hero position, the cut sheet (8 panels, slot in center) lies flat.
Scene 2 (3.3–5.6s): on "Fold the top row back", step 1 highlights; the top row rotates back behind the bottom row (rotateX away from viewer) leaving the strip 6 7 8 1; step 2 highlights.
Scene 3 (6.2–9.6s): on "Hold the two ends… Push them", steps 3–4 highlight; coral push arrows appear at both strip ends and the ends slide toward the center while the slot bows open (the strip compresses horizontally, the center rises).
Scene 4 (10.4–12.2s): on "diamond", the small diamond thumbnail at lower-left appears and the strip shows the diamond opening at its center.
Scene 5 (12.2–14.0s): on "plus shape", step 5 highlights; the strip resolves into the large "+" shape (four arms: 4 top, 1 bottom, 6 left, 8 right; center square outlined coral) — the hero moment; mono label '"+" shape' writes in.
Scene 6 (14.2–18.0s): on "Fold the four arms together", step 6 highlights; the arms swing together (rotateY pairs) and the book thumbnail at lower-right appears as the "+" closes; steps 7–9 highlight in quick sequence near "book". Hold on the closed state.''',
9:'''- blueprint: compose
- focal: the open zine turning its pages 1→8
- roles: open spread (left) = foreground subject · mono page counter "1 2 3 4 5 6 7 8" = supporting · NOTE card = supporting · cream = background
- sfx: none

Scene 1 (0.0–2.9s): on "the pages are in the sequence", the book from frame 1 opens to a spread and its pages turn (rotateY on the spine) 1→8 in an even rhythm; each turn fills the next counter digit from muted to ink.
Scene 2 (2.9–4.5s): the counter completes at "eight"; the last spread (pages 4–5 per sketch) settles.
Scene 3 (4.5–6.0s): on "complete", the NOTE card ("To make more copies, copy the flat sheet before you cut it.") rises in under the counter; hold.''',
10:'''- blueprint: titlecard-reveal (Reproduce)
- focal: "Make your zine." + "zine.imurph.com"
- roles: title + URL = foreground subject · closed book (left, −3°) = supporting · recap strip "TYPE · PRINT · CUT · FOLD" = supporting · cream = background
- sfx: none

Scene 1 (0.0–0.9s): the closed book is in place at left (from the crossfade); "Make your zine." rises in (slide-up crossfade, power3) on "Make your zine".
Scene 2 (1.4–3.0s): on "zine.imurph.com", the URL types on in coral mono (type-on, no caret).
Scene 3 (3.0–5.0s): the recap strip fades up; final hold, perfectly still, to the last frame.''',
}
for n,txt in SHOT.items():
    pat=re.compile(r'(## Frame %d — .*?\nkeyMessage: [^\n]*\n)'%n, re.S)
    m=pat.search(s); assert m,n
    s=s[:m.end()]+'\n'+txt+'\n'+s[m.end():]
open('STORYBOARD.md','w').write(s)
