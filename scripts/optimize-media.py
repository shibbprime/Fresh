#!/usr/bin/env python3
"""Re-encode landing-page stills and hero loop from assets/source/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "source"
OUT = ROOT / "public" / "media"


def cover_crop(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    ratio = max(size[0] / im.width, size[1] / im.height)
    nw, nh = int(im.width * ratio), int(im.height * ratio)
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - size[0]) // 2
    top = (nh - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def save_webp(im: Image.Image, path: Path, size: tuple[int, int], quality: int, cover: bool = False) -> None:
    frame = cover_crop(im, size) if cover else im.copy()
    if not cover:
        frame.thumbnail(size, Image.Resampling.LANCZOS)
    frame.save(path, "WEBP", quality=quality, method=6)
    print(f"{path.name}: {path.stat().st_size} bytes")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    hero = SRC / "hero-home-dusk.jpg"
    if not hero.exists():
        print(f"Missing {hero}", file=sys.stderr)
        return 1

    hero_im = Image.open(hero).convert("RGB")
    save_webp(hero_im, OUT / "hero-poster.webp", (1600, 900), 68, cover=True)
    save_webp(hero_im, OUT / "hero-poster-sm.webp", (800, 450), 65, cover=True)

    ffmpeg_src = OUT / "hero-ffmpeg-src.jpg"
    cover_crop(hero_im, (1280, 720)).save(ffmpeg_src, "JPEG", quality=88, optimize=True)

    for name, size, q in [
        ("roof-detail.jpg", (1200, 900), 75),
        ("kitchen-remodel.jpg", (1200, 900), 75),
        ("siding-craft.jpg", (1200, 900), 75),
    ]:
        path = SRC / name
        if path.exists():
            save_webp(Image.open(path).convert("RGB"), OUT / path.with_suffix(".webp").name, size, q)

    vf = (
        "scale=960:540,zoompan=z='min(1.0+0.0018*on,1.12)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)-on*0.12':d=72:s=960x540:fps=18,format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(ffmpeg_src),
            "-vf",
            vf,
            "-t",
            "4",
            "-c:v",
            "libvpx-vp9",
            "-b:v",
            "0",
            "-crf",
            "40",
            "-row-mt",
            "1",
            "-an",
            str(OUT / "hero-loop.webm"),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(ffmpeg_src),
            "-vf",
            vf,
            "-t",
            "4",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "28",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-an",
            str(OUT / "hero-loop.mp4"),
        ],
        check=True,
    )
    print("hero loops refreshed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
