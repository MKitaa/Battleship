import pygame
import sys
import random
from game_board import GameBoard
from ship import ShipManager
from button import Button
from menu import Menu

pygame.init()

pygame.mixer.init()

hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
miss_sound = pygame.mixer.Sound("assets/sounds/miss.mp3")

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 840
BACKGROUND_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra w Statki")

start_button = Button(525, 620, 200, 80, "Start")
exit_button = Button(525, 740, 200, 80, "Wyjście z gry")

menu = Menu(screen, "assets/menu/Battleship.png", start_button, exit_button)

CELL_SIZE = 50
boardPlayer = GameBoard(10, 10, CELL_SIZE, (50, 50))
boardOpponent = GameBoard(10, 10, CELL_SIZE, (700, 50))

ship_manager = ShipManager(CELL_SIZE)
opponent_ship_manager = ShipManager(CELL_SIZE)

random_button = Button(750, 580, 100, 50, "Losowo")
play_button = Button(870, 580, 100, 50, "Graj")

game_started = False
player_turn = True
in_menu = True

last_move_time = pygame.time.get_ticks()
move_delay = 500


def computer_turn():
    attempts = 0
    while attempts < 100:
        x = random.randint(boardPlayer.pos[0], boardPlayer.pos[0] + boardPlayer.cols * boardPlayer.cell_size - 1)
        y = random.randint(boardPlayer.pos[1], boardPlayer.pos[1] + boardPlayer.rows * boardPlayer.cell_size - 1)
        if boardPlayer.get_cell(x, y) not in boardPlayer.selected_cells:
            boardPlayer.select_cell(x, y, ship_manager)
            hit = boardPlayer.is_hit(boardPlayer.get_cell(x, y))
            if hit:
                hit_sound.play()
            else:
                miss_sound.play()
            return hit
        attempts += 1
    return False


def check_game_over():
    player_cells = ship_manager.get_all_ship_cells()
    opponent_cells = opponent_ship_manager.get_all_ship_cells()
    player_lost = all(cell in boardPlayer.hit_cells for cell in player_cells)
    opponent_lost = all(cell in boardOpponent.hit_cells for cell in opponent_cells)
    return player_lost, opponent_lost


def reset_game():
    global game_started, player_turn, boardPlayer, boardOpponent, ship_manager, opponent_ship_manager, in_menu
    game_started = False
    player_turn = True
    boardPlayer = GameBoard(10, 10, CELL_SIZE, (50, 50))
    boardOpponent = GameBoard(10, 10, CELL_SIZE, (700, 50))
    ship_manager = ShipManager(CELL_SIZE)
    opponent_ship_manager = ShipManager(CELL_SIZE)
    in_menu = True


running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if menu.handle_event(event):
                in_menu = False
            if exit_button.is_clicked(event):
                running = False
        else:
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
                        if opponent_ship_manager.is_hit(boardOpponent.get_cell(event.pos[0], event.pos[1])):
                            hit_sound.play()
                        else:
                            miss_sound.play()
                        player_lost, opponent_lost = check_game_over()
                        if player_lost or opponent_lost:
                            reset_game()
                        else:
                            hit = opponent_ship_manager.is_hit(boardOpponent.get_cell(event.pos[0], event.pos[1]))
                            if not hit:
                                player_turn = False
                                last_move_time = current_time

    if game_started and not player_turn and current_time - last_move_time > move_delay:
        if not computer_turn():
            player_turn = True
            last_move_time = current_time
        player_lost, opponent_lost = check_game_over()
        if player_lost or opponent_lost:
            reset_game()

    screen.fill(BACKGROUND_COLOR)

    if in_menu:
        menu.draw()
    else:
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
