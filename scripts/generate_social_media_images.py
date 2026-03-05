"""
Generate social media images for the Chromagnon Production Plan blog post.
Visual style: dark, cinematic, minimal text. Let the product images speak.
Matches docs.lzxindustries.net dark theme with orange accent.

Outputs:
  - chromagnon-social-instagram.png (1080x1080) — Instagram feed
  - chromagnon-social-facebook.png  (1200x630)  — Facebook / Open Graph
  - chromagnon-social-story.png     (1080x1920) — Instagram / Facebook story

Requires: Pillow
"""

import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog" / "2026-03-05-chromagnon-building-it-right"
FONT_DIR = ROOT / "static" / "font"

# Source images
FRONT_PANEL = BLOG_DIR / "chromagnon-front-panel.png"
CORE_BOARD = BLOG_DIR / "chromagnon-revI-core-board.jpg"
ENCLOSURE = BLOG_DIR / "chromagnon-sheet-metal-enclosure.png"
WORKBENCH = BLOG_DIR / "chromagnon-workbench.jpg"
LOGO_PNG = ROOT / "static" / "img" / "logo-dark-512.png"

# Fonts
FONT_DIN = str(FONT_DIR / "DIN1451-36breit.ttf")

# === Colors ===
BG = (27, 27, 29)
ACCENT = (214, 119, 10)
ACCENT_LIGHT = (245, 152, 46)
WHITE = (227, 227, 227)
MUTED = (100, 100, 100)
BODY_TEXT = (155, 155, 155)


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def place_logo(canvas, x, y, height):
    """Place the LZX logo at (x, y) with given height in pixels."""
    if not LOGO_PNG.exists():
        draw = ImageDraw.Draw(canvas)
        draw.text((x, y), "LZX", fill=ACCENT_LIGHT, font=_font(FONT_DIN, height))
        return canvas
    logo = Image.open(LOGO_PNG).convert('RGBA')
    lw, lh = logo.size
    target_h = height
    target_w = int(lw * (target_h / lh))
    logo = logo.resize((target_w, target_h), Image.LANCZOS)
    # Tint the logo to ACCENT_LIGHT color
    r, g, b = ACCENT_LIGHT
    pixels = logo.load()
    for py in range(target_h):
        for px in range(target_w):
            _, _, _, a = pixels[px, py]
            pixels[px, py] = (r, g, b, a)
    canvas.paste(logo, (x, y), logo)
    return canvas


def add_film_grain(img, intensity=0.03, seed=42):
    """Add subtle monochromatic film grain for depth on flat backgrounds."""
    w, h = img.size
    rng = random.Random(seed)
    grain = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pixels = grain.load()
    for y in range(h):
        for x in range(w):
            v = rng.randint(0, 255)
            a = int(255 * intensity)
            pixels[x, y] = (v, v, v, a)
    return Image.alpha_composite(img.convert('RGBA'), grain)


def place_front_panel(canvas, panel_img, y_center, scale=0.9, glow=True):
    """Place the front panel image (with transparency) centered on the canvas."""
    cw, ch = canvas.size
    bbox = panel_img.getbbox()
    panel_content = panel_img.crop(bbox) if bbox else panel_img

    pw, ph = panel_content.size
    target_w = int(cw * scale)
    target_h = int(ph * (target_w / pw))
    panel_content = panel_content.resize((target_w, target_h), Image.LANCZOS)

    px = (cw - target_w) // 2
    py = y_center - target_h // 2

    if glow:
        glow_layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        pad = 30
        glow_draw.ellipse(
            [(px - pad, py - pad), (px + target_w + pad, py + target_h + pad)],
            fill=(ACCENT[0], ACCENT[1], ACCENT[2], 25)
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=35))
        canvas = Image.alpha_composite(canvas, glow_layer)

    canvas.paste(panel_content, (px, py), panel_content)
    return canvas


# ============================================================================
# INSTAGRAM POST (1080x1080)
# Front panel floating on dark textured background, minimal text below.
# ============================================================================
def generate_instagram_post():
    M = 50  # consistent margin
    W, H = 1080, 1080
    canvas = Image.new('RGBA', (W, H), BG + (255,))

    # Front panel hero — upper area with clearance for text below
    if FRONT_PANEL.exists():
        panel = Image.open(FRONT_PANEL)
        canvas = place_front_panel(canvas, panel, y_center=290, scale=0.88, glow=True)

    # Subtle grain
    canvas = add_film_grain(canvas, intensity=0.03)
    draw = ImageDraw.Draw(canvas)

    # Thin accent lines top and bottom
    draw.rectangle([(0, 0), (W, 3)], fill=ACCENT)
    draw.rectangle([(0, H - 3), (W, H)], fill=ACCENT)

    # LZX logo — top left
    canvas = place_logo(canvas, M, 20, 44)
    draw = ImageDraw.Draw(canvas)
    # Date — top right
    draw.text((W - M, 36), "MARCH 5, 2026", fill=MUTED, font=_font(FONT_DIN, 26), anchor='ra')

    # Product name + tagline
    name_y = 570
    draw.rectangle([(M, name_y), (M + 160, name_y + 4)], fill=ACCENT)
    draw.text((M, name_y + 16), "CHROMAGNON", fill=WHITE, font=_font(FONT_DIN, 96))
    draw.text((M, name_y + 128), "Building it right.",
              fill=ACCENT_LIGHT, font=_font(FONT_DIN, 46))

    # Body text
    body_lines = ["Production update with the full schedule,",
                  "upcoming milestones, and planned monthly",
                  "progress reports through fulfillment."]
    for i, ln in enumerate(body_lines):
        draw.text((M, name_y + 194 + i * 32), ln,
                  fill=BODY_TEXT, font=_font(FONT_DIN, 26))

    # Divider
    draw.line([(M, H - 110), (M + 200, H - 110)], fill=(50, 50, 52), width=1)

    # CTA
    draw.text((M, H - 90), "New post on the LZX development blog",
              fill=ACCENT_LIGHT, font=_font(FONT_DIN, 34))
    draw.text((M, H - 44), "docs.lzxindustries.net/blog",
              fill=MUTED, font=_font(FONT_DIN, 28))

    out = BLOG_DIR / "chromagnon-social-instagram.png"
    canvas.convert('RGB').save(out, quality=95)
    print(f"  Instagram:  {out.name} ({out.stat().st_size:,} bytes)")


# ============================================================================
# FACEBOOK / OPEN GRAPH (1200x630)
# Front panel on right, text on left, workbench texture behind.
# ============================================================================
def generate_facebook_post():
    W, H = 1200, 630
    canvas = Image.new('RGBA', (W, H), BG + (255,))

    # Faint workbench texture
    if WORKBENCH.exists():
        tex = Image.open(WORKBENCH).convert('RGB')
        tw, th = tex.size
        ratio = W / H
        cur = tw / th
        if cur > ratio:
            nw = int(th * ratio)
            tex = tex.crop(((tw - nw) // 2, 0, (tw + nw) // 2, th))
        tex = tex.resize((W, H), Image.LANCZOS)
        tex = ImageEnhance.Brightness(tex).enhance(0.06)
        canvas.paste(tex, (0, 0))
        canvas = canvas.convert('RGBA')

    # Front panel on right side
    if FRONT_PANEL.exists():
        panel = Image.open(FRONT_PANEL)
        bbox = panel.getbbox()
        pc = panel.crop(bbox) if bbox else panel
        pw, ph = pc.size
        target_h = int(H * 0.55)
        target_w = int(pw * (target_h / ph))
        pc = pc.resize((target_w, target_h), Image.LANCZOS)

        px = W - target_w - 40
        py = (H - target_h) // 2

        # Glow — elliptical for softer look
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse(
            [(px - 20, py - 20), (px + target_w + 20, py + target_h + 20)],
            fill=(ACCENT[0], ACCENT[1], ACCENT[2], 20))
        canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(25)))
        canvas.paste(pc, (px, py), pc)

        # Left fade for text readability
        fade = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for x in range(W):
            if x < W * 0.42:
                a = int(255 * 0.85)
            elif x < W * 0.58:
                a = int(255 * 0.85 * (1 - (x - W * 0.42) / (W * 0.16)))
            else:
                a = 0
            fd.rectangle([(x, 0), (x + 1, H)], fill=(BG[0], BG[1], BG[2], a))
        canvas = Image.alpha_composite(canvas, fade)

    draw = ImageDraw.Draw(canvas)

    # Top/bottom accent
    M = 50  # consistent margin
    draw.rectangle([(0, 0), (W, 3)], fill=ACCENT)
    draw.rectangle([(0, H - 3), (W, H)], fill=ACCENT)

    # LZX logo
    canvas = place_logo(canvas, M, 16, 36)
    draw = ImageDraw.Draw(canvas)
    # Date
    draw.text((W - M, 28), "MARCH 5, 2026", fill=MUTED, font=_font(FONT_DIN, 20), anchor='ra')

    # Text — left, vertically centered
    ty = 110
    draw.rectangle([(M, ty), (M + 160, ty + 4)], fill=ACCENT)
    draw.text((M, ty + 16), "CHROMAGNON", fill=WHITE, font=_font(FONT_DIN, 72))
    draw.text((M, ty + 100), "Building it right.", fill=ACCENT_LIGHT, font=_font(FONT_DIN, 36))

    # Body text
    body_lines = ["Production update with the full schedule,",
                  "upcoming milestones, and planned monthly",
                  "progress reports through fulfillment."]
    for i, ln in enumerate(body_lines):
        draw.text((M, ty + 154 + i * 28), ln,
                  fill=BODY_TEXT, font=_font(FONT_DIN, 20))

    # Divider
    draw.line([(M, H - 96), (M + 140, H - 96)], fill=(50, 50, 52), width=1)

    # CTA
    draw.text((M, H - 76), "New post on the LZX development blog",
              fill=ACCENT_LIGHT, font=_font(FONT_DIN, 26))
    draw.text((M, H - 38), "docs.lzxindustries.net/blog",
              fill=MUTED, font=_font(FONT_DIN, 22))

    out = BLOG_DIR / "chromagnon-social-facebook.png"
    canvas.convert('RGB').save(out, quality=95)
    print(f"  Facebook:   {out.name} ({out.stat().st_size:,} bytes)")


# ============================================================================
# INSTAGRAM STORY (1080x1920)
# Front panel hero, title, tagline, CTA. Clean and simple.
# ============================================================================
def generate_instagram_story():
    M = 50  # consistent margin
    W, H = 1080, 1920
    canvas = Image.new('RGBA', (W, H), BG + (255,))

    # Top accent
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, 0), (W, 4)], fill=ACCENT)
    canvas = place_logo(canvas, M, 40, 50)
    draw = ImageDraw.Draw(canvas)
    draw.text((W - M, 54), "MARCH 5, 2026", fill=MUTED, font=_font(FONT_DIN, 26), anchor='ra')

    # Front panel hero — vertically centered in upper portion
    if FRONT_PANEL.exists():
        panel = Image.open(FRONT_PANEL)
        canvas = place_front_panel(canvas, panel, y_center=500, scale=0.92, glow=True)
        draw = ImageDraw.Draw(canvas)

    # Subtle grain
    canvas = add_film_grain(canvas, intensity=0.03)
    draw = ImageDraw.Draw(canvas)

    # Title + tagline — positioned with even breathing room
    title_y = 880
    draw.rectangle([(M, title_y), (M + 180, title_y + 4)], fill=ACCENT)
    draw.text((M, title_y + 20), "CHROMAGNON", fill=WHITE, font=_font(FONT_DIN, 110))
    draw.text((M, title_y + 152), "Building it right.",
              fill=ACCENT_LIGHT, font=_font(FONT_DIN, 54))

    # Body text
    body_lines = ["Production update with the full schedule,",
                  "upcoming milestones, and planned monthly",
                  "progress reports through fulfillment."]
    for i, ln in enumerate(body_lines):
        draw.text((M, title_y + 228 + i * 44), ln,
                  fill=BODY_TEXT, font=_font(FONT_DIN, 32))

    # Divider
    draw.line([(M, H - 180), (M + 220, H - 180)], fill=(50, 50, 52), width=1)

    # CTA — bottom
    draw.text((M, H - 155), "New post on the LZX development blog",
              fill=ACCENT_LIGHT, font=_font(FONT_DIN, 38))
    draw.text((M, H - 95), "docs.lzxindustries.net/blog",
              fill=MUTED, font=_font(FONT_DIN, 32))

    # Bottom accent
    draw.rectangle([(0, H - 4), (W, H)], fill=ACCENT)

    out = BLOG_DIR / "chromagnon-social-story.png"
    canvas.convert('RGB').save(out, quality=95)
    print(f"  Story:      {out.name} ({out.stat().st_size:,} bytes)")


# ============================================================================
if __name__ == '__main__':
    print("Generating social media images...")
    generate_instagram_post()
    generate_facebook_post()
    generate_instagram_story()
    print("Done.")
