"""Embed md/Unit*.md into content.js for index.html.

Usage:
  python tools/build_content.py

When index.html is opened straight from disk (file://), browsers block fetch()
of local files, so the page reads the markdown embedded here instead.
Re-run after adding or editing units.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content.js"


def main():
    units = {}
    for md in ROOT.glob("md/Unit*.md"):
        m = re.fullmatch(r"Unit(\d+)", md.stem)
        if m:
            units[int(m.group(1))] = md.read_text(encoding="utf-8")
    data = {str(n): units[n] for n in sorted(units)}
    OUT.write_text("window.HOTEL_CONTENT = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"embedded {len(data)} units, wrote {OUT}")


if __name__ == "__main__":
    main()
