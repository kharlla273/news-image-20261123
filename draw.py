#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026, save as entry.png.

Everything on the page is fixed text baked into this file: no input, no
network, no clock, so every run writes the same bytes.
Run:  python3 draw.py   (writes entry.png next to it)
"""
# Layout of the 1024x1024 front page, top to bottom:
#   Masthead (y 28-190): a double rule frames the paper's name in large
#   serif caps, the date in red sans bold, and a grey tagline underneath.
#   Lead story (y 204-~500): a red kicker, a two-line serif headline
#   ("CLIMATE TALKS / COLLAPSE"), a wrapped body paragraph, then a navy
#   banner carrying the pull quote about the final draft.
#   Illustration panel (64 px tall): a deep-sea band holding a cracked
#   globe on the left, a gold sun with rays on the right, and a caption
#   naming the COP31 venue; heat lines rise between globe and sun.
#   Four stories, two by two (each 112 px tall): a coloured side bar and
#   kicker, a serif headline, and a wrapped body paragraph per story.
#   "Also today" strip: two short items in one paragraph, then a rule
#   and a centred grey sources line at the foot of the page.
# Palette: warm newsprint paper, near-black ink, red and navy accents,
# gold for the sun; DejaVu Serif for headlines, DejaVu Sans for kickers.
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)   # warm newsprint
INK = (20, 20, 20)
RED = (176, 30, 30)
NAVY = (27, 58, 92)
SEA = (18, 42, 68)
GREY = (90, 86, 76)
RULE = (60, 58, 50)
GOLD = (201, 162, 39)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 46  # side margin

    # ---- masthead ---------------------------------------------------
    d.line([(m, 28), (W - m, 28)], fill=RULE, width=3)
    centred(d, W // 2, 40, "THE WORLD IN ONE DAY", font(SERIF, 56))
    d.line([(m, 120), (W - m, 120)], fill=RULE, width=2)
    centred(d, W // 2, 130, "MONDAY  \u2022  23 NOVEMBER 2026",
            font(SANS_B, 25), fill=RED)
    centred(d, W // 2, 162,
            "One day, six stories \u2014 the world as it happened",
            font(SERIF_REG, 19), fill=GREY)
    d.line([(m, 190), (W - m, 190)], fill=RULE, width=2)

    # ---- lead story -------------------------------------------------
    y = 204
    d.text((m, y), "LEAD STORY \u2014 CLIMATE", font=font(SANS_B, 19), fill=RED)
    tag = "NO DEAL AT COP31"
    d.text((W - m - d.textlength(tag, font=font(SANS_B, 19)), y),
           tag, font=font(SANS_B, 19), fill=GREY)
    y += 28
    d.text((m, y), "CLIMATE TALKS", font=font(SERIF, 58), fill=INK)
    y += 62
    d.text((m, y), "COLLAPSE", font=font(SERIF, 58), fill=RED)
    y += 66
    y = para(d, m, y,
             "The COP31 climate talks collapse without a deal: the "
             "final draft drops any mention of fossil fuels, and "
             "negotiators go home empty-handed. Australia's prime "
             "minister calls the failure a sign of difficult "
             "geopolitical times.",
             font(SERIF_REG, 24), W - 2 * m, 31)
    y += 8
    d.rectangle([(m, y), (W - m, y + 48)], fill=NAVY)
    d.text((m + 16, y + 11),
           "FINAL DRAFT DROPS \u201cFOSSIL FUELS\u201d  \u2022  NO DEAL REACHED",
           font=font(SANS_B, 20), fill=(255, 255, 255))
    y += 48 + 12

    # ---- illustration: cracked globe under a pale sun ---------------
    panel_y, panel_h = y, 64
    d.rectangle([(m, panel_y), (W - m, panel_y + panel_h)], fill=SEA)
    # sun, top right
    sx, sy, sr = W - m - 70, panel_y + 32, 22
    for ang in range(0, 360, 30):
        ex = sx + (sr + 10) * math.cos(math.radians(ang))
        ey = sy + (sr + 10) * math.sin(math.radians(ang))
        d.line([(sx, sy), (ex, ey)], fill=GOLD, width=3)
    d.ellipse([(sx - sr, sy - sr), (sx + sr, sy + sr)], fill=GOLD)
    # globe, left
    gx, gy, gr = m + 110, panel_y + 32, 24
    d.ellipse([(gx - gr, gy - gr), (gx + gr, gy + gr)],
              fill=(90, 140, 180), outline=(255, 255, 255), width=2)
    d.arc([(gx - gr, gy - gr), (gx + gr, gy + gr)], 300, 60,
          fill=(255, 255, 255), width=2)
    d.arc([(gx - gr, gy - gr), (gx + gr, gy + gr)], 120, 240,
          fill=(255, 255, 255), width=2)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=(255, 255, 255), width=2)
    # crack across the globe
    d.line([(gx - 14, gy - 22), (gx - 4, gy - 6), (gx - 12, gy + 6),
            (gx + 2, gy + 20)], fill=(255, 255, 255), width=3)
    # rising heat lines
    for hx in range(m + 200, m + 500, 60):
        d.line([(hx, panel_y + 52), (hx, panel_y + 30)], fill=GOLD, width=3)
        d.line([(hx + 8, panel_y + 56), (hx + 8, panel_y + 38)],
               fill=(255, 255, 255), width=2)
    d.text((m + 560, panel_y + 8), "COP31, ANTALYA",
           font=font(SANS_B, 20), fill=(255, 255, 255))
    d.text((m + 560, panel_y + 34), "talks end with no deal",
           font=font(SANS, 15), fill=(200, 205, 215))
    y = panel_y + panel_h + 12
    d.line([(m, y), (W - m, y)], fill=RULE, width=2)
    y += 12

    # ---- four stories, two by two -----------------------------------
    stories = [
        ("LIBYA \u2014 BENGHAZI", "BLAST HITS RUSSIAN SHIP",
         "Libya suspects a drone attack caused the blast on a "
         "Russian ship; 10 port workers hurt.", RED),
        ("MEXICO \u2014 SINALOA", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
         "Mexico arrests the FBI's most-wanted cartel boss after "
         "firefights leave 11 dead.", NAVY),
        ("MARKETS", "AI SELL-OFF SHAKES WALL ST",
         "The S&P 500 falls 3.7% in its worst week in 18 months; "
         "Nvidia drops 14%.", RED),
        ("INDONESIA", "FACTORY FIRE: DOZENS MISSING",
         "Rescuers recover 24 body bags after a factory fire; "
         "the search goes on for the missing.", NAVY),
    ]
    col_w = (W - 2 * m - 28) // 2
    row_h = 112
    for i, (kick, head, body, col) in enumerate(stories):
        cx = m + (i % 2) * (col_w + 28)
        cy = y + (i // 2) * row_h
        d.rectangle([(cx, cy + 3), (cx + 7, cy + 19)], fill=col)
        d.text((cx + 14, cy), kick, font=font(SANS_B, 16), fill=col)
        d.text((cx, cy + 24), head, font=font(SERIF, 24), fill=INK)
        para(d, cx, cy + 56, body, font(SERIF_REG, 18), col_w, 23)
    y += 2 * row_h + 4
    d.line([(m, y), (W - m, y)], fill=RULE, width=2)

    # ---- also today -------------------------------------------------
    y += 10
    d.text((m, y), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    y += 28
    y = para(d, m, y,
             "Nepal's PM Balendra Shah holds talks with PM Modi in "
             "New Delhi; South Korea's education minister quits over "
             "an AI exam-cheating scandal.",
             font(SERIF_REG, 19), W - 2 * m, 26, fill=INK)
    y += 8
    d.line([(m, y), (W - m, y)], fill=RULE, width=2)
    y += 8
    centred(d, W // 2, y,
            "Sources: AFP, Reuters, AP \u2014 23 November 2026",
            font(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
