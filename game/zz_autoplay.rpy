## Development-only autoplay harness. It does nothing unless the SEAS_AUTOPLAY
## environment variable names a directory. Then it plays the game on its own,
## saves a screenshot of every line into that directory, and picks menu options
## by the index in SEAS_CHOICE (default 0). The build excludes this file.

init 999 python:
    import os
    import json
    import time

    _ap_dir = os.environ.get("SEAS_AUTOPLAY")
    _ap_choice = int(os.environ.get("SEAS_CHOICE", "0"))
    _ap_delay = float(os.environ.get("SEAS_DELAY", "0.7"))
    _ap_state = { "n": 0, "started": False, "ui_index": 0 }
    _ap_menus = ["journal", "save", "preferences", "history", "about", "help"]
    _ap_wait = {"key": None, "since": 0.0}

    def _ap_ready(key):
        if _ap_wait["key"] != key:
            _ap_wait.update(key=key, since=time.monotonic())
            return False
        return time.monotonic() - _ap_wait["since"] >= 0.85

    def _ap_shot(tag=""):
        _ap_state["n"] += 1
        fn = os.path.join(_ap_dir, "%04d%s.png" % (_ap_state["n"], tag))
        with open(fn, "wb") as screenshot:
            screenshot.write(renpy.screenshot_to_bytes((1280, 720)))
        with open(os.path.join(_ap_dir, "events.jsonl"), "a") as events:
            events.write(json.dumps({"file": os.path.basename(fn),
                "location": renpy.get_filename_line(), "speaker": str(store.speaking_tag),
                "stan": store.stan_approval, "ford": store.ford_approval}) + "\n")

    def _ap_check_save():
        marker = os.path.join(_ap_dir, "save_test.json")
        verified = os.path.join(_ap_dir, "save_verified.json")
        slot = "_seas_autoplay_%d" % _ap_choice
        actual = {"stan": store.stan_approval, "ford": store.ford_approval,
            "name": store.player_name, "home": store.player_home,
            "pronouns": [store.p_subj, store.p_obj]}
        if os.path.exists(verified):
            return
        if not os.path.exists(marker):
            renpy.take_screenshot()
            renpy.save(slot)
            with open(marker, "w") as checkpoint:
                json.dump(actual, checkpoint)
            store.stan_approval = 999
            store.player_name = "UNRESTORED TEST VALUE"
            renpy.load(slot)
        else:
            with open(marker) as checkpoint:
                expected = json.load(checkpoint)
            assert actual == expected, "Save/load did not restore player state"
            with open(verified, "w") as result:
                json.dump(actual, result)
            renpy.unlink_save(slot)

    def _ap_tick():
        _preferences.text_cps = 0
        if renpy.get_screen("main_menu") and not _ap_state["started"]:
            if not _ap_ready("main_menu"):
                return
            _ap_shot("_mainmenu")
            _ap_state["started"] = True
            renpy.run(Start())
            return

        for menu in _ap_menus:
            if renpy.get_screen(menu):
                if not _ap_ready(menu):
                    return
                _ap_shot("_" + menu)
                return renpy.run(Return())

        if renpy.get_screen("the_end"):
            _ap_check_save()
            if not _ap_ready("end_%d" % _ap_state["ui_index"]):
                return
            if _ap_state["ui_index"] < len(_ap_menus):
                menu = _ap_menus[_ap_state["ui_index"]]
                _ap_state["ui_index"] += 1
                renpy.run(ShowMenu(menu))
                return
            _ap_shot("_end")
            with open(os.path.join(_ap_dir, "complete.json"), "w") as result:
                json.dump({"choice": _ap_choice, "screenshots": _ap_state["n"],
                    "stan": store.stan_approval, "ford": store.ford_approval}, result)
            renpy.quit()

        choice = renpy.get_screen("choice")
        if choice:
            _ap_shot("_choice")
            items = choice.scope["items"]
            item = items[min(_ap_choice, len(items) - 1)]
            return renpy.run(item.action)

        if renpy.get_screen("input"):
            _ap_shot("_input")
            renpy.queue_event("input_enter")
            return

        if renpy.get_screen("chapter_card"):
            if not _ap_ready("chapter_" + renpy.get_screen("chapter_card").scope["title"]):
                return
            _ap_shot("_chapter")
            renpy.queue_event("dismiss")
            return

        if renpy.get_screen("say"):
            _ap_shot()
            renpy.queue_event("dismiss")
            return

        renpy.queue_event("dismiss")

    if _ap_dir:
        os.makedirs(_ap_dir, exist_ok=True)
        config.always_shown_screens.append("_autoplay")
        config.main_menu_music = None
        _preferences.text_cps = 0
        _preferences.transitions = 2

screen _autoplay():
    zorder 1000
    timer _ap_delay repeat True action Function(_ap_tick)
