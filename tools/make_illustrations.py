"""Draws the stand-in illustrations used until real event photos arrive.
Usage: python3 tools/make_illustrations.py site/images/illustrations"""
import math, sys

MAROON, HALDI, MARIGOLD, LEAF, CREAM, BLUSH, INK, GOLD = "#9b1c2c", "#e3a514", "#e8742a", "#3d8a4b", "#fdf3d6", "#f4e3da", "#2a1418", "#c99a2e"

def svg(w, h, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'

def grad(id, a, b, vertical=True):
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'

def toran(w, y=0, n=None, sag=14):
    n = n or max(5, int(w / 38))
    out = [f'<path d="M0 {y+6}Q{w/2} {y+6+sag*2} {w} {y+6}" fill="none" stroke="{HALDI}" stroke-width="3"/>']
    for i in range(n):
        t = (i + .5) / n; x = w * t; yy = y + 6 + sag * 4 * t * (1 - t)
        rot = (t - .5) * -20
        out.append(f'<g transform="translate({x:.1f} {yy:.1f}) rotate({rot:.1f})"><path d="M0 0C8 7 7 19 0 27C-7 19 -8 7 0 0Z" fill="{LEAF}"/><path d="M0 3V23" stroke="#6fb07a" stroke-width="1.2"/></g>')
        out.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="5" fill="{MARIGOLD if i % 2 else HALDI}"/>')
    return "".join(out)

def marigold(x, y, r, c=MARIGOLD):
    petals = "".join(f'<circle cx="{x + r*.55*math.cos(a):.1f}" cy="{y + r*.55*math.sin(a):.1f}" r="{r*.5:.1f}" fill="{c}"/>' for a in [k * math.pi / 4 for k in range(8)])
    return petals + f'<circle cx="{x}" cy="{y}" r="{r*.45:.1f}" fill="{HALDI}"/><circle cx="{x}" cy="{y}" r="{r*.18:.1f}" fill="#b5531a"/>'

def lights(w, y, n, colors=(HALDI, "#fff3c4", MARIGOLD)):
    out = [f'<path d="M0 {y}Q{w/2} {y+30} {w} {y}" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width="1.5"/>']
    for i in range(n):
        t = (i + .5) / n; x = w * t; yy = y + 30 * 2 * t * (1 - t) * 1 + 4
        c = colors[i % len(colors)]
        out.append(f'<circle cx="{x:.1f}" cy="{yy+4:.1f}" r="9" fill="{c}" opacity=".25"/><circle cx="{x:.1f}" cy="{yy+4:.1f}" r="4" fill="{c}"/>')
    return "".join(out)

def food():
    b = [f'<defs>{grad("fbg", CREAM, BLUSH)}{grad("brass", "#f2c14e", "#b9801c")}</defs>',
         f'<rect width="400" height="300" fill="url(#fbg)"/>', lights(400, 18, 9),
         # counter
         f'<rect x="0" y="206" width="400" height="94" fill="{MAROON}"/><rect x="0" y="206" width="400" height="8" fill="{HALDI}"/>',
         f'<path d="M0 226h400" stroke="{HALDI}" stroke-width="2" stroke-dasharray="2 8"/>',
         # handi with steam
         '<path d="M58 140h84l-6 10c14 10 18 30 10 46-8 14-26 20-46 20s-38-6-46-20c-8-16-4-36 10-46Z" fill="url(#brass)"/>',
         f'<rect x="52" y="132" width="96" height="12" rx="6" fill="{GOLD}"/><circle cx="100" cy="126" r="7" fill="{GOLD}"/>',
         *[f'<path d="M{x} 118c-8-10 8-16 0-28" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>' for x in (86, 100, 114)],
         # banana leaf with rice and bowls
         f'<path d="M150 214C170 162 262 150 330 172C346 178 352 196 344 206Z" fill="{LEAF}"/><path d="M160 208C210 180 280 172 338 190" stroke="#6fb07a" stroke-width="2" fill="none"/>',
         '<ellipse cx="236" cy="190" rx="30" ry="14" fill="#fffaf0"/><ellipse cx="236" cy="184" rx="20" ry="9" fill="#fff"/>',
         *[f'<ellipse cx="{x}" cy="{y}" rx="14" ry="7" fill="{c}"/>' for x, y, c in ((190, 196, HALDI), (284, 186, MARIGOLD), (306, 196, "#fff7e6"), (268, 202, "#7cbf6a"))],
         # dosa on plate
         '<ellipse cx="344" cy="246" rx="44" ry="12" fill="#e9dfd4"/>',
         f'<path d="M306 244L382 238L344 196Z" fill="#e2a64a"/><path d="M314 242L372 237" stroke="#c4802a" stroke-width="2"/>',
    ]
    return svg(400, 300, "".join(b), "Illustration of a food counter with a brass handi, banana-leaf meal and dosa")

def stay():
    trees = "".join(f'<path d="M{x} {y}l{-s} {s*2.4}h{s*2}Z" fill="#1d3a2a"/><path d="M{x} {y+s*.9}l{-s*1.2} {s*2.6}h{s*2.4}Z" fill="#244a34"/>' for x, y, s in ((40, 120, 22), (82, 140, 18), (330, 110, 26), (372, 136, 20)))
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".8"/>' for x, y, r in ((40, 30, 1.5), (120, 50, 1), (210, 24, 1.6), (260, 60, 1), (360, 40, 1.4), (300, 18, 1)))
    b = [f'<defs>{grad("sky", "#24163a", MAROON)}</defs>', '<rect width="400" height="300" fill="url(#sky)"/>', stars,
         f'<circle cx="330" cy="58" r="22" fill="{CREAM}"/><circle cx="340" cy="52" r="20" fill="#3a1b3a"/>',
         trees, '<rect x="0" y="232" width="400" height="68" fill="#1b2e22"/>',
         # house
         f'<path d="M120 236V150l80-58 80 58v86Z" fill="{BLUSH}"/><path d="M106 156l94-70 94 70" fill="none" stroke="{MAROON}" stroke-width="12" stroke-linejoin="round"/>',
         *[f'<rect x="{x}" y="{y}" width="30" height="30" rx="3" fill="{HALDI}"/><path d="M{x+15} {y}v30M{x} {y+15}h30" stroke="{BLUSH}" stroke-width="3"/>' for x, y in ((138, 166), (232, 166))],
         f'<rect x="182" y="178" width="36" height="58" rx="18" fill="{MAROON}"/><circle cx="208" cy="208" r="3" fill="{HALDI}"/>',
         f'<g transform="translate(176 170) scale(.18)">{toran(270, 0, 6, 10)}</g>',
         # suitcase
         f'<rect x="262" y="214" width="42" height="30" rx="5" fill="{MARIGOLD}"/><path d="M274 214v-8h18v8" fill="none" stroke="{INK}" stroke-width="3"/><path d="M262 226h42" stroke="#b5531a" stroke-width="2"/>',
         '<path d="M0 244h400" stroke="#2c4a36" stroke-width="2"/>']
    return svg(400, 300, "".join(b), "Illustration of a cosy guest house among pine trees at night")

def haldi():
    petals = "".join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="3" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, c, r in ((40, 300, MARIGOLD, 20), (250, 330, HALDI, -30), (60, 360, HALDI, 60), (230, 250, MARIGOLD, 10), (40, 220, HALDI, -40), (270, 380, MARIGOLD, 30)))
    b = [f'<defs>{grad("hbg", "#ffd864", HALDI)}{grad("urli", "#f2c14e", "#a8701a")}</defs>', '<rect width="300" height="400" fill="url(#hbg)"/>',
         toran(300, 0, 7, 12), petals,
         '<ellipse cx="150" cy="268" rx="104" ry="26" fill="#a8701a" opacity=".35"/>',
         '<path d="M46 222h208c-6 40-48 62-104 62S52 262 46 222Z" fill="url(#urli)"/>',
         '<ellipse cx="150" cy="222" rx="104" ry="20" fill="#c98a1e"/><ellipse cx="150" cy="222" rx="92" ry="15" fill="#f0a020"/>',
         marigold(112, 218, 14), marigold(150, 224, 16, "#f2a81a"), marigold(190, 216, 13), marigold(132, 212, 9, "#ffcc33"),
         f'<path d="M206 196c18-30 46-30 52-50" fill="none" stroke="{LEAF}" stroke-width="4" stroke-linecap="round"/>',
         f'<path d="M258 146c-4 18-20 26-34 22 4-16 18-24 34-22Z" fill="{LEAF}"/>']
    return svg(300, 400, "".join(b), "Illustration of a brass bowl of turmeric with marigolds under a mango-leaf toran")

def sangeeth():
    notes = "".join(f'<g fill="{c}" transform="translate({x} {y}) rotate({r})"><ellipse cx="0" cy="14" rx="7" ry="5"/><rect x="5" y="-14" width="2.5" height="28"/><path d="M7.5 -14q10 4 8 14" fill="none" stroke="{c}" stroke-width="2.5"/></g>' for x, y, c, r in ((60, 120, HALDI, -10), (232, 100, "#f6b3c4", 12), (250, 190, HALDI, -6), (46, 210, "#f6b3c4", 8)))
    sparks = "".join(f'<path d="M{x} {y-6}L{x+1.5} {y-1.5}L{x+6} {y}L{x+1.5} {y+1.5}L{x} {y+6}L{x-1.5} {y+1.5}L{x-6} {y}L{x-1.5} {y-1.5}Z" fill="#fff3c4"/>' for x, y in ((100, 80), (200, 60), (270, 140), (30, 160), (150, 120)))
    b = [f'<defs>{grad("nbg", "#3a1950", "#7a3d8f")}{grad("drum", "#b42435", "#6e1220")}</defs>', '<rect width="300" height="400" fill="url(#nbg)"/>',
         lights(300, 12, 8), sparks, notes,
         '<ellipse cx="150" cy="352" rx="110" ry="18" fill="#000" opacity=".2"/>',
         '<g transform="translate(150 270) rotate(-12)">',
         '<rect x="-96" y="-56" width="192" height="112" rx="14" fill="url(#drum)"/>',
         f'<ellipse cx="-96" cy="0" rx="18" ry="56" fill="{CREAM}"/><ellipse cx="-96" cy="0" rx="12" ry="46" fill="#efe0c0"/>',
         f'<ellipse cx="96" cy="0" rx="18" ry="56" fill="{GOLD}"/>',
         f'<path d="M-84 -50L-50 50L-16 -50L18 50L52 -50L86 50" fill="none" stroke="{HALDI}" stroke-width="3"/>',
         f'<rect x="-96" y="-58" width="192" height="8" fill="{HALDI}"/><rect x="-96" y="50" width="192" height="8" fill="{HALDI}"/>',
         '</g>',
         f'<path d="M70 196L118 150" stroke="#e8c79a" stroke-width="6" stroke-linecap="round"/><path d="M214 250L262 214" stroke="#e8c79a" stroke-width="5" stroke-linecap="round"/>']
    return svg(300, 400, "".join(b), "Illustration of a dhol drum with music notes and string lights at night")

def vratham():
    def diya(x, y):
        return (f'<path d="M{x-26} {y}q26 22 52 0z" fill="{GOLD}"/><path d="M{x-26} {y}h52" stroke="#a8701a" stroke-width="3"/>'
                f'<path d="M{x} {y-34}c10 12 8 24 0 28c-8-4-10-16 0-28Z" fill="{MARIGOLD}"/><path d="M{x} {y-24}c4 6 4 12 0 15c-4-3-4-9 0-15Z" fill="#fff3c4"/>')
    leaves = "".join(f'<path d="M150 150c{dx} {-20} {dx*1.6} {-40} {dx*1.2} {-64}c{-dx*.8} {14} {-dx*1.1} {40} {-dx*1.2} {64}Z" fill="{LEAF}"/>' for dx in (-34, -18, 0.1, 18, 34))
    rang = "".join(f'<circle cx="150" cy="350" r="{r}" fill="none" stroke="{c}" stroke-width="4" stroke-dasharray="{d}"/>' for r, c, d in ((34, MAROON, "2 6"), (24, HALDI, "6 4"), (14, MARIGOLD, "3 3")))
    b = [f'<defs>{grad("vbg", "#e6f0f6", "#bcd6e6")}{grad("kal", "#f2c14e", "#a8701a")}</defs>', '<rect width="300" height="400" fill="url(#vbg)"/>',
         toran(300, 0, 7, 10), rang,
         '<ellipse cx="150" cy="306" rx="96" ry="14" fill="#1f5f8b" opacity=".18"/>',
         '<path d="M150 154c-56 0-78 50-62 100 10 30 34 46 62 46s52-16 62-46c16-50-6-100-62-100Z" fill="url(#kal)"/>',
         f'<rect x="112" y="150" width="76" height="14" rx="7" fill="{GOLD}"/><path d="M98 220h104" stroke="{MAROON}" stroke-width="6"/><path d="M98 232h104" stroke="{HALDI}" stroke-width="3"/>',
         f'<path d="M126 228l24 18 24-18" fill="none" stroke="{MAROON}" stroke-width="3"/>',
         leaves,
         '<ellipse cx="150" cy="104" rx="28" ry="34" fill="#8a5a2b"/><path d="M134 88c10-12 22-12 32 0" stroke="#6b4320" stroke-width="2" fill="none"/>',
         f'<path d="M126 114c16 8 32 8 48 0" stroke="{MAROON}" stroke-width="4" fill="none"/>',
         diya(56, 300), diya(244, 300)]
    return svg(300, 400, "".join(b), "Illustration of a kalash with mango leaves and coconut between two diyas")

def mandap():
    garl = "".join(f'<path d="M{x} 92v{l}" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1 9"/>' for x, l, c in ((96, 120, MARIGOLD), (124, 90, "#f6b3c4"), (276, 90, "#f6b3c4"), (304, 120, MARIGOLD), (200, 60, HALDI)))
    b = [f'<defs>{grad("mbg", BLUSH, "#f9efe3")}</defs>', '<rect width="400" height="500" fill="url(#mbg)"/>',
         f'<rect x="0" y="380" width="400" height="120" fill="#ead8cc"/><path d="M60 380h280l40 120H20Z" fill="#f6ede4"/>',
         f'<path d="M50 80h300v18H50Z" fill="{MAROON}"/><path d="M40 62h320l-10 22H50Z" fill="{HALDI}"/>',
         f'<path d="M50 98q37 30 75 0q37 30 75 0q37 30 75 0q37 30 75 0" fill="none" stroke="{LEAF}" stroke-width="6"/>',
         garl,
         *[f'<rect x="{x}" y="98" width="20" height="282" fill="{CREAM}"/><rect x="{x-4}" y="370" width="28" height="14" fill="{GOLD}"/><rect x="{x-4}" y="98" width="28" height="10" fill="{GOLD}"/>' for x in (54, 326)],
         f'<rect x="150" y="330" width="100" height="40" fill="{MAROON}"/><rect x="150" y="330" width="100" height="6" fill="{HALDI}"/>',
         f'<path d="M200 318c12 12 10 24 0 30c-10-6-12-18 0-30Z" fill="{MARIGOLD}"/><path d="M200 326c5 6 5 12 0 16c-5-4-5-10 0-16Z" fill="#fff3c4"/>',
         marigold(86, 380, 14), marigold(110, 388, 10, "#f6b3c4"), marigold(314, 380, 14), marigold(290, 388, 10, "#f6b3c4")]
    return svg(400, 500, "".join(b), "Illustration of a decorated wedding mandap with garlands")

def garlands():
    def ring(cx, cy, r, c1, c2):
        return "".join(f'<circle cx="{cx + r*math.cos(a):.1f}" cy="{cy + r*math.sin(a):.1f}" r="9" fill="{c1 if k % 2 else c2}"/>' for k, a in enumerate([j * 2 * math.pi / 30 for j in range(30)]))
    b = [f'<defs>{grad("gbg", MAROON, "#5e111b")}</defs>', '<rect width="400" height="500" fill="url(#gbg)"/>',
         toran(400, 0, 9, 14),
         ring(160, 270, 92, MARIGOLD, HALDI), ring(240, 270, 92, "#f6b3c4", "#fff7ef"),
         *[marigold(x, y, 10) for x, y in ((70, 430), (330, 440), (200, 120))]]
    return svg(400, 500, "".join(b), "Illustration of two interlinked wedding garlands")

def talambralu():
    def rnd(k):  # small deterministic scatter so the drawing never changes between runs
        return ((k * 9301 + 49297) % 233280) / 233280
    pts = []
    for k in range(140):
        a, r = rnd(k) * 2 * math.pi, math.sqrt(rnd(k + 500))
        pts.append((200 + 100 * r * math.cos(a), 304 + 26 * r * math.sin(a), int(rnd(k + 900) * 180), HALDI if k % 3 else "#fff"))
    grains = "".join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="3.5" ry="2" fill="{c}" transform="rotate({rot} {x:.1f} {y:.1f})"/>' for x, y, rot, c in pts)
    falling = "".join(f'<ellipse cx="{x}" cy="{y}" rx="3.5" ry="2" fill="{HALDI}" transform="rotate({r} {x} {y})"/>' for x, y, r in ((150, 150, 20), (220, 120, -30), (180, 200, 50), (250, 180, 10), (130, 220, -20), (270, 230, 40), (200, 240, 0)))
    b = [f'<defs>{grad("tbg", CREAM, "#f6dfa0")}{grad("plate", "#f2c14e", "#a8701a")}</defs>', '<rect width="400" height="500" fill="url(#tbg)"/>',
         toran(400, 0, 9, 14), falling,
         '<ellipse cx="200" cy="330" rx="140" ry="42" fill="#a8701a" opacity=".3"/>',
         '<ellipse cx="200" cy="310" rx="130" ry="40" fill="url(#plate)"/><ellipse cx="200" cy="304" rx="112" ry="32" fill="#e8b83a"/>',
         grains,
         *[marigold(x, y, 12) for x, y in ((112, 300), (288, 300))]]
    return svg(400, 500, "".join(b), "Illustration of a brass plate of talambralu rice")

def avatar(i):
    bgs = (BLUSH, CREAM, "#e3f0e4", "#f6e4e4", "#e6f0f6"); fgs = (MAROON, "#a8701a", LEAF, "#7a3d8f", "#1f5f8b")
    b = [f'<rect width="200" height="200" fill="{bgs[i]}"/>', f'<circle cx="100" cy="82" r="34" fill="{fgs[i]}"/>',
         f'<path d="M36 200c0-44 28-72 64-72s64 28 64 72Z" fill="{fgs[i]}"/>', f'<path d="M80 150l20 18 20-18" fill="none" stroke="{HALDI}" stroke-width="5" stroke-linejoin="round"/>']
    return svg(200, 200, "".join(b), "Illustration of a team member")

def birthday():
    balloons = "".join(f'<path d="M{x} {y+44}q-6 40 6 80" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width="1.5"/><ellipse cx="{x}" cy="{y}" rx="28" ry="34" fill="{c}"/><path d="M{x-4} {y+33}l4 9 4-9z" fill="{c}"/><ellipse cx="{x-9}" cy="{y-12}" rx="6" ry="9" fill="#fff" opacity=".35"/>' for x, y, c in ((70, 90, "#d6457a"), (128, 64, HALDI), (330, 84, "#3d8a4b"), (276, 60, "#7a3d8f")))
    confetti = "".join(f'<rect x="{x}" y="{y}" width="7" height="4" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, c, r in ((180, 40, MARIGOLD, 20), (220, 90, "#d6457a", -30), (40, 170, "#7a3d8f", 45), (360, 160, HALDI, 10), (200, 140, LEAF, 60), (250, 30, "#d6457a", 15)))
    b = [f'<defs>{grad("bbg", "#fdeef4", CREAM)}</defs>', '<rect width="400" height="300" fill="url(#bbg)"/>',
         f'<path d="M0 24l25 22 25-22 25 22 25-22 25 22 25-22 25 22 25-22 25 22 25-22 25 22 25-22 25 22 25-22 25 22 25-22" fill="none" stroke="{MAROON}" stroke-opacity=".25"/>',
         *[f'<path d="M{x} 24l12 0l-6 14z" fill="{c}"/>' for x, c in ((20, HALDI), (70, "#d6457a"), (120, LEAF), (170, MARIGOLD), (220, "#7a3d8f"), (270, HALDI), (320, "#d6457a"), (370, LEAF))],
         confetti, balloons,
         # play area: slide and blocks
         f'<rect x="0" y="248" width="400" height="52" fill="#f3dccf"/>',
         f'<path d="M24 248v-62h34v62" fill="none" stroke="{MARIGOLD}" stroke-width="6"/><path d="M58 190c30 6 50 30 64 58" fill="none" stroke="#7a3d8f" stroke-width="10" stroke-linecap="round"/><path d="M24 206h34M24 226h34" stroke="{MARIGOLD}" stroke-width="4"/>',
         *[f'<rect x="{x}" y="{y}" width="24" height="24" rx="3" fill="{c}"/>' for x, y, c in ((306, 224, HALDI), (332, 224, "#3d8a4b"), (319, 200, "#d6457a"))],
         # cake
         f'<rect x="164" y="212" width="80" height="36" rx="6" fill="{BLUSH}"/><rect x="164" y="212" width="80" height="10" rx="5" fill="#d6457a"/>',
         f'<rect x="174" y="184" width="60" height="30" rx="6" fill="#fff7ef"/><rect x="174" y="184" width="60" height="8" rx="4" fill="{HALDI}"/>',
         *[f'<rect x="{x}" y="166" width="5" height="18" fill="{c}"/><path d="M{x+2.5} 156c5 5 4 10 0 11c-4-1-5-6 0-11Z" fill="{MARIGOLD}"/>' for x, c in ((188, "#7a3d8f"), (202, "#3d8a4b"), (216, "#d6457a"))],
         f'<ellipse cx="204" cy="250" rx="54" ry="6" fill="{MAROON}" opacity=".15"/>']
    return svg(400, 300, "".join(b), "Illustration of a kids' birthday party with balloons, a cake and a play area")

def corporate():
    b = [f'<defs>{grad("cbg", "#1f2a3a", "#3c4a5a")}</defs>', '<rect width="400" height="300" fill="url(#cbg)"/>',
         lights(400, 14, 10, (HALDI, "#fff3c4")),
         # stage and screen
         f'<rect x="90" y="70" width="220" height="120" rx="6" fill="#fff" opacity=".1"/><rect x="100" y="80" width="200" height="100" rx="4" fill="{CREAM}"/>',
         f'<path d="M120 160l40-40 30 26 26-18 64 32" fill="none" stroke="{MAROON}" stroke-width="5" stroke-linejoin="round"/>',
         f'<circle cx="270" cy="104" r="12" fill="{HALDI}"/>',
         f'<rect x="40" y="200" width="320" height="22" fill="{MAROON}"/><rect x="40" y="200" width="320" height="5" fill="{HALDI}"/>',
         # podium
         f'<path d="M180 222l6-50h28l6 50z" fill="#2a3442"/><rect x="176" y="168" width="48" height="8" rx="2" fill="{GOLD}"/>',
         # audience
         *[f'<circle cx="{x}" cy="{y}" r="11" fill="#141c26"/><path d="M{x-16} {y+36}c0-18 7-24 16-24s16 6 16 24z" fill="#141c26"/>' for x, y in ((60, 250), (110, 256), (160, 250), (240, 250), (290, 256), (340, 250))],
         *[marigold(x, 222, 9) for x in (52, 348)]]
    return svg(400, 300, "".join(b), "Illustration of a corporate event stage with a screen, podium and audience")

out = sys.argv[1]
for name, fn in (("food", food), ("guest-stay", stay), ("haldi", haldi), ("sangeeth", sangeeth), ("vratham", vratham),
                 ("wedding-mandap", mandap), ("wedding-garlands", garlands), ("wedding-talambralu", talambralu),
                 ("birthday", birthday), ("corporate", corporate)):
    open(f"{out}/{name}.svg", "w").write(fn())
for i in range(5):
    open(f"{out}/team-{i+1}.svg", "w").write(avatar(i))
