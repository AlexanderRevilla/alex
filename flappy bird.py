import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_GAP = 150
PIPE_WIDTH = 60
PIPE_VEL = 3
FPS = 60

# Bird class
class Bird:
    def __init__(self):
        self.x = 60
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 20

    def jump(self):
        self.vel = BIRD_JUMP

    def move(self):
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self):
        pygame.draw.circle(SCREEN, YELLOW, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.passed = False

    def move(self):
        self.x -= PIPE_VEL

    def draw(self):
        # Top pipe
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        pygame.draw.rect(SCREEN, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

    def collide(self, bird):
        bird_rect = bird.get_rect()
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

def draw_window(bird, pipes, score):
    SCREEN.fill(BLUE)
    for pipe in pipes:
        pipe.draw()
    bird.draw()
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(text, (10, 10))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()

        # Add new pipes
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Move pipes and check for collisions
        remove = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                run = False
            if pipe.x + PIPE_WIDTH < 0:
                remove.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
        for r in remove:
            pipes.remove(r)

        # Check if bird hits the ground or goes above screen
        if bird.y + bird.radius > HEIGHT or bird.y - bird.radius < 0:
            run = False

        draw_window(bird, pipes, score)

    # Game over
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Game Over", True, WHITE)
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()