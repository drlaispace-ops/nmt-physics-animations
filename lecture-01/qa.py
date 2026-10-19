"""Контроль читабельності анімації.

    python qa.py <відео.mov> <аркуш.png> [кадрів=8]
        Витягує кадри рівномірно по ролику (+ останній), накладає їх на тло курсу
        і на сіре «живе відео», зменшує до 640×360 і складає контрольний аркуш.
    python qa.py --lint <сцена.py>
        Шукає в коді шрифти менші за 28 і смислові лінії тонші за 3.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (18, 24, 38)
FONT_PATH = str(Path.home() / "Library/Fonts/DejaVuSans.ttf")
CELL = (640, 360)


def duration(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def grab(video, t, dst, last=False):
    # Останній кадр беремо від кінця файлу: у коротких чернетках пошук за часом
    # іноді проскакує за кінець і ffmpeg не віддає жодного кадру.
    seek = ["-sseof", "-0.25"] if last else ["-ss", f"{t:.3f}"]
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", *seek, "-i", video,
         "-update", "1", "-frames:v", "1", "-pix_fmt", "rgba", dst],
        check=True,
    )
    return Image.open(dst).convert("RGBA")


def footage_plate(size):
    """Сіра градієнтна підкладка — замінник живого відео."""
    w, h = size
    plate = Image.new("RGBA", size)
    d = ImageDraw.Draw(plate)
    for x in range(w):
        v = int(70 + 90 * x / w)
        d.line([(x, 0), (x, h)], fill=(v, v - 6, v - 12, 255))
    return plate


def sheet(video, out, n=8):
    dur = duration(video)
    times = [dur * (i + 0.5) / n for i in range(n - 1)] + [max(dur - 0.05, 0)]
    font = ImageFont.truetype(FONT_PATH, 16)
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(times):
            fr = grab(video, t, f"{tmp}/f{i}.png", last=(i == len(times) - 1))
            on_bg = Image.new("RGBA", fr.size, BG + (255,))
            on_bg.alpha_composite(fr)
            on_ft = footage_plate(fr.size)
            on_ft.alpha_composite(fr)
            rows.append((t, on_bg.resize(CELL, Image.BICUBIC), on_ft.resize(CELL, Image.BICUBIC)))
    W = CELL[0] * 2 + 30
    H = (CELL[1] + 28) * len(rows) + 10
    img = Image.new("RGB", (W, H), (8, 10, 16))
    d = ImageDraw.Draw(img)
    y = 6
    for t, a, b in rows:
        d.text((10, y), f"{t:5.1f} с · 360p на тлі курсу | на «живому відео»", fill=(200, 200, 200), font=font)
        y += 22
        img.paste(a.convert("RGB"), (10, y))
        img.paste(b.convert("RGB"), (20 + CELL[0], y))
        y += CELL[1] + 6
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"аркуш: {out} ({len(rows)} кадрів, {dur:.1f} с)")


def lint(path):
    src = Path(path).read_text(encoding="utf-8")
    bad = []
    for n, line in enumerate(src.splitlines(), 1):
        for m in re.finditer(r"font_size\s*=\s*(\d+)", line):
            if int(m.group(1)) < 28:
                bad.append((n, f"font_size={m.group(1)}"))
        for m in re.finditer(r"\b[TL]\([^()]*?,\s*(\d+)\s*[,)]", line):
            if int(m.group(1)) < 28:
                bad.append((n, f"розмір {m.group(1)}"))
        for m in re.finditer(r"stroke_width\s*=\s*([\d.]+)", line):
            if 0 < float(m.group(1)) < 3 and "SW_GRID" not in line and "grid" not in line.lower():
                bad.append((n, f"stroke_width={m.group(1)} (лише для сітки)"))
        if "#6b7280" in line or re.search(r"\bMUTED\b(?!_)", line):
            bad.append((n, "колір MUTED — лише для декору, не для тексту"))
    for n, msg in bad:
        print(f"{path}:{n}: {msg}")
    print(f"lint: {len(bad)} зауважень")
    return len(bad)


if __name__ == "__main__":
    if sys.argv[1] == "--lint":
        sys.exit(1 if lint(sys.argv[2]) else 0)
    sheet(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
