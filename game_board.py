import pygame


class GameBoard:
    def __init__(self, rows, cols, cell_size, pos):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.pos = pos
        self.grid = self.create_grid()

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
                pygame.draw.rect(screen, (255, 255, 255), (cell[0], cell[1], self.cell_size, self.cell_size), 1)
