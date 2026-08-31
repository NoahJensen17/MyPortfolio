"""
Build strikethrough-redacted portfolio screenshots from the real BBA Tool originals.

Reads originals/BBA Tool/*.png and writes sanitized copies to
../img/BBA Tool/*.png. See redact_helpers.py for the shared strike/watermark
approach.

Two strike styles are used:
  - thin_strike: a single heavy line through the middle of one line of
    label:value text (item#, description, chart titles, etc), thick enough
    that the text underneath is not legible.
  - row_bar / col_bar: a thick bar spanning a data row or a stacked axis
    column. Only proprietary/identifying data is struck (item/customer
    numbers, names, costs); non-identifying columns (dates, counts,
    dropdowns, colored badges) are left visible.

Row/column pixel coordinates below were measured directly against the
original screenshots.

Run:
    py -3 build_bba_screenshots.py

Never edit files in originals/ — this script only reads them.
"""
import os
from PIL import Image, ImageDraw

from redact_helpers import thin_strike, row_bar, col_bar, stamp_watermark

BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE, "originals", "BBA Tool")
OUT_DIR = os.path.normpath(os.path.join(BASE, "..", "img", "BBA Tool"))


# --------------------------------------------------------------------------
# Image 1: OrderPointBatch_ChartScreen.png -> bba-1-item-detail.png
# ITEM INFORMATION panel: single-line label:value rows, thin strike over the
# value text. Chart title (fake item# echoed above the chart) also struck.
# --------------------------------------------------------------------------

def build_image1():
    src = os.path.join(SRC_DIR, "OrderPointBatch_ChartScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # value column x-range for the left ITEM INFORMATION panel
    x0, x1 = 89, 356
    # y = vertical center of each single-line row (measured against the panel)
    rows_y = [168, 188, 229, 249, 270, 291, 519]
    for y in rows_y:
        thin_strike(draw, y, x0, x1)

    # "Go to:" dropdown bar text, x=188..549, y=105..126
    thin_strike(draw, 116, 188, 549)

    # chart title (echoes the item# above the chart), x=1085..1195, y=322..348
    thin_strike(draw, 335, 1085, 1195, weight=8)

    # OP Cost value in the ORDER POINT panel, x=797..829, y=267..275
    row_bar(draw, 264, 278, 795, 832, weight=10)

    # primary (left) y-axis: rotated "Sales Qty" title (x=366..373) and tick
    # numbers (x=385..394) are two separate narrow columns, not one wide
    # band, so each gets its own vertical bar spanning the full axis height.
    col_bar(draw, 362, 378, 405, 795, weight=18)
    col_bar(draw, 381, 398, 405, 795, weight=18)

    # secondary (right) y-axis: tick numbers (x=1880..1899) and rotated
    # "Skid Qty" title (x=1908..1917); clears the colored legend badges
    # further left, which end around x=1827.
    col_bar(draw, 1876, 1903, 405, 795, weight=28)
    col_bar(draw, 1905, 1919, 405, 795, weight=16)

    # bottom-left YEAR/TOTAL/COMP% trend table: strike Total + Comp% columns
    # only (row bands measured at y~830-843, 844-857, 858-871, 872-885); Year
    # column left visible since a bare year isn't sensitive on its own.
    year_table_rows = [830, 844, 858, 872]
    for y0 in year_table_rows:
        row_bar(draw, y0, y0 + 13, 95, 345, weight=8)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-1-item-detail.png"))
    print("Saved bba-1-item-detail.png")


# --------------------------------------------------------------------------
# Image 2: Selection_MainScreen.png -> bba-2-item-grid.png
# Mixed grid (checkboxes present) - bar only spans text/numeric data columns,
# not the checkbox column.
# --------------------------------------------------------------------------

def build_image2():
    src = os.path.join(SRC_DIR, "Selection_MainScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # --- top-left "Item List" panel: rows y=133..312 (9 rows, 20px each),
    # item-number text column x=38..179 (whse column x=195..235 left intact)
    item_rows_y = [133, 153, 173, 193, 213, 233, 253, 273, 293]
    for y0 in item_rows_y:
        row_bar(draw, y0, y0 + 20, 36, 179, weight=6)

    # --- main data grid: rows y=493..852 in 30px bands, 12 rows.
    # Bar spans item# through subgroupdesc (all plain text/numeric columns);
    # no checkboxes in this grid's visible columns so full data width is safe.
    row_tops = list(range(493, 853, 30))
    x0, x1 = 10, 1919
    for y0 in row_tops:
        row_bar(draw, y0, y0 + 30, x0, x1, weight=8)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-2-item-grid.png"))
    print("Saved bba-2-item-grid.png")


# --------------------------------------------------------------------------
# Image 3: ReportingMenuScreen.png -> bba-3-exception-reporting.png
# Pure navigation/menu screen (report names only, no business data values) -
# passes through unmodified except for the watermark.
# --------------------------------------------------------------------------

def build_image3():
    src = os.path.join(SRC_DIR, "ReportingMenuScreen.png")
    im = Image.open(src).convert("RGB")
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-3-exception-reporting.png"))
    print("Saved bba-3-exception-reporting.png (pass-through, no data redaction needed)")


# --------------------------------------------------------------------------
# Image 4: OPCompareReview_TableScreen.png -> bba-4-op-compare.png
# Mixed grid (checkboxes, dropdowns, colored badges) - bar only spans the
# plain text/numeric columns (item#, description, skid qty, unit cost); the
# dropdown/badge columns further right are left untouched.
# --------------------------------------------------------------------------

def build_image4():
    src = os.path.join(SRC_DIR, "OPCompareReview_TableScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # data rows: y = 212.., 26px each, through the bottom of the image
    row_tops = list(range(212, im.size[1], 26))
    # item# through unit cost columns only (checkbox at x<90, dropdowns start ~x=590)
    x0, x1 = 90, 509

    for y0 in row_tops:
        row_bar(draw, y0, y0 + 26, x0, x1, weight=6)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-4-op-compare.png"))
    print("Saved bba-4-op-compare.png")


# --------------------------------------------------------------------------
# Image 5: TransactionDetail_FilteringScreen.png -> bba-5-transactional-detail.png
# Only the columns that actually identify a customer/item get struck (Item#/
# description, Cust Num, Cust Name, Max Customer, Name in the summary
# panels, institution names in the filter popup). Order Num, Ship Date,
# Year Month, Ord Date, Whse, and the numeric summary columns are left
# visible since they carry no identifying data on their own.
# --------------------------------------------------------------------------

def build_image5():
    src = os.path.join(SRC_DIR, "TransactionDetail_FilteringScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)

    # top item#/description bar: y=78..112
    thin_strike(draw, 93, 60, 500, weight=8)

    # --- Transactional Detail grid: rows y=178..497, 20px bands (16 rows).
    # Cust Num column (x=493..583) and Cust Name column (x=583..900) only.
    row_tops = list(range(178, 498, 20))
    for y0 in row_tops:
        row_bar(draw, y0, y0 + 19, 493, 900, weight=6)

    # --- filter popup checkbox list: 6 rows, text centered on y = 433, 459,
    # 485, 511, 537, 563 (26px spacing, measured directly). Keep the checkbox
    # glyph itself intact, strike only the label text; last row band stops at
    # y=575 to land just above the "Apply Filter" button (starts y=585).
    popup_rows = [(421, 445), (447, 471), (473, 497), (499, 523), (525, 549), (551, 575)]
    for (y0, y1) in popup_rows:
        row_bar(draw, y0, y1, 930, 1148, weight=6)

    # The open filter popup box (measured) sits over x=908..1158, y=178..615
    # and is opaque, so table rows underneath it must not be struck there -
    # the strike bar would draw past the popup's edge into empty margin and
    # look like it's leaking out from behind the box.
    POPUP_BOX = (908, 178, 1158, 615)

    # --- Month Summary table (bottom-left): Max Customer column only,
    # x=542..821 (before the "Max Cust..." numeric column starts ~x=825).
    # This column sits entirely left of the popup box, so no clipping needed.
    ms_rows = list(range(574, im.size[1], 20))
    for y0 in ms_rows:
        row_bar(draw, y0, y0 + 19, 542, 821, weight=6)

    # --- Customer Summary table (bottom-right): Name column only,
    # x=1108..1419 (before the "Total Shipped" numeric column starts). Rows
    # that overlap the popup box's y-range get clipped to start at the
    # popup's right edge instead of the column's real left edge.
    cs_rows = list(range(574, im.size[1], 20))
    for y0 in cs_rows:
        y1 = y0 + 19
        x0 = 1108
        if y0 < POPUP_BOX[3]:
            x0 = max(x0, POPUP_BOX[2])
        row_bar(draw, y0, y1, x0, 1419, weight=6)

    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-5-transactional-detail.png"))
    print("Saved bba-5-transactional-detail.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    build_image1()
    build_image2()
    build_image3()
    build_image4()
    build_image5()


if __name__ == "__main__":
    main()
