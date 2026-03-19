#!/usr/bin/env python3
"""
Flappy Cat - A Flappy Birds clone with flying cats and rainbow background
"""

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)

# Rainbow colors
RAINBOW_COLORS = [
    (255, 0, 0),      # Red
    (255, 127, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130),     # Indigo
    (148, 0, 211),    # Violet
]

# Game settings
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -9
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1500  # milliseconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Cat")
clock = pygame.time.Clock()

# Font
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)


def draw_rainbow_background(offset=0):
    """Draw animated rainbow gradient background."""
    stripe_height = SCREEN_HEIGHT // len(RAINBOW_COLORS)

    for i, color in enumerate(RAINBOW_COLORS):
        # Add some wave animation
        wave_offset = int(math.sin((offset + i * 20) * 0.02) * 10)
        y = i * stripe_height + wave_offset

        # Create gradient effect between stripes
        rect = pygame.Rect(0, y, SCREEN_WIDTH, stripe_height + 20)
        pygame.draw.rect(screen, color, rect)

    # Add some sparkle/star effects
    for _ in range(3):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(2, 4)
        alpha = random.randint(100, 255)
        star_color = (255, 255, 255)
        pygame.draw.circle(screen, star_color, (x, y), size)


def draw_cat(x, y, angle=0, flapping=False):
    """Draw a cute flying cat."""
    # Cat body (oval)
    body_color = (255, 165, 0)  # Orange cat
    body_rect = pygame.Rect(x - 20, y - 12, 40, 24)
    pygame.draw.ellipse(screen, body_color, body_rect)

    # Cat head (circle)
    head_x = x + 15
    head_y = y - 5
    pygame.draw.circle(screen, body_color, (head_x, head_y), 14)

    # Ears (triangles)
    ear_color = body_color
    inner_ear = (255, 192, 203)  # Pink inner ear

    # Left ear
    pygame.draw.polygon(screen, ear_color, [
        (head_x - 10, head_y - 10),
        (head_x - 5, head_y - 22),
        (head_x, head_y - 8)
    ])
    pygame.draw.polygon(screen, inner_ear, [
        (head_x - 8, head_y - 12),
        (head_x - 5, head_y - 18),
        (head_x - 2, head_y - 10)
    ])

    # Right ear
    pygame.draw.polygon(screen, ear_color, [
        (head_x + 10, head_y - 10),
        (head_x + 5, head_y - 22),
        (head_x, head_y - 8)
    ])
    pygame.draw.polygon(screen, inner_ear, [
        (head_x + 8, head_y - 12),
        (head_x + 5, head_y - 18),
        (head_x + 2, head_y - 10)
    ])

    # Eyes
    eye_color = (50, 205, 50)  # Green eyes
    pygame.draw.circle(screen, WHITE, (head_x - 5, head_y - 2), 5)
    pygame.draw.circle(screen, WHITE, (head_x + 5, head_y - 2), 5)
    pygame.draw.circle(screen, eye_color, (head_x - 5, head_y - 2), 3)
    pygame.draw.circle(screen, eye_color, (head_x + 5, head_y - 2), 3)
    pygame.draw.circle(screen, BLACK, (head_x - 5, head_y - 2), 1)
    pygame.draw.circle(screen, BLACK, (head_x + 5, head_y - 2), 1)

    # Nose
    pygame.draw.polygon(screen, (255, 105, 180), [
        (head_x, head_y + 2),
        (head_x - 3, head_y + 6),
        (head_x + 3, head_y + 6)
    ])

    # Whiskers
    whisker_color = (100, 100, 100)
    # Left whiskers
    pygame.draw.line(screen, whisker_color, (head_x - 8, head_y + 4), (head_x - 20, head_y), 1)
    pygame.draw.line(screen, whisker_color, (head_x - 8, head_y + 6), (head_x - 20, head_y + 6), 1)
    pygame.draw.line(screen, whisker_color, (head_x - 8, head_y + 8), (head_x - 20, head_y + 12), 1)
    # Right whiskers
    pygame.draw.line(screen, whisker_color, (head_x + 22, head_y + 4), (head_x + 34, head_y), 1)
    pygame.draw.line(screen, whisker_color, (head_x + 22, head_y + 6), (head_x + 34, head_y + 6), 1)
    pygame.draw.line(screen, whisker_color, (head_x + 22, head_y + 8), (head_x + 34, head_y + 12), 1)

    # Wings (animated based on flapping)
    wing_color = (255, 255, 255)
    wing_y_offset = -10 if flapping else 0

    # Left wing
    pygame.draw.ellipse(screen, wing_color, (x - 25, y - 20 + wing_y_offset, 20, 12))
    pygame.draw.ellipse(screen, (200, 200, 200), (x - 23, y - 18 + wing_y_offset, 16, 8))

    # Right wing (behind body, smaller)
    pygame.draw.ellipse(screen, (200, 200, 200), (x - 15, y - 15 + wing_y_offset, 15, 10))

    # Tail
    tail_wave = int(math.sin(pygame.time.get_ticks() * 0.01) * 5)
    pygame.draw.arc(screen, body_color, (x - 45, y - 5 + tail_wave, 30, 20), 0, math.pi, 4)

    # Cape (superhero cat!)
    cape_color = (138, 43, 226)  # Purple cape
    cape_points = [
        (x - 15, y - 8),
        (x - 35, y + 25),
        (x - 25, y + 30),
        (x - 10, y + 10),
    ]
    pygame.draw.polygon(screen, cape_color, cape_points)


def draw_pipe(x, gap_y):
    """Draw a pipe with gap at specified y position."""
    # Top pipe
    top_pipe_height = gap_y - PIPE_GAP // 2
    if top_pipe_height > 0:
        # Main pipe body
        pygame.draw.rect(screen, GREEN, (x, 0, PIPE_WIDTH, top_pipe_height))
        # Pipe rim
        pygame.draw.rect(screen, DARK_GREEN, (x - 5, top_pipe_height - 30, PIPE_WIDTH + 10, 30))
        # Highlight
        pygame.draw.rect(screen, (50, 180, 50), (x + 5, 0, 10, top_pipe_height - 30))

    # Bottom pipe
    bottom_pipe_y = gap_y + PIPE_GAP // 2
    bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y
    if bottom_pipe_height > 0:
        # Main pipe body
        pygame.draw.rect(screen, GREEN, (x, bottom_pipe_y, PIPE_WIDTH, bottom_pipe_height))
        # Pipe rim
        pygame.draw.rect(screen, DARK_GREEN, (x - 5, bottom_pipe_y, PIPE_WIDTH + 10, 30))
        # Highlight
        pygame.draw.rect(screen, (50, 180, 50), (x + 5, bottom_pipe_y + 30, 10, bottom_pipe_height - 30))


def check_collision(cat_x, cat_y, pipes):
    """Check if cat collides with pipes or screen boundaries."""
    # Cat hitbox (smaller than visual for fairness)
    cat_rect = pygame.Rect(cat_x - 15, cat_y - 10, 50, 20)

    # Screen boundaries
    if cat_y < 0 or cat_y > SCREEN_HEIGHT - 20:
        return True

    # Pipe collision
    for pipe_x, gap_y in pipes:
        # Top pipe
        top_pipe_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, gap_y - PIPE_GAP // 2)
        # Bottom pipe
        bottom_pipe_rect = pygame.Rect(pipe_x, gap_y + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT)

        if cat_rect.colliderect(top_pipe_rect) or cat_rect.colliderect(bottom_pipe_rect):
            return True

    return False


def show_start_screen():
    """Display the start screen."""
    offset = 0
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        offset += 1
        draw_rainbow_background(offset)

        # Draw floating cat
        cat_y = SCREEN_HEIGHT // 2 + int(math.sin(offset * 0.05) * 20)
        draw_cat(SCREEN_WIDTH // 2 - 50, cat_y, flapping=(offset % 20 < 10))

        # Title with shadow
        title_text = font_large.render("FLAPPY CAT", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 103))
        title_text = font_large.render("FLAPPY CAT", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Instructions
        inst_text = font_small.render("Press SPACE or Click to Flap", True, WHITE)
        screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, 450))

        start_text = font_medium.render("Click to Start!", True, WHITE)
        # Pulsing effect
        if (offset // 30) % 2 == 0:
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 500))

        pygame.display.flip()
        clock.tick(FPS)


def show_game_over(score, high_score):
    """Display game over screen."""
    offset = 0
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        offset += 1
        draw_rainbow_background(offset)

        # Draw sad cat
        draw_cat(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50)

        # Game Over text
        go_text = font_large.render("GAME OVER", True, BLACK)
        screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2 + 3, 153))
        go_text = font_large.render("GAME OVER", True, WHITE)
        screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 150))

        # Score
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 350))

        # High score
        if score >= high_score:
            hs_text = font_small.render("NEW HIGH SCORE!", True, (255, 215, 0))
        else:
            hs_text = font_small.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 400))

        # Restart instruction
        restart_text = font_small.render("Click to Play Again", True, WHITE)
        if (offset // 30) % 2 == 0:
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 500))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Main game loop."""
    high_score = 0

    while True:
        # Show start screen
        show_start_screen()

        # Game variables
        cat_x = 100
        cat_y = SCREEN_HEIGHT // 2
        cat_velocity = 0
        pipes = []  # List of (x, gap_y) tuples
        score = 0
        last_pipe_spawn = pygame.time.get_ticks()
        bg_offset = 0
        flap_animation = 0

        # Game loop
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        cat_velocity = FLAP_STRENGTH
                        flap_animation = 10
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cat_velocity = FLAP_STRENGTH
                    flap_animation = 10

            # Update cat position
            cat_velocity += GRAVITY
            cat_y += cat_velocity

            # Update flap animation
            if flap_animation > 0:
                flap_animation -= 1

            # Spawn pipes
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_spawn > PIPE_SPAWN_INTERVAL:
                gap_y = random.randint(150, SCREEN_HEIGHT - 150)
                pipes.append([SCREEN_WIDTH, gap_y])
                last_pipe_spawn = current_time

            # Update pipes
            for pipe in pipes:
                pipe[0] -= PIPE_SPEED

            # Remove off-screen pipes and count score
            new_pipes = []
            for pipe in pipes:
                if pipe[0] + PIPE_WIDTH > 0:
                    new_pipes.append(pipe)
                elif pipe[0] + PIPE_WIDTH > -PIPE_SPEED and pipe[0] + PIPE_WIDTH <= 0:
                    score += 1
            pipes = new_pipes

            # Check collision
            if check_collision(cat_x, cat_y, pipes):
                running = False

            # Draw everything
            bg_offset += 1
            draw_rainbow_background(bg_offset)

            # Draw pipes
            for pipe_x, gap_y in pipes:
                draw_pipe(pipe_x, gap_y)

            # Draw cat
            draw_cat(cat_x, cat_y, flapping=(flap_animation > 0))

            # Draw score
            score_text = font_medium.render(str(score), True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2 + 2, 52))
            score_text = font_medium.render(str(score), True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

            pygame.display.flip()
            clock.tick(FPS)

        # Update high score
        if score > high_score:
            high_score = score

        # Show game over screen
        show_game_over(score, high_score)


if __name__ == "__main__":
    main()
