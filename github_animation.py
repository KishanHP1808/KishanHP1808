from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# ============================================================
# CONFIGURATION
# ============================================================

WIDTH = 1400
HEIGHT = 500
FPS = 30

BG = (3, 4, 7)
WHITE = (245, 255, 245)
GREEN = (163, 230, 53)
BRIGHT_GREEN = (210, 255, 120)

NAME = "KISHAN H.P."

ROLES = [
    "FRONTEND DEVELOPER",
    "AI & WEB DEVELOPER",
    "PYTHON DEVELOPER",
    "UI/UX DEVELOPER",
    "PROBLEM SOLVER"
]

# Reproducible random effects
random.seed(42)


# ============================================================
# FONTS
# ============================================================

def load_font(size, bold=False):

    if bold:
        paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf"
        ]
    else:
        paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf"
        ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass

    return ImageFont.load_default()


NAME_FONT = load_font(52, True)
ROLE_FONT = load_font(46, True)
SMALL_FONT = load_font(18)


# ============================================================
# TEXT HELPERS
# ============================================================

def centered_text(draw, text, y, font, fill):

    box = draw.textbbox((0, 0), text, font=font)

    width = box[2] - box[0]

    x = (WIDTH - width) // 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )

    return x, width


# ============================================================
# BACKGROUND
# ============================================================

def draw_background(draw):

    # Very subtle horizontal scan lines
    for y in range(0, HEIGHT, 8):

        draw.line(
            [(0, y), (WIDTH, y)],
            fill=(8, 11, 12),
            width=1
        )

    # Tiny stars / particles
    random.seed(123)

    for _ in range(80):

        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        draw.ellipse(
            [x, y, x + 1, y + 1],
            fill=(20, 30, 20)
        )


# ============================================================
# GLOW FUNCTION
# ============================================================

def add_glow(base, objects, blur=15):

    glow = Image.new(
        "RGBA",
        base.size,
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    for obj in objects:
        obj(glow_draw)

    glow = glow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    base.alpha_composite(glow)


# ============================================================
# MUZZLE FLASH
# ============================================================

def draw_muzzle_flash(layer, x, y, strength):

    draw = ImageDraw.Draw(layer)

    # Large radial flash
    radius = int(45 * strength)

    for r in range(radius, 5, -5):

        alpha = int(
            120 * strength *
            (1 - r / max(radius, 1))
        )

        draw.ellipse(
            [
                x - r,
                y - r,
                x + r,
                y + r
            ],
            fill=(200, 255, 100, alpha)
        )

    # Horizontal flash rays
    for angle in [-0.35, -0.15, 0, 0.15, 0.35]:

        length = random.randint(50, 120) * strength

        x2 = x + math.cos(angle) * length
        y2 = y + math.sin(angle) * length

        draw.line(
            [(x, y), (x2, y2)],
            fill=(230, 255, 150, 230),
            width=random.randint(3, 7)
        )


# ============================================================
# BULLET
# ============================================================

def draw_bullet(layer, x, y, scale=1):

    draw = ImageDraw.Draw(layer)

    # Bullet glow
    glow_radius = int(25 * scale)

    draw.ellipse(
        [
            x - glow_radius,
            y - glow_radius,
            x + glow_radius,
            y + glow_radius
        ],
        fill=(150, 240, 50, 80)
    )

    # Bullet body
    r = int(9 * scale)

    draw.ellipse(
        [
            x - r,
            y - r,
            x + r,
            y + r
        ],
        fill=(245, 255, 220, 255)
    )

    # Bullet nose
    tip = int(22 * scale)

    draw.polygon(
        [
            (x + r, y),
            (x + r + tip, y - int(6 * scale)),
            (x + r + tip, y + int(6 * scale))
        ],
        fill=(163, 230, 53, 255)
    )


# ============================================================
# BULLET TRAIL
# ============================================================

def draw_trail(layer, x, y, length):

    draw = ImageDraw.Draw(layer)

    # Main tracer
    draw.line(
        [
            (x - length, y),
            (x - 15, y)
        ],
        fill=(163, 230, 53, 220),
        width=5
    )

    # Bright center
    draw.line(
        [
            (x - length,
             y),
            (x - 15,
             y)
        ],
        fill=(220, 255, 130, 230),
        width=2
    )

    # Random sparks
    for _ in range(12):

        sx = random.randint(
            int(x - length),
            int(x)
        )

        sy = y + random.randint(-15, 15)

        draw.ellipse(
            [
                sx,
                sy,
                sx + 2,
                sy + 2
            ],
            fill=(180, 255, 70, 180)
        )


# ============================================================
# IMPACT EXPLOSION
# ============================================================

def draw_impact(layer, x, y, frame):

    draw = ImageDraw.Draw(layer)

    progress = frame / 14

    radius = int(
        15 + progress * 75
    )

    # Shockwave ring
    draw.ellipse(
        [
            x - radius,
            y - radius,
            x + radius,
            y + radius
        ],
        outline=(170, 255, 70, 180),
        width=4
    )

    # Explosion rays
    for i in range(30):

        angle = (
            i / 30
        ) * math.pi * 2

        length = random.randint(
            30,
            100
        ) * progress

        x1 = x + math.cos(angle) * 10
        y1 = y + math.sin(angle) * 10

        x2 = x + math.cos(angle) * length
        y2 = y + math.sin(angle) * length

        draw.line(
            [
                (x1, y1),
                (x2, y2)
            ],
            fill=(190, 255, 80, 220),
            width=random.randint(2, 5)
        )


# ============================================================
# SPARKS
# ============================================================

def draw_sparks(layer, x, y, frame):

    draw = ImageDraw.Draw(layer)

    random.seed(frame * 99)

    for _ in range(35):

        angle = random.random() * math.pi * 2

        distance = random.randint(
            10,
            130
        ) * (frame / 15)

        sx = x + math.cos(angle) * distance
        sy = y + math.sin(angle) * distance

        draw.ellipse(
            [
                sx,
                sy,
                sx + random.randint(2, 5),
                sy + random.randint(2, 5)
            ],
            fill=(200, 255, 100, 220)
        )


# ============================================================
# SCREEN SHAKE
# ============================================================

def shake_amount(frame):

    if frame < 6:
        return random.randint(-6, 6)

    return 0


# ============================================================
# CREATE ANIMATION
# ============================================================

frames = []


for role_index, role in enumerate(ROLES):

    # --------------------------------------------------------
    # PHASE 1: ROLE APPEARS
    # --------------------------------------------------------

    for frame in range(32):

        image = Image.new(
            "RGBA",
            (WIDTH, HEIGHT),
            BG + (255,)
        )

        draw = ImageDraw.Draw(image)

        draw_background(draw)

        # Name
        centered_text(
            draw,
            NAME,
            70,
            NAME_FONT,
            WHITE
        )

        # Role
        centered_text(
            draw,
            role,
            175,
            ROLE_FONT,
            GREEN
        )

        # Small status line
        centered_text(
            draw,
            "// SYSTEM READY //",
            245,
            SMALL_FONT,
            (80, 120, 70)
        )

        frames.append(image.convert("RGB"))

    # --------------------------------------------------------
    # PHASE 2: MUZZLE FLASH
    # --------------------------------------------------------

    for frame in range(7):

        image = Image.new(
            "RGBA",
            (WIDTH, HEIGHT),
            BG + (255,)
        )

        draw = ImageDraw.Draw(image)

        draw_background(draw)

        centered_text(
            draw,
            NAME,
            70,
            NAME_FONT,
            WHITE
        )

        centered_text(
            draw,
            role,
            175,
            ROLE_FONT,
            GREEN
        )

        centered_text(
            draw,
            "// FIRE //",
            245,
            SMALL_FONT,
            BRIGHT_GREEN
        )

        muzzle_x = WIDTH // 2
        muzzle_y = 300

        flash_strength = 1 - frame / 7

        draw_muzzle_flash(
            image,
            muzzle_x,
            muzzle_y,
            flash_strength
        )

        frames.append(
            image.convert("RGB")
        )

    # --------------------------------------------------------
    # PHASE 3: BULLET FIRES
    # --------------------------------------------------------

    for frame in range(38):

        image = Image.new(
            "RGBA",
            (WIDTH, HEIGHT),
            BG + (255,)
        )

        draw = ImageDraw.Draw(image)

        draw_background(draw)

        # Slight screen shake
        shake = shake_amount(frame)

        # Name
        centered_text(
            draw,
            NAME,
            70 + shake,
            NAME_FONT,
            WHITE
        )

        # Role
        centered_text(
            draw,
            role,
            175 + shake,
            ROLE_FONT,
            GREEN
        )

        # Bullet movement
        start_x = WIDTH // 2
        end_x = WIDTH - 100

        progress = frame / 37

        bullet_x = (
            start_x +
            (end_x - start_x) *
            progress
        )

        bullet_y = 300 + shake

        # Trail length increases with speed
        trail_length = min(
            220,
            40 + frame * 5
        )

        draw_trail(
            image,
            bullet_x,
            bullet_y,
            trail_length
        )

        draw_bullet(
            image,
            bullet_x,
            bullet_y,
            1
        )

        frames.append(
            image.convert("RGB")
        )

    # --------------------------------------------------------
    # PHASE 4: IMPACT
    # --------------------------------------------------------

    for frame in range(15):

        image = Image.new(
            "RGBA",
            (WIDTH, HEIGHT),
            BG + (255,)
        )

        draw = ImageDraw.Draw(image)

        draw_background(draw)

        centered_text(
            draw,
            NAME,
            70,
            NAME_FONT,
            WHITE
        )

        centered_text(
            draw,
            role,
            175,
            ROLE_FONT,
            GREEN
        )

        centered_text(
            draw,
            "// IMPACT //",
            245,
            SMALL_FONT,
            BRIGHT_GREEN
        )

        impact_x = WIDTH - 100
        impact_y = 300

        draw_impact(
            image,
            impact_x,
            impact_y,
            frame
        )

        draw_sparks(
            image,
            impact_x,
            impact_y,
            frame
        )

        frames.append(
            image.convert("RGB")
        )


# ============================================================
# SAVE GIF
# ============================================================

print()
print("Rendering animation...")
print(f"Frames: {len(frames)}")

frames[0].save(
    "kishan_bullet_banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True
)

print()
print("========================================")
print(" BULLET ANIMATION CREATED SUCCESSFULLY")
print("========================================")
print()
print("Output:")
print("kishan_bullet_banner.gif")
print()