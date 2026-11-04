# Sea's Company

A non-commercial Gravity Falls fan visual novel adapted from `Sea's Company (Structured)(1).docx`. The game uses Ren'Py 8.5.3 at a virtual resolution of 1920 × 1080.

## Run the game

To launch the standalone Mac application, run:

```bash
open ~/workspace/seas-company/dist/SeasCompany.app
```

The shareable archive is `dist/SeasCompany-1.0-mac.zip` (about 69 MB). It includes the runtime; players do not need the SDK. The application is not signed or notarized.

To run the editable project with the installed SDK, run:

```bash
~/Applications/renpy-8.5.3-sdk/renpy.sh ~/workspace/seas-company run
```

Click or press Space/Enter to advance. Choose a menu option with the mouse or keyboard. Press Escape to open the game menu. Use **Journal** to see Stan's and Ford's trust, **Save** to save progress, and **Prefs** to change text speed and display settings.

The story branches into an evening with Stan, a museum visit with Ford, or the film festival. Each route rejoins the ending. The game contains no music, voices, or sound effects.

## Adaptation details

The adaptation preserves the document's dialogue, choices, alternate speaker names, approval changes, player inputs, action bubbles, and requested Ford poses. The audit of all 22 source comments is in [the comment audit](dev/COMMENT-AUDIT.md).

Presentation additions include chapter cards labeled “Timeline,” a Journal screen, speaker-focus dimming, a trust summary and route-dependent closing line, and an Atbash cipher on the title and ending screens. Obvious source typos were corrected, including a Stan line mislabeled as Ford and “Play” in place of “Player.”

Empty inputs use “Pat,” “nowhere in particular,” and “they/them.” Standard and custom subject/object pronoun pairs are supported. The 2026-11-03 revision adds the opening joke branch, removes the prototype-watercraft backstory, updates dialogue and approval points, and revises the dinner illustration. Stan wears a white suit for his animated evening entrance. Source expression names reuse matching existing expressions; his sly hand-rubbing is also described in the action bubble.

The Patron wears a towel rather than a speedo; the generated art contains no nudity.

## Asset sources

- Story: the supplied Word document; `dev/sc.md` retains its comments with anonymized author metadata. The original Word files stay local and are ignored by Git.
- Character sprites, backgrounds, dinner illustration, and base UI textures: generated for this adaptation using `gpt-image-2.5` through the local CLIProxyAPI service. Prompts and source images are preserved in `dev/`. The revised dinner and white-suit sprite were edited with the built-in image generation tool; their prompts are in `dev/revision-art.json`. These are not official production assets.
- UI panels, buttons, meters, and final image crops: `dev/build_assets.py`, using Pillow.
- [Crimson Text](https://fonts.google.com/specimen/Crimson+Text), [IM FELL English SC](https://fonts.google.com/specimen/IM+Fell+English+SC), and [Pirata One](https://fonts.google.com/specimen/Pirata+One): Google Fonts, under the SIL Open Font License. Their notices are included in `game/fonts/`.
- Engine: [Ren'Py](https://www.renpy.org/), under its bundled licenses.

Gravity Falls and its characters belong to their respective rights holders. This is an unofficial fan adaptation.

## Validate the project

Run lint and the pure Python helper tests:

```bash
~/Applications/renpy-8.5.3-sdk/renpy.sh ~/workspace/seas-company lint
cd ~/workspace/seas-company
python3 -m unittest discover -s dev -v
```

To run an automated playthrough with screenshots:

```bash
SEAS_AUTOPLAY="$HOME/workspace/seas-company/dev/shots0" \
SEAS_CHOICE=0 SEAS_DELAY=0.15 \
~/Applications/renpy-8.5.3-sdk/renpy.sh ~/workspace/seas-company run \
  --savedir "$HOME/workspace/seas-company/dev/test-saves"
```

Use a fresh output directory for each run. `SEAS_CHOICE` selects the menu index, clamped to the available choices: 0 covers Stan's route, 1 covers Ford's, and 2 covers the film festival. The harness also opens the Journal, Save, Preferences, History, About, and Help screens. It saves at the ending, changes player state, reloads, and verifies that the saved state returned. `save_verified.json` records the successful round trip. `events.jsonl` records screenshots and source locations; `complete.json` confirms that the ending was reached. The separate `--savedir` keeps test progress out of normal player saves. This is route coverage, not exhaustive coverage of every combination of choices.

Without `SEAS_AUTOPLAY`, the development harness does nothing. Distribution builds exclude it and the entire `dev/` directory.

## Rebuild the assets

The game runs without Python packages or network access beyond the SDK. To rebuild its art from the preserved sources, install Pillow in your development Python environment, then run:

```bash
python3 ~/workspace/seas-company/dev/build_assets.py
```

This reads source assets next to the script, not from `/tmp`. Regeneration of source images is separate and requires the local image service and its credentials; running the asset builder does not contact that service.

## Build a Mac distribution

```bash
~/Applications/renpy-8.5.3-sdk/renpy.sh launcher distribute \
  ~/workspace/seas-company --package mac --format app-zip --no-update \
  --destination ~/workspace/seas-company/dist
```

The resulting application includes its own runtime. It is not signed or notarized.

## Build the web version

The web version runs Ren'Py as WebAssembly in a desktop or phone browser. It needs Ren'Py's web support, which is installed in the SDK at `~/Applications/renpy-8.5.3-sdk/web/`. To reinstall it, download `renpy-8.5.3-web.zip` from the [Ren'Py 8.5.3 downloads](https://www.renpy.org/dl/8.5.3/) and unzip it into the SDK directory.

To build, run the launcher from the SDK directory:

```bash
cd ~/Applications/renpy-8.5.3-sdk
./renpy.sh launcher web_build ~/workspace/seas-company \
  --destination ~/workspace/seas-company/dist/SeasCompany-1.0-web
```

This writes `dist/SeasCompany-1.0-web/` (about 73 MB) and the same files as `dist/SeasCompany-1.0-web.zip`. The build reads three files from the project root:

- `web-icon.png`: the icon for the installable web app, made by `dev/build_assets.py`.
- `web-presplash.jpg`: the image shown while the game loads, made by `dev/build_assets.py`.
- `progressive_download.txt`: the rule list that Ren'Py created on the first build. Backgrounds and sprites download while the game runs; GUI images load up front.

To play the build locally, serve the folder over HTTP and open <http://127.0.0.1:8042/index.html>:

```bash
cd ~/workspace/seas-company/dist/SeasCompany-1.0-web
python3 -m http.server 8042 --bind 127.0.0.1
```

Opening `index.html` directly from disk does not work. Saves stay in the player's browser storage.

## Publish the web version

The web version is live at <https://seas-company.vercel.app>, in the existing `seas-company` Vercel project.

To build and publish on Vercel, run from the project root:

```bash
cd ~/workspace/seas-company
vercel deploy --prod
```

`.vercelignore` uploads game source, web icons, progressive download rules, and build scripts. It excludes local builds, saves, caches, development files, and credentials. Vercel runs `scripts/vercel-build.sh`, which downloads the pinned Ren'Py 8.5.3 SDK and web support into a temporary directory, builds the game without a display, and removes engine debug symbols. To create a preview deployment, run `vercel deploy` without `--prod`. No local SDK is needed for deployment.

On phones, Ren'Py uses its touch quick menu and a plain browser text field for name, home, and pronoun input. Otherwise phones show the same layout as desktop.

## Repository and deployment setup

Builds, saves, logs, credentials, Vercel linkage, original Word documents, and local handoff notes are ignored. The Python ignore rules come from [GitHub's Python template](https://github.com/github/gitignore/blob/main/Python.gitignore), with Ren'Py and project additions.

Set `RENPY_SDK` to your Ren'Py 8.5.3 SDK directory if it is installed elsewhere. From the repository root:

```bash
./scripts/build-web.sh                  # Rebuild only
vercel link --project seas-company      # Once per clone; select the existing team
vercel deploy                         # Build on Vercel and deploy a preview
vercel deploy --prod                  # Build on Vercel and deploy production
```

GitHub stores source and art; generated builds stay ignored. The optional `scripts/deploy-web.sh` wrapper forwards its arguments to `vercel deploy`. Each deployment builds fresh from source on Vercel. The same build configuration supports Git deployments if the repository is connected in Vercel; connecting it enables production builds from `main` and branch previews.

Image regeneration requires `IMAGE_API_KEY`; optionally set `IMAGE_API_BASE` to your OpenAI-compatible image service. Credentials are read from the environment and must never be committed. The asset builder and game do not require them.
