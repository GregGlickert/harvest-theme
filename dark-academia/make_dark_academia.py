#!/usr/bin/env python3
"""Dark academia pixel art wallpaper: a candlelit library at night. Standard library only."""
import math
import random
import struct
import sys
import zlib

PROFILES = {
    # art width, art height, block size, output width, output height, scene shift
    "laptop": (378, 246, 8, 3024, 1964, 0),
    "ultrawide": (640, 270, 4, 2560, 1080, 131),
}
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "laptop"
W, H, SCALE, OUT_W, OUT_H, DX = PROFILES[PROFILE]
XMIN, XMAX = -DX, W - DX  # scene coordinates of the image's edges
random.seed(1891)


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


C = {k: hex_rgb(v) for k, v in dict(
    void="#0D0907", shelf_back="#150E0A", wood_d="#2A1A12", wood="#3F2618", wood_l="#5A3820", wood_h="#7A5030",
    wall="#1D2A24", wall_d="#151F1A", stone_d="#39342C", stone="#4D473B", stone_l="#62594A",
    ox_d="#3E1114", ox="#6A1C20", ox_l="#8A2A2B", forest="#23402F", forest_l="#316048", navy="#1F2D4A",
    navy_l="#2F4468", plum="#3E2240", umber="#5C3A1E", mustard="#A67C2D", gold="#D0A63A", brass="#A8812F",
    parch="#E2D1A9", parch_d="#B8A27A", ink="#2B2420", bone="#D9CDB0", bone_d="#9C8F74", lead="#0E0E14",
    sky_top="#0B1226", sky_mid="#16244A", sky_low="#2C3F6B", moon="#F2EBCB", moon_d="#CFC8A8", star="#CBD6EE",
    spire="#080A14", flame="#FFF3B0", flame_o="#FFB43E", flame_r="#E8642A", wax="#EFE6CE", wax_d="#C2B595",
    ocean="#2C6470", land="#B59A5C",
).items()}
BOOKS = ["ox", "ox_d", "forest", "forest_l", "navy", "navy_l", "plum", "umber", "mustard", "ink", "ox_l", "wood_l"]

fb = [[C["void"]] * W for _ in range(H)]
glow = [[False] * W for _ in range(H)]


def px(x, y, c, emissive=False):
    x += DX
    if 0 <= x < W and 0 <= y < H:
        fb[y][x] = C[c] if isinstance(c, str) else c
        glow[y][x] = emissive


def rect(x, y, w, h, c, emissive=False):
    for j in range(y, y + h):
        for i in range(x, x + w):
            px(i, j, c, emissive)


def sprite(x, y, rows, key):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != " ":
                px(x + i, y + j, key[ch])


def shade(c, f):
    return tuple(min(255, int(v * f)) for v in c)


SKULL = [
    "   #####   ", "  #######  ", " ######### ", " #########%", " #..##..##%", " #..##..##%",
    "  ####.##% ", "   ######% ", "   #.#.#%  ", "   #.#.#%  ",
]
SKULL_KEY = {"#": "bone", "%": "bone_d", ".": "void"}
HOURGLASS = ["#######", " %   % ", " %ooo% ", "  %o%  ", "   %   ", "  %o%  ", " %ooo% ", " ooooo ", "#######"]
HOURGLASS_KEY = {"#": "brass", "%": "parch_d", "o": "mustard"}
JAR = ["  ###  ", "  %%%  ", " %%%%% ", "%%%%%%%", "%ggggg%", "%ggggg%", "%ggggg%", " %%%%% "]
JAR_KEY = {"#": "wood_h", "%": "bone_d", "g": "forest_l"}


def book(x, base, w, h, name):
    c = C[name]
    rect(x, base - h, w, h, c)
    rect(x, base - h, 1, h, shade(c, 1.35))
    rect(x + w - 1, base - h, 1, h, shade(c, 0.6))
    style = random.random()
    if style < 0.55:
        rect(x + 1, base - h + 2, w - 2, 1, "gold")
        rect(x + 1, base - 4, w - 2, 1, "gold")
    if style < 0.25:
        rect(x + 1, base - h + 5, w - 2, 3, "parch_d")
    elif style < 0.45:
        rect(x + w // 2, base - h + 5, 1, h // 2, "gold")


def flat_stack(x, base, n):
    y = base
    for _ in range(n):
        w = random.randint(16, 24)
        c = C[random.choice(BOOKS)]
        rect(x + (24 - w) // 2, y - 4, w, 4, c)
        rect(x + (24 - w) // 2, y - 4, w, 1, shade(c, 1.3))
        rect(x + (24 - w) // 2 + 2, y - 3, 2, 2, "gold")
        y -= 4


def shelves(x0, x1):
    rect(x0, 12, x1 - x0, 178, "wood")
    rows = list(range(15, 186, 34))
    for top in rows[:-1]:
        bottom = top + 31
        rect(x0 + 3, top, x1 - x0 - 6, 31, "shelf_back")
        rect(x0 + 3, top, x1 - x0 - 6, 2, "void")
        rect(x0, bottom, x1 - x0, 3, "wood_l")
        rect(x0, bottom, x1 - x0, 1, "wood_h")
        x = x0 + 4
        while x < x1 - 8:
            roll = random.random()
            if roll < 0.06 and x < x1 - 30:
                flat_stack(x, bottom, random.randint(2, 4))
                x += 26
            elif roll < 0.11 and x < x1 - 20:
                kind = random.choice(["skull", "glass", "jar"])
                if kind == "skull":
                    sprite(x + 1, bottom - 10, SKULL, SKULL_KEY)
                elif kind == "glass":
                    sprite(x + 2, bottom - 9, HOURGLASS, HOURGLASS_KEY)
                else:
                    sprite(x + 2, bottom - 8, JAR, JAR_KEY)
                x += 15
            elif roll < 0.15:
                x += random.randint(3, 7)  # a gap where a book was borrowed
            else:
                w = random.randint(4, 8)
                w = min(w, x1 - 4 - x)
                book(x, bottom, w, random.randint(19, 28), random.choice(BOOKS))
                x += w
    rect(x0, 0, x1 - x0, 12, "wood_d")
    rect(x0, 180, x1 - x0, 10, "wood_d")


def inside_arch(x, y, cx, hw, spring, bottom):
    if y > bottom or abs(x - cx) > hw:
        return False
    if y >= spring:
        return True
    r = hw * 1.3
    off = r - hw
    return math.hypot(x - (cx - off), y - spring) <= r and math.hypot(x - (cx + off), y - spring) <= r


def window():
    cx, hw, spring, bottom = 189, 52, 92, 152
    for y in range(0, bottom + 7):
        for x in range(cx - hw - 8, cx + hw + 9):
            if inside_arch(x, y, cx, hw + 7, spring, bottom + 6):
                block = ((x + (y // 8) % 2 * 6) // 12 + y // 8) % 3
                px(x, y, ["stone_d", "stone", "stone_d"][block])
                if y % 8 == 0 or (x + (y // 8) % 2 * 6) % 12 == 0:
                    px(x, y, shade(C["stone_d"], 0.7))
    # Night sky, moon and stars
    for y in range(0, bottom + 1):
        t = y / bottom
        sky = C["sky_top"] if t < 0.35 else C["sky_mid"] if t < 0.75 else C["sky_low"]
        for x in range(cx - hw, cx + hw + 1):
            if inside_arch(x, y, cx, hw, spring, bottom):
                dither = t < 0.35 and t > 0.25 and (x + y) % 2 == 0
                px(x, y, C["sky_mid"] if dither else sky, True)
    for _ in range(70):
        x, y = random.randint(cx - hw, cx + hw), random.randint(20, 118)
        if inside_arch(x, y, cx, hw, spring, bottom):
            px(x, y, "star", True)
    mx, my, mr = 221, 76, 13
    for y in range(my - mr, my + mr + 1):
        for x in range(mx - mr, mx + mr + 1):
            if math.hypot(x - mx, y - my) <= mr:
                dark = math.hypot(x - mx + 4, y - my + 3) < 3.2 or math.hypot(x - mx - 5, y - my - 4) < 2.4 or x - mx + y - my > 12
                px(x, y, "moon_d" if dark else "moon", True)
    # Spires of the college beyond the glass
    for x in range(cx - hw, cx + hw + 1):
        height = 12 + int(4 * math.sin(x * 0.4))
        for y in range(bottom - height, bottom + 1):
            if inside_arch(x, y, cx, hw, spring, bottom):
                px(x, y, "spire", True)
    for sx, sh, sw in [(155, 42, 5), (168, 30, 4), (201, 36, 5), (222, 48, 6), (176, 24, 7)]:
        for k in range(sh):
            half = sw if k < sh * 0.6 else max(0, int(sw * (sh - k) / (sh * 0.4)))
            rect(sx - half, bottom - k, half * 2 + 1, 1, "spire", True)
    for wx, wy in [(153, 128), (156, 134), (221, 124), (224, 132), (200, 132), (175, 138)]:
        rect(wx, wy, 2, 3, "flame_o", True)
    # Leaded glass
    for y in range(0, bottom + 1):
        for x in range(cx - hw, cx + hw + 1):
            if inside_arch(x, y, cx, hw, spring, bottom):
                on_mullion = abs(x - cx) <= 1 or abs(abs(x - cx) - 26) <= 1
                on_lattice = y >= spring - 18 and y % 20 == 12
                if on_mullion or on_lattice:
                    px(x, y, "lead", True)
                elif not inside_arch(x, y, cx, hw - 1, spring, bottom):
                    px(x, y, "lead", True)
    for a in range(0, 720):
        t = math.radians(a / 2)
        for r, c in ((15, "lead"), (14, "lead"), (7, "lead")):
            px(int(cx + r * math.cos(t)), int(68 + r * math.sin(t)), c, True)
    for k in range(8):
        t = math.radians(k * 45)
        for r in range(7, 15):
            px(int(cx + r * math.cos(t)), int(68 + r * math.sin(t)), "lead", True)
    rect(cx - hw - 7, bottom + 1, hw * 2 + 15, 4, "stone_l")


def curtain(x0, x1, flip):
    width = x1 - x0
    for y in range(8, 170):
        sway = int(2 * math.sin(y * 0.09))
        tie = 1.0 - 0.45 * math.exp(-((y - 104) / 16) ** 2)  # gathered at the tie-back
        w = int(width * tie)
        for i in range(w):
            x = x1 - 1 - i + 0 if flip else x0 + i
            band = (i + sway) % 8
            c = "ox_d" if band in (0, 1) else "ox_l" if band == 4 else "ox"
            px(x, y, c)
    for i in range(int(width * 0.7)):
        x = x1 - 1 - i if flip else x0 + i
        rect(x, 101, 1, 5, "gold")
    rect(112, 6, 154, 3, "brass")
    rect(112, 5, 154, 1, "gold")


def room():
    rect(XMIN, 0, W, 190, "wall")
    for x in range(118, 261, 24):
        rect(x, 12, 1, 150, "wall_d")
    rect(XMIN, 0, W, 5, "wood_d")
    rect(XMIN, 5, W, 2, "wood_l")
    for x in range(XMIN, XMAX, 6):
        rect(x, 7, 3, 3, "wood")
    # Floorboards
    for y in range(190, H):
        row = (y - 190) // 7
        for x in range(XMIN, XMAX):
            seam = (x + row * 37) % 64 == 0 or (y - 190) % 7 == 0
            px(x, y, "wood_d" if seam else ("wood" if row % 2 else (50, 31, 20)))
    rect(XMIN, 190, W, 2, "void")


def rug():
    x0, y0, x1, y1 = 52, 208, 326, H
    rect(x0, y0, x1 - x0, y1 - y0, "ox_d")
    rect(x0 + 3, y0 + 3, x1 - x0 - 6, 1, "gold")
    rect(x0 + 3, y0 + 3, 1, H, "gold")
    rect(x1 - 4, y0 + 3, 1, H, "gold")
    for y in range(y0 + 8, H):
        for x in range(x0 + 8, x1 - 8):
            d = abs((x - x0) % 28 - 14) + abs((y - y0) % 20 - 10)
            if d == 7:
                px(x, y, "mustard")
            elif d < 4:
                px(x, y, "navy")
            elif d == 12:
                px(x, y, "ox")


def desk():
    x0, x1, top = 88, 290, 168
    for x in (x0 + 8, x1 - 56):
        rect(x, top + 7, 48, 44, "wood")
        rect(x, top + 7, 2, 44, "wood_l")
        rect(x + 46, top + 7, 2, 44, "wood_d")
        for k in range(3):
            y = top + 10 + k * 13
            rect(x + 4, y, 40, 11, "wood_l")
            rect(x + 4, y + 10, 40, 1, "wood_d")
            rect(x + 4, y, 40, 1, "wood_h")
            rect(x + 20, y + 5, 8, 2, "gold")
        rect(x - 1, top + 50, 50, 4, "wood_d")
    rect(x0 + 56, top + 7, x1 - x0 - 112, 22, "wood_d")
    rect(x0 + 56, top + 29, x1 - x0 - 112, 25, "void")
    rect(x0, top, x1 - x0, 7, "wood_l")
    rect(x0, top, x1 - x0, 1, "wood_h")
    rect(x0, top + 6, x1 - x0, 1, "wood_d")


def globe(cx, base):
    r = 11
    cy = base - 17
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if math.hypot(x - cx, y - cy) <= r:
                u, v = x - cx, y - cy
                land = (
                    ((u + 4) / 5) ** 2 + ((v + 4) / 4) ** 2 + 0.3 * math.sin(u * 1.3 + v) < 1
                    or ((u + 1) / 3) ** 2 + ((v - 5) / 4) ** 2 + 0.3 * math.sin(v * 1.5) < 1
                    or ((u - 6) / 4) ** 2 + ((v + 2) / 6) ** 2 + 0.3 * math.cos(u + v * 1.2) < 1
                )
                px(x, y, "land" if land else "ocean")
                if x - cx + y - cy > 11:
                    px(x, y, shade(C["land"] if land else C["ocean"], 0.6))
    for a in range(-110, 80):
        t = math.radians(a)
        px(int(cx + 13 * math.cos(t)), int(cy + 13 * math.sin(t)), "brass")
    rect(cx - 1, cy + 12, 3, 4, "brass")
    rect(cx - 7, base - 2, 15, 2, "brass")


def candle(cx, base):
    rect(cx - 8, base - 2, 17, 2, "brass")
    rect(cx - 6, base - 3, 13, 1, "gold")
    rect(cx - 1, base - 8, 3, 5, "brass")
    rect(cx - 4, base - 9, 9, 1, "gold")
    rect(cx - 2, base - 28, 5, 19, "wax")
    rect(cx + 2, base - 28, 1, 19, "wax_d")
    rect(cx + 3, base - 22, 1, 6, "wax")
    px(cx, base - 29, "ink")
    rect(cx - 2, base - 35, 5, 5, "flame_o", True)
    rect(cx - 1, base - 38, 3, 3, "flame_o", True)
    rect(cx, base - 41, 1, 3, "flame_o", True)
    rect(cx - 1, base - 34, 3, 3, "flame", True)
    rect(cx, base - 36, 1, 2, "flame", True)
    px(cx - 3, base - 32, "flame_r", True)
    px(cx + 3, base - 32, "flame_r", True)
    return cx, base - 33


def open_book(x, base):
    w = 62
    rect(x - 2, base - 2, w + 4, 2, "ox_d")
    for i in range(w):
        lift = int(3 * math.sin(math.pi * (i % 31) / 31))
        rect(x + i, base - 11 - lift, 1, 9 + lift, "parch")
        if i % 31 == 0 or i % 31 == 30:
            rect(x + i, base - 11 - lift, 1, 9 + lift, "parch_d")
    for row in range(5):
        y = base - 11 + row * 2
        for i in range(3, w - 3):
            if i % 31 > 3 and i % 31 < 28 and (i * 7 + row * 11) % 9:
                px(x + i, y, "ink")


def quill_and_ink(x, base):
    rect(x, base - 7, 9, 7, "ink")
    rect(x + 1, base - 6, 1, 4, (70, 80, 110))
    rect(x + 2, base - 10, 5, 3, "ink")
    rect(x + 1, base - 11, 7, 1, "brass")
    for k in range(20):
        fx, fy = x + 5 + k // 2, base - 11 - k
        px(fx, fy, "bone_d")
        if k > 5:
            spread = min(3, (k - 5) // 2, 20 - k)
            for s in range(1, spread + 1):
                px(fx - s, fy, "bone")
                px(fx + s, fy, "parch")


def desk_stack(x, base):
    y = base
    for name, w, off in [("ox", 42, 0), ("forest", 36, 3), ("navy_l", 39, 1), ("mustard", 30, 6)]:
        c = C[name]
        rect(x + off, y - 6, w, 6, c)
        rect(x + off, y - 6, w, 1, shade(c, 1.35))
        rect(x + off, y - 1, w, 1, shade(c, 0.6))
        rect(x + off + 3, y - 5, 1, 4, "gold")
        rect(x + off + w - 4, y - 5, 1, 4, "gold")
        rect(x + off + w // 2 - 5, y - 4, 10, 2, "parch_d")
        y -= 6
    sprite(x + 14, y - 10, SKULL, SKULL_KEY)


def papers(x, base):
    rect(x, base - 1, 24, 1, "parch")
    rect(x + 3, base - 2, 22, 1, "parch_d")


def armchair(cx, base):
    rect(cx - 22, base - 66, 44, 44, "forest")
    rect(cx - 20, base - 68, 40, 2, "forest_l")
    for bx in (-12, 0, 12):
        for by in (-58, -46, -34):
            px(cx + bx, base + by, "void")
            px(cx + bx + 6, base + by + 6, "void")
    for wing in (cx - 29, cx + 22):
        rect(wing, base - 60, 7, 26, "forest_l")
    for arm in (cx - 31, cx + 20):
        rect(arm, base - 36, 11, 28, "forest_l")
        rect(arm, base - 36, 11, 1, "bone_d")
        rect(arm + 2, base - 32, 7, 7, "forest")
        px(arm + 5, base - 29, "gold")
    rect(cx - 20, base - 28, 40, 8, "forest_l")
    rect(cx - 20, base - 28, 40, 1, "bone_d")
    rect(cx - 20, base - 20, 40, 12, "forest")
    for lx in (cx - 28, cx + 24):
        rect(lx, base - 8, 4, 8, "wood_d")


def floor_lamp(x, base):
    rect(x - 8, base - 2, 17, 2, "brass")
    rect(x, base - 84, 2, 82, "brass")
    for k in range(15):
        half = 7 + k * 2 // 3
        rect(x - half, base - 104 + k, half * 2 + 2, 1, "forest_l" if k % 5 else "forest")
    rect(x - 15, base - 89, 32, 2, "flame", True)
    LIGHTS.append((x, base - 84, 0.95, 40))


def side_table(x, base):
    rect(x - 13, base - 34, 26, 3, "wood_h")
    rect(x - 13, base - 34, 26, 1, "parch_d")
    rect(x - 1, base - 31, 3, 29, "wood_h")
    rect(x - 8, base - 2, 17, 2, "wood_h")
    rect(x - 11, base - 38, 16, 4, "ox")
    rect(x - 11, base - 38, 16, 1, "ox_l")
    rect(x + 6, base - 39, 5, 5, "bone")
    px(x + 11, base - 37, "bone")


def ladder(x, base):
    rect(XMAX - 131, 13, 131, 2, "brass")
    for k in range(base - 14):
        lean = k // 9
        px(x + lean, 14 + k, "parch_d")
        px(x + 1 + lean, 14 + k, "wood_h")
        px(x + 26 + lean, 14 + k, "parch_d")
        px(x + 27 + lean, 14 + k, "wood_h")
        if k % 15 == 8:
            rect(x + lean, 14 + k, 28, 2, "parch_d")


def sconce(x, y):
    rect(x - 1, y + 2, 3, 12, "brass")
    rect(x - 5, y, 11, 2, "gold")
    rect(x - 2, y - 12, 5, 12, "wax")
    rect(x - 1, y - 16, 3, 4, "flame_o", True)
    rect(x, y - 19, 1, 3, "flame_o", True)
    rect(x, y - 15, 1, 3, "flame", True)
    LIGHTS.append((x, y - 15, 0.9, 34))


def floor_books(x, base):
    for w, name, off in [(30, "navy", 0), (25, "ox", 2), (28, "mustard", 1)]:
        c = C[name]
        rect(x + off, base - 5, w, 5, c)
        rect(x + off, base - 5, w, 1, shade(c, 1.3))
        rect(x + off + 3, base - 4, 1, 3, "gold")
        base -= 5


def wide_extras():
    shelves(XMIN, 0)
    shelves(378, XMAX)
    floor_lamp(-34, 226)
    armchair(-74, 232)
    side_table(-14, 234)
    ladder(432, 228)
    sconce(378, 76)
    sconce(0, 76)
    floor_books(330, 224)


def light():
    """Candle and moonlight with ordered dithering, which gives the banded pixel art glow."""
    bayer = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    levels = 9
    for y in range(H):
        for x in range(W):
            if glow[y][x]:
                continue
            warm = sum(s / (1 + (math.hypot(x - DX - lx, (y - ly) * 1.1) / r) ** 2) for lx, ly, s, r in LIGHTS)
            cool = 0.32 / (1 + (math.hypot(x - DX - 189, y - 95) / 75) ** 2)
            edge = math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2))
            base = 0.42 * (1 - 0.45 * max(0.0, edge - 0.45))
            value = base + warm + cool
            value = math.floor(value * levels + bayer[y % 4][x % 4] / 16) / levels
            warm_share = warm / (warm + cool + base)
            r, g, b = fb[y][x]
            c = (
                r * value * (1 + 0.16 * warm_share),
                g * value * (1 - 0.02 * warm_share),
                b * value * (1 - 0.28 * warm_share + 0.18 * cool / (cool + 0.3)),
            )
            fb[y][x] = tuple(min(255, int(round(v / 6) * 6)) for v in c)


def motes():
    fx, fy = FLAME
    for _ in range(26):
        t, r = random.uniform(0, math.tau), random.uniform(12, 70)
        i, j = int(fx + r * math.cos(t)), int(fy + r * math.sin(t) * 0.8)
        if 0 <= i + DX < W and 0 <= j < H and not glow[j][i + DX]:  # keep them out of the night sky
            px(i, j, "flame_o" if r < 40 else (150, 105, 60), True)


def save_png(path):
    rows = bytearray()
    for y in range(OUT_H):
        art_y = y // SCALE
        line = bytearray([0])
        for x in range(W):
            line += bytes(fb[art_y][x]) * SCALE
        rows += line

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", OUT_W, OUT_H, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(rows), 9)))
        f.write(chunk(b"IEND", b""))


room()
shelves(0, 118)
shelves(260, W)
window()
curtain(112, 136, False)
curtain(242, 266, True)
rug()
desk()
TOP = 168
globe(106, TOP)
FLAME = candle(136, TOP)
LIGHTS = [(*FLAME, 1.25, 42)]
open_book(158, TOP)
quill_and_ink(224, TOP)
desk_stack(240, TOP)
papers(146, TOP)
if PROFILE == "ultrawide":
    wide_extras()
light()
motes()
save_png(f"dark-academia-{OUT_W}x{OUT_H}.png")
