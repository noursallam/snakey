import pygame
from snake import Snake
from food import Food
from pathfinder import SimplePathfinder

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AI Snake Game')

        self.bg_image = pygame.image.load('assets/bg.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

    def handle_events(self):
        """Handle events like quitting the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Update the game logic"""
        self.snake.find_path_to_food(self.food.position)
        self.snake.move()

        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food = Food(self.snake)
            self.score += 1

        if self.snake.check_collision():
            self.running = False

    def draw(self):
        """Draw all elements on the screen"""
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_image, (0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def show_game_over(self):
        """Show the game over screen"""
        self.screen.fill(BLACK)
        game_over_text = self.font.render('Game Over!', True, WHITE)
        final_score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        self.screen.blit(self.bg_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)

        self.show_game_over()
        pygame.quit()
