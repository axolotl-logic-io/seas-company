## Characters, images, transforms and helpers for Sea's Company.

################################################################################
## Fonts
################################################################################

init python:
    # Use the real italic and bold faces of Crimson Text instead of synthesized ones.
    _crimson = "fonts/CrimsonText-Regular.ttf"
    config.font_replacement_map[_crimson, False, True] = ("fonts/CrimsonText-Italic.ttf", False, False)
    config.font_replacement_map[_crimson, True, False] = ("fonts/CrimsonText-Bold.ttf", False, False)
    config.font_replacement_map[_crimson, True, True] = ("fonts/CrimsonText-BoldItalic.ttf", False, False)


################################################################################
## Player details
################################################################################

default player_name = "You"
default player_home = "somewhere far from here"
default p_subj = "they"
default p_obj = "them"
default p_wants = "want"

init python:
    import re

    _PRONOUNS = {
        "he": ("he", "him", False),
        "him": ("he", "him", False),
        "she": ("she", "her", False),
        "her": ("she", "her", False),
        "they": ("they", "them", True),
        "them": ("they", "them", True),
    }

    def set_pronouns(text):
        """Turn input such as "she/her" or "xe/xem" into subject and object forms."""
        parts = [x for x in re.split(r"[/,\s]+", text.strip().lower()) if x]

        if not parts:
            subj, obj, plural = "they", "them", True
        elif parts[0] in _PRONOUNS:
            subj, obj, plural = _PRONOUNS[parts[0]]
        else:
            subj = parts[0]
            obj = parts[1] if len(parts) > 1 else parts[0]
            plural = False

        store.p_subj = subj
        store.p_obj = obj
        store.p_wants = "want" if plural else "wants"


################################################################################
## Approval
################################################################################

default stan_approval = 0
default ford_approval = 0

init python:

    def approve(who, amount):
        """Change a twin's approval and tell the player about it."""
        if who == "stan":
            store.stan_approval += amount
            name = "Stan"
        else:
            store.ford_approval += amount
            name = "Ford"

        if amount >= 2:
            msg = __("%s really liked that.") % name
        elif amount > 0:
            msg = __("%s liked that.") % name
        else:
            msg = __("%s will remember that.") % name

        renpy.notify(msg)


################################################################################
## Speaker focus
################################################################################
## The sprite of the twin who is talking stays bright; the other one dims a
## little. Narration and the player's lines leave everyone bright.

default speaking_tag = None

init -5 python:

    _focus_state = { }

    def speaker(tag):
        def callback(event, **kwargs):
            if event == "begin":
                store.speaking_tag = tag
        return callback

    class SpriteFocus(object):

        def __init__(self, tag):
            self.tag = tag

        def __call__(self, trans, st, at):
            sp = store.speaking_tag
            target = 1.0 if (sp is None or sp == self.tag) else 0.0

            value, last = _focus_state.get(self.tag, (target, at))
            dt = at - last
            if dt < 0 or dt > 1.0:
                value = target
            else:
                step = dt * 5.0
                if value < target:
                    value = min(target, value + step)
                else:
                    value = max(target, value - step)

            _focus_state[self.tag] = (value, at)

            dim = 1.0 - value
            trans.matrixcolor = BrightnessMatrix(-0.13 * dim) * SaturationMatrix(1.0 - 0.3 * dim)

            if value != target:
                return 1.0 / 30
            return 0.15


transform focus(tag):
    function SpriteFocus(tag)


################################################################################
## Characters
################################################################################

define config.say_attribute_transition = Dissolve(0.15)

define narrator = Character(None, what_italic=True, what_color="#3b2a1c", callback=speaker(None))

define p = Character("[player_name]", callback=speaker(None))
define p_think = Character("[player_name]", kind=p, what_italic=True, what_color="#5a4630",
    what_prefix="(", what_suffix=")")

define s = Character("Stan", image="stan", callback=speaker("stan"))
define s_voice = Character("A Voice", kind=s)
define s_beanie = Character("Beanie Guy", kind=s)

define f = Character("Ford", image="ford", callback=speaker("ford"))
define f_cleft = Character("Cleft Chin", kind=f)

define twins = Character("Stan & Ford", callback=speaker(None))

define patron = Character("Patron", image="patron", callback=speaker("patron"))
define lizard = Character("Lizard Head", image="lizard", callback=speaker("lizard"))


################################################################################
## Sprites
################################################################################

init python:
    for _n in ("neutral", "smile", "grin", "frown", "blush", "uncomfortable",
               "laugh", "embarrassed", "anxious", "grimace", "suit"):
        renpy.image(("stan", _n), At("images/sprites/stan_%s.png" % _n, focus("stan")))

    for _n in ("neutral", "smile", "grin", "frown", "blush", "uncomfortable",
               "shocked", "eyesclosed", "finger"):
        renpy.image(("ford", _n), At("images/sprites/ford_%s.png" % _n, focus("ford")))

    renpy.image(("stan", "sly"), At("images/sprites/stan_grin.png", focus("stan")))

    # Expression aliases chosen by context; the manuscript need not name assets.
    renpy.image(("stan", "excited"), At("images/sprites/stan_grin.png", focus("stan")))
    renpy.image(("ford", "embarrassed"), At("images/sprites/ford_blush.png", focus("ford")))
    renpy.image(("ford", "serious"), At("images/sprites/ford_frown.png", focus("ford")))

# Swim expressions are explicit in both show statements and dialogue.
# Ren'Py can otherwise prefer a shorter coat image name on expression changes.
init python:
    for _expr, _swim_expr in {
        "neutral": "smile", "smile": "smile", "grin": "smile",
        "laugh": "laugh", "blush": "blush", "embarrassed": "blush",
        "frown": "anxious", "uncomfortable": "anxious",
        "anxious": "anxious", "grimace": "anxious",
    }.items():
        renpy.image(("stan", "swim", _expr),
            At("images/sprites/stan_swim_%s.png" % _swim_expr, focus("stan")))


image patron = At("images/sprites/patron_speedo.png", focus("patron"))
image lizard = At("images/sprites/lizard.png", focus("lizard"))


################################################################################
## Backgrounds that reuse other art
################################################################################

image bg street night = Transform("bg street", matrixcolor=TintMatrix("#7487c4") * BrightnessMatrix(-0.28))
image bg street dusk = Transform("bg street", matrixcolor=TintMatrix("#e8a87c") * BrightnessMatrix(-0.06))
image bg bunk dark = Transform("bg bunk", matrixcolor=BrightnessMatrix(-0.35) * SaturationMatrix(0.6))

image sun_glare:
    Solid("#fff6d8")
    alpha 0.0
    block:
        ease 2.6 alpha 0.32
        ease 2.6 alpha 0.12
        repeat


################################################################################
## Transforms
################################################################################

## Usual two-person composition: Stan on the left, Ford on the right.
## Solo scenes can move them to keep the narrated subject visible.
transform left:
    xpos 0.25 xanchor 0.5 ypos 1.0 yanchor 1.0

transform right:
    xpos 0.75 xanchor 0.5 ypos 1.0 yanchor 1.0

transform center:
    xpos 0.5 xanchor 0.5 ypos 1.0 yanchor 1.0

transform farright:
    xpos 0.8 xanchor 0.5 ypos 1.0 yanchor 1.0

## Enter from off-screen.
transform enter_left:
    xpos -0.3 xanchor 0.5 ypos 1.0 yanchor 1.0
    easein 0.5 xpos 0.25

transform enter_right:
    xpos 1.3 xanchor 0.5 ypos 1.0 yanchor 1.0
    easein 0.5 xpos 0.75

## A blurry view that sharpens, for waking up.
transform wake:
    blur 40 matrixcolor BrightnessMatrix(-0.5)
    easein 2.5 blur 0 matrixcolor BrightnessMatrix(0.0)

## Gentle rocking of a boat.
transform rocking:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.04
    block:
        ease 3.2 rotate 0.6 yoffset 6
        ease 3.2 rotate -0.6 yoffset -6
        repeat

## Heat haze on the raft.
transform heat:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.05
    block:
        ease 4.0 zoom 1.07 yoffset 8
        ease 4.0 zoom 1.05 yoffset -4
        repeat

## Running through the streets.
transform running:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.12
    block:
        linear 0.18 yoffset -10 xoffset 6
        linear 0.18 yoffset 0 xoffset -6
        repeat

## A slow push-in for dramatic beats.
transform slow_push:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.0
    linear 14.0 zoom 1.08

## A little hop for excited sprites.
transform hop:
    easein 0.12 yoffset -24
    easeout 0.12 yoffset 0

transform dance:
    subpixel True
    easein 0.18 yoffset -12 xoffset -12
    ease 0.25 yoffset 0 xoffset 12
    ease 0.25 yoffset -8 xoffset -8
    easeout 0.2 yoffset 0 xoffset 0

define quick = Dissolve(0.25)
define slowfade = Fade(1.0, 0.6, 1.2)
define blackout = Fade(0.8, 1.2, 0.0)
