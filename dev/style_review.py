"""Build in-game mock-ups of the style options and a Word document for choosing a style.

Reads the current art from dev/bg and dev/spr, the options from dev/style-options/, and the
textbox, name tag, and fonts from game/. Writes dev/style-options/mockups/ and
dev/style-options/Sea's Company art style options.docx. Requires Pillow and python-docx.

The mock-ups approximate the game screen: they use the real textbox art, fonts, positions,
quick-menu bar, and speaker dimming, but skip animation and the action bubbles.

Run: uv run --no-project --with python-docx --with pillow python3 dev/style_review.py
"""
import os, sys

# dev/docx/ holds the unpacked source document; keep it from shadowing the python-docx package.
sys.path = [p for p in sys.path if os.path.abspath(p or ".") != os.path.dirname(os.path.abspath(__file__))]

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(os.path.dirname(HERE), "game")
OPT = os.path.join(HERE, "style-options")
MOCK = os.path.join(OPT, "mockups")
DOCX = os.path.join(OPT, "Sea's Company art style options.docx")
W, H = 1920, 1080

BG_STYLES = [
    ("current", "Current", None),
    ("a-episode", "A. Episode frame", "a-episode"),
    ("b-concept", "B. Concept art", "b-concept"),
    ("c-promo", "C. Promotional art", "c-promo"),
]
CHAR_STYLES = [
    ("current", "1. Current", None),
    ("flat", "2. Flat cel", "a-episode"),
    ("proportions", "3. Show proportions", "p-proportions"),
]

# Each scene: background, sprites as (file, x position, speaking), speaker name or None, line, context.
SCENES = [
    ("raft", [], None,
     "Nothing but dark water as far as the eye can see. The sun beats mercilessly upon your dehydrated body, "
     "sprawled as it is across a flotilla of plastic garbage and styrofoam chunks.",
     "The opening scene. Harsh midday sun, no characters on screen."),
    ("bunk", [("stan_neutral", 0.25, True), ("ford_neutral", 0.75, False)], "Beanie Guy",
     "Hey kid, you're finally awake!",
     "The twins' first appearance, in the bunk room. Stan is speaking, so Ford is dimmed."),
    ("dock", [("stan_neutral", 0.25, False), ("ford_finger", 0.75, True)], "Ford",
     "It's possible that the horn isn't that of a narwhal and may actually be evidence of an entirely unknown species!",
     "Reykjavik harbour in the afternoon, where the player chooses a route."),
    ("museum", [("ford_finger", 0.5, True)], "Ford",
     "Yes, just as I suspected! This horn is not ivory at all, and moreover, it's a {i}right-handed{/i} helical spiral!",
     "Ford's route: the whale museum. One character centered."),
    ("club_street", [("stan_grin", 0.25, True)], "Stan",
     "Oy, áttu kveikjara takk?",
     "Stan's route at night, outside the club with the neon monkey sign. This tests night and neon lighting."),
]

FONT = os.path.join(GAME, "fonts")
F_TEXT = ImageFont.truetype(os.path.join(FONT, "CrimsonText-Regular.ttf"), 36)
F_ITALIC = ImageFont.truetype(os.path.join(FONT, "CrimsonText-Italic.ttf"), 36)
F_NAME = ImageFont.truetype(os.path.join(FONT, "IMFeENsc28P.ttf"), 40)
F_QUICK = ImageFont.truetype(os.path.join(FONT, "IMFeENsc28P.ttf"), 24)
F_LABEL = ImageFont.truetype(os.path.join(FONT, "IMFeENsc28P.ttf"), 44)


def cover(im):
    """Cover-crop to 16:9 and scale to the game resolution, as build_assets.py does."""
    w, h = im.size
    tw = h * 16 / 9
    if tw <= w:
        left = (w - tw) / 2
        im = im.crop((int(left), 0, int(left + tw), h))
    else:
        th = w * 9 / 16
        top = (h - th) / 2
        im = im.crop((0, int(top), w, int(top + th)))
    return im.resize((W, H), Image.LANCZOS)


def background(scene, folder):
    path = os.path.join(HERE, "bg", f"{scene}.png") if folder is None else os.path.join(OPT, folder, f"bg_{scene}.png")
    return cover(Image.open(path).convert("RGB"))


# Show-proportion characters have bigger heads, so they are shown smaller to keep the same framing.
SPRITE_SCALE = {"p-proportions": 0.88}


def sprite(name, folder, speaking):
    path = os.path.join(HERE, "spr", f"{name}.png") if folder is None else os.path.join(OPT, folder, f"{name}.png")
    im = Image.open(path).convert("RGBA")
    height = int(1075 * SPRITE_SCALE.get(folder, 1.0))
    im = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
    if not speaking:  # The game's speaker focus: brightness -0.13, saturation 0.7.
        alpha = im.getchannel("A")
        rgb = ImageEnhance.Color(im.convert("RGB")).enhance(0.7)
        rgb = rgb.point(lambda v: max(0, v - 33))
        im = rgb.convert("RGBA")
        im.putalpha(alpha)
    return im


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def namebox(draw_on, name, x, y):
    src = Image.open(os.path.join(GAME, "gui", "namebox.png")).convert("RGBA")
    tw = int(ImageDraw.Draw(draw_on).textlength(name, font=F_NAME))
    w, h = tw + 80, src.height
    box = Image.new("RGBA", (w, h))
    box.paste(src.crop((0, 0, 40, h)), (0, 0))
    box.paste(src.crop((40, 0, src.width - 40, h)).resize((w - 80, h)), (40, 0))
    box.paste(src.crop((src.width - 40, 0, src.width, h)), (w - 40, 0))
    draw_on.alpha_composite(box, (x, y))
    ImageDraw.Draw(draw_on).text((x + 40, y + h // 2), name, font=F_NAME, fill="#f3dfae", anchor="lm",
                                 stroke_width=2, stroke_fill="#3a120f")


def mockup(scene, bg_folder, char_folder):
    name, sprites, who, line, _ = scene
    frame = background(name, bg_folder).convert("RGBA")
    for spr, xpos, speaking in sprites:
        im = sprite(spr, char_folder, speaking or who is None)
        frame.alpha_composite(im, (int(W * xpos - im.width / 2), H - im.height))

    bar = 46
    textbox = Image.open(os.path.join(GAME, "gui", "textbox.png")).convert("RGBA")
    top = H - bar - textbox.height
    frame.alpha_composite(textbox, ((W - textbox.width) // 2, top))
    if who:
        namebox(frame, who, 175, top - 30)

    d = ImageDraw.Draw(frame)
    italic = who is None
    font = F_ITALIC if italic else F_TEXT
    text = line.replace("{i}", "").replace("{/i}", "")
    for i, ln in enumerate(wrap(d, text, font, 1470)):
        d.text((215, top + 82 + i * 46), ln, font=font, fill="#3b2a1c" if italic else "#2b1d12", anchor="lt")

    d.rectangle([0, H - bar, W, H], fill="#2b1410")
    d.rectangle([0, H - bar, W, H - bar + 1], fill="#8c6022")
    links = "Back   Journal   History   Skip   Auto   Save   Q.Save   Q.Load   Prefs"
    d.text((W // 2, H - bar // 2), links, font=F_QUICK, fill="#f3dfae", anchor="mm")
    return frame.convert("RGB")


def save_jpg(im, path, width=1280):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.resize((width, int(im.height * width / im.width)), Image.LANCZOS).save(path, quality=86, optimize=True)
    return path


def character_sheet(names, label_folders, path):
    """All styles side by side for one character, each style labeled above its figures."""
    groups = []
    for label, folder in label_folders:
        ims = [Image.open(os.path.join(HERE, "spr", f"{n}.png") if folder is None
                          else os.path.join(OPT, folder, f"{n}.png")).convert("RGBA") for n in names]
        ims = [i.resize((int(i.width * 760 / i.height), 760), Image.LANCZOS) for i in ims]
        groups.append((label, ims))
    gap = 60
    width = sum(sum(i.width for i in ims) for _, ims in groups) + gap * (len(groups) + 1)
    sheet = Image.new("RGB", (width, 860), (214, 206, 190))
    d = ImageDraw.Draw(sheet)
    x = gap
    for label, ims in groups:
        group_w = sum(i.width for i in ims)
        d.text((x + group_w // 2, 50), label, font=F_LABEL, fill="#2b1d12", anchor="mm")
        for i in ims:
            sheet.paste(i, (x, 95), i)
            x += i.width
        x += gap
        if x < width - gap:
            d.line([(x - gap // 2, 30), (x - gap // 2, 830)], fill=(170, 160, 140), width=3)
    return save_jpg(sheet, path, 2000)


def build_images():
    out = {}
    for scene in SCENES:
        for key, _, bg_folder in BG_STYLES:
            chars = None if key == "current" else "p-proportions"
            out[(scene[0], key)] = save_jpg(mockup(scene, bg_folder, chars),
                                            os.path.join(MOCK, f"{scene[0]}-{key}.jpg"))
    bunk = SCENES[1]
    for key, _, folder in CHAR_STYLES:
        out[("combo", key)] = save_jpg(mockup(bunk, "a-episode", folder), os.path.join(MOCK, f"combo-a-{key}.jpg"))
    labels = [(label, folder) for _, label, folder in CHAR_STYLES]
    out["stan"] = character_sheet(["stan_neutral", "stan_grin"], labels, os.path.join(MOCK, "characters-stan.jpg"))
    out["ford"] = character_sheet(["ford_neutral", "ford_finger"], labels, os.path.join(MOCK, "characters-ford.jpg"))
    return out


# ---------------------------------------------------------------------------- document

def heading(doc, text, level):
    h = doc.add_heading(text, level)
    for r in h.runs:
        r.font.color.rgb = RGBColor(0x6b, 0x1f, 0x1f)
    return h


def para(doc, text, bold_lead=None, italic=False, size=None):
    p = doc.add_paragraph()
    if bold_lead:
        p.add_run(bold_lead).bold = True
    r = p.add_run(text)
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    return p


def picture(doc, path, width, caption=None):
    doc.add_picture(path, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if caption:
        c = para(doc, caption, italic=True, size=9)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER


def grid(doc, cells, cols=2, width=4.55):
    """A borderless table of images, each with a bold caption above it."""
    table = doc.add_table(rows=(len(cells) + cols - 1) // cols, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (caption, path) in enumerate(cells):
        cell = table.cell(i // cols, i % cols)
        p = cell.paragraphs[0]
        p.add_run(caption).bold = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.add_paragraph().add_run().add_picture(path, width=Inches(width))
        cell.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def bullet(doc, text, lead=None):
    p = doc.add_paragraph(style="List Bullet")
    if lead:
        p.add_run(lead).bold = True
    p.add_run(text)


def build_doc(img):
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Inches(11), Inches(8.5)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(0.6))
    doc.styles["Normal"].font.name = "Georgia"
    doc.styles["Normal"].font.size = Pt(11)

    heading(doc, "Sea's Company: art style options", 0)
    para(doc, "Draft for review, 2026-10-28. None of these images are in the game or on the website yet.", italic=True)

    heading(doc, "How to use this document", 1)
    para(doc, "Choose one background style and one character style. They are independent: any background style "
              "works with any character style. Each option redraws the current art with the same composition, so "
              "the comparisons show style alone. Once you choose, all 19 backgrounds and 21 character images get "
              "redrawn in that style, and the game and website are rebuilt.")
    para(doc, "The scene pictures are mock-ups of the game screen. They use the game's real textbox, name tag, "
              "fonts, positions, link bar and speaker dimming, but they are assembled outside the game.")

    heading(doc, "Background styles", 2)
    bullet(doc, "the glossy, highly detailed painted look now in the game, with cinematic glow lighting. It is "
                "closer to a feature film or anime than to the show.", "Current: ")
    bullet(doc, "made to look like a frame from an episode. Soft gouache-style painting, simpler shapes, a calmer "
                "palette and even lighting. The closest match to the show.", "A. Episode frame: ")
    bullet(doc, "like the show's development paintings. Visible brushstrokes and paper grain, moodier color, warm "
                "light against cool shadows.", "B. Concept art: ")
    bullet(doc, "like the show's promotional posters. Crisp edges, flat shapes with hard-edged shading, bright "
                "saturated color.", "C. Promotional art: ")

    heading(doc, "Character styles", 2)
    bullet(doc, "the current sprites: the show's character designs with realistic body proportions, soft shading, "
                "chest hair and detailed jacket folds.", "1. Current: ")
    bullet(doc, "the same proportions as now, with flat colors, one hard shadow tone and fewer fold lines.",
           "2. Flat cel: ")
    bullet(doc, "redrawn with the show's proportions: bigger heads, rounder bodies, white eyes with dot pupils, flat "
                "color. The closest match to the show.", "3. Show proportions: ")
    para(doc, "Character styles were also tried with the concept-art and promotional prompts, but those came out "
              "almost identical to the flat cel style, so they are not shown separately. All scene mock-ups for "
              "options A, B and C use the show-proportions characters, shown at 88% of the current sprite height "
              "so their bigger heads don't crowd the frame. Sprite size is easy to adjust later.", italic=True, size=10)

    doc.add_page_break()
    heading(doc, "Characters", 1)
    para(doc, "Each picture shows one character in all three styles. Within each style, the left figure is the "
              "neutral pose and the right one is an expression, to show that the style holds across poses.")
    picture(doc, img["stan"], 9.6, "Stan in each character style.")
    picture(doc, img["ford"], 9.6, "Ford in each character style.")

    for scene in SCENES:
        doc.add_page_break()
        title = scene[0].replace("_", " ").title()
        heading(doc, f"Scene: {title}", 1)
        para(doc, scene[4], italic=True)
        grid(doc, [(label, img[(scene[0], key)]) for key, label, _ in BG_STYLES])

    doc.add_page_break()
    heading(doc, "Character styles in one scene", 1)
    para(doc, "The bunk scene with option A backgrounds and each character style, to compare characters against "
              "the same background.")
    grid(doc, [(label, img[("combo", key)]) for key, label, _ in CHAR_STYLES], cols=2)

    doc.add_page_break()
    heading(doc, "Known issues in these drafts", 1)
    bullet(doc, "Option B changed the time of day in two scenes: the midday raft became a sunset, and the "
                "afternoon dock became dusk. A final pass would hold the time of day.", "Lighting: ")
    bullet(doc, "Ford must have six fingers on each hand. In the drafts, his raised hand is hard to count. "
                "Final images would be checked one by one.", "Ford's hands: ")
    bullet(doc, "Ford's cleft chin is faint in the show-proportions drafts.", "Ford's chin: ")
    bullet(doc, "Only Stan and Ford were redrawn. The Patron and Lizard Head, and the remaining expressions, "
                "would be redrawn after you choose.", "Coverage: ")
    bullet(doc, "Image moderation blocked some attempts because the prompts name a Disney show. Retries worked, "
                "but a full set of 40 images will take some retries.", "Generation: ")

    heading(doc, "Your choice", 1)
    para(doc, "Mark one in each row, and add any notes.")
    table = doc.add_table(rows=3, cols=2)
    table.style = "Table Grid"
    rows = [("Background style", "☐ Current    ☐ A. Episode frame    ☐ B. Concept art    ☐ C. Promotional art"),
            ("Character style", "☐ 1. Current    ☐ 2. Flat cel    ☐ 3. Show proportions"),
            ("Notes", "\n\n")]
    for r, (k, v) in enumerate(rows):
        table.cell(r, 0).paragraphs[0].add_run(k).bold = True
        table.cell(r, 1).paragraphs[0].add_run(v)
        table.cell(r, 0).width = Inches(2)
        table.cell(r, 1).width = Inches(7.8)

    para(doc, "")
    para(doc, "The source images are in dev/style-options/, one folder per option, and the mock-ups are in "
              "dev/style-options/mockups/. dev/style_options.py generates the options and dev/style_review.py "
              "builds this document.", size=9)
    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build_doc(build_images()))
