"""
Stamp the watermark onto the Test Calls App screenshots.

Unlike the BBA Tool and Pricing Tool scripts, this one does not draw any
strikethrough redaction — Noah hand-redacted the proprietary fields
(scenario description, test caller, customer#, order#/PR#, rep name)
directly in assets/img/Test Calls App/ himself. This script only adds the
missing watermark on top of that already-redacted work, in place.

Run:
    py -3 build_testcalls_screenshots.py
"""
import os
from PIL import Image

from redact_helpers import stamp_watermark

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.normpath(os.path.join(BASE, "..", "img", "Test Calls App"))

FILES = [
    "1-TestCallDashboard.png",
    "2-CreateScenario.png",
    "3-ReviewWeeklyCalls.png",
    "4-ReviewPerCall.png",
]


def main():
    for name in FILES:
        path = os.path.join(IMG_DIR, name)
        im = Image.open(path).convert("RGB")
        stamp_watermark(im)
        im.save(path)
        print(f"Watermarked {name}")


if __name__ == "__main__":
    main()
