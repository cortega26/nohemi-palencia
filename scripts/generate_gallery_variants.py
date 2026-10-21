#!/usr/bin/env python3
"""Build verifiable, non-generative WebP thumbnails for the documented originals.

Source-of-truth is data/obras.json. The two unverified catalog previews are
intentionally left untouched. Gallery derivatives never replace full-size artwork
images in metadata, detail pages or the zoom viewer.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'assets/obras/gallery'
WIDTHS = (480, 960)
QUALITY = 82


def generated_variants():
    works = json.loads((ROOT / 'data/obras.json').read_text('utf-8'))
    assert len(works) == 14
    for work in works:
        if not work.get('fuente_fotografia'):
            continue
        assert work['archivo'].endswith('-original-web.webp'), work['slug']
        source_path = ROOT / 'assets/obras' / work['archivo']
        assert source_path.is_file(), source_path
        with Image.open(source_path) as original:
            assert original.format == 'WEBP' and original.width > max(WIDTHS)
            assert original.mode in ('RGB', 'RGBA')
            for width in WIDTHS:
                height = round(original.height * width / original.width)
                smaller = original.resize((width, height), Image.Resampling.LANCZOS)
                dest = TARGET / f"{work['slug']}-{width}.webp"
                output = io.BytesIO()
                kwargs = {'format':'WEBP', 'quality':QUALITY, 'method':6}
                icc = original.info.get('icc_profile')
                if icc:
                    kwargs['icc_profile'] = icc
                smaller.save(output, **kwargs)
                content = output.getvalue()
                assert 4_000 < len(content) < source_path.stat().st_size, dest
                yield work['slug'], width, height, dest, content, source_path.stat().st_size


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true',
                        help='Check committed derivatives against their original image sources')
    args = parser.parse_args()
    count = 0
    original_bytes, tiny_bytes, retina_bytes = 0, 0, 0
    seen_sources = set()
    for slug, width, height, dest, encoded, source_bytes in generated_variants():
        if args.check:
            assert dest.is_file(), f'Missing generated image: {dest}'
            actual = dest.read_bytes()
            assert hashlib.sha256(actual).digest() == hashlib.sha256(encoded).digest(), f'Stale derivative: {dest}'
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(encoded)
        with Image.open(io.BytesIO(encoded)) as probe:
            assert probe.format == 'WEBP' and probe.size == (width, height)
        if slug not in seen_sources:
            original_bytes += source_bytes
            seen_sources.add(slug)
        if width == 480:
            tiny_bytes += len(encoded)
        else:
            retina_bytes += len(encoded)
        count += 1
        print(f'{slug}: {width} × {height}, {len(encoded):,} bytes', flush=True)
    assert count == 24 and len(seen_sources) == 12, 'Exactly 12 documented originals × 2 widths'
    print(f'SUMMARY originals={original_bytes:,} bytes; 480px={tiny_bytes:,} bytes; '
          f'960px={retina_bytes:,} bytes; verified={args.check}', flush=True)


if __name__ == '__main__':
    main()
