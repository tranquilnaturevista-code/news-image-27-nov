#!/usr/bin/env python3
"""Paint the front page for Friday 27 November 2026 and save entry.png.

A single-page newspaper that sums up the day's world news, painted with
Pillow from fixed copy and shapes. Nothing is fetched, nothing is timed
and nothing is random, so every run paints the same bytes.

The copy below is drawn from reporting first published on 27 November
2026 (AP, Reuters, BBC, the European Council press service, CNN). Where
the day's reporting left a figure unconfirmed it is not printed: the
Yemen item carries no casualty toll, because the coverage that day
reported strikes on both sides without a confirmed count.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 40
OUT_PATH = Path(__file__).resolve().parent / "entry.png"

PAPER_BG = (250, 246, 238)
INK_COL = (22, 20, 16)
CRIMSON = (172, 32, 24)
DEEP_BLUE = (16, 44, 84)
MUTED = (105, 100, 90)
TINT_A = (228, 238, 246)
TINT_B = (244, 232, 214)
HAIRLINE = (196, 186, 170)

FONT_ROOT = "/usr/share/fonts/truetype/liberation"
FACES = {
    "serif_b": "LiberationSerif-Bold",
    "serif": "LiberationSerif-Regular",
    "sans_b": "LiberationSans-Bold",
    "sans": "LiberationSans-Regular",
}


def typeface(face, size):
    """Load one Liberation face at the given point size."""
    return ImageFont.truetype(f"{FONT_ROOT}/{FACES[face]}.ttf", size)


def fit_words(canvas, text, face, width):
    """Split text into lines that fit `width`, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        joined = (current + " " + word).strip()
        if canvas.textlength(joined, font=face) <= width:
            current = joined
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(canvas, x, y, width, text, face, colour=INK_COL, spacing=1.3):
    """Paint a wrapped paragraph; hand back the y below its last line."""
    for line in fit_words(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=colour)
        y += round(face.size * spacing)
    return y


def draw_title(canvas, x, y, width, text, size, colour=INK_COL):
    """Paint a wrapped serif-bold headline; return the y below it."""
    face = typeface("serif_b", size)
    for line in fit_words(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=colour)
        y += round(size * 1.1)
    return y


def draw_tag(canvas, x, y, label, colour=CRIMSON, size=16):
    """Paint a small-caps section label; return the y below it."""
    face = typeface("sans_b", size)
    canvas.text((x, y), label.upper(), font=face, fill=colour)
    return y + size + 8


def draw_hline(canvas, x0, x1, y, thick=2, colour=INK_COL):
    """Paint a horizontal rule from x0 to x1 at height y."""
    canvas.line([(x0, y), (x1, y)], fill=colour, width=thick)


def story_card(canvas, x, top, width, height, story, tint=None):
    """Paint one story in a column: label, headline, body.

    `story` holds tag / place / head / body. A tint paints a soft panel
    behind the column; without one the column sits on bare paper.
    """
    if tint is not None:
        canvas.rounded_rectangle(
            [x, top, x + width, top + height], radius=6, fill=tint
        )
    pad = 16 if tint is not None else 0
    pen = top + (14 if tint is not None else 0)
    pen = draw_tag(canvas, x + pad, pen, story["tag"])
    if story.get("place"):
        face = typeface("sans_b", 15)
        canvas.text(
            (x + pad, pen - 22),
            story["place"].upper(),
            font=face,
            fill=DEEP_BLUE,
        )
    pen = draw_title(canvas, x + pad, pen + 2, width - 2 * pad,
                     story["head"], 25)
    draw_block(canvas, x + pad, pen + 6, width - 2 * pad,
               story["body"], typeface("sans", 17), spacing=1.28)


def main():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_BG)
    canvas = ImageDraw.Draw(sheet)
    far = PAGE_W - EDGE

    # --- frame ---------------------------------------------------------
    canvas.rectangle([12, 12, PAGE_W - 13, PAGE_H - 13],
                     outline=INK_COL, width=3)
    canvas.rectangle([20, 20, PAGE_W - 21, PAGE_H - 21],
                     outline=INK_COL, width=1)

    # --- nameplate -----------------------------------------------------
    canvas.text((EDGE, 34), "THE WORLD TODAY",
                font=typeface("serif_b", 58), fill=INK_COL)
    canvas.rectangle([EDGE, 108, far, 113], fill=CRIMSON)
    pen = 126
    face = typeface("sans_b", 16)
    canvas.text((EDGE, pen), "FRIDAY 27 NOVEMBER 2026",
                font=face, fill=MUTED)
    right = "ONE PAGE  ·  THE DAY'S WORLD NEWS"
    canvas.text((far - canvas.textlength(right, font=face), pen), right,
                font=face, fill=MUTED)
    draw_hline(canvas, EDGE, far, 152, 1, HAIRLINE)

    # --- lead story: Kuwait --------------------------------------------
    pen = 168
    face = typeface("sans_b", 16)
    canvas.text((EDGE, pen), "MIDDLE EAST", font=face, fill=CRIMSON)
    city = "KUWAIT CITY  ·  THE GULF"
    canvas.text((EDGE + 150, pen), city, font=face, fill=DEEP_BLUE)
    pen = draw_title(
        canvas, EDGE, pen + 30, far - EDGE,
        "Drone attack on Kuwait kills two Italian technicians", 38)
    pen = draw_block(
        canvas, EDGE, pen + 10, far - EDGE,
        "Kuwait says its air defences brought down several drones sent "
        "from Iran; debris from the intercepts killed two Italian "
        "technicians working on air defence and wounded a Kuwaiti and a "
        "Pakistani. The strike is the second Iranian attack on the Gulf "
        "state, a US ally, this month. Tehran denies any part in it.",
        typeface("serif", 21), spacing=1.3)
    draw_hline(canvas, EDGE, far, pen + 16, 3)
    draw_hline(canvas, EDGE, far, pen + 22, 1)

    # --- middle row: three stories --------------------------------------
    col_w = (far - EDGE - 2 * 24) // 3
    cols = [EDGE, EDGE + col_w + 24, EDGE + 2 * (col_w + 24)]
    top = pen + 40
    stories = [
        {"tag": "Gaza", "place": "",
         "head": "Ten die in Gaza strikes as ceasefire frays",
         "body": "Hospitals said five air strikes and a shooting left ten "
                 "Palestinians dead, among them a deputy Hamas minister "
                 "and his wife."},
        {"tag": "Europe", "place": "",
         "head": "Spain's Hernández de Cos to head the ECB",
         "body": "European Union leaders chose the former governor of "
                 "Spain's central bank to take over from Christine "
                 "Lagarde; the formal appointment follows in December."},
        {"tag": "European Union", "place": "",
         "head": "Twelve hours of talks, no EU budget deal",
         "body": "Leaders left Brussels still split over the budget for "
                 "2028–2034, though 24 countries backed a €45 billion "
                 "loan for Ukraine."},
    ]
    tints = [TINT_A, TINT_B, None]
    for x, story, tint in zip(cols, stories, tints):
        story_card(canvas, x, top, col_w, 218, story, tint)
    pen = top + 218
    draw_hline(canvas, EDGE, far, pen + 18, 2)

    # --- Yemen band -------------------------------------------------------
    pen = pen + 36
    band_top = pen
    pen = draw_title(canvas, EDGE + 24, pen, far - EDGE - 24,
                     "Saudi air strikes hit Yemen as Houthis strike a refinery",
                     26)
    pen = draw_block(
        canvas, EDGE + 24, pen + 4, far - EDGE - 24,
        "The coalition says it destroyed 50 Houthi targets, while the "
        "Houthis hit a Saudi oil refinery and the financial district in "
        "Riyadh.", typeface("sans", 17), spacing=1.28)
    # The crimson bar runs exactly as tall as the band's own text.
    canvas.rectangle([EDGE, band_top, EDGE + 8, pen], fill=CRIMSON)
    draw_hline(canvas, EDGE, far, pen + 18, 2)

    # --- also today -------------------------------------------------------
    pen = pen + 36
    draw_tag(canvas, EDGE, pen, "Also today")
    pen += 30
    briefs = [
        ("New York",
         "The 100th Macy's Thanksgiving Day Parade moves to Saturday "
         "after a storm forecast of gusts to 60 mph — the first weather "
         "delay in the parade's history."),
        ("Bangkok",
         "At least nine people are hurt in an explosion at an oil "
         "refinery; the operator is watching air quality around the "
         "site."),
        ("Black Friday",
         "About 183 million Americans are expected to shop across the "
         "Thanksgiving weekend, and three in five say they will use AI "
         "to help them choose."),
    ]
    for i, (label, text) in enumerate(briefs):
        x = cols[i]
        if i:
            canvas.line([(x - 12, pen), (x - 12, pen + 104)],
                        fill=MUTED, width=1)
        face = typeface("sans_b", 15)
        canvas.text((x, pen), label.upper(), font=face, fill=DEEP_BLUE)
        draw_block(canvas, x, pen + 26, col_w, text,
                   typeface("sans", 16), spacing=1.28)
    pen += 118

    # --- footer -----------------------------------------------------------
    draw_hline(canvas, EDGE, far, pen, 1, HAIRLINE)
    foot = typeface("sans", 15)
    canvas.text((EDGE, pen + 12),
                "Reporting: AP, Reuters, BBC, European Council, CNN "
                "· Friday 27 November 2026",
                font=foot, fill=MUTED)
    canvas.text((EDGE, pen + 34),
                "make.fun news-image-20261127 · a drawn summary, no "
                "photographs",
                font=foot, fill=MUTED)

    sheet.save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
