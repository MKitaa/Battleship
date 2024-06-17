import pygame
import sys
from game_board import GameBoard
from ship import ShipManager
from button import Button

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0) 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra w Statki")

boardPlayer = GameBoard(10, 10, 25, (50, 50))
boardOpponent = GameBoard(10, 10, 25, (700, 50))

ship_manager = ShipManager()

random_button = Button(850, 500, 100, 50, "Losowo")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ship_manager.handle_event(event, boardPlayer)
        if random_button.is_clicked(event):
            ship_manager.randomize_ships(boardPlayer)

    screen.fill(BACKGROUND_COLOR)

    boardPlayer.draw(screen)
    boardOpponent.draw(screen)

    ship_manager.draw(screen)

    random_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

