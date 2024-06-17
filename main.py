import pygame
import sys
import random
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
opponent_ship_manager = ShipManager()

random_button = Button(750, 500, 100, 50, "Losowo")
play_button = Button(870, 500, 100, 50, "Graj")

game_started = False
player_turn = True


def computer_turn():
    while True:
        x = random.randint(boardPlayer.pos[0], boardPlayer.pos[0] + boardPlayer.cols * boardPlayer.cell_size - 1)
        y = random.randint(boardPlayer.pos[1], boardPlayer.pos[1] + boardPlayer.rows * boardPlayer.cell_size - 1)
        if boardPlayer.get_cell(x, y) not in boardPlayer.selected_cells:
            boardPlayer.select_cell(x, y, ship_manager)
            break


def check_game_over():
    opponent_cells = opponent_ship_manager.get_all_ship_cells()
    return all(cell in boardOpponent.hit_cells for cell in opponent_cells)


def reset_game():
    global game_started, player_turn, boardPlayer, boardOpponent, ship_manager, opponent_ship_manager
    game_started = False
    player_turn = True
    boardPlayer = GameBoard(10, 10, 25, (50, 50))
    boardOpponent = GameBoard(10, 10, 25, (700, 50))
    ship_manager = ShipManager()
    opponent_ship_manager = ShipManager()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ship_manager.handle_event(event, boardPlayer, game_started)
        if not game_started:
            if random_button.is_clicked(event):
                ship_manager.randomize_ships(boardPlayer)
            if play_button.is_clicked(event):
                if ship_manager.all_ships_placed():
                    opponent_ship_manager.randomize_ships(boardOpponent)
                    game_started = True
                    print("Graj button clicked and opponent ships placed!")
        if game_started and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            if boardOpponent.pos[0] <= event.pos[0] <= boardOpponent.pos[
                0] + boardOpponent.cols * boardOpponent.cell_size and \
                    boardOpponent.pos[1] <= event.pos[1] <= boardOpponent.pos[
                1] + boardOpponent.rows * boardOpponent.cell_size:
                if boardOpponent.get_cell(event.pos[0], event.pos[1]) not in boardOpponent.selected_cells:
                    boardOpponent.select_cell(event.pos[0], event.pos[1], opponent_ship_manager)
                    if check_game_over():
                        reset_game()
                    else:
                        player_turn = False
                        computer_turn()
                        if check_game_over():
                            reset_game()
                        player_turn = True

    screen.fill(BACKGROUND_COLOR)

    boardPlayer.draw(screen)
    boardOpponent.draw(screen)

    ship_manager.draw(screen)
    opponent_ship_manager.draw(screen, hidden=True)

    boardPlayer.draw(screen)
    boardOpponent.draw(screen)

    if not game_started:
        random_button.draw(screen)
        play_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
