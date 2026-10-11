"""Write timeline.json (start/end of every dialogue sentence) for the Repetition,
Overlapping and Shadowing tracks, so index.html can record and replay line by line.

Usage: python tools/build_timeline.py <level folder | unit.md> [...]
       python tools/build_timeline.py            (all levels)

Exact times come from the TTS clip cache that build_unit_audio.py renders from:
the track is the same list of clips and gaps, so adding their lengths up gives
where each sentence sits in the mp3. Clips missing from the cache (or a sum that
no longer matches the mp3) fall back to ffmpeg silencedetect on the mp3, matched
in order with the clips the track should contain.

Output, per unit folder:
  {"3": [[start, end, line, sentence, pass], ...], "4": [...], "5": [...]}
line = index into the conversation lines, sentence = index inside the line
(Repetition only, else 0), pass = 0 for the first read, 1 for "Once more".
Run tools/build_manifest.py afterwards to embed the timelines in content.js.
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_unit_audio as bua  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STEPS = (3, 4, 5)
TOLERANCE = 0.3  # seconds the summed timeline may differ from the mp3


DEFAULT_RATE, DEFAULT_FEMALE, DEFAULT_MALE = bua.TTS_RATE, bua.FEMALE_VOICES, bua.MALE_VOICES


def configure(level):
    """Same per-level voices and speed as build_unit_audio.main — they decide the cache keys."""
    bua.TTS_RATE = bua.LEVEL_TTS_RATE.get(level, DEFAULT_RATE)
    bua.FEMALE_VOICES, bua.MALE_VOICES = bua.LEVEL_VOICES.get(level, (DEFAULT_FEMALE, DEFAULT_MALE))


def expected(step, conv):
    """The dialogue clips a track reads, in order, as (text, line, sentence, pass)."""
    out = []
    for p in range(2):
        for li, (_, text) in enumerate(conv):
            if step == 3:
                out += [(s, li, si, p) for si, s in enumerate(bua.sentences(text))]
            else:
                out.append((text, li, 0, p))
    return out


def clip_len(text, voice):
    with wave.open(str(bua.clip_path(text, voice))) as w:
        return w.getnframes() / bua.RATE


def mp3_length(mp3):
    err = subprocess.run([bua.FFMPEG, "-hide_banner", "-i", str(mp3)], capture_output=True, encoding="utf-8", errors="replace").stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None


def from_cache(track):
    """[(start, end, text, voice)] for every 'say' item, or None if a clip is missing."""
    t, says = 0.0, []
    for item in track.items:
        if item[0] == "gap":
            t += item[1]
            continue
        if not bua.clip_path(item[1], item[2]).exists():
            return None
        d = clip_len(item[1], item[2])
        says.append((t, t + d, item[1], item[2]))
        t += d
    return says, t


def from_silence(track, mp3):
    """Speech spans found in the mp3, paired in order with the track's 'say' items."""
    err = subprocess.run([bua.FFMPEG, "-hide_banner", "-i", str(mp3), "-af",
                          "silencedetect=noise=-40dB:d=0.3", "-f", "null", "-"],
                         capture_output=True, encoding="utf-8", errors="replace").stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    total = mp3_length(mp3) or 0
    spans, cur = [], 0.0
    for s, e in zip(starts, ends + [total]):
        if s - cur > 0.05:
            spans.append((cur, s))
        cur = e
    if total - cur > 0.05:
        spans.append((cur, total))
    items = [i for i in track.items if i[0] == "say"]
    if len(spans) != len(items):
        return None
    return [(a, b, i[1], i[2]) for (a, b), i in zip(spans, items)]


def build_tracks(d, unit_no):
    """The unit's tracks; pause lengths need cached clips, else only the clip order is usable."""
    try:
        return bua.build_tracks(d, unit_no)[0], True
    except (FileNotFoundError, wave.Error):
        real = bua.duration
        bua.duration = lambda text, voice: 1.0
        try:
            return bua.build_tracks(d, unit_no)[0], False
        finally:
            bua.duration = real


def unit_timeline(md):
    unit_no = int(re.findall(r"\d+", md.stem)[0])
    d = bua.parse_unit(md)
    conv, _ = bua.cast(d, unit_no)
    tracks, timed = build_tracks(d, unit_no)
    result, notes = {}, []
    for step in STEPS:
        mp3s = list(md.parent.glob(f"*_U{unit_no:02d}-{step}_*.mp3"))
        if not mp3s:
            notes.append(f"step {step}: no mp3")
            continue
        mp3, track, says, how = mp3s[0], tracks[step - 1], None, "cache"
        got = from_cache(track) if timed else None
        if got:
            says, total = got
            real = mp3_length(mp3)
            if real is not None and abs(real - total) > TOLERANCE:
                says = None  # clips were re-synthesised since the mp3 was made
        if says is None:
            how = "silence"
            says = from_silence(track, mp3)
        if says is None:
            notes.append(f"step {step}: could not match speech spans, skipped")
            continue
        dialogue = [s for s in says if s[3] != bua.NARRATOR]
        exp = expected(step, conv)
        if len(dialogue) != len(exp) or any(a[2] != b[0] for a, b in zip(dialogue, exp)):
            notes.append(f"step {step}: clip order does not match the dialogue, skipped")
            continue
        result[str(step)] = [[round(a, 2), round(b, 2), li, si, p]
                             for (a, b, _, _), (_, li, si, p) in zip(dialogue, exp)]
        if how != "cache":
            notes.append(f"step {step}: {how}")
    return result, notes


def unit_files(target):
    target = Path(target)
    if target.is_file():
        return [target]
    if re.match(r"Level \d+$", target.name):
        return sorted(target.glob("unit */unit *.md"), key=lambda p: int(re.findall(r"\d+", p.stem)[0]))
    return [f for lv in sorted(target.glob("Level *"), key=lambda p: int(re.findall(r"\d+", p.name)[0]))
            for f in unit_files(lv)]


def main(argv):
    files = [f for a in (argv or [ROOT]) for f in unit_files(a)]
    for md in files:
        level = int(re.search(r"Level (\d+)", str(md.resolve())).group(1))
        configure(level)
        try:
            tl, notes = unit_timeline(md)
        except Exception as e:  # one broken unit must not stop the rest
            print(f"Level {level} {md.parent.name}: FAILED {e}")
            continue
        out = md.parent / "timeline.json"
        if tl:
            out.write_text(json.dumps(tl, separators=(",", ":")), encoding="utf-8")
        print(f"Level {level} {md.parent.name}: steps {','.join(tl) or '-'}" + (f"  ({'; '.join(notes)})" if notes else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
