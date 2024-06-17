import pygame
import sys
from game_board import GameBoard
from ship import ShipManager

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra w Statki")

boardPlayer = GameBoard(10, 10, 25, (50, 50))
boardOpponent = GameBoard(10, 10, 25, (700, 50))

ship_manager = ShipManager()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    boardPlayer.draw(screen)
    boardOpponent.draw(screen)

    ship_manager.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
