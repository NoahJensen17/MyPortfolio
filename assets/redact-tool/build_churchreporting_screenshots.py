"""
Stamp the watermark onto the Church Reporting Tool screenshots.

Like the Test Calls App script, this one does not draw any strikethrough
redaction — Noah hand-redacted the proprietary fields (member/servant names,
attendance counts, and other identifying data) directly in
assets/redact-tool/originals/Church Reporting Tool/ himself. This script
reads those hand-redacted originals and writes the watermarked output to
assets/img/Church Reporting Tool/. Uses "church" instead of "company" in the
watermark text since this project isn't a Uline business tool.

Run:
    py -3 build_churchreporting_screenshots.py
"""
import os
from PIL import Image

from redact_helpers import stamp_watermark

BASE = os.path.dirname(os.path.abspath(__file__))
ORIGINALS_DIR = os.path.normpath(os.path.join(BASE, "originals", "Church Reporting Tool"))
IMG_DIR = os.path.normpath(os.path.join(BASE, "..", "img", "Church Reporting Tool"))

WATERMARK_TEXT = "Illustrative Data - Redacted for church data privacy"

# Maps each hand-redacted original (unnumbered) to its numbered output
# filename, matching the gallery order set on the project-4 page.
FILES = {
    "MainDashboard.png": "1-MainDashboard.png",
    "VolunteerData.png": "2-VolunteerData.png",
    "MembershipProgress.png": "3-MembershipProgress.png",
    "ProgressData.png": "4-ProgressData.png",
}


def main():
    for src_name, dst_name in FILES.items():
        src = os.path.join(ORIGINALS_DIR, src_name)
        dst = os.path.join(IMG_DIR, dst_name)
        im = Image.open(src).convert("RGB")
        stamp_watermark(im, text=WATERMARK_TEXT)
        im.save(dst)
        print(f"Watermarked {dst_name}")


if __name__ == "__main__":
    main()
