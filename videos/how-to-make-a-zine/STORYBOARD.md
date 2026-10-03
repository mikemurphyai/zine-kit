---
format: 1920x1080
duration: 90s
message: "You can make an 8-page zine from one sheet of paper: type your pages at zine.imurph.com, print, cut once, and fold."
arc: how-to-process
audience: "People new to zines, including people who read English as a second language"
mode: collaborative
music: soft light acoustic guitar underscore, warm, calm, handmade, low energy, no drums
language: en
style: "All voiceover and on-screen text in ASD-STE100 Simplified Technical English"
---

## Changes from v1

- User: "The pieces on Frame 8 look a lot smaller than the other pages." → Frame 8: the "+" shape is now the large hero object (same scale as the sheets in frames 4–7); diamond (before) and book (after) are smaller flanking steps.
- Agent judgment: Frame 2 tiles and glyphs enlarged to fill the frame.

## Resolved outside the video

- Kit fix approved by user: zine-kit.html Task 2 CAUTION moved before step 3 (matches frame 7). Copied to deploy/site/index.html; not yet uploaded.

## Locked

- Layout locked at storyboard v2 (user, 2026-10-03). Workers dress the confirmed sketch at `storyboard.html#frame-NN`; they never redraw it.

## Video direction

- **Palette (frame.md roles):** ground `cream` #f3f0e9 on every frame; cards `surface` #fdfaf4 with 1px `line` #ddd8cd border and 14px radius; diagram sheet `paper` #ffffff with a soft card shadow; text `ink` #17221d / `muted` #5a655f; the ONE voltage per frame is `coral` #e2703f (cut line, active step, URL, current-panel outline) with `tile-strong` #b8501f for kickers; CAUTION uses `caution` #7f5600 on `caution-bg` #fbf0d2 with `caution-line` #e2bb5c; NOTE and active-step highlight use `accent-soft` #fbe6da. Fold lines are dashed #b4b4b4.
- **Type:** Newsreader display (sentence case, 400, negative tracking; 600 only for task-card titles, as in the kit); Public Sans for steps, labels, body; IBM Plex Mono for kickers (uppercase, tracked), numbers, dimensions, URL.
- **Motion grammar:** smooth long-tail settles (`power3.out` default, `expo.out` for fast arrivals); no overshoot, no bounce anywhere. Every reveal lands on the voiceover word that names it (word times are in audio_meta.json); nothing enters before its cue. Paper moves like paper: folds are 3D rotations about the fold line (`rotateX` for bottom→top, `rotateY` for left→right) with `transform-origin` on the fold, a slight shadow darkening on the moving flap, `power2.inOut` so the flap accelerates and lands. Task-card step highlight moves row to row in step with the VO, the earlier steps dim to muted.
- **Spine:** the white sheet. It is the hero object from frame 3 to frame 8 (preview → large sheet → printed → folded → cut → "+"), and the closed book bookends it (frames 1, 9, 10). Keep its proportions (11:8.5, panels 2.75:4.25) exact everywhere.
- **Held frames:** frame 4 ends on a still "This is correct." (the breather before the procedure); frame 7 holds still for a beat after the CAUTION before the cut draws; frame 10 holds to the end. During holds only subtle jitter is allowed, and in this video prefer complete stillness.
- **Caption keep-out:** bottom 17% (y > 896px) is reserved for captions; all content sits above it.
- **Negative list:** no glow, no gradients, no bokeh, no drop-shadow heavier than the kit's card shadow, no hands or photos, no cursor except the form's text caret, no navy code surface, no ✱ mark, no slideshow (front-load then freeze), no screensaver (independent floating), no lazy breathing, no back-half pan/push, no new words on task cards (copy the kit verbatim, CAUTION before step 3).

## Frame 1 — One sheet, eight pages

- scene: A white sheet lies on the chalk ground; it folds and folds and stands up as a small book, then a serif title appears
- voiceover: "You can make a book of eight pages from one sheet of paper. It is a zine."
- duration: 6s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Concretization — show the finished object before the procedure
- beat: Curiosity + surprise
- blueprint: compose
- focal: the white sheet that folds into a small book
- roles: sheet/book = foreground subject · kicker + serif title = supporting · cream ground = background
- sfx: none

narrativeRole: Opens the gap: a whole book from one flat sheet looks impossible, so the viewer wants the method.
keyMessage: One sheet of paper becomes an eight-page zine.


Scene 1 (0.0–1.4s): a flat white sheet (8 faint dashed panels, 11:8.5) settles onto the cream ground left-of-center, ~40% of frame width, tilted −4°; entrance is a short drop + settle (power3). Asymmetric 60/40: sheet left, empty right waiting.
Scene 2 (1.4–3.4s): on "eight pages… one sheet", the sheet folds: bottom row rotates up onto the top (rotateX about the center fold), then folds in half twice left→right (rotateY), shrinking into a single panel; the folded panel stands up into the closed book (front cover "My first zine" in Newsreader, Page 1 · Front mono label) at the sketch position.
Scene 3 (3.4–4.5s): the coral arrow and the ghost of the flat sheet remain dim at left (opacity ~35%) as in the sketch; the mono kicker "ONE SHEET · ONE CUT · EIGHT PAGES" writes in at right (per-word staggered reveal → dynamic-content-sequencing).
Scene 4 (4.5–6.0s): on "zine", the title "How to make a zine" rises in by line (waterfall-entry, smooth) at display scale; hold still.

## Frame 2 — The procedure

- scene: Four step tiles assemble in a row — Type · Print · Cut · Fold — with the kit's line icons; a small "Necessary" list (printer, US Letter paper, scissors) settles under them
- voiceover: "Type your pages. Print one sheet. Cut it one time. Fold it."
- duration: 6.5s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-procedure.html
- type: product_intro
- persuasion: Frame-then-fill — state the four-step shape, then populate it
- beat: Orientation + clarity
- blueprint: grid-card-assemble (Adapt)
- focal: four step tiles Type · Print · Cut · Fold
- roles: tiles = foreground subject · "THE PROCEDURE" kicker + Necessary line = supporting · cream ground = background
- sfx: none

narrativeRole: Lands the whole message in beat 2 and gives the viewer the map that every later frame fills in.
keyMessage: The procedure has four steps — type, print, cut, fold.


Adapt: keep the staggered self-assemble into a row; each tile arrives on its own VO word instead of one cascade.
Scene 1 (0.0–0.6s): kicker "THE PROCEDURE" fades up top-left.
Scene 2 (0.3–1.4s): on "Type", tile 01 rises in (power3) and its three text lines draw left→right, the last one coral.
Scene 3 (1.9–2.6s): on "Print", tile 02 rises in; its small white sheet slides down into place.
Scene 4 (3.6–4.4s): on "Cut", tile 03 rises in; the coral line draws left→right and the scissors land at its end; "1 time" mono tag appears.
Scene 5 (5.2–5.9s): on "Fold", tile 04 rises in; the small book swings closed (rotateY) on its spine.
Scene 6 (5.6–6.5s): the "NECESSARY · A printer · US Letter paper · Scissors" line fades up bottom-left; hold.

## Frame 3 — Type your pages

- scene: A reconstructed kit form on the left (Page 1 · Front cover … Page 8 · Back cover); text types into the fields and each page appears in its panel on the sheet preview at the right
- voiceover: "Open zine.imurph.com. Type your eight pages in the form."
- duration: 6.5s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-type-pages.html
- type: feature_showcase
- persuasion: Demonstration — show the form fill the sheet live
- beat: Comprehension + ease
- blueprint: panel-edit-live-sync (Adapt)
- focal: the live coupling — form field text → sheet panel
- roles: kit form card (left) = foreground subject · sheet preview (right) = foreground target · URL chip + hand-drawn hint = supporting · cream = background
- sfx: none

narrativeRole: Step 1 of the map. Shows that the viewer only types in reading order; the kit does the hard layout.
keyMessage: You type the pages in order; the kit places them on the sheet.


Adapt: keep the bound-pair signature (edit here, it changes there in the same beat); the "control" is a typed text field, not a slider.
Scene 1 (0.0–0.7s): the form card and the empty sheet preview are in place at sketch positions (they arrived with the push-slide); the URL chip "zine.imurph.com" is hidden.
Scene 2 (0.7–2.8s): on "zine.imurph.com", the URL chip pops in coral-soft at the card's top-right (smooth scale 0.9→1), then a brief coral outline pulse on the chip.
Scene 3 (3.9–5.3s): on "Type", "My first zine" types into the Page 1 field with a caret (type-on with caret → discrete-text-sequence + context-sensitive-cursor); the SAME characters appear in panel 1 (bottom-right) which gets the coral active outline (control-target-sync).
Scene 4 (5.0–6.2s): on "form", Page 2 types "One sheet. One cut." and the text appears upside down in panel 2 (top row, far right); active outline moves to panel 2. The hint "To draw a page by hand, do not type on it." fades up bottom-right. Hold.

## Frame 4 — Why the top row is upside down

- scene: The sheet, large and centered: 8 panels numbered 5 4 3 2 over 6 7 8 1; the top row rotates 180° into place and a mono tag reads "Top row prints upside down"
- voiceover: "The top row prints upside down. This is correct."
- duration: 5s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/04-sheet-layout.html
- type: social_proof
- persuasion: Common-belief vs reality — pre-empt the "my print is wrong" worry
- beat: Puzzlement → reassurance
- blueprint: compose
- focal: the large sheet with panel numbers
- roles: sheet = foreground subject (~52% width, centered) · "TOP ROW PRINTS UPSIDE DOWN" kicker + ↻ = supporting · "This is correct." = supporting payoff · cream = background
- sfx: none

narrativeRole: Defuses the one moment a first-timer thinks the print failed; it establishes the sheet that is the stage for every task frame.
keyMessage: Upside-down pages on the top row are intended.


Scene 1 (0.0–0.5s): the large sheet is centered (arrives via zoom-through); all 8 numbers upright: 5 4 3 2 / 6 7 8 BACK 1 FRONT.
Scene 2 (0.5–2.2s): on "top row… upside down", the kicker writes in upper-left with the coral ↻, and the four top-row numbers rotate 180° one after another, right to left (2, 3, 4, 5), each a smooth power3 turn.
Scene 3 (3.6–5.0s): on "correct", "This is correct." sets in Newsreader italic lower-right (fade + small rise); then everything holds completely still (held frame).

## Frame 5 — Print the sheet

- scene: The kit's print-settings card: Paper US Letter · Orientation Landscape · Scale 100% · Margins None; the four rows check on in sequence as the line is spoken; the sheet slides out like paper from a printer
- voiceover: "Print the sheet in landscape on US Letter paper, at 100 percent scale, with no margins."
- duration: 8s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-print.html
- type: feature_showcase
- persuasion: Numbered enumeration — one setting per cue
- beat: Focus + confidence
- blueprint: grid-card-assemble (Adapt)
- focal: print-settings card with four rows
- roles: settings card (left) = foreground subject · printer slot + emerging sheet (right) = foreground payoff · shortcut line = supporting · cream = background
- sfx: none

narrativeRole: Step 2 of the map. The four settings are where a print goes wrong, so each one gets its own beat.
keyMessage: Landscape, US Letter, 100 percent, no margins.


Adapt: the "list that accumulates" is the four settings checking on in VO order; the payoff is the sheet leaving the printer.
Scene 1 (0.0–0.6s): settings card (title "Print the sheet", kicker "PRINT SETTINGS") and the dark printer slot are in place; all four rows show values with grey checks.
Scene 2 (1.5–5.6s): each row's check turns coral and its value goes bold on its VO word: "landscape" (1.5) → Orientation, "US Letter" (2.4) → Paper, "100 percent" (3.8) → Scale, "no margins" (5.3) → Margins.
Scene 3 (5.8–7.4s): the sheet slides down out of the printer slot (clip reveal from the slot edge, power2.inOut), its top row upside down, as in the sketch; the "⌘ P (Mac) · Ctrl P (Windows)" line fades up bottom-left. Hold.

## Frame 6 — Task 1: Make the fold lines

- scene: Stage = the white sheet as a top-down diagram at left, the kit's TASK 1 card at right with all 9 STE steps; the sheet folds bottom-to-top, opens, folds left-to-right twice, opens to show 8 equal panels in 2 rows of 4; the active step highlights in the card
- voiceover: "Task one. Make the fold lines. Fold the bottom edge to the top edge. Open the sheet. Fold the sheet in half two times, from left to right. Open the sheet. Make sure that you have eight equal panels."
- duration: 15s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-task1-fold-lines.html
- type: feature_showcase
- persuasion: Demonstration + signposting — diagram moves in step with the highlighted card line
- beat: Comprehension + momentum
- blueprint: compose
- focal: the sheet folding into fold lines
- roles: sheet diagram (left, ~45% width) = foreground subject · TASK 1 card (right, verbatim kit text, 10 steps) = supporting rail · fold-state labels + "8 equal panels / 2 rows of 4" tag = supporting · cream = background
- sfx: none

narrativeRole: Step 4 of the map, first half. Gives the sheet its fold lines, which the cut and the final fold depend on.
keyMessage: Fold and open the sheet until it shows 8 equal panels.


Layout: asymmetric 55/45 — diagram left, task card right (card is present from the push-slide with all steps muted).
Scene 1 (0.0–1.5s): on "Task one", the card header TASK 1 / "Make the fold lines" brightens; the printed sheet lies flat at left, printed side up, panel numbers faint; steps 1–2 highlight briefly together.
Scene 2 (3.3–5.0s): on "Fold the bottom edge", step 3 highlights; the bottom row rotates up onto the top row (rotateX about the horizontal center line); step 4 highlights as a thumbnail-crease line sweeps along the fold.
Scene 3 (5.8–6.6s): on "Open", step 5 highlights; the flap rotates back down, leaving a dashed horizontal fold line.
Scene 4 (7.3–9.8s): on "Fold the sheet in half two times", steps 6–7 highlight; the left half rotates over onto the right (rotateY about the center vertical), then the folded stack folds in half again (rotateY about its new center); step 8 crease sweep.
Scene 5 (10.6–11.6s): on "Open", step 9 highlights; both folds rotate back open, leaving dashed vertical lines at the quarters and center.
Scene 6 (12.1–15.0s): on "eight equal panels", step 10 highlights coral-soft; the 8 panels flash a soft coral outline one by one in reading order (fast stagger) and the mono tag "8 equal panels · 2 rows of 4" appears; hold.

## Frame 7 — Task 2: Cut the slot

- scene: Same stage. Sheet folds in half left-to-right; the yellow CAUTION card appears first in the task card; then a coral cut line draws from the folded edge along the horizontal fold and stops hard at the first vertical fold line, with a "2.75 in (70 mm)" mono dimension
- voiceover: "Task two. Cut the slot. Fold the sheet in half from left to right. Caution: do not cut past the first vertical fold line. If the cut is too long, the zine will come apart. Cut along the horizontal fold line from the folded edge."
- duration: 17.5s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-task2-cut.html
- type: feature_showcase
- persuasion: Stakes / consequence — the safety notice comes before its step, exactly as STE requires
- beat: Focus + caution
- blueprint: compose
- focal: the coral cut line that stops at the first vertical fold
- roles: folded half-sheet (left) = foreground subject · TASK 2 card with CAUTION before step 3 (right, verbatim) = supporting rail · dimension "2.75 in (70 mm)", "folded edge", "first vertical fold line" labels = supporting · cream = background
- sfx: none

narrativeRole: Step 3 of the map, and the one step that can damage the work. The coral cut line is the video's single voltage moment.
keyMessage: Cut only from the folded edge to the first vertical fold line.


Layout: asymmetric 50/50 — diagram left, card right.
Scene 1 (0.0–2.6s): on "Task two… Cut the slot", card header brightens; the opened sheet (8 panels, dashed fold lines) lies at left.
Scene 2 (2.7–5.6s): on "Fold the sheet in half", steps 1–2 highlight; the left half rotates over onto the right (rotateY), then the folded sheet slides so the folded edge is on the left (bold ink edge) — the sketch pose. Labels "folded edge" and "first vertical fold line" fade in.
Scene 3 (6.0–12.9s): on "Caution", the yellow CAUTION notice lifts to full strength (others dim) and its border pulses once; the first vertical fold line on the diagram turns coral-dashed as a stop marker on "first vertical fold line" (8.4). Then everything holds still through "the zine will come apart" (held beat).
Scene 4 (13.6–17.5s): on "Cut along", step 3 highlights; the coral cut line draws from the folded edge along the horizontal fold (svg-path-draw) with the scissors riding its head, and stops hard at the first vertical fold line (expo.out arrival, no overshoot); the dimension tag "├ 2.75 in (70 mm) ┤" fades in under it; step 4 highlights. Hold.

## Frame 8 — Task 3: Fold the zine

- scene: Same stage, turning to a three-quarter view. The top row folds back behind the bottom row; hands-free arrows push the two ends to the center; the slot opens into a diamond, then a "+" shape; the four arms fold together into a book
- voiceover: "Task three. Fold the zine. Fold the top row back, behind the bottom row. Hold the two ends. Push them slowly to the center. The slot opens into a diamond, then into a plus shape. Fold the four arms together to close the zine like a book."
- duration: 18s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/08-task3-fold-zine.html
- type: feature_showcase
- persuasion: Demonstration + progressive disclosure — the hardest spatial step shown one shape at a time (diamond → plus → book)
- beat: Fascination + "aha"
- blueprint: compose
- focal: the large "+" shape
- roles: "+" (center-left, ~31cqw square, same scale as sheets in frames 4–7) = foreground subject · diamond (lower-left) and book (lower-right) thumbnails = supporting before/after · TASK 3 card (right, verbatim, 9 steps) = supporting rail · push arrows = supporting · cream = background
- sfx: none

narrativeRole: Step 4 of the map, second half. The "+" fold is the hard-to-describe step, so the diagram does the explaining.
keyMessage: Push the ends to the center until the sheet makes a plus shape, then close it like a book.


Layout: asymmetric 55/45 per confirmed sketch v2 — hero "+" left-center, card right.
Scene 1 (0.0–3.2s): on "Task three… Fold the zine", card header brightens; at the hero position, the cut sheet (8 panels, slot in center) lies flat.
Scene 2 (3.3–5.6s): on "Fold the top row back", step 1 highlights; the top row rotates back behind the bottom row (rotateX away from viewer) leaving the strip 6 7 8 1; step 2 highlights.
Scene 3 (6.2–9.6s): on "Hold the two ends… Push them", steps 3–4 highlight; coral push arrows appear at both strip ends and the ends slide toward the center while the slot bows open (the strip compresses horizontally, the center rises).
Scene 4 (10.4–12.2s): on "diamond", the small diamond thumbnail at lower-left appears and the strip shows the diamond opening at its center.
Scene 5 (12.2–14.0s): on "plus shape", step 5 highlights; the strip resolves into the large "+" shape (four arms: 4 top, 1 bottom, 6 left, 8 right; center square outlined coral) — the hero moment; mono label '"+" shape' writes in.
Scene 6 (14.2–18.0s): on "Fold the four arms together", step 6 highlights; the arms swing together (rotateY pairs) and the book thumbnail at lower-right appears as the "+" closes; steps 7–9 highlight in quick sequence near "book". Hold on the closed state.

## Frame 9 — Check the zine

- scene: The finished zine flips page by page 1 → 8, a mono counter ticks with each page; a NOTE card (accent-soft) appears: "To make more copies, copy the flat sheet before you cut it."
- voiceover: "Make sure that the pages are in the sequence one to eight. Your zine is complete."
- duration: 6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-check.html
- type: benefit_highlight
- persuasion: Callback — the book from the hook, now made by the viewer
- beat: Satisfaction
- blueprint: compose
- focal: the open zine turning its pages 1→8
- roles: open spread (left) = foreground subject · mono page counter "1 2 3 4 5 6 7 8" = supporting · NOTE card = supporting · cream = background
- sfx: none

narrativeRole: Closes the loop from the hook: the impossible object is now in the viewer's hands, with one last check.
keyMessage: Pages 1 to 8 in order means the zine is correct.


Scene 1 (0.0–2.9s): on "the pages are in the sequence", the book from frame 1 opens to a spread and its pages turn (rotateY on the spine) 1→8 in an even rhythm; each turn fills the next counter digit from muted to ink.
Scene 2 (2.9–4.5s): the counter completes at "eight"; the last spread (pages 4–5 per sketch) settles.
Scene 3 (4.5–6.0s): on "complete", the NOTE card ("To make more copies, copy the flat sheet before you cut it.") rises in under the counter; hold.

## Frame 10 — Make your zine

- scene: Chalk ground, the closed zine at left; "Make your zine." in Newsreader and "zine.imurph.com" in coral mono at right; the four step words return small underneath as a recap strip
- voiceover: "Make your zine at zine.imurph.com."
- duration: 5s
- transition_in: crossfade
- status: animated
- src: compositions/frames/10-cta.html
- type: cta
- persuasion: Distillation — the whole video compressed to one URL
- beat: Resolve + inspiration
- blueprint: titlecard-reveal (Reproduce)
- focal: "Make your zine." + "zine.imurph.com"
- roles: title + URL = foreground subject · closed book (left, −3°) = supporting · recap strip "TYPE · PRINT · CUT · FOLD" = supporting · cream = background
- sfx: none

narrativeRole: Turns understanding into action with the one address the viewer has to remember.
keyMessage: zine.imurph.com.


Scene 1 (0.0–0.9s): the closed book is in place at left (from the crossfade); "Make your zine." rises in (slide-up crossfade, power3) on "Make your zine".
Scene 2 (1.4–3.0s): on "zine.imurph.com", the URL types on in coral mono (type-on, no caret).
Scene 3 (3.0–5.0s): the recap strip fades up; final hold, perfectly still, to the last frame.
