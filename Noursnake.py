import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRID_COLOR = (50, 50, 50)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with BFS")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Snake starts in the middle
        self.direction = (1, 0)  # Moving right
        self.grow_to = 0  # How much the snake should grow

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
        # Check for collisions with walls
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        # Check for collisions with the body
        if head in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake.body:
                return position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def bfs(start, goal, snake_body):
    # BFS to find the shortest path to food
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT and neighbor not in snake_body:
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []  # No path found
    path.append(start)
    path.reverse()
    return path[1:]  # Exclude the start point

def draw_grid(screen):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def main():
    snake = Snake()
    food = Food(snake)
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Find the path to the food using BFS
        path_to_food = bfs(snake.body[0], food.position, snake.body[1:])
        if path_to_food:
            next_pos = path_to_food[0]
            snake.direction = (next_pos[0] - snake.body[0][0], next_pos[1] - snake.body[0][1])
        snake.move()

        # Check if the snake eats the food
        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake)  # Generate new food
            score += 1

        # Check for collision
        if snake.check_collision():
            running = False

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        # Show the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(10)  # Game speed

    # Game Over screen
    screen.fill(BLACK)
    game_over_text = font.render('Game Over!', True, WHITE)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.flip()

    pygame.time.wait(2000)  # Wait before quitting
    pygame.quit()

if __name__ == "__main__":
    main()
