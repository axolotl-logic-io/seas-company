# Narration-led adaptation, 2026-11-04

Source: `Sea's Company (Structured)(2).docx`, mirrored in `sc.md`. The current manuscript supersedes the old image directions and expression comments. The game script makes presentation decisions; the author only needs to supply story text. This is an authored adaptation, not a runtime model that interprets prose during play.

## Staging decisions

- Rescue: keep Stan offscreen as “A Voice” until the twins enter the bunkroom. Their initial concern, the joke reactions, mutual blushes and the player's relapse determine expressions. Keep “Beanie Guy” and “Cleft Chin” speaker names until introductions.
- Recovery: Ford first appears in the bunkroom to help the player. Move to the galley when they arrive there; use the existing food illustration for dinner, then return to the bunk with Stan before sleep. Concern and reassurance replace leftover joke expressions.
- Arrival: Stan's conspiratorial offer uses his sly expression. Ford enters sternly. All three lodging choices converge on temporary passage; the game does not imply that choosing help home commits the player to permanent membership. Supplies and a rest precede the evening outings.
- Museum: Ford's enthusiasm and disappointment follow the conversation. Keep him to the right at the horn so its root remains visible. Narration supplies gloves before the sampling. Spoken question choices are echoed before Ford answers. Leaving the bathroom removes Ford; returning restores him. Each investigation choice retains its own discovery and escape. The museum security personnel remain narrated, rather than being represented by unrelated sprites.
- Stan after dark: retain the white suit for his dancing entrance, then wear the navy anorak over the same white suit and burgundy shirt outdoors. The patron's new art has the cigarette, lighter, monkey stamp and speedo described by the text. Stan changes to tropical trunks at the cubbies. Four generated expressions support the toast, bashful glance, serious warning and alarm. Every swimwear expression explicitly carries the `swim` attribute, including dialogue: Ren’Py otherwise prefers the shorter coat image names. Restore swimwear after scene clears inside the club, and show the anorak-over-suit images when they dress to leave. Hide him during the second beer run. Keep that evening ensemble through the apology and boat reunion. Hide Stan as the narration establishes a change into dry clothes before the hammock scene.
- Film festival: show Stan laughing and Ford blushing at the museum jokes. Ford is excited about the cipher while Stan is angry about the ending. Alarm and the escape follow the brawl. The chapter subtitle now describes the movie rather than an absent dinner.
- Outro: both twins help with the hammock, then leave the frame as the player settles down. All routes retain the manuscript's common ending.

## Prose and source fixes

Retain the manuscript's dialogue, all 12 menus, two backstories, approval changes, three evening routes, and repeat-menu semantics. A direct call exits the bunk menu; looking around and trying to rise are optional, once each. Standard player inputs and pronoun substitution remain.

Three brief connective additions establish temporary lodging after the arrival decision, food/rest before the outing, and Ford handing over sampling gloves. Longer narration is split at location changes. Correct the source's “Play” speaker typo and Ford's glance at himself. Remove the old hand-rubbing action bubble, which came from superseded art directions. Remaining action bubbles represent actions still present in this manuscript, such as turning to a speaker or whispering.

Existing backgrounds already cover every narrated location; no new location art was required. New character artwork, its exact prompts, and runtime paths are in `context-art.json` and `evening-art.json`. The built-in image generator produced all new art; `build_assets.py` converts the retained source PNGs into runtime sizes. Background patrons remain discreetly framed; narration is unchanged.

## Verification

See the current section of `VALIDATION.md` for lint, helper tests, route runs, costume checks, and build results. Automated playthrough evidence lives in `validation/context-*`; the development harness is excluded from distribution builds. Old saves can point into changed script passages; start a new game to review this revision.
