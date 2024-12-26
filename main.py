import pygame
from game import Game
from snake import Snake


if __name__ == "__main__":
    pygame.init()
    game = Game()  # Create the game instance
    game.run()  # Run the game
