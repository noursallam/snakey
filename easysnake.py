import pygame
import random
import collections  # For queue in BFS

# Game Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Pathfinding for Beginners')

# Simple Breadth-First Search (BFS) Pathfinder
class SimplePathfinder:
    @staticmethod
    def find_path(start, goal, snake_body):
        """
        Simple Breadth-First Search to find path
        Explanation:
        1. Start at snake's head
        2. Try to find shortest path to food
        3. Avoid snake's body and game boundaries
        """
        # Possible moves: right, left, down, up
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        
        # Queue to explore paths
        queue = collections.deque([[start]])
        
        # Keep track of visited positions
        visited = set([start])
        
        while queue:
            # Get current path
            path = queue.popleft()
            
            # Last position in current path
            current = path[-1]
            
            # Found the goal!
            if current == goal:
                return path[1:]  # Skip first position (current head)
            
            # Try all possible moves
            for move in moves:
                # Calculate next position
                next_pos = (current[0] + move[0], current[1] + move[1])
                
                # Check if move is valid:
                # 1. Inside game boundaries
                # 2. Not in snake's body
                # 3. Not already visited
                if (0 <= next_pos[0] < GRID_WIDTH and 
                    0 <= next_pos[1] < GRID_HEIGHT and 
                    next_pos not in snake_body and 
                    next_pos not in visited):
                    
                    # Create new path
                    new_path = list(path)
                    new_path.append(next_pos)
                    
                    # Add to queue and mark as visited
                    queue.append(new_path)
                    visited.add(next_pos)
        
        # No path found
        return []

# Snake Class with Simple Pathfinding
class Snake:
    def __init__(self):
        # Start in middle of screen
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.path_to_food = []  # Path to food
        self.grow_to = 0

    def find_path_to_food(self, food_position):
        """
        Find path to food using BFS
        Easy explanation:
        - Look for shortest route to food
        - Avoid running into myself
        """
        self.path_to_food = SimplePathfinder.find_path(
            self.body[0],  # Start from head
            food_position,  # Goal is food
            self.body[1:]   # Avoid my body
        )

    def move(self):
        # If we have a path, follow it
        if self.path_to_food:
            # Set direction to next step
            next_pos = self.path_to_food[0]
            self.direction = (
                next_pos[0] - self.body[0][0],
                next_pos[1] - self.body[0][1]
            )
            self.path_to_food.pop(0)  # Remove first step
        
        # Move snake
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

        # Grow or shrink
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.body.pop()

    def grow(self):
        # Make snake longer
        self.grow_to += 1

    def check_collision(self):
        head = self.body[0]
        # Hit wall
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Hit myself
        if head in self.body[1:]:
            return True
        
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                             (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                              GRID_SIZE-1, GRID_SIZE-1))

# Food Class
class Food:
    def __init__(self, snake):
        # Create food away from snake
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        while True:
            position = (
                random.randint(0, GRID_WIDTH-1), 
                random.randint(0, GRID_HEIGHT-1)
            )
            if position not in snake.body:
                return position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, 
                         (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, 
                          GRID_SIZE-1, GRID_SIZE-1))

# Main Game Loop
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

        # Find path to food
        snake.find_path_to_food(food.position)
        
        # Move snake
        snake.move()

        # Eat food
        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake)
            score += 1

        # Check game over
        if snake.check_collision():
            running = False

        # Drawing
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # Show score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)  # Game speed

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render('Game Over!', True, WHITE)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
    screen.blit(final_score_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
    pygame.display.flip()

    pygame.time.wait(2000)
    pygame.quit()

# Create clock and run game
clock = pygame.time.Clock()
if __name__ == "__main__":
    main()