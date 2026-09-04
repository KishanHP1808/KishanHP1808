from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
import os

# ============================================================
# SETTINGS
# ============================================================

WIDTH = 1400
HEIGHT = 500

FPS = 15
SKILL_SECONDS = 3

OUTPUT = "cyber_skill_banner.gif"

SKILLS = [
    "FRONTEND DEVELOPER",
    "AI & WEB DEVELOPER",
    "PYTHON DEVELOPER",
    "UI / UX DEVELOPER",
    "AI & ML",
    "PROBLEM SOLVER",
    "OPEN SOURCE"
]

# Center of the skill
TARGET_X = 800
TARGET_Y = 270


# ============================================================
# FONTS
# ============================================================

def get_font(size):
    paths = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/bahnschrift.ttf"
    ]

    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


SKILL_FONT = get_font(42)
HUD_FONT = get_font(15)
SMALL_FONT = get_font(12)


# ============================================================
# CYBER BACKGROUND
# ============================================================

def make_background(frame):

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (1, 4, 8)
    )

    draw = ImageDraw.Draw(image)

    # --------------------------------------------------------
    # DARK CYBER GRID
    # --------------------------------------------------------

    for x in range(0, WIDTH, 40):
        draw.line(
            [(x, 0), (x, HEIGHT)],
            fill=(4, 25, 32),
            width=1
        )

    for y in range(0, HEIGHT, 40):
        draw.line(
            [(0, y), (WIDTH, y)],
            fill=(4, 25, 32),
            width=1
        )

    # --------------------------------------------------------
    # FUTURISTIC BUILDINGS
    # --------------------------------------------------------

    random.seed(123)

    for x in range(0, WIDTH, 65):

        building_height = random.randint(
            70,
            210
        )

        building_width = random.randint(
            40,
            60
        )

        top = HEIGHT - building_height

        draw.rectangle(
            [
                x,
                top,
                x + building_width,
                HEIGHT
            ],
            fill=(3, 8, 13),
            outline=(7, 45, 55),
            width=1
        )

        # Windows

        for wy in range(
            top + 15,
            HEIGHT - 10,
            18
        ):

            for wx in range(
                x + 8,
                x + building_width - 5,
                14
            ):

                if random.random() < 0.25:

                    draw.rectangle(
                        [
                            wx,
                            wy,
                            wx + 3,
                            wy + 5
                        ],
                        fill=(0, 120, 145)
                    )

    # --------------------------------------------------------
    # HORIZON
    # --------------------------------------------------------

    draw.line(
        [(0, 350), (WIDTH, 350)],
        fill=(0, 100, 120),
        width=2
    )

    # --------------------------------------------------------
    # CYBER FLOOR
    # --------------------------------------------------------

    for y in range(365, HEIGHT, 20):

        draw.line(
            [(0, y), (WIDTH, y)],
            fill=(3, 30, 37),
            width=1
        )

    for x in range(-WIDTH, WIDTH * 2, 100):

        draw.line(
            [
                (TARGET_X, 350),
                (x, HEIGHT)
            ],
            fill=(3, 28, 35),
            width=1
        )

    # --------------------------------------------------------
    # TERMINAL PANELS
    # --------------------------------------------------------

    panels = [
        (25, 60, 290, 190),
        (1100, 65, 1370, 205),
        (25, 305, 300, 450),
        (1090, 310, 1370, 450)
    ]

    for x1, y1, x2, y2 in panels:

        draw.rectangle(
            [x1, y1, x2, y2],
            fill=(2, 7, 11),
            outline=(0, 70, 85),
            width=1
        )

        draw.rectangle(
            [x1, y1, x2, y1 + 22],
            fill=(3, 17, 22)
        )

        draw.text(
            [x1 + 8, y1 + 5],
            "SYSTEM://TERMINAL",
            font=SMALL_FONT,
            fill=(0, 190, 215)
        )

        random.seed(x1 + frame // 4)

        for line in range(7):

            text = ""

            for i in range(22):
                text += random.choice(
                    "01ABCDEF<>[]{}#$/"
                )

            draw.text(
                [
                    x1 + 8,
                    y1 + 34 + line * 16
                ],
                text,
                font=SMALL_FONT,
                fill=(0, 110, 100)
            )

    # --------------------------------------------------------
    # NETWORK NODES
    # --------------------------------------------------------

    random.seed(456)

    nodes = []

    for i in range(25):

        x = random.randint(320, 1080)
        y = random.randint(30, 450)

        nodes.append((x, y))

    for i in range(len(nodes) - 1):

        x1, y1 = nodes[i]
        x2, y2 = nodes[i + 1]

        if random.random() > 0.3:

            draw.line(
                [(x1, y1), (x2, y2)],
                fill=(0, 45, 55),
                width=1
            )

    for x, y in nodes:

        draw.ellipse(
            [
                x - 3,
                y - 3,
                x + 3,
                y + 3
            ],
            fill=(0, 190, 210)
        )

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    draw.rectangle(
        [340, 55, 465, 82],
        outline=(220, 35, 35),
        width=1
    )

    draw.text(
        [350, 61],
        "THREAT: ACTIVE",
        font=SMALL_FONT,
        fill=(255, 50, 50)
    )

    # --------------------------------------------------------
    # MOVING SCAN LINE
    # --------------------------------------------------------

    scan_y = (frame * 6) % HEIGHT

    draw.line(
        [(0, scan_y), (WIDTH, scan_y)],
        fill=(0, 70, 80),
        width=1
    )

    return image


# ============================================================
# HUD
# ============================================================

def draw_hud(draw):

    draw.text(
        [30, 25],
        "CYBER WARFIELD // ONLINE",
        font=HUD_FONT,
        fill=(0, 210, 235)
    )

    draw.text(
        [1160, 25],
        "TARGET LOCKED",
        font=HUD_FONT,
        fill=(0, 255, 120)
    )

    draw.text(
        [30, 470],
        "NEURAL NETWORK // ACTIVE",
        font=SMALL_FONT,
        fill=(0, 110, 125)
    )

    draw.text(
        [1180, 470],
        "SYSTEM 0x7F",
        font=SMALL_FONT,
        fill=(0, 110, 125)
    )

    # Target brackets

    s = 75

    draw.line(
        [
            (TARGET_X - s, TARGET_Y - s),
            (TARGET_X - 45, TARGET_Y - s)
        ],
        fill=(0, 190, 210),
        width=2
    )

    draw.line(
        [
            (TARGET_X - s, TARGET_Y - s),
            (TARGET_X - s, TARGET_Y - 45)
        ],
        fill=(0, 190, 210),
        width=2
    )

    draw.line(
        [
            (TARGET_X + s, TARGET_Y - s),
            (TARGET_X + 45, TARGET_Y - s)
        ],
        fill=(0, 190, 210),
        width=2
    )

    draw.line(
        [
            (TARGET_X + s, TARGET_Y - s),
            (TARGET_X + s, TARGET_Y - 45)
        ],
        fill=(0, 190, 210),
        width=2
    )


# ============================================================
# FUTURISTIC TACTICAL LAUNCHER
# ============================================================

def draw_launcher(draw, recoil=0):

    x = 35
    y = TARGET_Y + recoil

    # Main armored body

    draw.polygon(
        [
            (x, y - 25),
            (x + 65, y - 38),
            (x + 125, y - 30),
            (x + 160, y - 10),
            (x + 160, y + 12),
            (x + 120, y + 27),
            (x + 60, y + 30),
            (x, y + 18)
        ],
        fill=(7, 12, 17),
        outline=(65, 80, 85),
        width=2
    )

    # Upper rail

    draw.rectangle(
        [
            x + 20,
            y - 47,
            x + 110,
            y - 35
        ],
        fill=(8, 15, 20),
        outline=(0, 100, 120),
        width=1
    )

    # Front barrel

    draw.rectangle(
        [
            x + 145,
            y - 8,
            x + 205,
            y + 8
        ],
        fill=(10, 15, 18),
        outline=(65, 75, 78),
        width=2
    )

    # Energy chamber

    draw.ellipse(
        [
            x + 142,
            y - 17,
            x + 178,
            y + 17
        ],
        fill=(4, 9, 13),
        outline=(255, 100, 20),
        width=2
    )

    # Cyan core

    draw.ellipse(
        [
            x + 43,
            y - 10,
            x + 63,
            y + 10
        ],
        fill=(0, 210, 235)
    )

    # Grip

    draw.polygon(
        [
            (x + 70, y + 20),
            (x + 102, y + 18),
            (x + 112, y + 65),
            (x + 80, y + 68)
        ],
        fill=(5, 9, 13),
        outline=(45, 60, 65),
        width=2
    )

    # Tactical details

    draw.line(
        [
            (x + 15, y - 5),
            (x + 75, y - 5)
        ],
        fill=(0, 120, 135),
        width=2
    )

    draw.rectangle(
        [
            x + 20,
            y + 7,
            x + 35,
            y + 13
        ],
        fill=(255, 100, 20)
    )


# ============================================================
# MUZZLE ENERGY
# ============================================================

def draw_muzzle_flash(image, progress):

    layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    x = 240
    y = TARGET_Y

    strength = 1.0 - progress

    # Glow

    radius = int(55 * strength)

    if radius > 0:

        draw.ellipse(
            [
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ],
            fill=(255, 90, 10, 55)
        )

    # Energy cone

    length = int(110 * strength)

    draw.polygon(
        [
            (x, y - 14),
            (x + length, y),
            (x, y + 14)
        ],
        fill=(255, 125, 20, 180)
    )

    # Bright core

    draw.ellipse(
        [
            x - 12,
            y - 12,
            x + 18,
            y + 12
        ],
        fill=(255, 240, 180, 230)
    )

    layer = layer.filter(
        ImageFilter.GaussianBlur(4)
    )

    image = image.convert("RGBA")
    image.alpha_composite(layer)

    return image.convert("RGB")


# ============================================================
# PROJECTILE
# ============================================================

def draw_projectile(image, x, y):

    layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    # Long hot trail

    draw.line(
        [
            (x - 180, y),
            (x - 8, y)
        ],
        fill=(255, 80, 10, 45),
        width=22
    )

    draw.line(
        [
            (x - 140, y),
            (x - 8, y)
        ],
        fill=(255, 120, 20, 150),
        width=7
    )

    draw.line(
        [
            (x - 80, y),
            (x - 5, y)
        ],
        fill=(255, 240, 180, 230),
        width=3
    )

    # Glow

    draw.ellipse(
        [
            x - 22,
            y - 22,
            x + 22,
            y + 22
        ],
        fill=(255, 90, 10, 70)
    )

    layer = layer.filter(
        ImageFilter.GaussianBlur(5)
    )

    image = image.convert("RGBA")
    image.alpha_composite(layer)

    draw = ImageDraw.Draw(image)

    # Projectile core

    draw.ellipse(
        [
            x - 7,
            y - 7,
            x + 9,
            y + 7
        ],
        fill=(255, 245, 210, 255)
    )

    draw.ellipse(
        [
            x,
            y - 4,
            x + 14,
            y + 4
        ],
        fill=(255, 180, 40, 255)
    )

    return image.convert("RGB")


# ============================================================
# SKILL TEXT
# ============================================================

def draw_skill(image, skill, opacity=255):

    layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    box = draw.textbbox(
        (0, 0),
        skill,
        font=SKILL_FONT
    )

    text_width = box[2] - box[0]
    text_height = box[3] - box[1]

    x = TARGET_X - text_width // 2
    y = TARGET_Y - text_height // 2

    # Orange glow

    draw.text(
        (x, y),
        skill,
        font=SKILL_FONT,
        fill=(255, 90, 15, opacity)
    )

    glow = layer.filter(
        ImageFilter.GaussianBlur(12)
    )

    image = image.convert("RGBA")
    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)

    # Main text

    draw.text(
        (x, y),
        skill,
        font=SKILL_FONT,
        fill=(245, 245, 240, opacity),
        stroke_width=2,
        stroke_fill=(255, 120, 25, opacity)
    )

    # Burn mark underneath

    line_y = y + text_height + 12

    draw.line(
        [
            (x, line_y),
            (x + text_width, line_y)
        ],
        fill=(255, 110, 25, opacity),
        width=2
    )

    return image.convert("RGB")


# ============================================================
# IMPACT
# ============================================================

def draw_impact(image, frame):

    layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    progress = frame / 18.0

    # Flash

    radius = int(
        75 * (1.0 - progress)
    )

    if radius > 0:

        draw.ellipse(
            [
                TARGET_X - radius,
                TARGET_Y - radius,
                TARGET_X + radius,
                TARGET_Y + radius
            ],
            fill=(
                255,
                150,
                30,
                int(170 * (1.0 - progress))
            )
        )

    # Shockwave

    shock = int(
        10 + progress * 130
    )

    alpha = int(
        180 * (1.0 - progress)
    )

    if alpha > 0:

        draw.ellipse(
            [
                TARGET_X - shock,
                TARGET_Y - shock,
                TARGET_X + shock,
                TARGET_Y + shock
            ],
            outline=(
                255,
                110,
                20,
                alpha
            ),
            width=4
        )

    # Sparks

    random.seed(
        frame * 50
    )

    for i in range(55):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        distance = random.randint(
            15,
            130
        ) * progress

        x = (
            TARGET_X +
            math.cos(angle) * distance
        )

        y = (
            TARGET_Y +
            math.sin(angle) * distance
        )

        length = random.randint(
            3,
            12
        )

        draw.line(
            [
                (x, y),
                (
                    x + math.cos(angle) * length,
                    y + math.sin(angle) * length
                )
            ],
            fill=(
                255,
                random.randint(80, 220),
                25,
                230
            ),
            width=2
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(1)
    )

    image = image.convert("RGBA")
    image.alpha_composite(layer)

    return image.convert("RGB")


# ============================================================
# CREATE ANIMATION
# ============================================================

frames = []

print()
print("========================================")
print(" CYBER SKILL BANNER")
print("========================================")
print()

for number, skill in enumerate(SKILLS):

    print(
        f"[{number + 1}/{len(SKILLS)}] {skill}"
    )

    # ========================================================
    # 1. SHOW CURRENT SKILL FOR 3 SECONDS
    # ========================================================

    for frame in range(
        FPS * SKILL_SECONDS
    ):

        # FIXED:
        # cyber_background(frame)
        # was undefined.
        # The actual background function is make_background().
        image = make_background(frame)

        draw = ImageDraw.Draw(image)

        draw_hud(draw)
        draw_launcher(draw)

        image = draw_skill(
            image,
            skill
        )

        frames.append(image)

    # ========================================================
    # 2. FIRING FLASH
    # ========================================================

    for frame in range(7):

        image = make_background(frame)

        draw = ImageDraw.Draw(image)

        draw_hud(draw)

        draw_launcher(
            draw,
            recoil=-frame
        )

        image = draw_skill(
            image,
            skill
        )

        image = draw_muzzle_flash(
            image,
            frame / 7.0
        )

        frames.append(image)

    # ========================================================
    # 3. PROJECTILE TRAVELS TO CENTER
    # ========================================================

    travel_frames = 30

    for frame in range(
        travel_frames
    ):

        image = make_background(frame)

        draw = ImageDraw.Draw(image)

        draw_hud(draw)
        draw_launcher(draw)

        image = draw_skill(
            image,
            skill
        )

        progress = (
            frame /
            (travel_frames - 1)
        )

        bullet_x = (
            245 +
            (
                TARGET_X - 245
            ) * progress
        )

        image = draw_projectile(
            image,
            bullet_x,
            TARGET_Y
        )

        frames.append(image)

    # ========================================================
    # 4. IMPACT + ERASE OLD SKILL
    # ========================================================

    for frame in range(18):

        image = make_background(frame)

        draw = ImageDraw.Draw(image)

        draw_hud(draw)
        draw_launcher(draw)

        # Fade old skill

        opacity = int(
            255 *
            (
                1 -
                frame / 18.0
            )
        )

        if opacity > 0:

            image = draw_skill(
                image,
                skill,
                opacity
            )

        image = draw_impact(
            image,
            frame
        )

        frames.append(image)


# ============================================================
# SAVE
# ============================================================

print()
print("Saving GIF...")
print()

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True
)

print()
print("========================================")
print(" DONE")
print("========================================")
print()
print("File created:")
print(OUTPUT)
print()