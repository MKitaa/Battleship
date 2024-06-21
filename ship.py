import pygame


class Ship:
    def __init__(self, x, y, width, height, image_path):
        self.initial_pos = (x, y)
        self.initial_width = width
        self.initial_height = height
        self.image_path = image_path
        self.vertical = True
        self.on_board = False
        self.scale_factor = 0.9
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
