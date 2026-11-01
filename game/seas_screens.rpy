## Custom screens for Sea's Company: chapter cards, the journal and the ending.

################################################################################
## Chapter card
################################################################################

screen chapter_card(title, subtitle=""):
    zorder 50
    modal True

    add Solid("#0b0806cc")

    frame at chapter_in:
        style "chapter_frame"

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10

            add "gui/hand.png":
                xalign 0.5
                zoom 0.42

            text _("Timeline") style "chapter_kicker"
            text title style "chapter_title"

            if subtitle:
                text subtitle style "chapter_subtitle"

    timer 3.2 action Return()
    key "dismiss" action Return()

transform chapter_in:
    on show:
        alpha 0.0 yoffset 30
        easein 0.6 alpha 1.0 yoffset 0
    on hide:
        easeout 0.5 alpha 0.0 yoffset -20

style chapter_frame is empty:
    background Frame("gui/chapter_card.png", 40, 40)
    xalign 0.5
    yalign 0.45
    xsize 1100
    ysize 520
    padding (60, 40)

style chapter_kicker is default:
    font "fonts/IMFeENsc28P.ttf"
    size 32
    color "#7a6650"
    kerning 4
    xalign 0.5

style chapter_title is default:
    font "fonts/PirataOne-Regular.ttf"
    size 92
    color "#6b1f1f"
    xalign 0.5
    text_align 0.5
    layout "subtitle"
    xmaximum 960

style chapter_subtitle is default:
    font "fonts/CrimsonText-Italic.ttf"
    size 34
    color "#3b2a1c"
    xalign 0.5
    text_align 0.5


label chapter(title, subtitle=""):
    window hide
    call screen chapter_card(title, subtitle) with dissolve
    return


################################################################################
## Journal
################################################################################
## A page of the castaway's notes on their rescuers, reachable from the quick
## menu and the game menu.

init python:

    def trust_words(value):
        if value >= 9:
            return _("Thick as thieves")
        if value >= 6:
            return _("Fast friends")
        if value >= 3:
            return _("Warming up to you")
        if value >= 0:
            return _("Sizing you up")
        return _("Wary")

screen journal():
    tag menu

    use game_menu(_("Journal")):

        vbox:
            spacing 26
            xfill True

            text _("Field notes of [player_name], castaway of [player_home] ([p_subj]/[p_obj])."):
                style "journal_intro"

            hbox:
                spacing 40

                use journal_entry("stan", _("Stan Pines"), _("A.K.A. \"Beanie Guy.\" Pulled me out of the ocean. Picks locks faster than I can blink. Calls everyone \"kid.\""), stan_approval)
                use journal_entry("ford", _("Ford Pines"), _("A.K.A. \"Cleft Chin.\" Doctor, scientist, carrier of the Science Bag. Six fingers on each hand (!!)."), ford_approval)

            text _("{i}Trust grows with the choices you make. Neither twin forgets.{/i}"):
                style "journal_footer"

screen journal_entry(tag, name, blurb, value):

    frame:
        style "journal_card"

        hbox:
            spacing 20

            fixed:
                xsize 180
                ysize 280
                add Crop((150, 0, 420, 600), "images/sprites/%s_neutral.png" % tag):
                    zoom 0.43
                    xalign 0.5

            vbox:
                spacing 10
                xsize 340

                text name style "journal_name"
                text blurb style "journal_blurb"
                null height 6
                text _("Trust") style "journal_label"
                bar value StaticValue(max(0, min(value, 12)), 12):
                    style "journal_meter"
                text trust_words(value) style "journal_trust"

style journal_intro is default:
    font "fonts/CrimsonText-Italic.ttf"
    size 34
    color "#3b2a1c"

style journal_footer is journal_intro:
    size 28
    color "#7a6650"

style journal_card is empty:
    background Frame("gui/frame.png", 30, 30)
    padding (34, 34)
    xsize 650

style journal_name is default:
    font "fonts/PirataOne-Regular.ttf"
    size 52
    color "#6b1f1f"

style journal_blurb is default:
    size 27
    color "#2b1d12"

style journal_label is default:
    font "fonts/IMFeENsc28P.ttf"
    size 26
    color "#7a6650"

style journal_trust is default:
    font "fonts/CrimsonText-Italic.ttf"
    size 28
    color "#6b1f1f"

style journal_meter is bar:
    xsize 340
    ysize 26
    left_bar Frame("gui/meter_full.png", 13, 0)
    right_bar Frame("gui/meter_empty.png", 13, 0)


################################################################################
## Ending card
################################################################################

screen the_end():
    modal True

    add "bg storage"
    add Solid("#0b0806b0")

    frame at chapter_in:
        style "chapter_frame"
        ysize 700
        yalign 0.5

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 14

            text _("The End?") style "chapter_title"

            text _("Stan's trust: [stan_approval]   ·   Ford's trust: [ford_approval]"):
                style "chapter_subtitle"

            null height 10

            if stan_approval > ford_approval:
                text _("You and Stan are already plotting your next caper."):
                    style "ending_line"
            elif ford_approval > stan_approval:
                text _("Ford has started a new journal page with your name on it."):
                    style "ending_line"
            else:
                text _("The Stan-O-War III has found its third crew member."):
                    style "ending_line"

            null height 24

            text "GSV HVZ PVVKH RGH HVXIVGH" style "ending_cipher"
            text _("(Hint: A is Z.)") style "ending_hint"

            null height 24

            textbutton _("Return to the dock"):
                style "ending_button"
                xalign 0.5
                action Return()

style ending_line is chapter_subtitle:
    color "#6b1f1f"

style ending_cipher is default:
    font "fonts/IMFeENsc28P.ttf"
    size 36
    kerning 6
    color "#3b2a1c"
    xalign 0.5

style ending_hint is ending_cipher:
    size 22
    kerning 0
    color "#7a6650"

style ending_button is button:
    background Frame("gui/button/choice_idle_background.png", 70, 20)
    hover_background Frame("gui/button/choice_hover_background.png", 70, 20)
    padding (70, 18)

style ending_button_text is button_text:
    font "fonts/IMFeENsc28P.ttf"
    size 34
    idle_color "#2b1d12"
    hover_color "#f3dfae"
