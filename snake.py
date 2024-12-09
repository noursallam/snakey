import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_COLOR = (50, 50, 50)  # Dark gray for grid lines

# Game Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock to control game speed
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_to = 0

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.body.pop()

    def grow(self):
        self.grow_to += 1

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Self collision
        if head in self.body[1:]:
            return True
        
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                             (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                              GRID_SIZE-1, GRID_SIZE-1))

class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        while True:
            position = (random.randint(0, GRID_WIDTH-1), 
                        random.randint(0, GRID_HEIGHT-1))
            if position not in snake.body:
                return position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, 
                         (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, 
                          GRID_SIZE-1, GRID_SIZE-1))

def draw_grid(screen):
    # Vertical lines
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    
    # Horizontal lines
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def load_background_image(image_path):
    try:
        # Load the background image
        background = pygame.image.load(image_path)
        # Scale the image to fit the screen
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except pygame.error:
        print(f"Cannot load image: {image_path}")
        # Return a default surface if image loading fails
        return pygame.Surface((WIDTH, HEIGHT))

def main(background_image_path=None):
    # Load background image if provided
    background = load_background_image(background_image_path) if background_image_path else None
    
    snake = Snake()
    food = Food(snake)
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        # Move snake
        snake.move()

        # Check food collision
        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake)
            score += 1

        # Check game over
        if snake.check_collision():
            running = False

        # Drawing
        # First draw the background (if exists)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # Draw grid
        draw_grid(screen)

        snake.draw(screen)
        food.draw(screen)

        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()

        # Control game speed
        clock.tick(10)

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render('Game Over!', True, WHITE)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
    screen.blit(final_score_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
    pygame.display.flip()

    # Wait before closing
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    # Run with the background image 'bg.png'
    main('bg.png')