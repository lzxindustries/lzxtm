"""
Generate Instagram/Facebook social media post images for the Chromagnon Production Plan blog post.
Uses the same visual style as the timeline graphic and docs site (dark bg, orange accent).
Composites existing Chromagnon images with branded typography.

Outputs:
  - chromagnon-social-instagram.png (1080x1080) — Instagram feed post
  - chromagnon-social-facebook.png  (1200x630)  — Facebook/Open Graph share
  - chromagnon-social-story.png     (1080x1920) — Instagram/Facebook story

Requires: matplotlib, Pillow
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog" / "2026-03-05-chromagnon-production-plan"
FONT_DIR = ROOT / "static" / "font"
LOGO_DIR = ROOT / "static" / "img"

# Source images
FRONT_PANEL = BLOG_DIR / "chromagnon-front-panel.png"
CORE_BOARD = BLOG_DIR / "chromagnon-revI-core-board.jpg"
ENCLOSURE = BLOG_DIR / "chromagnon-sheet-metal-enclosure.png"
TIMELINE = BLOG_DIR / "chromagnon-timeline-graphic.png"

# Fonts
FONT_DIN = str(FONT_DIR / "DIN1451-36breit.ttf")
FONT_RELIEF = str(FONT_DIR / "ReliefSingleLine-Regular.ttf")

# === Color scheme (matches docs site + timeline graphic) ===
BG_COLOR = (27, 27, 29)           # #1b1b1d
ACCENT = (214, 119, 10)           # #d6770a
ACCENT_LIGHT = (245, 152, 46)     # #f5982e
TEXT_WHITE = (227, 227, 227)      # #e3e3e3
TEXT_MUTED = (153, 153, 153)      # #999999
DARK_OVERLAY = (15, 15, 17)       # Slightly darker for overlays


def load_and_register_fonts():
    """Register custom fonts with matplotlib."""
    for font_path in [FONT_DIN, FONT_RELIEF]:
        if Path(font_path).exists():
            fm.fontManager.addfont(font_path)


def crop_center(img, target_w, target_h):
    """Crop image from center to target aspect ratio, then resize."""
    w, h = img.size
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Too wide — crop sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Too tall — crop top/bottom
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def darken_image(img, factor=0.35):
    """Darken an image for use as background."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def add_gradient_overlay(img, direction='bottom', intensity=0.85):
    """Add a gradient overlay fading to dark from the specified direction."""
    w, h = img.size
    gradient = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    for y in range(h):
        if direction == 'bottom':
            alpha = int(255 * intensity * (y / h) ** 1.5)
        elif direction == 'top':
            alpha = int(255 * intensity * ((h - y) / h) ** 1.5)
        else:
            alpha = int(255 * intensity * (y / h))
        draw.rectangle([(0, y), (w, y + 1)], fill=(BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], alpha))

    return Image.alpha_composite(img.convert('RGBA'), gradient)


def draw_accent_line(draw, x, y, width, thickness=4):
    """Draw a horizontal orange accent line."""
    draw.rectangle([(x, y), (x + width, y + thickness)], fill=ACCENT)


def draw_text_with_font(draw, position, text, font_path, size, color, anchor='la'):
    """Draw text using a PIL ImageFont (with fallback)."""
    from PIL import ImageFont
    try:
        font = ImageFont.truetype(font_path, size)
    except (OSError, IOError):
        font = ImageFont.load_default()
    draw.text(position, text, fill=color, font=font, anchor=anchor)
    return font


def get_text_bbox(draw, text, font_path, size):
    """Get text bounding box dimensions."""
    from PIL import ImageFont
    try:
        font = ImageFont.truetype(font_path, size)
    except (OSError, IOError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


# ============================================================================
# INSTAGRAM POST (1080x1080)
# ============================================================================
def generate_instagram_post():
    W, H = 1080, 1080
    canvas = Image.new('RGBA', (W, H), BG_COLOR + (255,))
    draw = ImageDraw.Draw(canvas)

    # -- Background: front panel image, darkened, with gradient --
    if FRONT_PANEL.exists():
        bg = Image.open(FRONT_PANEL).convert('RGB')
        bg = crop_center(bg, W, H)
        bg = darken_image(bg, factor=0.25)
        bg_rgba = bg.convert('RGBA')
        # Add strong bottom gradient for text readability
        bg_rgba = add_gradient_overlay(bg_rgba, 'bottom', intensity=0.95)
        canvas = Image.alpha_composite(canvas, bg_rgba)
        draw = ImageDraw.Draw(canvas)

    # -- Top accent bar --
    draw.rectangle([(0, 0), (W, 5)], fill=ACCENT)

    # -- LZX text mark (top left area) --
    draw_text_with_font(draw, (60, 40), "LZX", FONT_DIN, 28, ACCENT_LIGHT)

    # -- Date badge (top right) --
    draw_text_with_font(draw, (W - 60, 40), "MARCH 2026", FONT_DIN, 22, TEXT_MUTED, anchor='ra')

    # -- Main title block (lower portion) --
    title_y = 680

    # Accent line above title
    draw_accent_line(draw, 60, title_y, 120, thickness=4)

    # "CHROMAGNON" in large type
    draw_text_with_font(draw, (60, title_y + 20), "CHROMAGNON", FONT_DIN, 72, TEXT_WHITE)

    # Subtitle
    draw_text_with_font(draw, (60, title_y + 105), "THE PRODUCTION PLAN", FONT_DIN, 36, ACCENT_LIGHT)

    # Accent line below subtitle
    draw_accent_line(draw, 60, title_y + 160, 80, thickness=3)

    # Key details
    details = [
        "First unit ships August 2026",
        "FPGA-based DSP • Field-proven platform",
        "All pre-orders honored at original price",
    ]
    for i, detail in enumerate(details):
        draw_text_with_font(draw, (60, title_y + 185 + i * 36), detail,
                          FONT_DIN, 22, TEXT_MUTED if i > 0 else TEXT_WHITE)

    # -- Bottom accent bar --
    draw.rectangle([(0, H - 5), (W, H)], fill=ACCENT)

    # -- URL bottom right --
    draw_text_with_font(draw, (W - 60, H - 35), "docs.lzxindustries.net", FONT_DIN, 18, TEXT_MUTED, anchor='ra')

    # Save
    out = BLOG_DIR / "chromagnon-social-instagram.png"
    canvas.convert('RGB').save(out, dpi=(150, 150), quality=95)
    print(f"  Instagram post: {out} ({out.stat().st_size:,} bytes)")


# ============================================================================
# FACEBOOK / OPEN GRAPH (1200x630)
# ============================================================================
def generate_facebook_post():
    W, H = 1200, 630
    canvas = Image.new('RGBA', (W, H), BG_COLOR + (255,))
    draw = ImageDraw.Draw(canvas)

    # -- Right side: front panel image as background element --
    if FRONT_PANEL.exists():
        panel = Image.open(FRONT_PANEL).convert('RGBA')
        # Scale to fit right side
        panel_h = H
        panel_w = int(panel.width * (panel_h / panel.height))
        panel = panel.resize((panel_w, panel_h), Image.LANCZOS)
        # Darken
        panel_rgb = panel.convert('RGB')
        panel_rgb = darken_image(panel_rgb, factor=0.3)
        # Place on right side
        x_offset = W - panel_w + panel_w // 4
        canvas.paste(panel_rgb, (x_offset, 0))
        draw = ImageDraw.Draw(canvas)

        # Add left gradient to blend with text area
        gradient = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        grad_draw = ImageDraw.Draw(gradient)
        for x in range(W):
            if x < W * 0.5:
                alpha = int(255 * 0.95)
            elif x < W * 0.75:
                progress = (x - W * 0.5) / (W * 0.25)
                alpha = int(255 * (0.95 - 0.75 * progress))
            else:
                alpha = int(255 * 0.2)
            grad_draw.rectangle([(x, 0), (x + 1, H)], fill=(BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], alpha))
        canvas = Image.alpha_composite(canvas, gradient)
        draw = ImageDraw.Draw(canvas)

    # -- Top accent bar --
    draw.rectangle([(0, 0), (W, 4)], fill=ACCENT)

    # -- LZX brand --
    draw_text_with_font(draw, (50, 35), "LZX", FONT_DIN, 24, ACCENT_LIGHT)

    # -- Main content (left side) --
    content_y = 140

    # Accent line
    draw_accent_line(draw, 50, content_y, 100, thickness=4)

    # Title
    draw_text_with_font(draw, (50, content_y + 18), "CHROMAGNON", FONT_DIN, 64, TEXT_WHITE)
    draw_text_with_font(draw, (50, content_y + 92), "THE PRODUCTION PLAN", FONT_DIN, 30, ACCENT_LIGHT)

    # Accent line
    draw_accent_line(draw, 50, content_y + 140, 70, thickness=3)

    # Key points
    points = [
        "Ship Unit #1: August 2026",
        "FPGA-based DSP on field-proven platform",
        "All pre-orders honored at original price",
    ]
    for i, point in enumerate(points):
        bullet_color = ACCENT if i == 0 else TEXT_MUTED
        draw_text_with_font(draw, (50, content_y + 165 + i * 34), point,
                          FONT_DIN, 20, bullet_color if i == 0 else TEXT_MUTED)

    # -- Bottom accent bar --
    draw.rectangle([(0, H - 4), (W, H)], fill=ACCENT)

    # -- URL --
    draw_text_with_font(draw, (50, H - 35), "docs.lzxindustries.net", FONT_DIN, 16, TEXT_MUTED)

    # -- Date --
    draw_text_with_font(draw, (W - 50, H - 35), "MARCH 5, 2026", FONT_DIN, 16, TEXT_MUTED, anchor='ra')

    # Save
    out = BLOG_DIR / "chromagnon-social-facebook.png"
    canvas.convert('RGB').save(out, dpi=(150, 150), quality=95)
    print(f"  Facebook/OG:    {out} ({out.stat().st_size:,} bytes)")


# ============================================================================
# INSTAGRAM STORY (1080x1920)
# ============================================================================
def generate_instagram_story():
    W, H = 1080, 1920
    canvas = Image.new('RGBA', (W, H), BG_COLOR + (255,))
    draw = ImageDraw.Draw(canvas)

    # -- Top accent bar --
    draw.rectangle([(0, 0), (W, 5)], fill=ACCENT)

    # -- LZX brand top --
    draw_text_with_font(draw, (60, 50), "LZX", FONT_DIN, 32, ACCENT_LIGHT)
    draw_text_with_font(draw, (W - 60, 55), "MARCH 2026", FONT_DIN, 22, TEXT_MUTED, anchor='ra')

    # -- Front panel image (top section) --
    panel_y = 120
    if FRONT_PANEL.exists():
        panel = Image.open(FRONT_PANEL).convert('RGB')
        # Fit to width with some padding
        panel_w = W - 120
        panel_h = int(panel.height * (panel_w / panel.width))
        if panel_h > 550:
            panel_h = 550
            panel_w = int(panel.width * (panel_h / panel.height))
        panel = panel.resize((panel_w, panel_h), Image.LANCZOS)
        # Center horizontally
        px = (W - panel_w) // 2
        canvas.paste(panel, (px, panel_y))
        draw = ImageDraw.Draw(canvas)
        panel_bottom = panel_y + panel_h + 30
    else:
        panel_bottom = panel_y + 50

    # -- Title section --
    title_y = panel_bottom + 10
    draw_accent_line(draw, 60, title_y, 120, thickness=4)

    draw_text_with_font(draw, (60, title_y + 20), "CHROMAGNON", FONT_DIN, 64, TEXT_WHITE)
    draw_text_with_font(draw, (60, title_y + 95), "THE PRODUCTION PLAN", FONT_DIN, 32, ACCENT_LIGHT)

    draw_accent_line(draw, 60, title_y + 145, 80, thickness=3)

    # -- Key milestones as a vertical list --
    milestones_y = title_y + 180
    milestones = [
        ("MAR 12", "Videomancer Firmware Update", True),
        ("APR", "RevI Board Design Complete", False),
        ("MAY", "Prototype in Hand", False),
        ("JUN", "Production-Ready", False),
        ("AUG", "Ship Unit #1", False),
        ("SEP+", "Fulfillment at Scale", False),
    ]

    for i, (date, desc, done) in enumerate(milestones):
        y = milestones_y + i * 52
        # Date column
        date_color = ACCENT if not done else (58, 138, 58)  # green if done
        draw_text_with_font(draw, (60, y), date, FONT_DIN, 22, date_color)
        # Description
        desc_color = TEXT_WHITE if done or i <= 1 else TEXT_MUTED
        draw_text_with_font(draw, (260, y), desc, FONT_DIN, 22, desc_color)
        # Status dot
        dot_color = (58, 138, 58) if done else (ACCENT if i <= 1 else (85, 85, 85))
        dot_x, dot_y_center = 230, y + 12
        draw.ellipse([(dot_x - 6, dot_y_center - 6), (dot_x + 6, dot_y_center + 6)], fill=dot_color)

    # -- Timeline graphic (if exists) --
    timeline_y = milestones_y + len(milestones) * 52 + 40
    if TIMELINE.exists():
        tl = Image.open(TIMELINE).convert('RGB')
        tl_w = W - 80
        tl_h = int(tl.height * (tl_w / tl.width))
        tl = tl.resize((tl_w, tl_h), Image.LANCZOS)
        canvas.paste(tl, (40, timeline_y))
        draw = ImageDraw.Draw(canvas)

    # -- Bottom section --
    draw_text_with_font(draw, (60, H - 100), "All pre-orders honored at original price", FONT_DIN, 22, TEXT_WHITE)
    draw_text_with_font(draw, (60, H - 60), "docs.lzxindustries.net", FONT_DIN, 18, TEXT_MUTED)

    # -- Bottom accent bar --
    draw.rectangle([(0, H - 5), (W, H)], fill=ACCENT)

    # Save
    out = BLOG_DIR / "chromagnon-social-story.png"
    canvas.convert('RGB').save(out, dpi=(150, 150), quality=95)
    print(f"  Instagram story: {out} ({out.stat().st_size:,} bytes)")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == '__main__':
    load_and_register_fonts()
    print("Generating social media images...")
    print()
    generate_instagram_post()
    generate_facebook_post()
    generate_instagram_story()
    print()
    print("Done. All images saved to blog post folder.")
