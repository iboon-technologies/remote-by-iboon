"""
Renders every Remote by iBoon icon from one drawing, so they cannot drift.

    python res/iboon/make_icons.py

The mark: iboon-ui's brand pine (#0e6e5a) rounded square, a white monitor and
an upward arrow -- the same as TeamViewer by iBoon's favicon. It stands in
until an official `remote-by-iboon_logo.png` exists; replace draw() then.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BRAND = (14, 110, 90, 255)
WHITE = (255, 255, 255, 255)
SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0e6e5a"/><rect x="6.5" y="8" width="19" height="13" rx="2" fill="none" stroke="#fff" stroke-width="2"/><path d="M12 25h8M16 21v4" stroke="#fff" stroke-width="2" stroke-linecap="round"/><path d="M13 14.5l3-3 3 3M16 11.5v6" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
"""


def draw(size: int, background: bool = True) -> Image.Image:
    """The mark at `size`, drawn 4x larger and scaled down for clean edges."""
    s = size * 4
    u = s / 32  # one unit of the 32x32 SVG grid
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fg = WHITE if background else BRAND
    if background:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=8 * u, fill=BRAND)
    w = max(1, round(2 * u))
    # Monitor.
    d.rounded_rectangle([6.5 * u, 8 * u, 25.5 * u, 21 * u], radius=2 * u, outline=fg, width=w)
    # Stand.
    d.line([16 * u, 21 * u, 16 * u, 25 * u], fill=fg, width=w)
    d.line([12 * u, 25 * u, 20 * u, 25 * u], fill=fg, width=w)
    # Arrow up.
    aw = max(1, round(1.8 * u))
    d.line([16 * u, 11.5 * u, 16 * u, 17.5 * u], fill=fg, width=aw)
    d.line([13 * u, 14.5 * u, 16 * u, 11.5 * u, 19 * u, 14.5 * u], fill=fg, width=aw, joint="curve")
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    res = ROOT / "res"
    for name, size in [("icon.png", 1024), ("mac-icon.png", 1024), ("32x32.png", 32), ("64x64.png", 64),
                       ("128x128.png", 128), ("128x128@2x.png", 256)]:
        draw(size).save(res / name)
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    draw(256).save(res / "icon.ico", sizes=ico_sizes)
    draw(256).save(ROOT / "flutter/windows/runner/resources/app_icon.ico", sizes=ico_sizes)
    draw(64).save(res / "tray-icon.ico", sizes=[(16, 16), (24, 24), (32, 32)])
    # macOS menu-bar templates: the glyph alone, dark and light.
    draw(44, background=False).save(res / "mac-tray-dark-x2.png")
    draw(44, background=False).save(res / "mac-tray-light-x2.png")
    for svg in ["flutter/assets/icon.svg", "res/logo.svg", "res/logo-header.svg"]:
        (ROOT / svg).write_text(SVG, encoding="utf-8")
    print("icons written")


if __name__ == "__main__":
    main()
