import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (0, -CELL_SIZE)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
clock = pygame.time.Clock()
score = 0

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    return [head] + snake[:-1]

def check_collision(snake):
    head = snake[0]
    
    if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT):
        return True
    if head in snake[1:]:
        return True
    return False

def place_food(snake):
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake:
            return pos


running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    
    if snake[0] == food:
        score += 1
        food = place_food(snake)
    else:
        snake.pop()

   
    if check_collision(snake):
        print(f"Game Over! Your score: {score}")
        pygame.quit()
        sys.exit()

   
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()