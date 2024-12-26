import random
import pygame

GRID_WIDTH = 800 // 20
GRID_HEIGHT = 600 // 20
GRID_SIZE = 20
RED = (255, 0, 0)

class Food:
    def __init__(self, snake):
        """Initialize the food and place it at a random position"""
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        """Generate a random position for the food"""
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake.body:
                return position

    def draw(self, screen):
        """Draw the food on the screen"""
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
