#!/usr/bin/env python3
"""Writes wallpaper.svg: a dusk harvest scene. Rendered to PNG with headless Chrome."""
import math
import random
import sys

W, H = 3024, 1964
random.seed(1126)
LEAF_COLORS = ["#E8863A", "#E9B949", "#C9562B", "#B5702C", "#D99A3E"]


def hill(base, amp, freq, phase):
    pts = [f"M0,{H}"]
    for x in range(0, W + 41, 40):
        y = base + amp * math.sin(x * freq + phase) + amp * 0.4 * math.sin(x * freq * 2.3 + phase * 1.7)
        pts.append(f"L{x},{y:.1f}")
    pts.append(f"L{W},{H}Z")
    return "".join(pts)


def hill_y(base, amp, freq, phase, x):
    return base + amp * math.sin(x * freq + phase) + amp * 0.4 * math.sin(x * freq * 2.3 + phase * 1.7)


def leaf(x, y, size, rot, color, opacity):
    path = "M0,-1 C.55,-.75 .75,-.2 .5,.25 C.35,.55 .15,.75 0,1 C-.15,.75 -.35,.55 -.5,.25 C-.75,-.2 -.55,-.75 0,-1Z"
    return (
        f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f}) scale({size:.0f})" opacity="{opacity:.2f}">'
        f'<path d="{path}" fill="{color}"/>'
        f'<path d="M0,-.8 L0,1.35" stroke="#241A14" stroke-opacity=".45" stroke-width=".05" fill="none"/></g>'
    )


def pumpkin(x, y, s):
    lobes = "".join(
        f'<ellipse cx="{dx * s:.0f}" cy="0" rx="{rx * s:.0f}" ry="{s * .78:.0f}" fill="{c}"/>'
        for dx, rx, c in [(-.72, .42, "#B85F24"), (.72, .42, "#B85F24"), (-.38, .46, "#CF7029"), (.38, .46, "#CF7029"), (0, .42, "#E8863A")]
    )
    stem = (
        f'<path d="M{-s * .09:.0f},{-s * .68:.0f} C{-s * .08:.0f},{-s * .95:.0f} {s * .02:.0f},{-s * 1.08:.0f} {s * .2:.0f},{-s * 1.12:.0f} '
        f'L{s * .24:.0f},{-s * .98:.0f} C{s * .12:.0f},{-s * .92:.0f} {s * .1:.0f},{-s * .8:.0f} {s * .1:.0f},{-s * .68:.0f}Z" fill="#4F4A2A"/>'
    )
    return f'<g transform="translate({x} {y})">{stem}{lobes}</g>'


def tree(x, y, s):
    return (
        f'<rect x="{x - s * .05:.0f}" y="{y - s * .5:.0f}" width="{s * .1:.0f}" height="{s * .55:.0f}" fill="#1C140F"/>'
        f'<circle cx="{x}" cy="{y - s * .75:.0f}" r="{s * .42:.0f}" fill="#1C140F"/>'
        f'<circle cx="{x - s * .28:.0f}" cy="{y - s * .55:.0f}" r="{s * .3:.0f}" fill="#1C140F"/>'
        f'<circle cx="{x + s * .28:.0f}" cy="{y - s * .55:.0f}" r="{s * .3:.0f}" fill="#1C140F"/>'
    )


far = (1340, 46, 0.0021, 0.6)
mid = (1500, 60, 0.0016, 2.4)
near = (1700, 44, 0.0013, 4.1)

trees = "".join(
    tree(x, hill_y(*mid, x) + 12, s)
    for x, s in [(240, 190), (390, 130), (2420, 170), (2560, 240), (2730, 150), (1080, 96)]
)
leaves = "".join(
    leaf(
        random.uniform(0, W),
        random.uniform(40, 1350) ** 1.0,
        random.uniform(16, 46),
        random.uniform(0, 360),
        random.choice(LEAF_COLORS),
        random.uniform(0.45, 0.95),
    )
    for _ in range(58)
)
ground_leaves = "".join(
    leaf(
        random.uniform(0, W),
        random.uniform(1760, 1950),
        random.uniform(12, 26),
        random.uniform(0, 360),
        random.choice(LEAF_COLORS),
        random.uniform(0.35, 0.75),
    )
    for _ in range(70)
)
pumpkins = (
    pumpkin(560, 1760, 92) + pumpkin(735, 1800, 62) + pumpkin(2140, 1790, 76)
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#1C140F"/><stop offset=".38" stop-color="#3A2418"/>
<stop offset=".6" stop-color="#8A4A22"/><stop offset=".74" stop-color="#E8863A"/>
</linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#F4CF74" stop-opacity=".75"/>
<stop offset=".35" stop-color="#E8863A" stop-opacity=".3"/><stop offset="1" stop-color="#E8863A" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<circle cx="1512" cy="1270" r="760" fill="url(#glow)"/>
<circle cx="1512" cy="1270" r="210" fill="#F4CF74"/>
<path d="{hill(*far)}" fill="#6A3A20"/>
<path d="{hill(*mid)}" fill="#3F2517"/>
{trees}
<path d="{hill(*near)}" fill="#241A14"/>
{pumpkins}
{ground_leaves}
{leaves}
</svg>"""

with open(sys.argv[1], "w") as f:
    f.write(svg)
