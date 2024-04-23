import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
FONT = pygame.font.Font(None, 60)

# Define game objects
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.score = 0

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_ai(self, ball):
        if self.rect.centery < ball.rect.centery:
            self.move_down()
        elif self.rect.centery > ball.rect.centery:
            self.move_up()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 3
        self.speed_y = 3
        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])

    def update(self):
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y

        # Check collisions with walls first
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction_y *= -1

        # Check if ball goes out of bounds
        if self.rect.left <= 0:
            paddle2.score += 1
            self.reset()
        elif self.rect.right >= WIDTH:
            paddle1.score += 1
            self.reset()

        # Check collisions with paddles
        if pygame.sprite.spritecollideany(self, paddles):
            self.direction_x *= -1
            self.speed_x += 0.5  # Increase speed after hitting a paddle
            self.speed_y += 0.5

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.direction_x *= random.choice([1, -1])
        self.speed_x = 3
        self.speed_y = 3

def main_menu():
    while True:
        SCREEN.fill(BLACK)
        draw_text("Press any key to start", FONT, WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    SCREEN.blit(text_surface, text_rect)

# Create paddles and ball
paddle1 = Paddle(30, HEIGHT // 2)
paddle2 = Paddle(WIDTH - 30, HEIGHT // 2)
ball = Ball()

# Group for paddles
paddles = pygame.sprite.Group()
paddles.add(paddle1, paddle2)

# Group for all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1, paddle2, ball)

# Main game loop
clock = pygame.time.Clock()
main_menu()  # Show main menu before starting the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check for continuous key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle2.rect.top > 0:
        paddle2.move_up()
    if keys[pygame.K_DOWN] and paddle2.rect.bottom < HEIGHT:
        paddle2.move_down()

    # AI control for paddle1
    paddle1.move_ai(ball)

    # Update
    all_sprites.update()

    # Render
    SCREEN.fill(BLACK)
    pygame.draw.line(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    all_sprites.draw(SCREEN)

    # Display scores
    draw_text(str(paddle1.score), FONT, WHITE, WIDTH // 4, 50)
    draw_text(str(paddle2.score), FONT, WHITE, 3 * WIDTH // 4, 50)

    # Check if a player has won
    if paddle1.score >= 5 or paddle2.score >= 5:
        winner = "Player 1" if paddle1.score >= 5 else "Player 2"
        draw_text(f"{winner} Wins!", FONT, WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)
        paddle1.score = 0
        paddle2.score = 0
        main_menu()  # Go back to main menu after a player wins

    # Flip the display
    pygame.display.flip()
    clock.tick(60)
