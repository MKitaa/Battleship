import pygame
import sys
import random
from game_board import GameBoard
from ship_manager import ShipManager
from button import Button
from menu import Menu
from slider import Slider


class BattleshipGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.miss_sound = pygame.mixer.Sound("assets/sounds/miss.mp3")
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.play(-1)

        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 852
        self.BACKGROUND_COLOR = (0, 0, 0)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Gra w Statki")

        self.start_button = Button(500, 640, 200, 80, "Start")
        self.exit_button = Button(500, 760, 200, 80, "Wyjście z gry")

        self.menu = Menu(self.screen, "assets/menu/Battleship.png", self.start_button, self.exit_button)

        self.CELL_SIZE = 47
        self.boardPlayer = GameBoard(10, 10, self.CELL_SIZE, (123, 193))
        self.boardOpponent = GameBoard(10, 10, self.CELL_SIZE, (655, 193))

        self.ship_manager = ShipManager(self.CELL_SIZE)
        self.opponent_ship_manager = ShipManager(self.CELL_SIZE)

        self.random_button = Button(850, 780, 100, 50, "Losowo")
        self.play_button = Button(970, 780, 100, 50, "Graj")

        self.game_started = False
        self.player_turn = True
        self.in_menu = True

        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = 500

        self.background_image = pygame.image.load("assets/board/board.jpeg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.volume_slider = Slider(1050, 20, 100, 20, initial_val=pygame.mixer.music.get_volume())

        self.hit_image = pygame.image.load("assets/token/hit.png").convert_alpha()
        self.miss_image = pygame.image.load("assets/token/miss.png").convert_alpha()
        self.hit_image = pygame.transform.scale(self.hit_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.miss_image = pygame.transform.scale(self.miss_image, (self.CELL_SIZE, self.CELL_SIZE))

    def computer_turn(self):
        attempts = 0
        while attempts < 100:
            x = random.randint(self.boardPlayer.pos[0],
                               self.boardPlayer.pos[0] + self.boardPlayer.cols * self.boardPlayer.cell_size - 1)
            y = random.randint(self.boardPlayer.pos[1],
                               self.boardPlayer.pos[1] + self.boardPlayer.rows * self.boardPlayer.cell_size - 1)
            if self.boardPlayer.get_cell(x, y) not in self.boardPlayer.selected_cells:
                self.boardPlayer.select_cell(x, y, self.ship_manager, is_player_board=True)
                hit = self.boardPlayer.is_hit(self.boardPlayer.get_cell(x, y))
                if hit:
                    self.hit_sound.play()
                else:
                    self.miss_sound.play()
                return hit
            attempts += 1
        return False

    def check_game_over(self):
        player_cells = self.ship_manager.get_all_ship_cells()
        opponent_cells = self.opponent_ship_manager.get_all_ship_cells()
        player_lost = all(cell in self.boardPlayer.hit_cells for cell in player_cells)
        opponent_lost = all(cell in self.boardOpponent.hit_cells for cell in opponent_cells)
        return player_lost, opponent_lost

    def reset_game(self, winner_message="", winner_color=(255, 255, 255)):
        self.game_started = False
        self.player_turn = True
        self.boardPlayer = GameBoard(10, 10, self.CELL_SIZE, (123, 193))
        self.boardOpponent = GameBoard(10, 10, self.CELL_SIZE, (655, 193))
        self.ship_manager = ShipManager(self.CELL_SIZE)
        self.opponent_ship_manager = ShipManager(self.CELL_SIZE)
        self.in_menu = True
        self.menu.set_winner_message(winner_message, winner_color)

    def handle_events(self, current_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.in_menu:
                if self.menu.handle_event(event):
                    self.in_menu = False
                if self.exit_button.is_clicked(event):
                    return False
            else:
                self.ship_manager.handle_event(event, self.boardPlayer, self.game_started)
                self.volume_slider.handle_event(event)
                pygame.mixer.music.set_volume(self.volume_slider.get_value())
                if not self.game_started:
                    self.handle_pre_game_events(event)
                else:
                    self.handle_in_game_events(event, current_time)
        return True

    def handle_pre_game_events(self, event):
        if self.random_button.is_clicked(event):
            self.click_sound.play()
            self.ship_manager.randomize_ships(self.boardPlayer)
        if self.play_button.is_clicked(event):
            self.click_sound.play()
            if self.ship_manager.all_ships_placed():
                self.opponent_ship_manager.randomize_ships(self.boardOpponent)
                self.game_started = True
                print("Graj button clicked and opponent ships placed!")

    def handle_in_game_events(self, event, current_time):
        if self.player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            if self.boardOpponent.pos[0] <= event.pos[0] <= self.boardOpponent.pos[
                0] + self.boardOpponent.cols * self.boardOpponent.cell_size and \
                    self.boardOpponent.pos[1] <= event.pos[1] <= self.boardOpponent.pos[
                1] + self.boardOpponent.rows * self.boardOpponent.cell_size:
                if self.boardOpponent.get_cell(event.pos[0], event.pos[1]) not in self.boardOpponent.selected_cells:
                    self.boardOpponent.select_cell(event.pos[0], event.pos[1], self.opponent_ship_manager,
                                                   is_player_board=False)
                    self.handle_shot_result(self.boardOpponent.get_cell(event.pos[0], event.pos[1]), current_time)

    def handle_shot_result(self, cell, current_time):
        if self.opponent_ship_manager.is_hit(cell):
            self.hit_sound.play()
        else:
            self.miss_sound.play()

        player_lost, opponent_lost = self.check_game_over()
        if player_lost or opponent_lost:
            self.handle_game_over(player_lost, opponent_lost)
        else:
            if not self.opponent_ship_manager.is_hit(cell):
                self.player_turn = False
                self.last_move_time = current_time

    def update_game_state(self, current_time):
        if self.game_started and not self.player_turn and current_time - self.last_move_time > self.move_delay:
            if not self.computer_turn():
                self.player_turn = True
                self.last_move_time = current_time

            player_lost, opponent_lost = self.check_game_over()
            if player_lost or opponent_lost:
                self.handle_game_over(player_lost, opponent_lost)

    def handle_game_over(self, player_lost, opponent_lost):
        winner_message = "Wygrałeś!" if opponent_lost else "Przegrałeś!"
        winner_color = (0, 255, 0) if opponent_lost else (255, 0, 0)
        self.reset_game(winner_message, winner_color)

    def draw_screen(self):
        self.screen.fill(self.BACKGROUND_COLOR)

        if self.in_menu:
            self.menu.draw()
        else:
            self.screen.blit(self.background_image, (0, 0))
            self.boardPlayer.draw(self.screen)
            self.boardOpponent.draw(self.screen)
            self.ship_manager.draw(self.screen)
            self.opponent_ship_manager.draw(self.screen, hidden=True)
            self.boardPlayer.draw_fire_animations(self.screen)
            self.boardOpponent.draw_hits(self.screen, self.hit_image, self.miss_image, is_player_board=False)
            self.boardPlayer.draw_hits(self.screen, self.hit_image, self.miss_image, is_player_board=True)

            if not self.game_started:
                self.random_button.draw(self.screen)
                self.play_button.draw(self.screen)

        self.volume_slider.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            running = self.handle_events(current_time)
            self.update_game_state(current_time)
            self.draw_screen()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = BattleshipGame()
    game.run()
