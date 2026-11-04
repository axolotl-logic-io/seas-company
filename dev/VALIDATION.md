# Evening outfit and ending hint (2026-11-04)

The dancing entrance still uses the white suit and burgundy dress shirt. New `evening` images put the navy anorak over those clothes; the outfit stays explicit through all clothed dialogue and show statements on Stan's route. It returns after the swimwear sequence and stays until the narrated change into dry clothes aboard the boat. Removed the ending's alphabet hint and its unused style; the cipher remains.

Three Stan-route playthroughs (`validation/evening-outfit0`, `evening-outfit1`, and `evening-outfit2`) cover all outdoor dialogue branches and all three toasts. Each reaches the ending and verifies save/load. `check_evening_costumes.py` verifies the displayed attributes through the dance, layered evening clothes, swimwear, and return to evening clothes. These runs contain 37/38/35 evening-outfit frames and 29/30/29 swimwear frames, respectively. The existing helper tests pass. Ren'Py lint passes without warnings: 341 dialogue blocks, 6,335 words, 12 menus.

The smile image needed a rendering correction for stray opacity outside the silhouette. Its matching blush pose now supplies a clean `AlphaMask` in Ren'Py; the original generated PNGs remain intact. Exact accepted prompts, paths and generation limitations are in `evening-art.json`. `build_assets.py` can build selected sprite names without rewriting unrelated assets.

A final render-corrected playthrough (`validation/evening-final`) repeats the ending, save/load and costume assertions. Reviewed the anorak-over-suit screenshot after the dance, the dressed apology, and the ending without its hint. Refreshed Mac and web packages match the final script, image definitions and ending screen byte for byte, and exclude the development harness.

# Narration-led revision validation (2026-11-04)

Updated against `Sea's Company (Structured)(2).docx`; `sc.md` now mirrors this manuscript without superseded art directions. Adaptation decisions are in `CONTEXT-ADAPTATION.md` and exact built-in image generation prompts in `context-art.json`.

Ren'Py 8.5.3 lint passes without warnings: 340 dialogue blocks, 6,322 words, 12 menus (`context-lint.log`). All three helper tests pass (`context-helper-tests.log`). Five playthroughs reach the ending and verify save/load in separate save directories:

| Coverage | Stan / Ford approval | Evidence directory |
| --- | --- | --- |
| Stan, corrected costume sequence | 15 / 2 | `validation/context-stan-verified` |
| Ford, museum lookout | 0 / 13 | `validation/context-final1` |
| Film festival | 1 / 6 | `validation/context-final2` |
| Ford, wander during testing | 7 / 1 | `validation/context-museum0` |
| Ford, help with testing | 0 / 10 | `validation/context-museum2` |

Each directory has `complete.json`, `save_verified.json`, source-linked events and screenshots. Costume assertions in `costume_verified.json` confirm every visible Stan frame from undressing until the club exit has `swim`, and later dressed frames do not. Reviewed screenshots of the laughing swimsuit sprite, the serious warning, and the dressed apology; transparent sprites render cleanly against the backgrounds. The new patron art matches the speedo, lighter and hand stamp. Existing backgrounds already support the narrated locations.

An initial harness run failed because displayed image tags are a set, which JSON cannot serialize. The harness now writes a sorted list. Initial Stan coverage then caught Ren'Py dropping the swim attribute when choosing shorter expression names. The game now specifies swim attributes explicitly in both dialogue and show statements; the corrected Stan run is the release evidence. Other route behavior was unchanged by that fix.

Mac and web distributions rebuilt. Refreshed `dist/SeasCompany.app` from the Mac archive and verified its script exactly matches the workspace. Both archives exclude the autoplay harness and development files. Web source is rebuilt, but no browser smoke test or live deployment was performed for this revision. These checks cover all three evening routes and all museum investigation branches, not every possible combination of earlier choices. Start a new game for this revision because old saves can reference changed script passages.

---

# Document revision validation (2026-11-03)

Updated against `Sea's Company (Structured)(1).docx`, comparing paragraph text directly with the previous Word source. The anonymized source mirror in `sc.md` reflects the new document.

Ren'Py 8.5.3 lint passes: 326 dialogue blocks, 6,174 words, 12 menus. All three Python helper tests pass. Three automated routes reach the ending and verify save/load restoration in isolated save directories:

| Route | Ending Stan / Ford trust | Evidence |
| --- | --- | --- |
| Stan | 15 / 2 | `validation/revision-route0/complete.json` |
| Ford | 0 / 13 | `validation/revision-route1/complete.json` |
| Film festival | 1 / 6 | `validation/revision-route2/complete.json` |

These runs cover both opening-joke responses, both remaining backstories, all three evening routes, and the added museum lookout approval. They do not cover every combination of choices. Screenshots and save verification remain in the corresponding validation directories.

Revised dinner artwork and Stan's white-suit sprite use the built-in image tool. Prompt descriptions, paths, expression aliases, and generation limitations are recorded in `revision-art.json`. The sly hand-rubbing pose uses existing grin art and an action bubble after two image-tool rejections. The suit sprite leaves extra headroom for its entrance sway and bounce; its source and build scaling are preserved.

Mac and web distributions rebuilt from the revised source. The local Mac app is refreshed from the new archive. Production hosting is unchanged.

---

# Validation results

Validated on 2026-10-27 on macOS with Ren'Py 8.5.3.26051504.

## Automated checks

- Ren'Py lint: passes without errors or warnings (`lint.log`). The script contains 326 dialogue blocks, 6,162 words, and 11 menus.
- Pure Python helper tests: all three tests pass (`helper-tests.log`). They cover standard, empty, and custom pronouns; signed approval updates and notification text; and trust description thresholds.
- Route playthroughs: all three exit with status 0 (`validation-runs.log`).
- Save/load: each route saves at the ending, deliberately changes Stan's approval to 999 and the player name to a sentinel, reloads, and verifies the original player details and trust values. Each `save_verified.json` confirms restoration. The temporary named save is removed afterward.

| Route | Menu index | Ending trust: Stan / Ford | Screenshots | Evidence |
| --- | --- | --- | --- | --- |
| Stan after dark | 0 | 10 / 4 | 184 | `validation/route0/complete.json` |
| A night at the museum | 1 | 2 / 6 | 177 | `validation/route1/complete.json` |
| Film festival | 2 | 5 / 3 | 142 | `validation/route2/complete.json` |

A fourth film-route run verifies the final notification fix and repeats save/load in an isolated save directory (`validation/notification-check/`, 142 screenshots). The prior version displayed literal bold tags in approval notifications because Ren'Py's notification screen escapes markup. Notifications now use plain text, and the helper test asserts those exact strings.

All 645 screenshots from these four runs remain available as losslessly compressed PNGs. `events.jsonl` in each route directory records the screenshot's source statement, speaker focus, and trust values.

## Visual review

Reviewed representative screenshots of:

- the main menu title, navigation, and cipher;
- narration, named dialogue, long paragraphs, action bubbles, and quick navigation;
- both twins' sprite positions and inactive-speaker dimming;
- chapter cards, including the two-line film-festival title;
- the dinner illustration;
- Journal portraits, card bounds, and trust meters;
- save slots, preference checkboxes, radio buttons, and sliders;
- History, About, Help, and the route-specific endings.

Fixed Journal content that exceeded its card width. Darkened quick-menu idle text. Hid unused audio controls because the game has no audio. The harness waits for animated screens and transitions to settle before taking their screenshots.

The document's 22 comments were checked against the implementation in `COMMENT-AUDIT.md`. The initial twin appearance is instantaneous, as comment 11 specifies.

## Mac package

Built `../dist/SeasCompany-1.0-mac.zip` with the bundled runtime and custom application icon. Extracted it to `../dist/SeasCompany.app`.

Verified that the archive excludes `dev/`, other distribution files, player saves, `HANDOFF.md`, and both source and compiled autoplay harness files. It includes the font copyright and license notices.

Ran lint successfully using the packaged application's own executable and packaged game directory (`package-lint.log`). Opened the standalone application through Launch Services; its process remains running for the user. The package is unsigned and not notarized.

## Web package

On 2026-10-28, built `../dist/SeasCompany-1.0-web/` with Ren'Py 8.5.3 web support. The web support zip matched the official SHA-256 checksum. The game package excludes `dev/`, player saves, `HANDOFF.md`, and the autoplay harness.

Served the build locally and drove it with Playwright in headless Chromium:

- Desktop (1280 × 720): reached the main menu within 5 seconds and played about 130 steps with no console errors. The steps covered dialogue, three choice menus, typed name input, defaults for empty input, sprites, speaker dimming, and an approval notification. Backgrounds and sprites appeared sharp on first display.
- Saves: saved to slot 1, reloaded the page, and loaded the slot. The game returned to the saved line.
- Phone (iPhone 13 profile, landscape and portrait): checked the main menu, dialogue, game menu, Save, Preferences, and Journal.

The phone check found the template's phone styles still active. They gave dialogue a dark textbox with dark text and pointed at bar, slider, scrollbar, and check box images that don't exist. The fix removed those overrides and the phone font sizes. Phones now use the desktop styles. The unused template images moved to `unused-template/phone/`. Lint and helper tests pass after the change.

The quick menu links were hard to read over the textbox edge and backgrounds. They now sit on an opaque dark bar, 46 pixels tall on desktop and 64 on touch screens, and the textbox sits directly above it. Screenshots of narration, dialogue with sprites, a choice menu, and the phone layout showed no overlap with dialogue.

The browser text input looks plainer than the rest of the game. Ren'Py uses it so phone keyboards open. Not tested: Safari, Firefox, real phones, audio (the game has none), and a full playthrough in the browser.

## Scope and limitations

These are automated route playthroughs plus manual review of selected screenshots, not a human read-through of every line. Fixed menu indices cover the three main routes and the initial repeat-menu behavior, not every possible combination of choices within each route. Save/load validation checks state restoration through Ren'Py's API; it does not exercise every save-menu button, cloud sync, or rollback sequence.

Earlier development runs used the normal save directories. Their progress and preferences were moved, without deletion, to `test-saves-local/` and `test-saves-user/` so the user's first playthrough starts clean. Future documented test commands use a separate `--savedir`.
