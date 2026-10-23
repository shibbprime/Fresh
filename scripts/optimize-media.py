#!/usr/bin/env python3
"""Build responsive WebP/AVIF/JPEG variants from Blake's source stills. No metadata."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

try:
    import pillow_avif  # noqa: F401
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "source"
OUT = ROOT / "public" / "media"

HERO_WIDTHS = (640, 1280, 1920, 2560)
GALLERY_WIDTHS = (800, 1600)

HERO = [
    "hero-rosemount-outdoor-fireplace.jpg",
    "hero-mobile-rosemount-outdoor-fireplace.jpg",
]
LOOPS = [
    "loop-01-rosemount-outdoor-fireplace.jpg",
    "loop-02-rosemount-navy-kitchen.jpg",
    "loop-03-apple-valley-deck-aerial.jpg",
    "loop-04-farmington-four-season-porch.jpg",
    "loop-05-bloomington-open-kitchen.jpg",
]
GALLERY = [
    "gallery-rosemount-stone-fireplace.jpg",
    "gallery-lakeville-custom-cabinets.jpg",
    "gallery-apple-valley-constellation-coffee.jpg",
    "gallery-apple-valley-composite-deck.jpg",
    "gallery-burnsville-basement-wet-bar.jpg",
    "gallery-bloomington-walk-in-shower.jpg",
    "gallery-credit-river-navy-siding.jpg",
    "gallery-burnsville-home-theater.jpg",
    "gallery-apple-valley-roofing-aerial.jpg",
]


def strip_and_save(im: Image.Image, path: Path, fmt: str, **kwargs) -> int:
    clean = im.convert("RGB")
    # Drop any attached metadata by saving from a fresh RGB image.
    save_kw = {"optimize": True}
    save_kw.update(kwargs)
    if fmt == "JPEG":
        save_kw.setdefault("quality", 82)
        save_kw.setdefault("progressive", True)
        save_kw["exif"] = b""
    elif fmt == "WEBP":
        save_kw.setdefault("quality", 78)
        save_kw.setdefault("method", 6)
    elif fmt == "AVIF":
        save_kw.setdefault("quality", 55)
    clean.save(path, fmt, **save_kw)
    return path.stat().st_size


def resize_width(im: Image.Image, width: int) -> Image.Image:
    if im.width <= width:
        return im.copy()
    ratio = width / im.width
    height = max(1, round(im.height * ratio))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def emit_set(stem: str, source_name: str, widths: tuple[int, ...]) -> dict:
    path = SRC / source_name
    im = Image.open(path)
    im.load()
    # Cap widths to native size (Credit River max 1200, etc.)
    usable = [w for w in widths if w <= im.width]
    if not usable or usable[-1] != im.width:
        # Always include native width as the largest JPEG/WebP/AVIF
        native = im.width
        usable = sorted(set([w for w in widths if w < native] + [native]))

    sizes: dict[str, dict] = {"width": im.width, "height": im.height, "variants": {}}
    for w in usable:
        frame = resize_width(im, w)
        for fmt, ext, kw in (
            ("WEBP", "webp", {"quality": 78}),
            ("AVIF", "avif", {"quality": 52}),
            ("JPEG", "jpg", {"quality": 82, "progressive": True}),
        ):
            out = OUT / f"{stem}-{w}.{ext}"
            nbytes = strip_and_save(frame, out, fmt, **kw)
            sizes["variants"].setdefault(str(w), {})[ext] = nbytes
            print(f"{out.name}: {nbytes}")
    return sizes


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.iterdir():
        if old.is_file():
            old.unlink()

    report: dict = {}
    for name in HERO + LOOPS:
        stem = Path(name).stem
        report[stem] = emit_set(stem, name, HERO_WIDTHS)
    for name in GALLERY:
        stem = Path(name).stem
        # Credit River is already ≤1200 — keep widths ≤1200
        widths = GALLERY_WIDTHS
        if "credit-river" in name:
            widths = (800, 1200)
        report[stem] = emit_set(stem, name, widths)

    (OUT / "manifest-sizes.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Wrote public/media/manifest-sizes.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
