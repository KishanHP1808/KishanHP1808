from PIL import Image, ImageDraw, ImageFont
import math

# ==============================
# SETTINGS
# ==============================

WIDTH = 1200
HEIGHT = 400

BACKGROUND = (5, 5, 8)
WHITE = (245, 245, 245)
GREEN = (163, 230, 53)
DARK_GREEN = (80, 180, 30)

FPS = 30

# Text that will appear one after another
LINES = [
    "FRONTEND DEVELOPER",
    "AI & WEB DEVELOPER",
    "PYTHON DEVELOPER",
    "UI/UX ENTHUSIAST",
    "PROBLEM SOLVER"
]

# ==============================
# FONTS
# ==============================

try:
    FONT = ImageFont.truetype(
        "C:/Windows/Fonts/arialbd.ttf",
        42
    )

    SMALL_FONT = ImageFont.truetype(
        "C:/Windows/Fonts/arial.ttf",
        20
    )

except:
    FONT = ImageFont.load_default()
    SMALL_FONT = ImageFont.load_default()


# ==============================
# HELPER FUNCTIONS
# ==============================

def centered_text(draw, text, y, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    text_width = box[2] - box[0]

    x = (WIDTH - text_width) // 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )

    return x, text_width


def draw_bullet(draw, x, y, progress):
    """
    Draws a bullet travelling from center to right.
    """

    start_x = WIDTH // 2
    end_x = WIDTH - 120

    current_x = start_x + (end_x - start_x) * progress

    # Bullet trail
    trail_length = 180

    for i in range(trail_length, 0, -8):

        alpha = 1 - (i / trail_length)

        green = (
            int(GREEN[0] * alpha),
            int(GREEN[1] * alpha),
            int(GREEN[2] * alpha)
        )

        draw.line(
            [
                (current_x - i, y),
                (current_x - i - 15, y)
            ],
            fill=green,
            width=4
        )

    # Bullet glow
    radius = 12

    for r in range(30, radius, -3):

        alpha = (30 - r) / 30

        glow = (
            int(GREEN[0] * alpha),
            int(GREEN[1] * alpha),
            int(GREEN[2] * alpha)
        )

        draw.ellipse(
            [
                current_x - r,
                y - r,
                current_x + r,
                y + r
            ],
            fill=glow
        )

    # Bullet
    draw.ellipse(
        [
            current_x - radius,
            y - radius,
            current_x + radius,
            y + radius
        ],
        fill=WHITE
    )

    # Green bullet tip
    draw.polygon(
        [
            (current_x + radius, y),
            (current_x + radius + 18, y - 7),
            (current_x + radius + 18, y + 7)
        ],
        fill=GREEN
    )


def draw_explosion(draw, x, y, frame):

    # Explosion animation
    radius = int(10 + frame * 2)

    for i in range(12):

        angle = (i / 12) * math.pi * 2

        x2 = x + math.cos(angle) * radius
        y2 = y + math.sin(angle) * radius

        draw.line(
            [(x, y), (x2, y2)],
            fill=GREEN,
            width=3
        )


# ==============================
# CREATE GIF
# ==============================

frames = []

for line_index, text in enumerate(LINES):

    # --------------------------------
    # PHASE 1: TEXT APPEARS
    # --------------------------------

    for frame in range(25):

        img = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BACKGROUND
        )

        draw = ImageDraw.Draw(img)

        # Name
        centered_text(
            draw,
            "KISHAN H.P.",
            60,
            FONT,
            WHITE
        )

        # Text
        centered_text(
            draw,
            text,
            170,
            FONT,
            GREEN
        )

        frames.append(img)

    # --------------------------------
    # PHASE 2: BULLET FIRES
    # --------------------------------

    for frame in range(35):

        img = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BACKGROUND
        )

        draw = ImageDraw.Draw(img)

        # Name
        centered_text(
            draw,
            "KISHAN H.P.",
            60,
            FONT,
            WHITE
        )

        # Text
        centered_text(
            draw,
            text,
            170,
            FONT,
            GREEN
        )

        progress = frame / 34

        draw_bullet(
            draw,
            WIDTH // 2,
            230,
            progress
        )

        frames.append(img)

    # --------------------------------
    # PHASE 3: IMPACT
    # --------------------------------

    for frame in range(10):

        img = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BACKGROUND
        )

        draw = ImageDraw.Draw(img)

        centered_text(
            draw,
            "KISHAN H.P.",
            60,
            FONT,
            WHITE
        )

        centered_text(
            draw,
            text,
            170,
            FONT,
            GREEN
        )

        draw_explosion(
            draw,
            WIDTH - 100,
            230,
            frame
        )

        frames.append(img)


# ==============================
# SAVE GIF
# ==============================

frames[0].save(
    "kishan_github_banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000 // FPS,
    loop=0,
    optimize=True
)

print("GIF created successfully!")
print("File: kishan_github_banner.gif")