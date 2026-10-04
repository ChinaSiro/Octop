"""Android Chrome rejects a maskable icon that still has an alpha channel."""

from __future__ import annotations

import json
import struct
from pathlib import Path

_PUBLIC = Path(__file__).resolve().parents[3] / "dashboard" / "public"


def _png_color_type(path: Path) -> int:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height, _bit, color = struct.unpack(">IIBB", data[16:26])
    assert width > 0 and height > 0
    return color


def test_maskable_icons_are_opaque_rgb() -> None:
    manifest = json.loads((_PUBLIC / "manifest.json").read_text(encoding="utf-8"))
    maskable = [icon for icon in manifest["icons"] if icon.get("purpose") == "maskable"]
    assert maskable
    for icon in maskable:
        src = icon["src"].lstrip("/")
        path = _PUBLIC / src
        assert path.is_file(), src
        # color type 2 is RGB. Type 6 (RGBA) is what Android's WebAPK mint rejects
        # when the icon is declared maskable.
        assert _png_color_type(path) == 2, src
