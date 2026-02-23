# Snake Game built using Python and Pygame
# Features: food, scoring, restart, self-collision, increasing speedimport pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font_big = pygame.font.SysFont(None, 55)
font_small = pygame.font.SysFont(None, 30)

high_score = 0


def reset_game():
    snake = [(100, 100)]
    dx = CELL
    dy = 0
    food = (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )
    score = 0
    return snake, dx, dy, food, score


snake, dx, dy, food, score = reset_game()
game_over = False
running = True

while running:
    clock.tick(10 + score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELL
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELL
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = CELL
            else:
                if event.key == pygame.K_r:
                    snake, dx, dy, food, score = reset_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

    if not game_over:
        head_x = snake[0][0] + dx
        head_y = snake[0][1] + dy
        new_head = (head_x, head_y)

        # Boundary collision
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        # Self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = (
                    random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL)
                )
            else:
                snake.pop()

    if game_over and score > high_score:
        high_score = score

    # Drawing
    screen.fill((0, 0, 0))

    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0),
                         (segment[0], segment[1], CELL, CELL))

    pygame.draw.rect(screen, (255, 0, 0),
                     (food[0], food[1], CELL, CELL))

    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font_small.render(f"High Score: {high_score}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 35))

    if game_over:
        over_text = font_big.render("GAME OVER", True, (255, 0, 0))
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        screen.blit(over_text, (WIDTH // 2 - 140, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - 170, HEIGHT // 2 + 10))

    pygame.display.update()

pygame.quit()

sys.exit()
