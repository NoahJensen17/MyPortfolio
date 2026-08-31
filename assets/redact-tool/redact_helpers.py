"""
Shared strikethrough-redaction helpers used by the per-project build scripts
(build_bba_screenshots.py, build_pricing_screenshots.py, ...).

Redaction approach: proprietary business data is struck through with a solid
black line drawn directly over the original pixels (data stays underneath
the line, nothing is repainted or fabricated). A small "Illustrative Data"
watermark is stamped in the bottom-right corner of every output image.

Never edit files under originals/ — build scripts only read them.
"""
from PIL import Image, ImageDraw, ImageFont

WATERMARK_TEXT = "Illustrative Data - Redacted for company data privacy"

FONT_REGULAR = "arial.ttf"


def load_font(size):
    try:
        return ImageFont.truetype(FONT_REGULAR, size)
    except OSError:
        return ImageFont.load_default()


def thin_strike(draw, y, x0, x1, weight=6):
    """Single strikethrough line through one line of label:value text."""
    draw.line((x0, y, x1, y), fill=(20, 20, 20), width=weight)


def row_bar(draw, y0, y1, x0, x1, weight=8):
    """Thick bar spanning a data row, centered in the row band."""
    mid = (y0 + y1) // 2
    draw.line((x0, mid, x1, mid), fill=(10, 10, 10), width=weight)


def col_bar(draw, x0, x1, y0, y1, weight=8):
    """Thick vertical bar spanning a stacked column of labels (e.g. an axis)."""
    mid = (x0 + x1) // 2
    draw.line((mid, y0, mid, y1), fill=(10, 10, 10), width=weight)


def stamp_watermark(img, text=WATERMARK_TEXT):
    width, height = img.size
    font_size = max(12, width // 80)
    font = load_font(font_size)

    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    padding = 8
    x = width - text_w - padding * 2
    y = height - text_h - padding * 2

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [x, y, width - padding // 2, height - padding // 2],
        fill=(0, 0, 0, 140),
    )
    composited = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.paste(composited)

    draw = ImageDraw.Draw(img)
    draw.text((x + padding, y + padding // 2), text, font=font, fill=(255, 255, 255))
