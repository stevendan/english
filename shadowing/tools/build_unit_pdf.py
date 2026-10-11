"""Check and build 1-page A4 unit PDFs in the Speak Up English layout.

Usage:
  python tools/build_unit_pdf.py <unit.md | level folder> [--check]

A unit .md follows the 6-block template ([HEADER], [1] … [6]). For each unit the
script validates the template rules, then writes <unit>.pdf next to the .md
(unless --check is given).

Inline markup:
  **text**   bold (grammar point in Conversation / Study Notes headline)
  [[text]]   blue bold grammar keyword (Grammar Focus examples)
  __text__   replaced part in Substitution Drill
  ________   Role Play blank
  ‿          linking mark
"""
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph, Spacer, Table, TableStyle

FONT_DIR = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Arial", FONT_DIR + "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_DIR + "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", FONT_DIR + "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", FONT_DIR + "arialbi.ttf"))
pdfmetrics.registerFont(TTFont("Tahoma", FONT_DIR + "tahoma.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                              italic="Arial-Italic", boldItalic="Arial-BoldItalic")

TEAL = HexColor("#7BA7AF")
TIP_BG = HexColor("#DCE9F7")
TRACK = "#F7D774"
BLUE = "#2E5597"
LIGHT_BLUE = "#3C78D8"
ORANGE = "#E07B00"
GREY = "#9A9A9A"
GREEN = "#3A9D5D"
LABEL_COLORS = {"smooth": BLUE, "linking": BLUE, "change": BLUE, "weak": GREY, "strong": ORANGE}
LABELS = tuple(LABEL_COLORS)

BASE = 8.8
S = {
    "body": ParagraphStyle("body", fontName="Arial", fontSize=BASE, leading=BASE * 1.32),
    "italic": ParagraphStyle("italic", fontName="Arial-Italic", fontSize=BASE - 0.4, leading=BASE * 1.28),
    "bold": ParagraphStyle("bold", fontName="Arial-Bold", fontSize=BASE + 0.4, leading=BASE * 1.4),
    "label": ParagraphStyle("label", fontName="Arial", fontSize=BASE - 0.4, leading=BASE * 1.25, leftIndent=10),
    "indent": ParagraphStyle("indent", fontName="Arial", fontSize=BASE, leading=BASE * 1.38, leftIndent=12),
    "tip": ParagraphStyle("tip", fontName="Arial", fontSize=BASE - 0.5, leading=BASE * 1.25),
    "header": ParagraphStyle("header", fontName="Arial-Bold", fontSize=BASE + 0.2, leading=BASE * 1.3, textColor=white),
}


# ---------------------------------------------------------------- parsing

def strip_markup(text):
    return re.sub(r"\*\*|\[\[|\]\]|(?<!_)__(?!_)", "", text)


def split_groups(lines):
    groups, cur = [], []
    for line in lines:
        if line.strip():
            cur.append(line.strip())
        elif cur:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def track_of(header_line):
    return header_line.split("—")[-1].strip() if "—" in header_line else ""


def parse_unit(path):
    text = Path(path).read_text(encoding="utf-8")
    blocks, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^\[(HEADER|[1-6])\]\s*(.*)$", line.strip())
        if m:
            current = m.group(1)
            blocks[current] = {"head": m.group(2), "lines": []}
        elif current:
            blocks[current]["lines"].append(line)

    missing = [k for k in ("HEADER", "1", "2", "3", "4", "5", "6") if k not in blocks]
    if missing:
        raise ValueError(f"missing blocks: {missing}")

    unit_label, cd_label = [p.strip() for p in blocks["HEADER"]["head"].split("—")]
    data = {"unit_label": unit_label, "cd_label": cd_label}

    conv_lines = [l.strip() for l in blocks["1"]["lines"] if l.strip()]
    data["conversation"] = {
        "track": track_of(blocks["1"]["head"]),
        "context": conv_lines[0],
        "lines": [tuple(p.strip() for p in l.split(":", 1)) for l in conv_lines[1:]],
    }

    items, tip, in_tip = [], [], False
    for line in blocks["2"]["lines"]:
        s = line.strip()
        if not s:
            continue
        if s == "[MẸO PHÁT ÂM]":
            in_tip = True
        elif in_tip:
            tip.append(s)
        elif re.match(r"^\d+\.\s", s):
            items.append({"sentence": re.sub(r"^\d+\.\s*", "", s), "labels": [], "note": []})
        elif s.split(":", 1)[0] in LABELS:
            k, v = s.split(":", 1)
            items[-1]["labels"].append((k, v.strip()))
        else:
            items[-1]["note"].append(s)
    for it in items:
        it["note"] = " ".join(it["note"])
    data["speak_like_a_native"] = {"track": track_of(blocks["2"]["head"]), "items": items, "tip": tip}

    data["study_notes"] = [{"en": strip_markup(g[0]), "vi": g[1], "explain": g[2:]}
                           for g in split_groups(blocks["3"]["lines"])]
    data["grammar_focus"] = [{"title": g[0], "explain": g[1], "examples": g[2:]}
                             for g in split_groups(blocks["4"]["lines"])]

    data["role_play"] = {
        "track": track_of(blocks["5"]["head"]),
        "lines": [tuple(p.strip() for p in l.split(":", 1)) for l in blocks["5"]["lines"] if l.strip()],
    }

    sd_items = []
    for line in blocks["6"]["lines"]:
        s = line.strip()
        if re.match(r"^\d+\.\s", s):
            sd_items.append({"sentence": re.sub(r"^\d+\.\s*", "", s), "options": []})
        elif re.match(r"^[abc]\.\s", s):
            sd_items[-1]["options"].append(s[3:].strip())
    data["substitution_drill"] = {"track": track_of(blocks["6"]["head"]), "items": sd_items}
    return data


# ---------------------------------------------------------------- checks

def words(text):
    return [w for w in re.split(r"\s+", strip_markup(text)) if re.search(r"[A-Za-z0-9]", w)]


def check_unit(d, max_turn_words=6):
    problems = []
    conv = d["conversation"]["lines"]
    plain = [strip_markup(t) for _, t in conv]
    speakers = [n for n, _ in conv]
    b_name = speakers[1] if len(speakers) > 1 else None

    if len(conv) != 4:
        problems.append(f"Conversation has {len(conv)} turns (expected 4)")
    counts = [len(words(t)) for _, t in conv]
    for (name, t), n in zip(conv, counts):
        if not 3 <= n <= max_turn_words:
            problems.append(f"Turn '{name}: {strip_markup(t)}' has {n} words (3–{max_turn_words})")
    if not 20 <= sum(counts) <= 30:
        problems.append(f"Conversation total {sum(counts)} words (20–30)")
    bolds = sum(len(re.findall(r"\*\*.+?\*\*", t)) for _, t in conv)
    if bolds < 3:
        problems.append(f"Grammar point bold only {bolds} times (≥3)")

    sln = d["speak_like_a_native"]["items"]
    if len(sln) != 3:
        problems.append(f"Speak Like a Native has {len(sln)} sentences (expected 3)")
    for it in sln:
        if not any(it["sentence"] in p for p in plain):
            problems.append(f"Speak sentence not verbatim: {it['sentence']}")
    if not 3 <= len(d["speak_like_a_native"]["tip"]) <= 5:
        problems.append("MẸO PHÁT ÂM should have 3–5 sentences")

    if len(d["study_notes"]) != 2:
        problems.append(f"Study Notes has {len(d['study_notes'])} items (expected 2)")
    for gf in d["grammar_focus"]:
        if not 2 <= len(gf["examples"]) <= 3:
            problems.append(f"Grammar '{gf['title']}' has {len(gf['examples'])} examples (2–3)")
        for ex in gf["examples"]:
            for part in re.split(r"\s+[–-]\s+", ex):
                if len(words(part)) > 7:
                    problems.append(f"Grammar example over 7 words: {ex}")
            if strip_markup(ex) in " ".join(plain):
                problems.append(f"Grammar example copied from dialogue: {ex}")

    sd = d["substitution_drill"]["items"]
    originals = []
    for it in sd:
        m = re.search(r"__(.+?)__", it["sentence"])
        originals.append(m.group(1) if m else "")
        full = strip_markup(it["sentence"])
        if not any(full in strip_markup(t) for n, t in conv if n == b_name):
            problems.append(f"Drill sentence not in B's lines: {full}")
        if len(it["options"]) != 3:
            problems.append(f"Drill '{full}' has {len(it['options'])} options")
        for opt in it["options"]:
            if not 1 <= len(words(opt)) <= 3:
                problems.append(f"Drill option not 1–3 words: {opt}")
    if len(sd) != 3:
        problems.append(f"Substitution Drill has {len(sd)} sentences (expected 3)")

    rp = d["role_play"]["lines"]
    blanks = sum(t.count("________") for _, t in rp)
    if blanks != 3:
        problems.append(f"Role Play has {blanks} blanks (expected 3)")
    fill = iter(originals)
    for i, ((who, t), conv_text) in enumerate(zip(rp, plain)):
        expected_who = "A" if i % 2 == 0 else "B"
        if who != expected_who:
            problems.append(f"Role Play line {i + 1} speaker {who} (expected {expected_who})")
        if who == "A" and "________" in t:
            problems.append("Role Play blank in A's line")
        rebuilt = re.sub(r"_{4,}", lambda m: next(fill, "?"), t)
        if rebuilt != conv_text:
            problems.append(f"Role Play line {i + 1} ≠ Conversation: '{rebuilt}' vs '{conv_text}'")
    return problems, counts


# ---------------------------------------------------------------- rendering

def md(text):
    """Inline markup → reportlab paragraph XML."""
    t = escape(text)
    t = re.sub(r"\[\[(.+?)\]\]", rf"<font color='{BLUE}'><b>\1</b></font>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"_{4,}", "\x00", t)
    t = re.sub(r"__(.+?)__", rf"<u><b><font color='{GREEN}'>\1</font></b></u>", t)
    t = t.replace("\x00", f"<font color='{GREEN}'>{'_' * 14}</font>")
    return t.replace("‿", "<font name='Tahoma'>‿</font>")


def X(xml, style="body"):
    return Paragraph(xml, S[style])


def P(text, style="body"):
    return X(md(text), style)


def highlight(sentence, labels):
    """Colour the phrases named in the labels: blue for smooth/linking/change, orange for strong, grey for weak."""
    colors, prio = [None] * len(sentence), [0] * len(sentence)
    for kind, value in labels:
        rank = 2 if kind in ("weak", "strong") else 1
        for phrase in re.findall(r"“([^”]+)”", value):
            pattern = r"(?<!\w)" + re.escape(phrase.replace("‿", " ")) + r"(?!\w)"
            for m in re.finditer(pattern, sentence, re.I):
                for i in range(m.start(), m.end()):
                    if rank >= prio[i]:
                        colors[i], prio[i] = LABEL_COLORS[kind], rank
    out, i = [], 0
    while i < len(sentence):
        j = i
        while j < len(sentence) and colors[j] == colors[i]:
            j += 1
        chunk = escape(sentence[i:j])
        out.append(f"<font color='{colors[i]}'>{chunk}</font>" if colors[i] else chunk)
        i = j
    return "".join(out)


def bar(title, track, width):
    right = ParagraphStyle("r", parent=S["header"], alignment=2, fontName="Arial")
    t = Table([[X(escape(title), "header"), Paragraph(f"<font color='{TRACK}'>{escape(track)}</font>", right)]],
              colWidths=[width * 0.6, width * 0.4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [t, Spacer(1, 6)]


def dialogue(lines, width, name_w):
    t = Table([[P(who + ":"), P(say)] for who, say in lines], colWidths=[name_w, width - name_w])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
    ]))
    return t


def tip_box(lines, width):
    t = Table([[[P("• " + line, "tip") for line in lines]]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TIP_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def build(d, out_path, title):
    page_w, page_h = A4
    margin_x, margin_top, margin_bottom = 15 * mm, 13 * mm, 11 * mm
    gutter = 9 * mm
    col_w = (page_w - 2 * margin_x - gutter) / 2
    name_w = max(pdfmetrics.stringWidth(n + ":", "Arial", BASE) for n, _ in d["conversation"]["lines"]) + 8

    # Band 1: Conversation | Study Notes
    conv = d["conversation"]
    b1_left = bar("Conversation", conv["track"], col_w) + [
        X(f"<i>{escape(conv['context'])}</i>"), Spacer(1, 5), dialogue(conv["lines"], col_w, name_w)]
    b1_right = bar("Study Notes", "", col_w)
    for note in d["study_notes"]:
        b1_right += [X(f"<b>{escape(note['en'])}</b>"), X(f"<font color='{LIGHT_BLUE}'>{md(note['vi'])}</font>")]
        b1_right += [P(line, "italic") for line in note["explain"]] + [Spacer(1, 7)]

    # Band 2: Speak Like a Native | Grammar Focus
    sln = d["speak_like_a_native"]
    b2_left = bar("Speak Like a Native", sln["track"], col_w)
    for i, it in enumerate(sln["items"], 1):
        b2_left += [X(f"{i}. {highlight(it['sentence'], it['labels'])}", "bold"), Spacer(1, 1)]
        b2_left += [X(f"<font color='{LABEL_COLORS[k]}'><i>{k}:</i></font> {md(v)}", "label") for k, v in it["labels"]]
        b2_left += [Spacer(1, 2), P(it["note"]), Spacer(1, 7)]
    b2_left += [tip_box(sln["tip"], col_w)]
    b2_right = bar("Grammar Focus", "", col_w)
    for sec in d["grammar_focus"]:
        b2_right += [X(f"<font color='{GREEN}'><b>{escape(sec['title'])}</b></font>"), Spacer(1, 2),
                     P(sec["explain"], "italic"), Spacer(1, 5)]
        b2_right += [P(ex, "indent") for ex in sec["examples"]] + [Spacer(1, 6)]

    # Band 3: Role Play | Substitution Drill
    rp = d["role_play"]
    b3_left = bar("Role Play", rp["track"], col_w) + [dialogue(rp["lines"], col_w, 20)]
    sd = d["substitution_drill"]
    b3_right = bar("Substitution Drill", sd["track"], col_w)
    for i, it in enumerate(sd["items"], 1):
        b3_right += [X(f"{i}.&nbsp;&nbsp;{md(it['sentence'])}")]
        b3_right += [X(f"<b>{letter}.</b> {md(opt)}", "indent") for letter, opt in zip("abc", it["options"])]
        b3_right += [Spacer(1, 6)]

    c = canvas.Canvas(str(out_path), pagesize=A4)
    c.setTitle(title)
    c.setFont("Arial-Bold", 10)
    c.drawString(margin_x, page_h - margin_top + 3, d["unit_label"])
    c.setFont("Arial", 10)
    c.drawRightString(margin_x + col_w, page_h - margin_top + 3, d["cd_label"])

    def height(story):
        return sum(f.wrapOn(c, col_w, page_h)[1] for f in story)

    bands = [(b1_left, b1_right), (b2_left, b2_right), (b3_left, b3_right)]
    heights = [max(height(l), height(r)) for l, r in bands]
    band_gap = 10
    available = page_h - margin_top - 2 - margin_bottom
    needed = sum(heights) + band_gap * (len(bands) - 1)
    if needed > available:
        raise ValueError(f"content is {needed - available:.0f}pt too tall for one page")

    y = page_h - margin_top - 2
    for (left, right), h in zip(bands, heights):
        for x, story in ((margin_x, left), (margin_x + col_w + gutter, right)):
            frame = Frame(x, y - h - 1, col_w, h + 1, leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0)
            frame.addFromList(story, c)
            if story:
                raise ValueError("a block did not fit in its frame")
        y -= h + band_gap
    c.save()


def main(argv):
    check_only = "--check" in argv
    target = Path(next(a for a in argv if not a.startswith("--")))
    files = sorted(target.glob("unit */unit *.md"), key=lambda p: int(re.findall(r"\d+", p.stem)[0])) \
        if target.is_dir() else [target]
    level = re.search(r"Level \d+", str(target.resolve()))
    failed = False
    for f in files:
        d = parse_unit(f)
        problems, counts = check_unit(d)
        status = "OK" if not problems else f"{len(problems)} problem(s)"
        print(f"{f.name}: words/turn {counts} = {sum(counts)} — {status}")
        for p in problems:
            print("   -", p)
        failed |= bool(problems)
        if not check_only:
            title = f"Speak Up English - {level.group(0) if level else ''} - {d['unit_label']}"
            try:
                build(d, f.with_suffix(".pdf"), title)
                print("   wrote", f.with_suffix(".pdf"))
            except (ValueError, OSError) as e:
                print("   PDF NOT written:", e)
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
