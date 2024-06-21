import pygame
import random

class Ship:
    def __init__(self, x, y, width, height, image_path):
        self.initial_pos = (x, y)
        self.initial_width = width
        self.initial_height = height
        self.image_path = image_path
        self.vertical = True
        self.on_board = False
        self.scale_factor = 0.9  # Zmniejszenie rozmiaru obrazów o 10%
        self.load_image()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False

    def load_image(self):
        self.image = pygame.image.load(self.image_path).convert_alpha()
        scaled_width = int(self.initial_width * self.scale_factor)
        scaled_height = int(self.initial_height * self.scale_factor)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

    def draw(self, screen, hidden=False):
        if not hidden:
            screen.blit(self.image, self.rect.topleft)

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
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

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
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.ships = self.create_ships()

    def create_ships(self):
        ships = [
            Ship(100, 670, self.cell_size, self.cell_size, "assets/ships/patrolBoat/patrolBoat.png"),
            Ship(150, 670, self.cell_size, self.cell_size * 2, "assets/ships/cruiser/cruiser.png"),
            Ship(200, 670, self.cell_size, self.cell_size * 3, "assets/ships/destroyer/destroyer.png"),
            Ship(250, 670, self.cell_size, self.cell_size * 4, "assets/ships/submarine/submarine.png"),
            Ship(300, 670, self.cell_size, self.cell_size * 5, "assets/ships/carrier/carrier.png")
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
        all_placed = False

        while not all_placed:
            game_board.reset_occupied_cells()
            all_placed = True

            for ship in self.ships:
                placed = False
                max_attempts = 100
                while not placed and max_attempts > 0:
                    max_attempts -= 1
                    ship.vertical = random.choice([True, False])
                    ship.rect.width, ship.rect.height = (ship.initial_width, ship.initial_height) if ship.vertical else (
                        ship.initial_height, ship.initial_width)
                    ship.load_image()  # reload image to match orientation
                    if not ship.vertical:
                        ship.image = pygame.transform.rotate(ship.image, 90)

                    potential_positions = [
                        (x, y)
                        for x in range(game_board.pos[0], game_board.pos[0] + game_board.cols * game_board.cell_size, game_board.cell_size)
                        for y in range(game_board.pos[1], game_board.pos[1] + game_board.rows * game_board.cell_size, game_board.cell_size)
                    ]
                    random.shuffle(potential_positions)

                    for x, y in potential_positions:
                        ship.rect.topleft = (x, y)
                        if game_board.ship_fits(ship, (x, y)):
                            game_board.add_ship(ship)
                            placed = True
                            break
                        else:
                            ship.reset_position()

                if not placed:
                    all_placed = False
                    break

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
