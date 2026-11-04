"""Builds the V5 logo SVGs with text converted to paths, so they render the same everywhere.
Usage: python3 tools/make_logo.py <rozha-one.ttf> <martel-sans-800.ttf> <out-dir>"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

MAROON, HALDI, LEAF, IVORY = "#9b1c2c", "#e3a514", "#3d8a4b", "#fbfaf7"

def text_path(font, text, x, y, size, tracking=0.0, anchor="start"):
    """Return (svg path d, width) for text with its baseline at y."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    upm = font["head"].unitsPerEm
    s = size / upm
    names = [cmap[ord(c)] for c in text]
    width = sum(gs[n].width * s for n in names) + tracking * size * (len(text) - 1)
    if anchor == "middle":
        x -= width / 2
    pen = SVGPathPen(gs)
    cx = x
    for n in names:
        gs[n].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[n].width * s + tracking * size
    return pen.getCommands(), width

def leaf(x, y, l=17, w=6.2, rot=0):
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot})">'
            f'<path d="M0 0C{w} {l*.3:.1f} {w*.8:.1f} {l*.75:.1f} 0 {l}C{-w*.8:.1f} {l*.75:.1f} {-w} {l*.3:.1f} 0 0Z" fill="{LEAF}"/>'
            f'<path d="M0 2V{l-3}" stroke="#6fb07a" stroke-width="1"/></g>')

def mark(rozha, ox=0, oy=0, ring=True):
    """Round badge: maroon disc, haldi ring, a mango-leaf toran of five leaves (one per partner) and V5."""
    parts = [f'<g transform="translate({ox} {oy})">',
             f'<circle cx="60" cy="60" r="56" fill="{MAROON}"/>']
    if ring:
        parts.append(f'<circle cx="60" cy="60" r="50.5" fill="none" stroke="{HALDI}" stroke-width="2.2"/>')
    parts.append(f'<path d="M24 31Q60 47 96 31" fill="none" stroke="{HALDI}" stroke-width="2.4" stroke-linecap="round"/>')
    for i, t in enumerate([0.14, 0.32, 0.5, 0.68, 0.86]):
        x = 24 + 72 * t
        y = 31 + 32 * t * (1 - t)
        rot = (t - 0.5) * -24
        parts.append(leaf(x, y, rot=rot))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.3" fill="{HALDI}"/>')
    d, _ = text_path(rozha, "V5", 60, 96, 44, anchor="middle")
    parts.append(f'<path d="{d}" fill="{IVORY}"/>')
    parts.append('</g>')
    return "".join(parts)

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def main(rozha_path, martel_path, out):
    rozha, martel = TTFont(rozha_path), TTFont(martel_path)
    # Badge on its own: favicon, social avatar.
    open(f"{out}/mark.svg", "w").write(svg(120, 120, mark(rozha), "V5 Events"))
    # Horizontal lockups, for light and dark backgrounds.
    for name, word, sub in [("logo.svg", MAROON, "#6a5558"), ("logo-light.svg", IVORY, "#f2c14e")]:
        d1, w1 = text_path(rozha, "V5 Events", 138, 70, 54)
        d2, w2 = text_path(martel, "EVENT MANAGEMENT · SEATTLE", 140, 100, 13, tracking=0.16)
        width = int(max(138 + w1, 140 + w2) + 6)
        body = mark(rozha) + f'<path d="{d1}" fill="{word}"/><path d="{d2}" fill="{sub}"/>'
        open(f"{out}/{name}", "w").write(svg(width, 120, body, "V5 Events, event management, Seattle"))

if __name__ == "__main__":
    main(*sys.argv[1:4])
