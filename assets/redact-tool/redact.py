"""
Redaction tool for portfolio screenshots.

Usage:
    python redact.py input.png output.png --box 100,200,400,260 --box 50,50,300,90

Each --box is a pixel rectangle "left,top,right,bottom" (measured from the
top-left corner of the image, e.g. via Paint's cursor position readout or
Snip & Sketch). The tool paints solid black rectangles over each region,
flattens the result to a new PNG (original file is never modified), and
stamps a small watermark in the bottom-right corner.

Run with --help for all options.
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

WATERMARK_TEXT = "Data redacted — for portfolio illustration only"


def parse_box(value):
    parts = [int(p.strip()) for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            f"Box '{value}' must be 'left,top,right,bottom'"
        )
    return tuple(parts)


def redact(input_path, output_path, boxes, watermark_text=WATERMARK_TEXT):
    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for box in boxes:
        draw.rectangle(box, fill=(0, 0, 0))

    if watermark_text:
        _stamp_watermark(img, draw, watermark_text)

    img.save(output_path, "PNG")
    print(f"Saved redacted image to {output_path}")


def _stamp_watermark(img, draw, text):
    width, height = img.size
    font_size = max(12, width // 80)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    padding = 8
    x = width - text_w - padding * 2
    y = height - text_h - padding * 2

    # semi-transparent backing plate so the watermark stays legible on any background
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [x, y, width - padding // 2, height - padding // 2],
        fill=(0, 0, 0, 140),
    )
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))

    draw = ImageDraw.Draw(img)
    draw.text((x + padding, y + padding // 2), text, font=font, fill=(255, 255, 255))


def main():
    parser = argparse.ArgumentParser(description="Redact and watermark a screenshot.")
    parser.add_argument("input", help="Path to the original screenshot")
    parser.add_argument("output", help="Path to write the redacted PNG")
    parser.add_argument(
        "--box",
        action="append",
        type=parse_box,
        default=[],
        dest="boxes",
        help="Region to black out, as left,top,right,bottom (repeatable)",
    )
    parser.add_argument(
        "--watermark",
        default=WATERMARK_TEXT,
        help="Watermark text (default: standard redaction notice)",
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="Skip stamping a watermark",
    )
    args = parser.parse_args()

    redact(
        args.input,
        args.output,
        args.boxes,
        watermark_text=None if args.no_watermark else args.watermark,
    )


if __name__ == "__main__":
    main()
