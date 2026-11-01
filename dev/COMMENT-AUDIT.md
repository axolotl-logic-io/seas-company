# Source comment audit

The preserved document is `sc.docx`; the extracted XML is in `docx/word/`. Its `comments.xml` contains 22 comments, with IDs 0–21. `sc.md` retains all 22 comment markers.

| ID | Source meaning | Implementation |
| --- | --- | --- |
| 0 | Clear the scene and display the raft background | `scene bg raft at heat` in `script.rpy` |
| 1 | Narr abbreviates narrator | Unattributed Ren'Py narration |
| 2 | Narr uses the narrator dialogue box | Custom `narrator` character and shared say screen |
| 3 | Display an alternate character name | `s_voice`, `s_beanie`, `f_cleft` |
| 4 | Keep Stan's identity behind the alternate name | `kind=s`, preserving his callback and image tag |
| 5 | Branch displays a menu | Ren'Py `menu` statements |
| 6 | The branch item is clickable text | Menu captions |
| 7 | Parentheses in menu captions have no special meaning | Literal parenthesized captions |
| 8 | Run the indented lines after selection | Ren'Py menu blocks |
| 9 | Repeat a branch without the selected option | `menu bunk_branch` with `set bunk_menu` |
| 10 | Repeat a branch without the selected option | Both repeat paths jump to `bunk_branch` |
| 11 | Show the sprite instantly | The first Stan and Ford appearances have no transition |
| 12 | Position the sprite at left; center is the default | Explicit `left` and `right` transforms at 0.25 and 0.75 |
| 13 | Branches can change reality and rejoin later | Separate Stan, Ford, and film labels, each joining `outro` |
| 14 | Increment Stan's approval by two | `approve("stan", 2)` |
| 15 | Prompt for the player's name and interpolate it | `renpy.input`, `player_name`, and dialogue interpolation |
| 16 | Create Ford's eyes-closed and raised-finger poses | `ford eyesclosed`, `ford finger` |
| 17 | Add two to approval; negative changes are possible | `approve` adds the signed amount; helper tests cover a negative value |
| 18 | Use an action bubble | `show_act` and the say screen's action frame |
| 19 | Bracketed notes are developer comments | Source note preserved as an in-code comment; the dinner illustration also appears as `cg dinner` |
| 20 | Render Ford's frown image | `ford frown` and its generated sprite |
| 21 | Curly-brace content belongs in the action bubble | Source action notes become `show_act`; internal thoughts use `p_think` |

Comments 9 and 10 refer to “Voice your concerns” as an example, but their anchors are the two repeat paths in the initial bunk menu. The repeat behavior follows those anchors.

Later appearances and expression updates use brief transitions, as comment 12 permits.
