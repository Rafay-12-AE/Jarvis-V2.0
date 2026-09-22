import math
import random

import pygame

from core.ui_state import (
    get_ui_state,
    shutdown_requested
)


# ============================================================
# JARVIS UI
# ============================================================

WIDTH = 800
HEIGHT = 700

# 30 FPS is more than enough for this animation and reduces
# unnecessary rendering load while Jarvis is processing voice/AI.
FPS = 30

BACKGROUND = (3, 6, 14)

DIM_TEXT = (105, 125, 145)

STATE_COLORS = {
    "SLEEPING": (45, 80, 110),
    "LISTENING": (0, 210, 255),
    "THINKING": (125, 80, 255),
    "SPEAKING": (0, 255, 200),
}

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 - 30


# ============================================================
# PARTICLES
# ============================================================

def create_particles():

    particles = []

    for _ in range(55):

        particles.append(
            {
                "angle": random.uniform(
                    0,
                    math.tau
                ),

                "distance": random.uniform(
                    120,
                    250
                ),

                "speed": random.uniform(
                    0.08,
                    0.35
                ),

                "size": random.uniform(
                    1,
                    3
                ),
            }
        )

    return particles


# ============================================================
# GLOW
# ============================================================

def draw_glow(
    surface,
    center,
    radius,
    color,
    strength
):

    glow_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    layers = 14

    for layer in range(
        layers,
        0,
        -1
    ):

        extra = layer * 8

        alpha = int(
            (
                5
                + (layers - layer) * 1.5
            )
            * strength
        )

        alpha = min(
            255,
            alpha
        )

        pygame.draw.circle(
            glow_surface,
            (
                color[0],
                color[1],
                color[2],
                alpha
            ),
            center,
            int(radius + extra)
        )

    surface.blit(
        glow_surface,
        (0, 0)
    )


# ============================================================
# PARTICLES
# ============================================================

def draw_particles(
    surface,
    particles,
    color,
    state,
    dt,
    time_value
):

    if state == "SLEEPING":

        brightness = 0.25
        speed_multiplier = 0.15

    elif state == "THINKING":

        brightness = 0.9
        speed_multiplier = 2.0

    elif state == "SPEAKING":

        brightness = 1.0
        speed_multiplier = 1.2

    else:

        brightness = 0.75
        speed_multiplier = 0.7


    for particle in particles:

        particle["angle"] += (
            particle["speed"]
            * dt
            * speed_multiplier
        )

        wobble = math.sin(
            time_value * 2
            + particle["angle"] * 3
        ) * 7

        distance = (
            particle["distance"]
            + wobble
        )

        x = (
            CENTER_X
            + math.cos(
                particle["angle"]
            )
            * distance
        )

        y = (
            CENTER_Y
            + math.sin(
                particle["angle"]
            )
            * distance
        )

        particle_color = (
            int(
                color[0]
                * brightness
            ),

            int(
                color[1]
                * brightness
            ),

            int(
                color[2]
                * brightness
            )
        )

        pygame.draw.circle(
            surface,
            particle_color,
            (
                int(x),
                int(y)
            ),
            max(
                1,
                int(
                    particle["size"]
                )
            )
        )


# ============================================================
# ENERGY RINGS
# ============================================================

def draw_energy_rings(
    surface,
    color,
    state,
    time_value
):

    ring_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )


    if state == "SLEEPING":

        intensity = 0.25
        movement = 0.4

    elif state == "LISTENING":

        intensity = 0.8
        movement = 1.2

    elif state == "THINKING":

        intensity = 1.0
        movement = 2.5

    else:

        intensity = 1.0
        movement = 1.8


    for index in range(3):

        pulse = math.sin(
            time_value * movement
            + index * 1.8
        )

        radius = (
            125
            + index * 28
            + pulse * 7
        )

        alpha = int(
            (45 - index * 10)
            * intensity
        )

        pygame.draw.circle(
            ring_surface,
            (
                color[0],
                color[1],
                color[2],
                alpha
            ),
            (
                CENTER_X,
                CENTER_Y
            ),
            int(radius),
            2
        )


    surface.blit(
        ring_surface,
        (0, 0)
    )


# ============================================================
# ORB
# ============================================================

def draw_orb(
    surface,
    state,
    time_value
):

    color = STATE_COLORS[
        state
    ]


    # ---------------- SLEEPING ----------------

    if state == "SLEEPING":

        pulse = (
            math.sin(
                time_value * 1.3
            )
            * 3
        )

        glow_strength = 0.45


    # ---------------- LISTENING ----------------

    elif state == "LISTENING":

        pulse = (
            math.sin(
                time_value * 3.0
            )
            * 6
        )

        glow_strength = 1.0


    # ---------------- THINKING ----------------

    elif state == "THINKING":

        pulse = (
            math.sin(
                time_value * 5.0
            )
            * 4
        )

        glow_strength = 1.15


    # ---------------- SPEAKING ----------------

    else:

        pulse = (
            math.sin(
                time_value * 7.0
            )
            * 8
        )

        glow_strength = 1.3


    radius = (
        92
        + pulse
    )


    # ---------------- OUTER GLOW ----------------

    draw_glow(
        surface,
        (
            CENTER_X,
            CENTER_Y
        ),
        radius,
        color,
        glow_strength
    )


    # ---------------- ENERGY RINGS ----------------

    draw_energy_rings(
        surface,
        color,
        state,
        time_value
    )


    # ---------------- ORB BODY ----------------

    orb_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    layers = 35


    for layer in range(
        layers,
        0,
        -1
    ):

        ratio = (
            layer
            / layers
        )

        layer_radius = (
            radius
            * ratio
        )

        brightness = (
            0.35
            + (1 - ratio) * 0.65
        )

        red = min(
            255,
            int(
                color[0]
                * brightness
                + (1 - ratio) * 90
            )
        )

        green = min(
            255,
            int(
                color[1]
                * brightness
                + (1 - ratio) * 90
            )
        )

        blue = min(
            255,
            int(
                color[2]
                * brightness
                + (1 - ratio) * 100
            )
        )

        pygame.draw.circle(
            orb_surface,
            (
                red,
                green,
                blue,
                255
            ),
            (
                CENTER_X,
                CENTER_Y
            ),
            int(
                layer_radius
            )
        )


    # ---------------- INTERNAL ENERGY ----------------

    energy_speed = (
        2.8
        if state == "THINKING"
        else 1.3
    )

    energy_angle = (
        time_value
        * energy_speed
    )

    energy_x = (
        CENTER_X
        + math.cos(
            energy_angle
        )
        * radius
        * 0.32
    )

    energy_y = (
        CENTER_Y
        + math.sin(
            energy_angle
        )
        * radius
        * 0.32
    )

    pygame.draw.circle(
        orb_surface,
        (
            240,
            250,
            255,
            115
        ),
        (
            int(
                energy_x
            ),
            int(
                energy_y
            )
        ),
        int(
            radius * 0.42
        )
    )


    # ---------------- BRIGHT CORE ----------------

    pygame.draw.circle(
        orb_surface,
        (
            235,
            250,
            255,
            210
        ),
        (
            CENTER_X,
            CENTER_Y
        ),
        int(
            radius * 0.25
        )
    )


    surface.blit(
        orb_surface,
        (0, 0)
    )


# ============================================================
# TEXT
# ============================================================

def draw_text(
    surface,
    state,
    title_font,
    state_font,
    hint_font
):

    # ---------------- TITLE ----------------

    title = title_font.render(
        "J  A  R  V  I  S",
        True,
        DIM_TEXT
    )

    title_rect = title.get_rect(
        center=(
            CENTER_X,
            65
        )
    )

    surface.blit(
        title,
        title_rect
    )


    # ---------------- STATE ----------------

    state_color = STATE_COLORS[
        state
    ]

    state_text = state_font.render(
        state,
        True,
        state_color
    )

    state_rect = state_text.get_rect(
        center=(
            CENTER_X,
            CENTER_Y + 185
        )
    )

    surface.blit(
        state_text,
        state_rect
    )


    # ---------------- HINT ----------------

    hint = hint_font.render(
        "ESC  CLOSE JARVIS",
        True,
        DIM_TEXT
    )

    hint_rect = hint.get_rect(
        center=(
            CENTER_X,
            HEIGHT - 45
        )
    )

    surface.blit(
        hint,
        hint_rect
    )


# ============================================================
# UI LOOP
# ============================================================

def run_ui():

    pygame.init()


    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT
        )
    )

    pygame.display.set_caption(
        "Jarvis"
    )


    clock = pygame.time.Clock()


    title_font = pygame.font.SysFont(
        "arial",
        20
    )

    state_font = pygame.font.SysFont(
        "arial",
        28,
        bold=True
    )

    hint_font = pygame.font.SysFont(
        "arial",
        16
    )


    particles = create_particles()

    time_value = 0.0

    running = True


    # ========================================================
    # RENDER LOOP
    # ========================================================

    while running:

        dt = (
            clock.tick(FPS)
            / 1000.0
        )

        time_value += dt


        # ----------------------------------------------------
        # JARVIS SHUTDOWN SIGNAL
        # ----------------------------------------------------

        if shutdown_requested():

            running = False

            continue


        # ----------------------------------------------------
        # WINDOW EVENTS
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False


        # ----------------------------------------------------
        # CURRENT JARVIS STATE
        # ----------------------------------------------------

        state = get_ui_state()


        if state not in STATE_COLORS:

            state = "SLEEPING"


        # ----------------------------------------------------
        # DRAW
        # ----------------------------------------------------

        screen.fill(
            BACKGROUND
        )


        color = STATE_COLORS[
            state
        ]


        draw_particles(
            screen,
            particles,
            color,
            state,
            dt,
            time_value
        )


        draw_orb(
            screen,
            state,
            time_value
        )


        draw_text(
            screen,
            state,
            title_font,
            state_font,
            hint_font
        )


        pygame.display.flip()


    # ========================================================
    # CLOSE UI
    # ========================================================

    pygame.quit()


# ============================================================
# STANDALONE MODE
# ============================================================

if __name__ == "__main__":

    run_ui()