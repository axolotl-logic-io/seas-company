"""Convert generated art into Ren'Py game assets and draw the GUI pieces."""
import glob, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageEnhance

SRC = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(os.path.dirname(SRC), "game")
IMG = os.path.join(GAME, "images")
GUI = os.path.join(GAME, "gui")
FONTS = os.path.join(GAME, "fonts")
random.seed(7)

INK = (43, 29, 18, 255)
GOLD = (214, 160, 70, 255)
GOLD_DARK = (140, 96, 34, 255)
MAROON = (107, 31, 31, 255)

parch_src = Image.open(f"{SRC}/ui/parchment.png").convert("RGB")
leather_src = Image.open(f"{SRC}/ui/leather.png").convert("RGB")


def tex(src, w, h):
    """Tile/crop a texture to w x h."""
    out = Image.new("RGB", (w, h))
    sw, sh = src.size
    for y in range(0, h, sh):
        for x in range(0, w, sw):
            out.paste(src, (x, y))
    return out


def rough_mask(w, h, inset=8, amp=5, radius=14):
    """A rounded-rect mask with a slightly deckled (torn paper) edge."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([inset, inset, w - inset - 1, h - inset - 1], radius=radius, fill=255)
    # nibble edges
    for _ in range(int((w + h) * 1.2)):
        side = random.randint(0, 3)
        r = random.randint(1, amp)
        if side == 0:
            x, y = random.randint(0, w), inset + random.randint(-1, 2)
        elif side == 1:
            x, y = random.randint(0, w), h - inset - random.randint(-1, 2)
        elif side == 2:
            x, y = inset + random.randint(-1, 2), random.randint(0, h)
        else:
            x, y = w - inset - random.randint(-1, 2), random.randint(0, h)
        d.ellipse([x - r, y - r, x + r, y + r], fill=0 if random.random() < 0.6 else 255)
    return m.filter(ImageFilter.GaussianBlur(0.8))


def burn_edges(img, mask, strength=110, blur=18):
    """Darken the paper near its edges like old parchment."""
    edge = mask.filter(ImageFilter.GaussianBlur(blur))
    inv = ImageChops.invert(edge).point(lambda v: min(255, int(v * strength / 100)))
    dark = Image.new("RGB", img.size, (92, 58, 24))
    return Image.composite(dark, img, inv)


def panel(w, h, src=None, border=INK, border_w=3, inset=10, shadow=True, amp=4, radius=14, burn=True, inner_line=True):
    src = src or parch_src
    base = tex(src, w, h)
    mask = rough_mask(w, h, inset=inset, amp=amp, radius=radius)
    if burn:
        base = burn_edges(base, mask)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sm = mask.filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * 0.55)
        sh.putalpha(sm)
        out = Image.alpha_composite(out, ImageChops.offset(sh, 3, 5))
    p = base.convert("RGBA")
    p.putalpha(mask)
    out = Image.alpha_composite(out, p)
    if inner_line and border:
        d = ImageDraw.Draw(out)
        o = inset + 9
        d.rounded_rectangle([o, o, w - o - 1, h - o - 1], radius=max(2, radius - 6), outline=border, width=border_w)
        o2 = o + 6
        d.rounded_rectangle([o2, o2, w - o2 - 1, h - o2 - 1], radius=max(2, radius - 10),
                            outline=border[:3] + (90,), width=1)
    return out


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)


def bg_assets():
    os.makedirs(IMG + "/bg", exist_ok=True)
    for f in glob.glob(f"{SRC}/bg/*.png"):
        n = os.path.splitext(os.path.basename(f))[0]
        im = Image.open(f).convert("RGB")
        # cover-crop to 16:9 then scale to 1920x1080
        w, h = im.size
        tw = h * 16 / 9
        if tw <= w:
            l = (w - tw) / 2
            im = im.crop((int(l), 0, int(l + tw), h))
        else:
            th = w * 9 / 16
            t = (h - th) / 2
            im = im.crop((0, int(t), w, int(t + th)))
        im = im.resize((1920, 1080), Image.LANCZOS)
        prefix = "cg" if n == "dinner" else "bg"
        im.save(f"{IMG}/bg/{prefix} {n.replace('_', ' ')}.jpg", quality=90)


def sprite_assets(names=None):
    os.makedirs(IMG + "/sprites", exist_ok=True)
    for f in glob.glob(f"{SRC}/spr/*.png"):
        n = os.path.splitext(os.path.basename(f))[0]
        if names is not None and n not in names:
            continue
        im = Image.open(f).convert("RGBA")
        # Match the evening and swim outfits, leaving headroom for the dance.
        fit_height = (n in ("stan_suit", "patron_speedo")
                      or n.startswith(("stan_swim_", "stan_evening_")))
        scale = 1020 / im.height if fit_height else 0.7
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        im.save(f"{IMG}/sprites/{n}.png", optimize=True)


def gui_assets():
    # Text box: a parchment banner across the bottom.
    tb = Image.new("RGBA", (1920, 300), (0, 0, 0, 0))
    p = panel(1720, 280, inset=12, amp=5, radius=18)
    hand = Image.open(f"{SRC}/ui/hand6.png").convert("RGBA").resize((150, 140), Image.LANCZOS)
    hand.putalpha(hand.getchannel("A").point(lambda v: int(v * 0.13)))
    p.alpha_composite(hand, (1720 - 200, 280 - 175))
    tb.alpha_composite(p, (100, 14))
    save(tb, f"{GUI}/textbox.png")

    # Name box: maroon leather tag with gold stitching.
    nb = panel(420, 78, src=leather_src, border=GOLD, border_w=2, inset=4, amp=2, radius=10, burn=False)
    d = ImageDraw.Draw(nb)
    for x in range(22, 400, 14):
        d.line([x, 13, x + 7, 13], fill=GOLD, width=2)
        d.line([x, 64, x + 7, 64], fill=GOLD, width=2)
    save(nb, f"{GUI}/namebox.png")

    # Action bubble: small parchment tag.
    ab = panel(360, 56, inset=3, amp=1, radius=26, burn=False, inner_line=False)
    d = ImageDraw.Draw(ab)
    d.rounded_rectangle([3, 3, 356, 52], radius=24, outline=INK, width=2)
    save(ab, f"{GUI}/act_bubble.png")

    # Choice buttons.
    ci = panel(1200, 88, inset=6, amp=2, radius=12)
    save(ci, f"{GUI}/button/choice_idle_background.png")
    ch = panel(1200, 88, src=leather_src, border=GOLD, inset=6, amp=2, radius=12, burn=False)
    save(ch, f"{GUI}/button/choice_hover_background.png")
    ci2 = ci.copy()
    ci2.putalpha(ci2.getchannel("A").point(lambda v: int(v * 0.45)))
    save(ci2, f"{GUI}/button/choice_insensitive_background.png")

    # Generic frame (confirm, notify, input).
    save(panel(600, 300, inset=8, amp=3, radius=16), f"{GUI}/frame.png")
    save(panel(600, 300, inset=8, amp=3, radius=16), f"{GUI}/notify.png")

    # Game menu background: leather cover with a parchment page.
    gm = tex(leather_src, 1920, 1080).convert("RGBA")
    gm = ImageEnhance.Brightness(gm).enhance(0.75)
    page = panel(1440, 1020, inset=10, amp=4, radius=10)
    gm.alpha_composite(page, (450, 30))
    # gold hand on the cover, top-left
    hand2 = Image.open(f"{SRC}/ui/hand6.png").convert("RGBA").resize((200, 188), Image.LANCZOS)
    gm.alpha_composite(hand2, (125, 60))
    d = ImageDraw.Draw(gm)
    d.rectangle([30, 30, 430, 1050], outline=GOLD_DARK, width=3)
    d.rectangle([40, 40, 420, 1040], outline=GOLD_DARK[:3] + (120,), width=1)
    save(gm, f"{GUI}/game_menu.png")
    # Overlays are baked into game_menu.png; keep them transparent.
    clear = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    save(clear, f"{GUI}/overlay/game_menu.png")
    save(Image.new("RGBA", (1920, 1080), (10, 6, 4, 150)), f"{GUI}/overlay/confirm.png")

    # Main menu: sunset boat with a dark gradient for the title + menu on the left.
    mm = Image.open(f"{IMG}/bg/bg menu.jpg").convert("RGBA")
    grad = Image.new("L", (1920, 1080))
    gd = ImageDraw.Draw(grad)
    for x in range(1920):
        a = 210 if x < 380 else max(0, int(210 - (x - 380) * 0.33))
        gd.line([x, 0, x, 1080], fill=a)
    shade = Image.new("RGBA", (1920, 1080), (14, 10, 22, 255))
    shade.putalpha(grad)
    mm.alpha_composite(shade)
    save(mm.convert("RGB"), f"{GUI}/main_menu.png")
    save(clear, f"{GUI}/overlay/main_menu.png")

    # Chapter card / journal page background.
    save(panel(1200, 560, inset=10, amp=4, radius=10), f"{GUI}/chapter_card.png")

    # Bars and sliders.
    def bar(w, h, color, src=None):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        if src is not None:
            t = tex(src, w, h).convert("RGBA")
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=255)
            t.putalpha(m)
            im = t
        else:
            ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=color)
        ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, outline=INK, width=2)
        return im

    save(bar(600, 30, GOLD), f"{GUI}/slider/horizontal_idle_bar.png")
    save(bar(600, 30, (236, 186, 96, 255)), f"{GUI}/slider/horizontal_hover_bar.png")
    thumb = Image.new("RGBA", (34, 44), (0, 0, 0, 0))
    ImageDraw.Draw(thumb).rounded_rectangle([2, 2, 31, 41], radius=8, fill=MAROON, outline=GOLD, width=3)
    save(thumb, f"{GUI}/slider/horizontal_idle_thumb.png")
    thumb_h = Image.new("RGBA", (34, 44), (0, 0, 0, 0))
    ImageDraw.Draw(thumb_h).rounded_rectangle([2, 2, 31, 41], radius=8, fill=(150, 45, 45, 255), outline=(250, 210, 120, 255), width=3)
    save(thumb_h, f"{GUI}/slider/horizontal_hover_thumb.png")
    save(bar(30, 600, (120, 90, 60, 160)), f"{GUI}/scrollbar/vertical_idle_bar.png")
    save(bar(30, 600, (120, 90, 60, 200)), f"{GUI}/scrollbar/vertical_hover_bar.png")
    th = Image.new("RGBA", (30, 120), (0, 0, 0, 0))
    ImageDraw.Draw(th).rounded_rectangle([2, 2, 27, 117], radius=12, fill=MAROON, outline=GOLD, width=2)
    save(th, f"{GUI}/scrollbar/vertical_idle_thumb.png")
    save(th, f"{GUI}/scrollbar/vertical_hover_thumb.png")
    for n in ("bar/left", "bar/right"):
        save(bar(600, 30, GOLD if n.endswith("left") else (90, 60, 40, 220)), f"{GUI}/{n}.png")

    # Approval meter pieces.
    save(bar(400, 26, GOLD), f"{GUI}/meter_full.png")
    save(bar(400, 26, (90, 60, 40, 200)), f"{GUI}/meter_empty.png")

    # Window icon.
    ic = Image.open(f"{SRC}/ui/icon.png").convert("RGBA").resize((256, 256), Image.LANCZOS)
    save(ic, f"{GUI}/window_icon.png")
    app_icon = Image.open(f"{SRC}/ui/icon.png").convert("RGBA")
    app_icon.save(os.path.join(os.path.dirname(GAME), "icon.icns"))
    app_icon.save(os.path.join(os.path.dirname(GAME), "icon.ico"),
                  sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    save(Image.open(f"{SRC}/ui/hand6.png").convert("RGBA").resize((220, 206), Image.LANCZOS), f"{GUI}/hand.png")

    # Generic buttons: transparent when idle, a faint ink wash on hover.
    save(Image.new("RGBA", (450, 49), (0, 0, 0, 0)), f"{GUI}/button/idle_background.png")
    hb = Image.new("RGBA", (450, 49), (0, 0, 0, 0))
    ImageDraw.Draw(hb).rounded_rectangle([0, 4, 449, 44], radius=10, fill=(107, 31, 31, 38))
    save(hb, f"{GUI}/button/hover_background.png")

    # Check and radio markers: a small ink box, filled maroon when selected.
    for kind in ("check", "radio"):
        empty = Image.new("RGBA", (27, 49), (0, 0, 0, 0))
        d = ImageDraw.Draw(empty)
        if kind == "check":
            d.rectangle([3, 16, 19, 32], outline=(122, 102, 80, 255), width=2)
        else:
            d.ellipse([3, 16, 19, 32], outline=(122, 102, 80, 255), width=2)
        save(empty, f"{GUI}/button/{kind}_foreground.png")
        full = empty.copy()
        d = ImageDraw.Draw(full)
        if kind == "check":
            d.rectangle([3, 16, 19, 32], fill=MAROON, outline=INK, width=2)
        else:
            d.ellipse([3, 16, 19, 32], fill=MAROON, outline=INK, width=2)
        save(full, f"{GUI}/button/{kind}_selected_foreground.png")

    # Save slots: a parchment card with an inked frame around the thumbnail.
    for state, src, border in (("idle", parch_src, INK), ("hover", leather_src, GOLD)):
        card = panel(414, 309, src=src, border=None, inset=4, amp=2, radius=10, burn=(state == "idle"), inner_line=False)
        d = ImageDraw.Draw(card)
        d.rectangle([13, 13, 15 + 384 + 1, 15 + 216 + 1], outline=border, width=3)
        save(card, f"{GUI}/button/slot_{state}_background.png")

    # Remaining bar and slider orientations.
    save(bar(30, 600, GOLD), f"{GUI}/bar/bottom.png")
    save(bar(30, 600, (90, 60, 40, 220)), f"{GUI}/bar/top.png")
    save(bar(30, 600, GOLD), f"{GUI}/slider/vertical_idle_bar.png")
    save(bar(30, 600, (236, 186, 96, 255)), f"{GUI}/slider/vertical_hover_bar.png")
    save(thumb.rotate(90, expand=True), f"{GUI}/slider/vertical_idle_thumb.png")
    save(thumb_h.rotate(90, expand=True), f"{GUI}/slider/vertical_hover_thumb.png")
    save(bar(600, 22, (120, 90, 60, 160)), f"{GUI}/scrollbar/horizontal_idle_bar.png")
    save(bar(600, 22, (120, 90, 60, 200)), f"{GUI}/scrollbar/horizontal_hover_bar.png")
    hth = Image.new("RGBA", (120, 22), (0, 0, 0, 0))
    ImageDraw.Draw(hth).rounded_rectangle([1, 1, 118, 20], radius=10, fill=MAROON, outline=GOLD, width=2)
    save(hth, f"{GUI}/scrollbar/horizontal_idle_thumb.png")
    save(hth, f"{GUI}/scrollbar/horizontal_hover_thumb.png")


def web_assets():
    """Write the icon and loading image that the Ren'Py web build reads from the project root."""
    root = os.path.dirname(GAME)
    Image.open(f"{SRC}/ui/icon.png").convert("RGBA").resize((512, 512), Image.LANCZOS).save(
        os.path.join(root, "web-icon.png"), optimize=True)
    Image.open(f"{IMG}/bg/bg menu.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS).save(
        os.path.join(root, "web-presplash.jpg"), quality=85, optimize=True)


if __name__ == "__main__":
    bg_assets()
    sprite_assets()
    gui_assets()
    web_assets()
    print("done")
