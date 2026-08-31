"""
Build strikethrough-redacted portfolio screenshots from the real Pricing
Tool originals.

Reads originals/Pricing Tool/*.png and writes sanitized copies to
../img/Pricing Tool/*.png. See redact_helpers.py for the shared strike/
watermark approach.

Only proprietary/identifying data is struck (competitor names, item
numbers, descriptions, vendor names, costs, prices, GP%). Structural/
navigational data (catalog codes, subgroup numbers, marketing class codes,
dates, single-letter flags) is left visible, consistent with the BBA Tool
screenshots.

Row/column pixel coordinates below were measured directly against the
original screenshots.

Run:
    py -3 build_pricing_screenshots.py

Never edit files in originals/ — this script only reads them.
"""
import os
from PIL import Image, ImageDraw

from redact_helpers import row_bar, stamp_watermark

BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE, "originals", "Pricing Tool")
OUT_DIR = os.path.normpath(os.path.join(BASE, "..", "img", "Pricing Tool"))


# --------------------------------------------------------------------------
# MainMenuButtons.png -> pricing-1-main-menu.png
# Pure navigation menu (report category tiles, no business data) - passes
# through unmodified except for the watermark.
# --------------------------------------------------------------------------

def build_main_menu():
    src = os.path.join(SRC_DIR, "MainMenuButtons.png")
    im = Image.open(src).convert("RGB")
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "pricing-1-main-menu.png"))
    print("Saved pricing-1-main-menu.png (pass-through, no data redaction needed)")


# --------------------------------------------------------------------------
# CompetitorInfoEntry.png -> pricing-2-competitor-entry.png
# Single competitor/item record with real pricing data throughout both
# panels. Category/classification fields (Mktg. Class, Prod. Group,
# Subgroup, Does Not Match?, Drop Ship?, DrpShp/DelFlag flags) are left
# visible as structural metadata, matching the BBA Tool precedent.
# --------------------------------------------------------------------------

def build_competitor_entry():
    src = os.path.join(SRC_DIR, "CompetitorInfoEntry.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # left "Core Information" panel value boxes (weight = measured text
    # height + generous padding so the bar fully covers the glyphs; row_bar
    # draws one line centered in (y0,y1), so an undersized weight leaves the
    # top or bottom of the text peeking out).
    row_bar(draw, 254, 268, 305, 716, weight=22)   # Competitor Name
    row_bar(draw, 287, 298, 305, 466, weight=18)   # Uline Item#
    row_bar(draw, 322, 333, 305, 516, weight=18)   # Competitor Item#
    row_bar(draw, 394, 405, 250, 716, weight=18)   # Note (first line)
    row_bar(draw, 492, 503, 300, 716, weight=18)   # Uline Description
    row_bar(draw, 632, 643, 300, 500, weight=18)   # Prod. Manager

    # left panel "Competitor Price Detail" values (measured: Quantity P1
    # text y=760-771, Price P1 y=792-803, Conversion Factor y=886-894)
    row_bar(draw, 758, 774, 240, 320, weight=20)   # Quantity P1
    row_bar(draw, 790, 806, 240, 320, weight=20)   # Price P1
    row_bar(draw, 883, 897, 305, 385, weight=18)   # Conversion Factor

    # right "Competitor Reference Info" panel value boxes (measured: City/
    # State + ID# text y=253-265, Items in database y=290-301, Website
    # y=326-340)
    row_bar(draw, 252, 268, 975, 1250, weight=22)  # City, State
    row_bar(draw, 252, 268, 1300, 1410, weight=22) # ID #
    row_bar(draw, 288, 304, 975, 1395, weight=20)  # Items in database
    row_bar(draw, 324, 342, 975, 1395, weight=22)  # Website

    # "Competitor XREF Detail" table data row: Comp Item#, ConvFac, and the
    # "Doesn't Match? and Note" column (item description); DrpShp/DelFlag
    # single-letter flags are left visible.
    row_bar(draw, 469, 483, 865, 1320, weight=18)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "pricing-2-competitor-entry.png"))
    print("Saved pricing-2-competitor-entry.png")


# --------------------------------------------------------------------------
# BulkCompetitorChanges.png -> pricing-3-bulk-changes.png
# Filter dropdowns + two identical CURRENT/CHANGED data tables. Last Update
# and Last Update By columns are left visible (dates + a system name, not
# identifying); every other data column is struck.
# --------------------------------------------------------------------------

def build_bulk_changes():
    src = os.path.join(SRC_DIR, "BulkCompetitorChanges.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # filter dropdowns (measured text y=213..229)
    row_bar(draw, 213, 229, 145, 375, weight=22)   # Competitor Filter
    row_bar(draw, 213, 229, 530, 760, weight=22)   # Competitor Item Filter

    # CURRENT Competitor Data table: 8 rows, 30px bands starting y=385
    # (measured text y=385..397 per row -> weight padded well past that span)
    current_rows = list(range(385, 385 + 30 * 8, 30))
    for y0 in current_rows:
        row_bar(draw, y0, y0 + 13, 160, 1190, weight=22)

    # CHANGED Competitor Data table: 8 rows. Row spacing here runs ~29px
    # (not the CURRENT table's clean 30px), so each row start was measured
    # directly rather than assumed, to avoid drift compounding by the last row.
    changed_rows = [716, 745, 774, 803, 832, 861, 890, 919]
    for y0 in changed_rows:
        row_bar(draw, y0, y0 + 14, 160, 1190, weight=22)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "pricing-3-bulk-changes.png"))
    print("Saved pricing-3-bulk-changes.png")


# --------------------------------------------------------------------------
# NoteFormEntry.png -> pricing-4-note-entry.png
# The free-text Comment box is the only proprietary content on this screen;
# note type, marketing class/subgroup selectors, and the subgroup lookup
# table are all structural/navigational, matching the BBA Tool precedent.
# --------------------------------------------------------------------------

def build_note_entry():
    src = os.path.join(SRC_DIR, "NoteFormEntry.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # "5. Enter Comment:" textarea content (measured text y=440..451)
    row_bar(draw, 440, 452, 145, 400, weight=20)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "pricing-4-note-entry.png"))
    print("Saved pricing-4-note-entry.png")


# --------------------------------------------------------------------------
# ReportBuildout.png -> pricing-5-report-buildout.png
# Reports menu + subgroup selection/lookup panel, all empty in this
# screenshot (no populated business data) - passes through unmodified
# except for the watermark.
# --------------------------------------------------------------------------

def build_report_buildout():
    src = os.path.join(SRC_DIR, "ReportBuildout.png")
    im = Image.open(src).convert("RGB")
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "pricing-5-report-buildout.png"))
    print("Saved pricing-5-report-buildout.png (pass-through, no data redaction needed)")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    build_main_menu()
    build_competitor_entry()
    build_bulk_changes()
    build_note_entry()
    build_report_buildout()


if __name__ == "__main__":
    main()
