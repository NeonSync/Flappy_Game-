import pygame
import asyncio
import platform
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.5
flap_strength = -8

pipe_width = 50
pipe_gap = 120
pipe_speed = 3
pipes = []
score = 0
last_pipe = pygame.time.get_ticks()

font = pygame.font.SysFont("arial", 24)

game_over = False
countdown = None
win_score = 10

def setup():
    global bird_y, bird_velocity, pipes, score, game_over, last_pipe, countdown
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False
    last_pipe = pygame.time.get_ticks()
    countdown = 3  # Start countdown at 3

def spawn_pipe():
    gap_y = random.randint(100, HEIGHT - 100)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, gap_y - pipe_gap // 2)
    bottom_pipe = pygame.Rect(WIDTH, gap_y + pipe_gap // 2, pipe_width, HEIGHT)
    return top_pipe, bottom_pipe

def check_collision():
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_y < 0 or bird_y > HEIGHT:
        return True
    return False

def update_loop():
    global bird_y, bird_velocity, pipes, score, game_over, last_pipe, countdown

    if countdown is not None:
        if countdown > 0:
            return  # Skip updates during countdown
        elif countdown <= 0:
            countdown = None  # End countdown

    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > 1500:
            pipes.extend(spawn_pipe())
            last_pipe = current_time

        for pipe in pipes[:]:
            pipe.x -= pipe_speed
            if pipe.right < 0:
                pipes.remove(pipe)
                if pipe.y == 0:
                    score += 1
                    if score >= win_score:
                        game_over = True  # Win condition

        if check_collision():
            game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and countdown is None:
                bird_velocity = flap_strength
            if event.key == pygame.K_r and game_over:
                setup()

    screen.fill(BLUE)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
    pygame.draw.circle(screen, WHITE, (bird_x, int(bird_y)), bird_radius)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if countdown is not None:
        countdown_text = font.render(f"{int(countdown) if countdown > 0 else 'Go!'}", True, BLACK)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        countdown -= 1 / FPS  # Decrease countdown by 1/FPS seconds per frame
    elif game_over:
        if score >= win_score:
            end_text = font.render(f"You Win! Score: {score} Press Tab", True, BLACK)
        else:
            end_text = font.render(f"Game Over! Score: {score} Press Tab", True, BLACK)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

FPS = 60

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())