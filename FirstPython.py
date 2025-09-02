#My first python game - Flappy Bird
#
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_GAP = 150
PIPE_WIDTH = 60
PIPE_VEL = 3
FPS = 60

# Bird settings
bird_x = 50
bird_y = HEIGHT // 2
bird_vel = 0
bird_radius = 20

# Pipes
pipes = []
score = 0
font = pygame.font.SysFont(None, 40)

def create_pipe():
    y = random.randint(100, HEIGHT - 100)
    pipe = {'x': WIDTH, 'top': y - PIPE_GAP // 2, 'bottom': y + PIPE_GAP // 2}
    return pipe

def draw_bird():
    pygame.draw.circle(SCREEN, RED, (bird_x, int(bird_y)), bird_radius)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(SCREEN, GREEN, (pipe['x'], 0, PIPE_WIDTH, pipe['top']))
        pygame.draw.rect(SCREEN, GREEN, (pipe['x'], pipe['bottom'], PIPE_WIDTH, HEIGHT - pipe['bottom']))

def check_collision():
    global bird_y
    if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
        return True
    for pipe in pipes:
        if pipe['x'] < bird_x + bird_radius < pipe['x'] + PIPE_WIDTH:
            if bird_y - bird_radius < pipe['top'] or bird_y + bird_radius > pipe['bottom']:
                return True
    return False

def show_score():
    score_text = font.render(f"Score: {score}", True, BLUE)
    SCREEN.blit(score_text, (10, 10))

clock = pygame.time.Clock()
pipes.append(create_pipe())
running = True
game_over = False

while running:
    clock.tick(FPS)
    SCREEN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = BIRD_JUMP
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset game
                bird_y = HEIGHT // 2
                bird_vel = 0
                pipes = [create_pipe()]
                score = 0
                game_over = False

    if not game_over:
        bird_vel += GRAVITY
        bird_y += bird_vel

        # Move pipes
        for pipe in pipes:
            pipe['x'] -= PIPE_VEL

        # Add new pipe
        if pipes[-1]['x'] < WIDTH - 200:
            pipes.append(create_pipe())

        # Remove off-screen pipes
        if pipes[0]['x'] < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        # Collision
        if check_collision():
            game_over = True

    draw_bird()
    draw_pipes()
    show_score()

    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, RED)
        SCREEN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

pygame.quit()
sys.exit()
