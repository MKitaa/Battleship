import pygame
import random
from ships import PatrolBoat, Cruiser, Destroyer, Submarine, Carrier


class ShipManager:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.ships = self.create_ships()

    def create_ships(self):
        ships = [
            PatrolBoat(100, 670, self.cell_size),
            Cruiser(150, 670, self.cell_size),
            Destroyer(200, 670, self.cell_size),
            Submarine(250, 670, self.cell_size),
            Carrier(300, 670, self.cell_size)
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
                    ship.rect.width, ship.rect.height = (
                    ship.initial_width, ship.initial_height) if ship.vertical else (
                        ship.initial_height, ship.initial_width)
                    ship.load_image()  
                    if not ship.vertical:
                        ship.image = pygame.transform.rotate(ship.image, 90)

                    potential_positions = [
                        (x, y)
                        for x in range(game_board.pos[0], game_board.pos[0] + game_board.cols * game_board.cell_size,
                                       game_board.cell_size)
                        for y in range(game_board.pos[1], game_board.pos[1] + game_board.rows * game_board.cell_size,
                                       game_board.cell_size)
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
