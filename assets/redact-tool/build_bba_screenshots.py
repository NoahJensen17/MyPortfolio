"""
Build fabricated-data portfolio screenshots from the real BBA Tool originals.

This script reads the read-only originals in originals/ and produces sanitized
copies in ../img/ with:
  - all proprietary business data (real item numbers, descriptions, vendors,
    costs, customer names, order numbers) painted over and replaced with
    fabricated but plausible-looking placeholder values of the same shape,
  - the logged-in user's name badge replaced with a fabricated username,
  - a small "Illustrative data" watermark stamped in the bottom-right corner.

Approach: for each region to redact we sample the real background color
immediately next to the region (panels are white or light gray banded rows,
not pure white), paint a rectangle of that color over the original text, then
draw fabricated replacement text roughly matching the original position/size/
weight. Row/column pixel coordinates below were measured directly against the
original screenshots (see the coordinate comments per image).

Run:
    python build_bba_screenshots.py

Never edit files in originals/ — this script only reads them.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE, "originals")
OUT_DIR = os.path.normpath(os.path.join(BASE, "..", "img"))

WATERMARK_TEXT = "Illustrative data — not actual company figures"

FONT_REGULAR = "arial.ttf"
FONT_BOLD = "arialbd.ttf"

random.seed(42)


# --------------------------------------------------------------------------
# generic helpers
# --------------------------------------------------------------------------

def load_font(size, bold=False):
    name = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def sample_bg(im, x, y):
    """Sample a background color near (x, y), used to paint over a region."""
    return im.getpixel((x, y))


def paint(draw, box, color):
    draw.rectangle(box, fill=color)


def text_left(draw, xy, text, font, fill=(37, 36, 35)):
    draw.text(xy, text, font=font, fill=fill)


def stamp_watermark(img, text=WATERMARK_TEXT):
    """Same pattern as redact.py's _stamp_watermark: semi-transparent dark
    backing plate + white text, bottom-right corner."""
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


def redact_user_badge(im, draw):
    """The header shows a logged-in user pill badge in the top-right of every
    screen. This is the portfolio owner's own name, not proprietary company
    data, so it is left as the real name rather than fabricated."""
    return


# --------------------------------------------------------------------------
# fabricated data pools (all fictional, no resemblance to real values used)
# --------------------------------------------------------------------------

FAKE_ITEM_DESCS = [
    "STANDARD FOLDING UTILITY CART", "18X24 STORAGE BIN", "24X36 WIRE SHELF",
    "HEAVY DUTY PACKING TAPE 2IN", "STACKABLE TOTE BOX BLUE", "ADJUSTABLE WORK TABLE",
    "SAFETY CONE 28IN ORANGE", "CORRUGATED SHIPPING BOX 12X12", "FOAM PACKING SHEET",
    "STEEL SHELVING UNIT 5-TIER", "ERGONOMIC ANTI-FATIGUE MAT", "LABEL PRINTER RIBBON",
    "PALLET WRAP STRETCH FILM", "WAREHOUSE HAND TRUCK", "PLASTIC PARTS BIN SMALL",
    "CABLE MANAGEMENT SLEEVE", "INDUSTRIAL FLOOR SQUEEGEE", "RECYCLED CARDBOARD DIVIDER",
    "MOBILE TOOL CABINET", "BUNGEE CORD ASSORTMENT PACK",
]

FAKE_GROUP_NAMES = [
    "Storage Bins", "Wire Shelving", "Packing Supplies", "Totes And Bins",
    "Work Tables", "Safety Equipment", "Shipping Boxes", "Floor Care",
    "Hand Trucks", "Cable Management",
]

FAKE_SUBGROUP_NAMES = [
    "Blue Totes", "Wire Shelf Units", "Poly Tape", "Utility Carts",
    "Corner Guards", "Anti-Fatigue Mats", "Ribbon Supplies", "Stretch Film",
]

FAKE_VENDOR_NAMES = [
    "ACME SUPPLY CO.", "NORTHGATE INDUSTRIAL", "PINECREST WAREHOUSE CO.",
    "STERLING MATERIALS INC.", "REDWOOD LOGISTICS SUPPLY",
]

FAKE_CUSTOMER_NAMES = [
    "NORTHFIELD LOGISTICS", "BRAMBLE RETAIL GROUP", "CEDARVIEW DISTRIBUTION",
    "HARBORLINE FREIGHT LLC", "SUMMIT RIDGE FOODS", "GREENFIELD MACHINE WORKS",
    "TRUEPATH TRANSPORT INC", "MAPLEWOOD BOTTLING CO", "STONEBRIDGE HOLDINGS LLC",
    "IRONGATE WAREHOUSING", "BLUE HARBOR TEXTILES", "VANTAGE POINT SUPPLY",
    "RIVERBEND PACKAGING", "COPPERLINE INDUSTRIES", "FAIRWIND LOGISTICS CO",
    "WESTMOOR FURNITURE RENTAL", "ASHGROVE ELECTRIC SUPPLY", "CLEARWATER FOODS INC",
    "PRAIRIE OAK VENDING", "LANTERN HILL BAKERY", "GRANITE PEAK HVAC INC",
    "SILVERLEAF LAUNDRY CO", "CROSSROADS CONTRACT FLOORING", "MERIDIAN LAB SUPPLY",
    "BEACON POINT PURCHASING", "OAKHAVEN LOBSTER CO", "DELTA STREAM CORP",
    "HIGHLAND PARK ATHLETICS", "TUMBLEWEED FREIGHT LLC", "CASCADE RIDGE SCHOOLS",
    "FOUNDRY ROW INSTITUTE", "PARKSIDE UNIVERSITY", "EASTGATE ARTS CENTER",
    "MILLBROOK CENTER THE", "QUARRY HILL SERVICES", "LATTICE WORKS THE",
    "BROADFIELD INSTITUTE INC THE", "ELMWOOD PUBLIC SCHOOLS", "CLARKSTON ARTS INSTITUTE",
    "BAYRIDGE CENTER THE", "TIDEWATER CO",
]

FAKE_CITY_INSTITUTIONS = [
    "BROADFIELD INSTITUTE INC THE", "ELMWOOD PUBLIC SCHOOLS", "CLARKSTON ARTS INSTITUTE",
    "BAYRIDGE CENTER THE", "TIDEWATER CO", "COASTAL VENDING SERVICES",
]


def fake_item_number(rng, prefix="X"):
    return f"{prefix}-{rng.randint(1000, 9999)}"


def fake_order_number(rng, digits=8):
    lo = 10 ** (digits - 1)
    hi = 10 ** digits - 1
    return str(rng.randint(lo, hi))


def fake_cust_num(rng):
    return str(rng.randint(1000000, 29999999))


# --------------------------------------------------------------------------
# Image 1: OrderPointBatch_ChartScreen.png -> bba-1-item-detail.png
# --------------------------------------------------------------------------

def build_image1():
    src = os.path.join(SRC_DIR, "OrderPointBatch_ChartScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    rng = random.Random(1)

    fake_item = "X-2048"
    fake_desc = "STANDARD FOLDING UTILITY CART"
    fake_group = "410  Utility Carts"
    fake_subgroup = "2210 Folding Cart Standard"
    fake_vend = "48213"
    fake_vend_desc = "ACME SUPPLY CO."
    fake_cost = "$87.50"

    label_font = load_font(13)
    bold_val_font = load_font(13, bold=True)

    # left ITEM INFORMATION panel value column: x = 89..357
    x0, x1 = 89, 356
    rows = {
        "item": (157, 178, fake_item, True),
        "description": (178, 198, fake_desc, False),
        "group": (219, 239, fake_group, False),
        "subgroup": (239, 259, fake_subgroup, False),
        "vend": (259, 280, fake_vend, False),
        "vend_desc": (280, 301, fake_vend_desc, False),
        "cost": (509, 529, fake_cost, True),
    }
    for key, (y0, y1, text, bold) in rows.items():
        bg = sample_bg(im, x0 + 2, (y0 + y1) // 2)
        paint(draw, (x0, y0, x1, y1), bg)
        font = bold_val_font if bold else label_font
        fill = (7, 117, 176) if key == "item" else (46, 41, 37)
        text_left(draw, (x0, y0 + 3), text, font, fill=fill)

    # "Go to:" dropdown bar, x=178..549, y=105..126 (white bg with border kept)
    bg = sample_bg(im, 300, 116)
    paint(draw, (179, 106, 549, 125), bg)
    text_left(draw, (188, 109), f"{fake_item} — J6 — {fake_desc}", load_font(13), fill=(46, 41, 37))

    # chart title "H-1054" -> fake item number, bg (247,247,247)
    bg = sample_bg(im, 1090, 330)
    paint(draw, (1085, 322, 1195, 348), bg)
    tf = load_font(20)
    draw.text((1090, 326), fake_item, font=tf, fill=(46, 41, 37))

    redact_user_badge(im, draw)
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-1-item-detail.png"))
    print("Saved bba-1-item-detail.png")


# --------------------------------------------------------------------------
# Image 2: Selection_MainScreen.png -> bba-2-item-grid.png
# --------------------------------------------------------------------------

def build_image2():
    src = os.path.join(SRC_DIR, "Selection_MainScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    rng = random.Random(2)
    font = load_font(13)
    link_font = load_font(13)

    # --- top-left "Item List" panel: rows y=133..312 (9 rows, 20px each),
    # item-number text column x=38..179, whse text column x=195..235 (kept, "I6")
    item_rows_y = [133, 153, 173, 193, 213, 233, 253, 273, 293]
    for y0 in item_rows_y:
        y1 = y0 + 20
        bg = sample_bg(im, 160, y0 + 10)
        paint(draw, (33, y0, 179, y1), bg)
        fake_it = fake_item_number(rng)
        text_left(draw, (40, y0 + 3), fake_it, font, fill=(7, 117, 176))

    # --- main data grid: rows y=493..852 in 30px bands, 12 rows
    row_tops = list(range(493, 853, 30))
    columns = {
        # name: (x0, x1)
        "item": (10, 130),
        "desc": (135, 431),
        "onhand": (1059, 1152),
        "onorder": (1152, 1247),
        "avg2mo": (1247, 1340),
        "avg6mo": (1340, 1433),
        "group": (1433, 1521),
        "groupdesc": (1521, 1694),
        "subgroup": (1694, 1789),
        "subgroupdesc": (1789, 1919),
    }

    for y0 in row_tops:
        y1 = y0 + 30
        row_bg = sample_bg(im, 900, y0 + 15)

        fake_it = fake_item_number(rng)
        fake_desc = rng.choice(FAKE_ITEM_DESCS)
        onhand = rng.randint(5, 150)
        onorder = round(rng.uniform(0, 120), 1)
        avg2 = round(rng.uniform(1, 90), 1)
        avg6 = round(rng.uniform(50, 700), 0)
        group_num = rng.randint(100, 900)
        group_name = rng.choice(FAKE_GROUP_NAMES)
        subgroup_num = rng.randint(1000, 9000)
        subgroup_name = rng.choice(FAKE_SUBGROUP_NAMES)

        # item#
        paint(draw, (columns["item"][0], y0, columns["item"][1], y1), row_bg)
        text_left(draw, (columns["item"][0] + 2, y0 + 6), fake_it, link_font, fill=(7, 117, 176))

        # description
        paint(draw, (columns["desc"][0], y0, columns["desc"][1], y1), row_bg)
        text_left(draw, (columns["desc"][0] + 4, y0 + 6), fake_desc, font, fill=(46, 41, 37))

        # numeric columns
        for key, val in [("onhand", onhand), ("onorder", onorder), ("avg2mo", avg2), ("avg6mo", avg6)]:
            x0, x1 = columns[key]
            paint(draw, (x0, y0, x1, y1), row_bg)
            s = str(val)
            text_left(draw, (x0 + 4, y0 + 6), s, font, fill=(46, 41, 37))

        # group / groupdesc / subgroup / subgroupdesc
        x0, x1 = columns["group"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        text_left(draw, (x0 + 4, y0 + 6), str(group_num), font, fill=(46, 41, 37))

        x0, x1 = columns["groupdesc"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        text_left(draw, (x0 + 4, y0 + 6), group_name, font, fill=(46, 41, 37))

        x0, x1 = columns["subgroup"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        text_left(draw, (x0 + 4, y0 + 6), str(subgroup_num), font, fill=(46, 41, 37))

        x0, x1 = columns["subgroupdesc"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        text_left(draw, (x0 + 4, y0 + 6), subgroup_name, font, fill=(46, 41, 37))

    redact_user_badge(im, draw)
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-2-item-grid.png"))
    print("Saved bba-2-item-grid.png")


# --------------------------------------------------------------------------
# Image 3: ReportingMenuScreen.png -> bba-3-exception-reporting.png
# Pure navigation/menu screen (report names only, no business data values) -
# passes through unmodified except for the user badge + watermark.
# --------------------------------------------------------------------------

def build_image3():
    src = os.path.join(SRC_DIR, "ReportingMenuScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    redact_user_badge(im, draw)
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-3-exception-reporting.png"))
    print("Saved bba-3-exception-reporting.png (pass-through, no data redaction needed)")


# --------------------------------------------------------------------------
# Image 4: OPCompareReview_TableScreen.png -> bba-4-op-compare.png
# --------------------------------------------------------------------------

def build_image4():
    src = os.path.join(SRC_DIR, "OPCompareReview_TableScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    rng = random.Random(4)
    font = load_font(12)
    link_font = load_font(12)

    # data rows: y = 212.., 26px each, through the bottom of the image
    # (last row may be partially cut off by the window edge)
    row_tops = list(range(212, im.size[1], 26))
    columns = {
        "item": (90, 182),
        "desc": (184, 377),
        "skidqty": (379, 435),
        "unitcost": (437, 509),
        "usage": (1127, 1183),
        "convfac_newop": (1185, 1264),
        "current_op": (1266, 1338),
        "new_op_skids": (1340, 1417),
    }

    for y0 in row_tops:
        y1 = y0 + 26
        row_bg = sample_bg(im, 1900, y0 + 13)

        fake_it = fake_item_number(rng, prefix=rng.choice(["H", "S"]))
        fake_desc = rng.choice(FAKE_ITEM_DESCS)
        skid_qty = rng.choice([12, 18, 24, 36, 48, 60, 96, 120, 360, 999])
        unit_cost = f"${rng.uniform(0.5, 200):.2f}"
        usage = rng.randint(2, 900)
        current_op = usage  # mirrors usage in the source data
        new_op_skids = round(usage / rng.choice([10, 15, 20, 30]), 1)

        paint(draw, (columns["item"][0], y0, columns["item"][1], y1), row_bg)
        text_left(draw, (columns["item"][0] + 2, y0 + 6), fake_it, link_font, fill=(7, 117, 176))

        paint(draw, (columns["desc"][0], y0, columns["desc"][1], y1), row_bg)
        text_left(draw, (columns["desc"][0] + 4, y0 + 6), fake_desc, font, fill=(46, 41, 37))

        x0, x1 = columns["skidqty"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        s = str(skid_qty)
        bbox = draw.textbbox((0, 0), s, font=font)
        text_left(draw, (x1 - (bbox[2] - bbox[0]) - 6, y0 + 6), s, font, fill=(46, 41, 37))

        x0, x1 = columns["unitcost"]
        paint(draw, (x0, y0, x1, y1), row_bg)
        bbox = draw.textbbox((0, 0), unit_cost, font=font)
        text_left(draw, (x1 - (bbox[2] - bbox[0]) - 6, y0 + 6), unit_cost, font, fill=(46, 41, 37))

        for key, val in [("usage", usage), ("convfac_newop", current_op), ("current_op", current_op), ("new_op_skids", new_op_skids)]:
            x0, x1 = columns[key]
            paint(draw, (x0, y0, x1, y1), row_bg)
            s = str(val)
            bbox = draw.textbbox((0, 0), s, font=font)
            text_left(draw, (x1 - (bbox[2] - bbox[0]) - 6, y0 + 6), s, font, fill=(46, 41, 37))

    redact_user_badge(im, draw)
    stamp_watermark(im)
    im.save(os.path.join(OUT_DIR, "bba-4-op-compare.png"))
    print("Saved bba-4-op-compare.png")


# --------------------------------------------------------------------------
# Image 5: TransactionDetail_FilteringScreen.png -> bba-5-transactional-detail.png
# --------------------------------------------------------------------------

def build_image5():
    src = os.path.join(SRC_DIR, "TransactionDetail_FilteringScreen.png")
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    rng = random.Random(5)
    font = load_font(13)

    fake_item = "X-2048"
    fake_desc = "STANDARD FOLDING UTILITY CART"

    # top item#/description bar: real bar spans y=78..112, x=4..~360
    # (measured directly), paint generously to x=500 for margin.
    bg = sample_bg(im, 200, 90)
    paint(draw, (4, 78, 500, 111), bg)
    text_left(draw, (10, 84), "ITEM#", load_font(11), fill=(120, 120, 120))
    text_left(draw, (60, 82), fake_item, load_font(14, bold=True), fill=(46, 41, 37))
    text_left(draw, (150, 82), fake_desc, load_font(14), fill=(46, 41, 37))

    # --- Transactional Detail grid: rows y=178..497, 20px bands (16 rows)
    row_tops = list(range(178, 498, 20))
    col_ordnum = (3, 108)
    col_custnum = (493, 583)
    col_custname = (583, 900)

    used_names = FAKE_CUSTOMER_NAMES.copy()
    rng.shuffle(used_names)
    name_cycle = used_names + used_names  # enough to cover rows without exhausting

    for i, y0 in enumerate(row_tops):
        y1 = y0 + 19
        row_bg = sample_bg(im, 700, y0 + 9)

        fake_order = fake_order_number(rng, 8)
        fake_cnum = fake_cust_num(rng)
        fake_name = name_cycle[i % len(name_cycle)]

        paint(draw, (col_ordnum[0], y0, col_ordnum[1], y1), row_bg)
        text_left(draw, (col_ordnum[0] + 4, y0 + 3), fake_order, font, fill=(7, 117, 176))

        paint(draw, (col_custnum[0], y0, col_custnum[1], y1), row_bg)
        text_left(draw, (col_custnum[0] + 4, y0 + 3), fake_cnum, font, fill=(7, 117, 176))

        paint(draw, (col_custname[0], y0, col_custname[1], y1), row_bg)
        text_left(draw, (col_custname[0] + 4, y0 + 3), fake_name, font, fill=(46, 41, 37))

    # --- filter popup checkbox list: 6 rows, x=910..1145, redact institution names
    # (real text for the last row extends to y~567, just before the Apply
    # Filter button border at y=576, so the last band is stretched to 575
    # to fully cover it with margin)
    popup_bg = sample_bg(im, 1000, 430)
    popup_rows = [(422, 446), (446, 470), (470, 494), (494, 518), (518, 542), (542, 575)]
    for i, (y0, y1) in enumerate(popup_rows):
        paint(draw, (908, y0, 1148, y1), popup_bg)
        # keep the checkbox glyph itself (small blue check box ~ x=912-926); redraw a check box + fake name
        draw.rectangle((912, y0 + 6, 926, y0 + 20), outline=(7, 117, 176), width=1)
        draw.line((914, y0 + 13, 918, y0 + 17), fill=(7, 117, 176), width=2)
        draw.line((918, y0 + 17, 924, y0 + 8), fill=(7, 117, 176), width=2)
        text_left(draw, (932, y0 + 4), FAKE_CITY_INSTITUTIONS[i], font, fill=(46, 41, 37))

    # --- Month Summary table (bottom-left): Max Customer column x=540..823.
    # Extend through the image bottom edge to catch the partially cut-off
    # last visible row.
    ms_rows = list(range(574, im.size[1], 20))
    for y0 in ms_rows:
        y1 = y0 + 19
        row_bg = sample_bg(im, 300, y0 + 9)
        fake_name = rng.choice(FAKE_CUSTOMER_NAMES)
        paint(draw, (542, y0, 821, y1), row_bg)
        text_left(draw, (546, y0 + 3), fake_name, font, fill=(46, 41, 37))

    # --- Customer Summary table (bottom-right): Name column. The column's
    # text can start as far left as x=1112 depending on row (measured
    # directly against real rows), well left of the panel title's x=1153,
    # so paint from x=1108 to fully cover it with margin.
    cs_rows = list(range(574, im.size[1], 20))
    used2 = FAKE_CUSTOMER_NAMES.copy()
    rng.shuffle(used2)
    for i, y0 in enumerate(cs_rows):
        y1 = y0 + 19
        row_bg = sample_bg(im, 1450, y0 + 9)
        fake_name = used2[i % len(used2)]
        paint(draw, (1108, y0, 1419, y1), row_bg)
        text_left(draw, (1159, y0 + 3), fake_name, font, fill=(46, 41, 37))

    redact_user_badge(im, draw)
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
