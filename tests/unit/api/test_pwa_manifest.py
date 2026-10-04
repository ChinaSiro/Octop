"""Keep the rounded transparent logo. Do not declare it maskable.

Android Chrome prefers a maskable icon for the launcher. A maskable asset
has to be a full-bleed opaque square, which replaced the rounded mark with
a flat plate. Installability only requires purpose ``any`` icons.
"""

from __future__ import annotations

import json
import struct
from pathlib import Path

_PUBLIC = Path(__file__).resolve().parents[3] / "dashboard" / "public"


def _png_color_type(path: Path) -> int:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    _width, _height, _bit, color = struct.unpack(">IIBB", data[16:26])
    return color


def test_manifest_keeps_rounded_icons_and_skips_maskable() -> None:
    manifest = json.loads((_PUBLIC / "manifest.json").read_text(encoding="utf-8"))
    icons = manifest["icons"]
    assert all(icon.get("purpose") != "maskable" for icon in icons)
    by_src = {icon["src"]: icon for icon in icons}
    assert by_src["/pwa-192.png"]["purpose"] == "any"
    assert by_src["/pwa-512.png"]["purpose"] == "any"
    # Color type 6 is RGBA: the rounded corners stay transparent.
    assert _png_color_type(_PUBLIC / "pwa-192.png") == 6
    assert _png_color_type(_PUBLIC / "pwa-512.png") == 6
