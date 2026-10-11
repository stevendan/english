"""Scan the Level folders and write content.js for index.html.

Usage:
  python tools/build_manifest.py

Browsers cannot list folders, so index.html reads this manifest to know which
levels, units, mp3 tracks, markdown and PDF files exist. The markdown text is
embedded too, so the page also works when opened straight from disk (file://),
where fetch() of local files is blocked. Re-run after adding or editing units.
"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content.js"


def num(path):
    m = re.search(r"\d+", path.name)
    return int(m.group()) if m else 0


def rel(path):
    return path.relative_to(ROOT).as_posix()


def track_info(mp3):
    # 2-15_U07-1_Conversation.mp3 -> track 15, step 1, "Conversation"
    m = re.match(r"^\d+-(\d+)_U\d+-(\d)_(.+)$", mp3.stem)
    if not m:
        return None
    return {"track": int(m.group(1)), "step": int(m.group(2)),
            "name": m.group(3).replace("_", " "), "file": rel(mp3)}


def scan_unit(folder):
    mds = sorted(folder.glob("*.md"))
    pdfs = sorted(folder.glob("*.pdf"))
    tracks = sorted(filter(None, (track_info(p) for p in folder.glob("*.mp3"))), key=lambda t: t["step"])
    return {
        "name": folder.name,
        "number": num(folder),
        "folder": rel(folder),
        "md": rel(mds[0]) if mds else None,
        "mdText": mds[0].read_text(encoding="utf-8") if mds else None,
        "pdf": rel(pdfs[0]) if pdfs else None,
        "tracks": tracks,
    }


def main():
    levels = []
    for level_dir in sorted((p for p in ROOT.glob("Level *") if p.is_dir()), key=num):
        units = [scan_unit(u) for u in sorted((p for p in level_dir.glob("unit *") if p.is_dir()), key=num)]
        if units:
            levels.append({"name": level_dir.name, "number": num(level_dir), "units": units})

    data = {"generated": datetime.now().isoformat(timespec="seconds"), "levels": levels}
    OUT.write_text("window.SPEAKUP_CONTENT = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    for lv in levels:
        with_md = sum(1 for u in lv["units"] if u["md"])
        print(f"{lv['name']}: {len(lv['units'])} units, {with_md} with markdown")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
