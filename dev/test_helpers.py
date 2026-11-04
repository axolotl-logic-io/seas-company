"""Test pure game helpers without launching Ren'Py: python3 -m unittest discover -s dev."""
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

GAME = Path(__file__).resolve().parent.parent / "game"


def python_blocks(path):
    source = path.read_text()
    return "\n".join(textwrap.dedent(m.group(1)) for m in re.finditer(
        r"^init(?: -?\d+)? python:\n((?:[ \t].*\n|\n)+)", source, re.MULTILINE))


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.notifications = []
        self.store = SimpleNamespace(stan_approval=0, ford_approval=0)
        self.env = {
            "store": self.store, "_": lambda text: text, "__": lambda text: text,
            "config": SimpleNamespace(font_replacement_map={}),
            "renpy": SimpleNamespace(notify=self.notifications.append, image=lambda *args: None),
            "At": lambda *args: None, "AlphaMask": lambda *args: None,
            "focus": lambda tag: None,
        }
        exec(python_blocks(GAME / "definitions.rpy"), self.env)
        exec(python_blocks(GAME / "seas_screens.rpy"), self.env)

    def test_pronoun_forms(self):
        cases = {
            "": ("they", "them", "want"),
            "  ": ("they", "them", "want"),
            "SHE/HER": ("she", "her", "wants"),
            "he, him": ("he", "him", "wants"),
            "them": ("they", "them", "want"),
            "her": ("she", "her", "wants"),
            "xe/xem": ("xe", "xem", "wants"),
            "ze": ("ze", "ze", "wants"),
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.env["set_pronouns"](value)
                self.assertEqual((self.store.p_subj, self.store.p_obj, self.store.p_wants), expected)

    def test_approval_and_notifications(self):
        approve = self.env["approve"]
        approve("stan", 2)
        approve("stan", 1)
        approve("ford", -1)
        self.assertEqual((self.store.stan_approval, self.store.ford_approval), (3, -1))
        self.assertEqual(self.notifications, [
            "Stan really liked that.",
            "Stan liked that.",
            "Ford will remember that.",
        ])

    def test_trust_thresholds(self):
        for value, expected in [(-1, "Wary"), (0, "Sizing you up"),
                                (3, "Warming up to you"), (6, "Fast friends"),
                                (9, "Thick as thieves"), (20, "Thick as thieves")]:
            with self.subTest(value=value):
                self.assertEqual(self.env["trust_words"](value), expected)


if __name__ == "__main__":
    unittest.main()
