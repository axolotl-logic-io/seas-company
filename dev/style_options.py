"""Generate alternate art styles for review. Writes to dev/style-options/; never touches game/.

Each option redraws the current background or sprite from dev/bg and dev/spr, keeping its
composition, so the review compares style alone.

Usage: python3 style_options.py [OPTION ...] [--only NAME ...]
"""
import argparse, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "style-options")

KEEP_BG = ("Keep the same composition, camera angle, layout, objects and time of day as the reference image. "
           "Simplify small clutter, but keep every notable prop from the reference, such as photos, drawings, books, "
           "signs, bottles, lamps and exhibits. "
           "No people, no characters, no text, no captions, no watermark, no border. ")
KEEP_SPR = ("Keep the same character, outfit, colors, pose, framing and size in the image as the reference. "
            "Isolated on a fully transparent background, no ground shadow, no text, no border. ")

OPTIONS = {
    "a-episode": {
        "title": "A. Episode frame",
        "bg": ("Repaint this scene as a background painting from the Disney animated TV series Gravity Falls, so it looks "
               "like a frame from an episode. Show background style: hand-painted gouache look with soft, visible brush "
               "texture; simplified, slightly geometric shapes; no black outlines on the background; a slightly muted, "
               "natural palette of dusty teals, forest greens, warm browns and soft purples; gentle, even lighting instead "
               "of dramatic glow or bloom; fewer tiny details; calm open areas where characters "
               "would stand. "),
        "spr": ("Redraw this character exactly as he would appear in an episode of the Disney animated TV series Gravity "
                "Falls, matching the show's official character model sheets. Show character style: thin, even, dark line "
                "art; completely flat cel colors with at most one hard-edged shadow tone; no gradients, no texture, no "
                "hatching; simple white eyes with small black dot pupils; simplified clothing with only a few fold lines; "
                "stubble shown as a flat grey-blue tone on the jaw, not individual hairs. "),
    },
    "b-concept": {
        "title": "B. Concept art",
        "bg": ("Repaint this scene as development concept art for the Disney animated TV series Gravity Falls, in the "
               "style of the show's background painters: loose traditional gouache and watercolor on textured paper, "
               "visible brushstrokes and paper grain, soft edges, simplified shapes, moody atmospheric color with a "
               "slightly eerie, mysterious feeling, warm light against cool shadows, fewer small details. "),
        "spr": ("Redraw this character as development concept art for the Disney animated TV series Gravity Falls: "
                "the show's character design with slightly sketchy, hand-inked pencil line art of varying weight, "
                "flat colors laid in like gouache with a little visible brush texture and one soft shadow tone, "
                "simple white eyes with small black dot pupils. "),
    },
    "p-proportions": {
        "title": "Show proportions (characters only)",
        "spr": ("Redraw this character with the proportions and drawing conventions of the Disney animated TV series "
                "Gravity Falls character model sheets. Change the proportions: a noticeably bigger head relative to the "
                "body, a large rounded torso, shorter legs and simpler, rounder hands. Eyes are plain white ovals behind "
                "the glasses with small solid black dot pupils. Thin, even, dark line art; completely flat cel colors "
                "with one hard-edged shadow tone; no gradients, no texture, no chest hair, no hatching; simplified "
                "clothing with very few fold lines; stubble shown as one flat grey tone on the jaw. Keep the same "
                "outfit, colors, expression and gesture. Shown from mid-thigh up. "),
    },
    "c-promo": {
        "title": "C. Promotional art",
        "bg": ("Repaint this scene as official promotional key art for the Disney animated TV series Gravity Falls: "
               "crisp, clean digital vector-like shapes, flat color areas with simple cel-shaded light and shadow "
               "shapes, bright, saturated, cheerful colors, sharp edges, no painterly texture, simplified details. "),
        "spr": ("Redraw this character as official promotional art for the Disney animated TV series Gravity Falls: "
                "crisp, clean digital line art of even weight, bright saturated flat colors with simple hard-edged "
                "cel shading and a single small highlight, simple white eyes with small black dot pupils, polished "
                "and graphic. "),
    },
}

# Scenes shown in the review document: (background, sprites shown in the mock-up).
BACKGROUNDS = ["raft", "bunk", "dock", "museum", "club_street"]
SPRITES = {
    "stan_neutral": " He is Stan Pines: red knit beanie, thick black glasses, big round pink nose, white tank top, open navy anorak, five fingers per hand.",
    "ford_neutral": " He is Ford Pines: windswept grey hair with silver streaks, cleft chin, thin glasses, big round pink nose, maroon turtleneck, open navy anorak, SIX fingers on each hand.",
    "stan_grin": " He is Stan Pines: red knit beanie, thick black glasses, big round pink nose, white tank top, open navy anorak, big toothy grin, thumb pointing at himself, five fingers per hand.",
    "ford_finger": " He is Ford Pines: windswept grey hair, cleft chin, thin glasses, maroon turtleneck, open navy anorak, eager grin, one index finger raised, SIX fingers on each hand.",
}


def jobs_for(option, only):
    o = OPTIONS[option]
    jobs = []
    for bg in BACKGROUNDS if "bg" in o else []:
        if only and bg not in only:
            continue
        jobs.append((os.path.join(OUT, option, f"bg_{bg}.png"), o["bg"] + KEEP_BG,
                     os.path.join(HERE, "bg", f"{bg}.png"), "1920x1088", False))
    for spr, who in SPRITES.items():
        if only and spr not in only:
            continue
        jobs.append((os.path.join(OUT, option, f"{spr}.png"), o["spr"] + KEEP_SPR + who,
                     os.path.join(HERE, "spr", f"{spr}.png"), "1024x1536", True))
    return [j for j in jobs if not os.path.exists(j[0])]


def run(job):
    out, prompt, ref, size, transparent = job
    cmd = [sys.executable, os.path.join(HERE, "gen.py"), out, prompt, "--ref", ref, "--size", size, "--tries", "8"]
    if transparent:
        cmd.append("--transparent")
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.stdout.strip() + " " + r.stderr.strip()[-300:]).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("options", nargs="*", default=list(OPTIONS))
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [j for o in a.options for j in jobs_for(o, a.only)]
    print(f"{len(jobs)} images to generate", flush=True)
    with ThreadPoolExecutor(a.workers) as ex:
        for line in ex.map(run, jobs):
            print(line, flush=True)


if __name__ == "__main__":
    main()
