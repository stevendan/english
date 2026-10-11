"""Build the 7 mp3 tracks of each unit from its .md, modelled on the Level 4 discs.

Usage: python tools/build_unit_audio.py <unit.md | level folder>

Needs: pip install edge-tts imageio-ffmpeg
Track layout per unit (position p = 0..3 inside its CD, track = 7p + k):
  1 Conversation        intro, context, full dialogue
  2 Speak Like a Native each sentence 3 times with a pause to repeat
  3 Repetition          each sentence + pause, whole dialogue twice
  4 Overlapping         dialogue twice (read along)
  5 Shadowing           dialogue twice (speak right after)
  6 Role Play           A's lines with B's turns left silent (twice), then the model
  7 Substitution Drill  number, letter, full substituted sentence, pause
File names follow Level 4: "1-01_U01-1_Conversation.mp3".
"""
import asyncio
import hashlib
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import edge_tts
import imageio_ffmpeg

sys.path.insert(0, str(Path(__file__).parent))
from build_unit_pdf import parse_unit, strip_markup  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RATE = 44100
CACHE = Path(tempfile.gettempdir()) / "speakup_tts_cache"
TTS_RATE = "-5%"

NARRATOR = "en-US-ChristopherNeural"
FEMALE_VOICES = ["en-US-AvaNeural", "en-US-EmmaNeural", "en-US-AriaNeural", "en-US-JennyNeural", "en-US-MichelleNeural"]
MALE_VOICES = ["en-US-AndrewNeural", "en-US-BrianNeural", "en-US-GuyNeural", "en-US-EricNeural",
               "en-US-RogerNeural", "en-US-SteffanNeural"]
FEMALE_NAMES = {"Emma", "Sarah", "Linh", "Anna", "Mai", "Yuki", "Phuong", "Hoa", "Olivia", "Ana", "Jisoo", "Lan",
                "Amy", "Kathy", "Tara", "Naomi",
                "Grace", "Trang", "Sophie", "Hannah", "Lily", "Julia", "Rachel", "Maria", "Lucy", "Nina", "Ella",
                "Zoe",  # Level 2
                "Kate", "Hien", "Fiona", "Lien", "Clara", "Kim", "Alice", "Ruby", "Diana", "Hanh", "Isabel",
                "Laura"}  # Level 3

SECTIONS = ["Conversation", "Speak Like a Native", "Repetition", "Overlapping", "Shadowing",
            "Role Play", "Substitution Drill"]


# ---------------------------------------------------------------- TTS clips

def clip_path(text, voice):
    key = hashlib.sha1(f"{voice}|{TTS_RATE}|{text}".encode()).hexdigest()[:16]
    return CACHE / f"{key}.wav"


async def synth(text, voice, sem):
    out = clip_path(text, voice)
    if out.exists():
        return
    async with sem:
        for attempt in range(4):
            try:
                mp3 = out.with_suffix(".mp3")
                await edge_tts.Communicate(text, voice, rate=TTS_RATE).save(str(mp3))
                trim = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                        "silenceremove=start_periods=1:start_threshold=-50dB,areverse")
                subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(mp3), "-af", trim,
                                "-ac", "1", "-ar", str(RATE), "-sample_fmt", "s16", str(out)], check=True)
                mp3.unlink()
                return
            except Exception as e:  # network hiccups: retry
                if attempt == 3:
                    raise RuntimeError(f"TTS failed for {text!r}: {e}")
                await asyncio.sleep(2 * (attempt + 1))


def duration(text, voice):
    with wave.open(str(clip_path(text, voice))) as w:
        return w.getnframes() / RATE


# ---------------------------------------------------------------- track scripts

class Track:
    """A timeline of ('say', text, voice) and ('gap', seconds) items."""

    def __init__(self):
        self.items = []

    def say(self, text, voice, gap=0.0):
        self.items.append(("say", text, voice))
        if gap:
            self.gap(gap)

    def gap(self, seconds):
        self.items.append(("gap", seconds))

    def clips(self):
        return [(i[1], i[2]) for i in self.items if i[0] == "say"]


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def fill(sentence, option):
    return re.sub(r"__(.+?)__", option, sentence)


def cast(d, unit_no):
    """Dialogue lines (markup stripped) and a voice per speaker, rotating voices across units."""
    conv = [(name, strip_markup(text)) for name, text in d["conversation"]["lines"]]
    f_i = m_i = unit_no - 1
    voices = {}
    for name in dict.fromkeys(n for n, _ in conv):
        if name in FEMALE_NAMES:
            voices[name] = FEMALE_VOICES[f_i % len(FEMALE_VOICES)]
            f_i += 1
        else:
            voices[name] = MALE_VOICES[m_i % len(MALE_VOICES)]
            m_i += 1
    return conv, voices


def timed_clips(d, unit_no):
    """Clips whose length sets a pause: dialogue turns and sentences, Speak sentences, drill sentences."""
    conv, voices = cast(d, unit_no)
    b_name = conv[1][0]
    clips = set()
    for name, text in conv:
        clips.add((text, voices[name]))
        clips.update((s, voices[name]) for s in sentences(text))
    for item in d["speak_like_a_native"]["items"]:
        who = next((n for n, text in conv if item["sentence"] in text), b_name)
        clips.add((item["sentence"], voices[who]))
    for item in d["substitution_drill"]["items"]:
        clips.update((strip_markup(fill(item["sentence"], o)), voices[b_name]) for o in item["options"])
    return clips


def build_tracks(d, unit_no):
    conv, voices = cast(d, unit_no)
    a_name, b_name = conv[0][0], conv[1][0]

    def intro(t, section, instruction=None):
        t.say(f"Unit {unit_no}.", NARRATOR, 0.9)
        t.say(f"{section}.", NARRATOR, 1.5)
        if instruction:
            t.say(instruction, NARRATOR, 1.5)

    def dialogue(t, pause_between=0.45):
        for name, text in conv:
            t.say(text, voices[name], pause_between)

    tracks = []

    t = Track()  # 1 Conversation
    intro(t, SECTIONS[0])
    t.say(d["conversation"]["context"], NARRATOR, 1.6)
    dialogue(t)
    t.gap(2.5)
    tracks.append(t)

    t = Track()  # 2 Speak Like a Native
    intro(t, SECTIONS[1], "Listen and repeat.")
    numbers = ["one", "two", "three"]
    for i, item in enumerate(d["speak_like_a_native"]["items"]):
        who = next((n for n, text in conv if item["sentence"] in text), b_name)
        t.say(f"Number {numbers[i]}.", NARRATOR, 1.5)
        for rep in range(3):
            t.say(item["sentence"], voices[who], None)
            t.gap(1.8 * duration(item["sentence"], voices[who]) + (0.4 if rep < 2 else 1.6))
    tracks.append(t)

    t = Track()  # 3 Repetition
    intro(t, SECTIONS[2], "Listen and repeat.")
    for _ in range(2):
        for name, text in conv:
            for s in sentences(text):
                t.say(s, voices[name])
                t.gap(1.7 * duration(s, voices[name]) + 0.6)
        t.gap(1.5)
    tracks.append(t)

    t = Track()  # 4 Overlapping
    intro(t, SECTIONS[3], "Read the text aloud, together with the speakers.")
    dialogue(t)
    t.gap(1.6)
    t.say("Once more.", NARRATOR, 1.2)
    dialogue(t)
    t.gap(2.5)
    tracks.append(t)

    t = Track()  # 5 Shadowing
    intro(t, SECTIONS[4], "Listen, and speak right after the speakers. Don't look at the text.")
    dialogue(t)
    t.gap(1.6)
    t.say("Once more.", NARRATOR, 1.2)
    dialogue(t)
    t.gap(2.5)
    tracks.append(t)

    t = Track()  # 6 Role Play
    intro(t, SECTIONS[5], "You are B. Say B's lines in the pauses.")
    for rnd in range(2):
        if rnd:
            t.say("Once more.", NARRATOR, 1.2)
        for name, text in conv:
            if name == a_name:
                t.say(text, voices[name], 0.3)
            else:
                t.gap(1.5 * duration(text, voices[name]) + 1.8)
        t.gap(1.0)
    t.say("Now, listen to the conversation.", NARRATOR, 1.2)
    dialogue(t)
    t.gap(2.5)
    tracks.append(t)

    t = Track()  # 7 Substitution Drill
    intro(t, SECTIONS[6], "Listen and repeat.")
    for i, item in enumerate(d["substitution_drill"]["items"]):
        t.say(f"Number {numbers[i]}.", NARRATOR, 1.2)
        for letter, opt in zip("ABC", item["options"]):
            s = strip_markup(fill(item["sentence"], opt))
            t.say(f"{letter}.", NARRATOR, 1.0)
            t.say(s, voices[b_name])
            t.gap(2.0 * duration(s, voices[b_name]) + 1.0)
    tracks.append(t)
    return tracks, voices


# ---------------------------------------------------------------- rendering

def render(track, out_mp3, tags):
    silence = lambda s: b"\x00\x00" * int(RATE * s)
    pcm = bytearray()
    for item in track.items:
        if item[0] == "gap":
            pcm += silence(item[1])
        else:
            with wave.open(str(clip_path(item[1], item[2]))) as w:
                pcm += w.readframes(w.getnframes())
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "track.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(bytes(pcm))
        meta = sum((["-metadata", f"{k}={v}"] for k, v in tags.items()), [])
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(wav), "-ac", "2", "-ar", str(RATE),
                        "-c:a", "libmp3lame", "-b:a", "128k", "-id3v2_version", "3", *meta, str(out_mp3)],
                       check=True)
    return len(pcm) / 2 / RATE


async def main(argv):
    target = Path(argv[0])
    files = sorted(target.glob("unit */unit *.md"), key=lambda p: int(re.findall(r"\d+", p.stem)[0])) \
        if target.is_dir() else [target]
    level = re.search(r"Level (\d+)", str(target.resolve())).group(1)
    CACHE.mkdir(exist_ok=True)
    sem = asyncio.Semaphore(4)

    for f in files:
        unit_no = int(re.findall(r"\d+", f.stem)[0])
        d = parse_unit(f)
        # Pauses depend on clip lengths, so synthesise the timed clips first, then the rest.
        await asyncio.gather(*(synth(t, v, sem) for t, v in timed_clips(d, unit_no)))
        tracks, voices = build_tracks(d, unit_no)
        await asyncio.gather(*(synth(t, v, sem) for tr in tracks for t, v in set(tr.clips())))

        disc, pos = (unit_no - 1) // 4 + 1, (unit_no - 1) % 4
        print(f"unit {unit_no}: voices {voices}")
        for k, (track, section) in enumerate(zip(tracks, SECTIONS), 1):
            no = 7 * pos + k
            name = f"{disc}-{no:02d}_U{unit_no:02d}-{k}_{section.replace(' ', '_')}.mp3"
            tags = {"title": f"{disc}-{no:02d} U{unit_no:02d}-{k} {section}",
                    "album": f"Speak Up English Enhanced Level {level} [Disc {disc}]",
                    "artist": "Speak Up English", "track": f"{no}/28", "disc": f"{disc}/3"}
            secs = render(track, f.parent / name, tags)
            print(f"   {name}  {secs:5.1f}s")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
