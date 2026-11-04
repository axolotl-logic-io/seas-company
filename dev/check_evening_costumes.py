"""Verify a Stan-route autoplay log against the narrated clothing transitions.

Usage: python3 dev/check_evening_costumes.py dev/validation/<run>
The game's actual displayed image attributes are recorded by zz_autoplay.rpy.
"""
import json
import sys
from collections import Counter
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "game/script.rpy"


def check(run_dir):
    source = SCRIPT.read_text().splitlines()
    start = source.index("label stan_after_dark:") + 1
    stop = source.index("label reykjavik_international_film_festival:") + 1

    def marker(text):
        return next(i + 1 for i, line in enumerate(source)
                    if start <= i + 1 < stop and text in line)

    dance = marker("show stan suit at center, dance")
    coat = marker("show stan evening grin at center")
    swim = marker("show stan swim smile with dissolve")
    redressed = marker("show stan evening anxious at center with dissolve")
    changed = marker('"After changing into dry clothes,')
    counts = Counter()
    events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines()]
    for event in events:
        file, line = event["location"]
        attrs = event["stan_attributes"]
        if not file.endswith("game/script.rpy") or not attrs:
            continue
        if dance <= line < coat:
            expected = "suit"
        elif coat <= line < swim or redressed <= line < changed:
            expected = "evening"
        elif swim <= line < redressed:
            expected = "swim"
        elif changed <= line < stop:
            raise AssertionError("Stan should be offscreen while changing: %s" % event)
        else:
            continue
        assert expected in attrs, "%s: expected %s, got %s" % (event["file"], expected, attrs)
        counts[expected] += 1
    assert all(counts[k] > 0 for k in ("suit", "evening", "swim")), counts
    assert (run_dir / "complete.json").exists(), "Playthrough must reach the ending"
    assert (run_dir / "save_verified.json").exists(), "Save/load must pass"
    result = dict(counts)
    (run_dir / "costume_verified.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(name, check(Path(name)))
