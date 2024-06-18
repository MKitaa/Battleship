import pygame
import random


class Ship:
    def __init__(self, x, y, width, height):
        self.initial_pos = (x, y)
        self.initial_width = width
        self.initial_height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.vertical = True
        self.on_board = False

    def draw(self, screen, hidden=False):
        if not hidden:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)

    def handle_event(self, event, game_board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 1:
                    if self.on_board:
                        game_board.remove_ship(self)
                    self.dragging = True
                    self.mouse_x, self.mouse_y = event.pos
                    self.offset_x = self.rect.x - self.mouse_x
                    self.offset_y = self.rect.y - self.mouse_y
                elif event.button == 3:
                    if self.rect.topleft == self.initial_pos:
                        self.rotate(game_board)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                game_board.add_ship(self)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.mouse_x, self.mouse_y = event.pos
                self.rect.x = self.mouse_x + self.offset_x
                self.rect.y = self.mouse_y + self.offset_y

    def reset_position(self):

        self.rect.topleft = self.initial_pos
        if not self.vertical:
            self.rotate(None, reset=True)
        self.on_board = False

    def rotate(self, game_board, reset=False):
        if not reset:
            self.vertical = not self.vertical
        self.rect.width, self.rect.height = self.rect.height, self.rect.width

        if game_board and not game_board.adjust_ship_position(self):
            self.reset_position()
        else:
            self.on_board = True

    def get_cells(self):
        cells = []
        if self.vertical:
            for i in range(self.rect.height // self.initial_height):
                cells.append((self.rect.x, self.rect.y + i * self.initial_height))
        else:
            for i in range(self.rect.width // self.initial_width):
                cells.append((self.rect.x + i * self.initial_width, self.rect.y))
        return cells


class ShipManager:
    def __init__(self):
        self.ships = self.create_ships()

    def create_ships(self):
        ships = [
            Ship(50, 400, 25, 25),
            Ship(100, 400, 25, 50),
            Ship(150, 400, 25, 100),
            Ship(200, 400, 25, 125),
            Ship(250, 400, 25, 150)
        ]
        return ships

    def draw(self, screen, hidden=False):
        for ship in self.ships:
            ship.draw(screen, hidden)

    def handle_event(self, event, game_board, game_started):
        if not game_started:
            for ship in self.ships:
                ship.handle_event(event, game_board)

    def randomize_ships(self, game_board):
        game_board.reset_occupied_cells()

        for ship in self.ships:
            placed = False
            attempts = 0
            max_attempts = 100
            while not placed and attempts < max_attempts:
                attempts += 1
                ship.vertical = random.choice([True, False])
                ship.rect.width, ship.rect.height = (ship.initial_width, ship.initial_height) if ship.vertical else (
                ship.initial_height, ship.initial_width)

                max_x = game_board.pos[0] + game_board.cols * game_board.cell_size - ship.rect.width
                max_y = game_board.pos[1] + game_board.rows * game_board.cell_size - ship.rect.height

                x = random.randint(game_board.pos[0], max_x)
                y = random.randint(game_board.pos[1], max_y)

                x = (x // game_board.cell_size) * game_board.cell_size
                y = (y // game_board.cell_size) * game_board.cell_size

                ship.rect.topleft = (x, y)
                if game_board.ship_fits(ship, (x, y)):
                    game_board.add_ship(ship)
                    placed = True
                else:
                    ship.reset_position()

            if not placed:
                print(f"Could not place the ship after {max_attempts} attempts.")

    def all_ships_placed(self):
        return all(ship.on_board for ship in self.ships)

    def is_hit(self, cell):
        for ship in self.ships:
            if ship.rect.collidepoint(cell[0], cell[1]):
                return True
        return False

    def get_all_ship_cells(self):
        all_cells = []
        for ship in self.ships:
            all_cells.extend(ship.get_cells())
        return all_cells

