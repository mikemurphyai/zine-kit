# One-Sheet Zine Kit

A browser-based kit for making an 8-page zine from one sheet of US Letter paper. Fill in your pages, print the sheet, then fold and cut it into a zine.

## What it does

- Gives you a form for the 8 pages of the zine, in reading order, with a live preview of the print sheet.
- Puts each page in the correct panel and orientation on the sheet, so the zine reads correctly after you fold it.
- Shows fold-and-cut instructions on the page, and can print them on a second sheet.

## The STE experiment

The project also tests **ASD-STE100 Simplified Technical English (STE)**. All the fold-and-cut instructions are written in it.

STE is a controlled-language standard that began in aerospace maintenance manuals. It limits grammar and vocabulary so that people can follow instructions without confusion, including people who read English as a second language.

Instructions for folding a zine make a good test subject. The task is physical and in sequence, and it has one step that can damage the work (the cut). It also has a spatial step that is hard to describe (the "+" fold). If STE handles these clearly, it can handle most how-to writing. The rules used are listed in [STE notes](#ste-notes).

## Files

| File | What it is |
|---|---|
| `zine-kit.html` | **The kit.** A self-contained page where you fill in 8 zine pages, preview the print sheet, and print it. It includes the fold-and-cut instructions written in STE. |
| `media/` | The how-to video (`how-to-make-a-zine-v2.mp4`, 1 min 34 s, narrated in STE) and its poster image. The page plays it above the task cards. It does not print. |
| `deploy/` | Docker Compose file, nginx config, the deployed copy of the page (`site/index.html` and `site/media/`), and a README with update steps for the hosted site. |
| `README.md` | This file. |

## Hosted version: zine.imurph.com

The kit is hosted at <https://zine.imurph.com>. It is public, and no sign-in is needed. The request path is:

```
Browser → Cloudflare (proxy, HTTPS) → Traefik (routing) → nginx container in /docker/zine (serves index.html)
```

- **Nothing is stored on the server.** Each visitor's zine is saved only in their own browser.
- **Search engines are asked not to list the page.** nginx sends a `noindex` header, so people find the site only through a shared link. To allow listing, remove the `X-Robots-Tag` line from `deploy/default.conf`.
- **To update the page:** after you change `zine-kit.html`, follow `deploy/README.md`.

## Requirements

- A desktop browser. Chrome is recommended because the print layout was written for it.
- An internet connection, which the page uses to load its fonts from Google Fonts. Without one, the page still works but uses fallback fonts, so text may fit differently.
- A printer that takes US Letter paper (8.5 × 11 in).
- Scissors.

There is nothing to install or build.

## Make a zine

1. Open the kit in Chrome. Use <https://zine.imurph.com>, or open the local `zine-kit.html`: double-click it in Finder, or run this command from this folder:

   ```sh
   open -a "Google Chrome" zine-kit.html
   ```

2. Type your pages in the form on the left, from page 1 (front cover) to page 8 (back cover). The sheet preview on the right updates as you type.
   - To draw a page by hand, leave it empty. It prints blank.
   - If a page shows a yellow warning, its content will not fit. Shorten the text or use a smaller image.
3. Under **Lettering**, choose a lettering style (Typewriter, Marker, Serif, or Sans) and the print options.
4. Press **⌘P** and use these print settings:

   | Setting | Value |
   |---|---|
   | Paper | US Letter |
   | Orientation | Landscape |
   | Scale | 100% (Actual size) |
   | Margins | None |

5. Follow Tasks 1–3 at the bottom of the page to fold, cut, and assemble the zine.

**To check that the print is correct:** in the print preview, you should see exactly one landscape page, or two if "Print the instructions on a second sheet" is on. The top row should be upside down. That is intended, because the top row flips over when you fold the zine.

Print from zine.imurph.com or the local file. If the page is shown inside another app (for example, as a Claude artifact), that app may block printing.

## How the sheet works

The sheet is 11 × 8.5 in landscape, divided into 8 panels of 2.75 × 4.25 in (70 × 108 mm):

```
+--------+--------+--------+--------+
|   5    |   4    |   3    |   2    |   <- printed upside down
+--------+========+========+--------+   ==== cut line (5.5 in)
|   6    |   7    | 8 BACK | 1 FRONT|
+--------+--------+--------+--------+
```

The form lets you enter pages in reading order, and the page places each one in the correct panel. Content prints on one side only, because the back of the sheet ends up hidden inside the folded zine.

## Behavior and limitations

- **Your work saves to the browser.** The kit stores your pages in `localStorage` under the key `one-sheet-zine-kit-v1`. Each copy of the page (the local file, the hosted site, or any other copy) stores its data separately, so fill in your zine in the same copy you print from.
- **Images are scaled down** to 1000 px on the long edge so that they fit in browser storage. If storage is still full, your text is saved but the images are not, and the page shows a message.
- **"Clear all" and "Load example" ask for a second click** before they replace your pages.
- **Fold lines do not print by default.** If the printer shifts the image slightly, printed fold lines will not match the real folds and will make folding harder. Fold edge to edge instead, as Task 1 says.
- **Not yet checked:** a real print on paper, and printing from Safari or Firefox.

## STE notes

These are the STE rules the instructions follow, for reference when writing more STE:

- **One instruction per sentence.** "Fold" and "Push along the fold" are separate steps.
- **Sentence length.** A procedural sentence has 20 words or fewer. A descriptive sentence has 25 words or fewer.
- **Imperative mood and active voice.** Write "Cut along the fold line," not "The paper should be cut."
- **Approved words, each with one meaning.** Examples of the substitutions used:

  | Not approved | Used instead |
  |---|---|
  | unfold | open |
  | crease | fold line |
  | ensure / verify | make sure |
  | need (verb) | necessary |
  | lengthwise | "so that the long edges are at the top and the bottom" |

- **No phrasal verbs, and no verbs in the "-ing" form.**
- **A safety notice comes before its step.** A WARNING is for risk of injury, and a CAUTION is for risk of damage. Each one gives the command first and the reason second.
- **A NOTE contains information only**, never an instruction you must follow.

The word choices above were checked against STE rules from memory, not against the official dictionary. The words "fold" and "outer" are worth a check against the standard.

**Official source:** <https://www.asd-ste100.org>, where you can request a copy of the standard.

## Change the kit

All the HTML, CSS, and JavaScript are in `zine-kit.html`, and the page needs no build step. Edit the file, then reload it in the browser.

- The page text and the STE task cards are in the HTML, in the section with `id="howto"`.
- The example zine content is in the `EXAMPLE` array in the script.
- The panel print order is in `ORDER = [5, 4, 3, 2, 6, 7, 8, 1]` (top row, then bottom row, left to right).

**To publish it as a Claude artifact,** remove the `<!doctype>`, `<html>`, `<head>`, and `<body>` wrapper tags first, because the artifact host adds its own. The local file includes them so that it renders correctly when you open it directly.

## Ideas for next STE experiments

- Rewrite another real procedure in STE, such as a setup guide from an existing README, and compare the two versions.
- Build a small STE checker that flags sentences over 20 or 25 words, passive voice, and common unapproved words.

## License

- **Code** (the kit page, deploy config, and video build scripts): [MIT](LICENSE).
- **How-to video and poster image** (`media/`, and the video's audio in `videos/how-to-make-a-zine/assets/`): [CC BY-NC 4.0](media/LICENSE.md). The music was made with a model whose weights are licensed for non-commercial use only.
- **Fonts** in `videos/how-to-make-a-zine/assets/fonts/` (Newsreader, Public Sans, IBM Plex Mono): SIL Open Font License 1.1. The license text for each font is in that folder.
