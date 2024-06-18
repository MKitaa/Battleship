import pygame


class GameBoard:
    def __init__(self, rows, cols, cell_size, pos):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.pos = pos
        self.grid = self.create_grid()
        self.occupied_cells = []
        self.selected_cells = []
        self.hit_cells = []

    def create_grid(self):
        start_x, start_y = self.pos
        grid = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                row_cells.append((start_x, start_y))
                start_x += self.cell_size
            grid.append(row_cells)
            start_x = self.pos[0]
            start_y += self.cell_size
        return grid

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell_rect = pygame.Rect(cell[0], cell[1], self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cell_rect, 1)

        for cell in self.selected_cells:
            cell_rect = pygame.Rect(cell[0], cell[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (255, 0, 0), cell_rect)

        for cell in self.hit_cells:
            cell_rect = pygame.Rect(cell[0], cell[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (0, 255, 0), cell_rect)

    def get_cell(self, x, y):
        for row in self.grid:
            for cell in row:
                cell_rect = pygame.Rect(cell[0], cell[1], self.cell_size, self.cell_size)
                if cell_rect.collidepoint(x, y):
                    return cell
        return None

    def add_ship(self, ship):
        top_left_cell = self.get_cell(ship.rect.x, ship.rect.y)
        if top_left_cell and self.ship_fits(ship, top_left_cell):
            self.remove_ship(ship)
            ship.rect.topleft = top_left_cell
            self.occupied_cells.append(ship.rect.copy())
            ship.on_board = True
        else:
            ship.reset_position()

    def remove_ship(self, ship):
        if ship.on_board:
            temp_rect = ship.rect.copy()
            self.occupied_cells = [cell for cell in self.occupied_cells if not temp_rect.colliderect(cell)]
            ship.on_board = False

    def ship_fits(self, ship, top_left_cell):
        ship_right = top_left_cell[0] + ship.rect.width
        ship_bottom = top_left_cell[1] + ship.rect.height
        board_right = self.pos[0] + self.cols * self.cell_size
        board_bottom = self.pos[1] + self.rows * self.cell_size

        if ship_right > board_right or ship_bottom > board_bottom:
            return False

        temp_rect = pygame.Rect(top_left_cell[0], top_left_cell[1], ship.rect.width, ship.rect.height)
        expanded_rect = temp_rect.inflate(self.cell_size * 2, self.cell_size * 2)
        for occupied in self.occupied_cells:
            if expanded_rect.colliderect(occupied):
                return False

        return True

    def adjust_ship_position(self, ship):
        top_left_cell = self.get_cell(ship.rect.x, ship.rect.y)
        if not top_left_cell:
            return False
        if self.ship_fits(ship, top_left_cell):
            ship.rect.topleft = top_left_cell
            return True
        else:
            return False

    def reset_occupied_cells(self):
        self.occupied_cells = []

    def select_cell(self, x, y, opponent):
        cell = self.get_cell(x, y)
        if cell and cell not in self.selected_cells:
            self.selected_cells.append(cell)
            if opponent.is_hit(cell):
                self.hit_cells.append(cell)

