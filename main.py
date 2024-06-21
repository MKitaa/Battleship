import pygame
import sys
import random
from game_board import GameBoard
from ship import ShipManager
from button import Button
from menu import Menu
from slider import Slider

pygame.init()
pygame.mixer.init()

hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
miss_sound = pygame.mixer.Sound("assets/sounds/miss.mp3")
click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.play(-1)  # Play the music in a loop

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 852
BACKGROUND_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra w Statki")

start_button = Button(500, 640, 200, 80, "Start")
exit_button = Button(500, 760, 200, 80, "Wyjście z gry")

menu = Menu(screen, "assets/menu/Battleship.png", start_button, exit_button)

CELL_SIZE = 47
boardPlayer = GameBoard(10, 10, CELL_SIZE, (123, 193))
boardOpponent = GameBoard(10, 10, CELL_SIZE, (655, 193))

ship_manager = ShipManager(CELL_SIZE)
opponent_ship_manager = ShipManager(CELL_SIZE)

random_button = Button(850, 780, 100, 50, "Losowo")
play_button = Button(970, 780, 100, 50, "Graj")

game_started = False
player_turn = True
in_menu = True

last_move_time = pygame.time.get_ticks()
move_delay = 500

background_image = pygame.image.load("assets/board/board.jpeg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

volume_slider = Slider(1050, 20, 100, 20, initial_val=pygame.mixer.music.get_volume())

hit_image = pygame.image.load("assets/token/hit.png").convert_alpha()
miss_image = pygame.image.load("assets/token/miss.png").convert_alpha()
hit_image = pygame.transform.scale(hit_image, (CELL_SIZE, CELL_SIZE))
miss_image = pygame.transform.scale(miss_image, (CELL_SIZE, CELL_SIZE))

def computer_turn():
    attempts = 0
    while attempts < 100:
        x = random.randint(boardPlayer.pos[0], boardPlayer.pos[0] + boardPlayer.cols * boardPlayer.cell_size - 1)
        y = random.randint(boardPlayer.pos[1], boardPlayer.pos[1] + boardPlayer.rows * boardPlayer.cell_size - 1)
        if boardPlayer.get_cell(x, y) not in boardPlayer.selected_cells:
            boardPlayer.select_cell(x, y, ship_manager, is_player_board=True)
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

def reset_game(winner_message="", winner_color=(255, 255, 255)):
    global game_started, player_turn, boardPlayer, boardOpponent, ship_manager, opponent_ship_manager, in_menu
    game_started = False
    player_turn = True
    boardPlayer = GameBoard(10, 10, CELL_SIZE, (123, 193))
    boardOpponent = GameBoard(10, 10, CELL_SIZE, (655, 193))
    ship_manager = ShipManager(CELL_SIZE)
    opponent_ship_manager = ShipManager(CELL_SIZE)
    in_menu = True
    menu.set_winner_message(winner_message, winner_color)

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
            volume_slider.handle_event(event)
            pygame.mixer.music.set_volume(volume_slider.get_value())
            if not game_started:
                if random_button.is_clicked(event):
                    click_sound.play()
                    ship_manager.randomize_ships(boardPlayer)
                if play_button.is_clicked(event):
                    click_sound.play()
                    if ship_manager.all_ships_placed():
                        opponent_ship_manager.randomize_ships(boardOpponent)
                        game_started = True
                        print("Graj button clicked and opponent ships placed!")
            if game_started and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                if boardOpponent.pos[0] <= event.pos[0] <= boardOpponent.pos[0] + boardOpponent.cols * boardOpponent.cell_size and \
                        boardOpponent.pos[1] <= event.pos[1] <= boardOpponent.pos[1] + boardOpponent.rows * boardOpponent.cell_size:
                    if boardOpponent.get_cell(event.pos[0], event.pos[1]) not in boardOpponent.selected_cells:
                        boardOpponent.select_cell(event.pos[0], event.pos[1], opponent_ship_manager, is_player_board=False)
                        if opponent_ship_manager.is_hit(boardOpponent.get_cell(event.pos[0], event.pos[1])):
                            hit_sound.play()
                        else:
                            miss_sound.play()
                        player_lost, opponent_lost = check_game_over()
                        if player_lost or opponent_lost:
                            winner_message = "Wygrałeś!" if opponent_lost else "Przegrałeś!"
                            winner_color = (0, 255, 0) if opponent_lost else (255, 0, 0)
                            reset_game(winner_message, winner_color)
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
            winner_message = "Wygrałeś!" if opponent_lost else "Przegrałeś!"
            winner_color = (0, 255, 0) if opponent_lost else (255, 0, 0)
            reset_game(winner_message, winner_color)

    screen.fill(BACKGROUND_COLOR)

    if in_menu:
        menu.draw()
    else:
        screen.blit(background_image, (0, 0))

        boardPlayer.draw(screen)
        boardOpponent.draw(screen)

        ship_manager.draw(screen)
        opponent_ship_manager.draw(screen, hidden=True)

        boardPlayer.draw_fire_animations(screen)
        boardOpponent.draw_hits(screen, hit_image, miss_image, is_player_board=False)
        boardPlayer.draw_hits(screen, hit_image, miss_image, is_player_board=True)

        if not game_started:
            random_button.draw(screen)
            play_button.draw(screen)

    volume_slider.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
