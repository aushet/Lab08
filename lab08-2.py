import pygame
import random
import sys

# Инициализация
pygame.init()

# Экран өлшемдері
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Түстер
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Экран мен таймер
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Levels")
clock = pygame.time.Clock()

# Қаріптер
font = pygame.font.SysFont("Arial", 20)

# Жемісті кездейсоқ, бос орынға қою
def random_food(snake, walls):
    while True:
        x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
        y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in walls:
            return x, y

# Қабырғаларды жасау (қалауыңа қарай өзгерте аласың)
def create_walls(level):
    walls = set()
    if level >= 2:
        for i in range(10, 20):
            walls.add((i * CELL_SIZE, 10 * CELL_SIZE))
    if level >= 3:
        for i in range(5, 15):
            walls.add((20 * CELL_SIZE, i * CELL_SIZE))
    return walls

# Негізгі ойын функциясы
def main():
    snake = [(100, 100), (80, 100)]
    direction = (CELL_SIZE, 0)
    food = random_food(snake, [])
    level = 1
    score = 0
    speed = 10
    food_eaten = 0
    walls = create_walls(level)

    running = True
    while running:
        screen.fill(BLACK)

        # Басқару
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        elif keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        elif keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        elif keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Жыланды жылжыту
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Шекарадан шығу → game over
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake or
            new_head in walls):
            print("Game over!")
            pygame.quit()
            sys.exit()

        snake.insert(0, new_head)

        # Жемісті жеді ма?
        if new_head == food:
            score += 1
            food_eaten += 1
            food = random_food(snake, walls)
        else:
            snake.pop()

        # Уровень ауыстыру
        if food_eaten >= 3:
            level += 1
            speed += 2
            food_eaten = 0
            walls = create_walls(level)

        # Жыланды салу
        for block in snake:
            pygame.draw.rect(screen, GREEN, (*block, CELL_SIZE, CELL_SIZE))

        # Жеміс салу
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Қабырға салу
        for wall in walls:
            pygame.draw.rect(screen, BLUE, (*wall, CELL_SIZE, CELL_SIZE))

        # Ұпай мен деңгейді шығару
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 30))

        pygame.display.flip()
        clock.tick(speed)

# Ойынды бастау
main()