import pygame

class Menu:
    def __init__(self, screen, image_path, button):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (1000, 840))
        self.button = button

    def draw(self):
        self.draw_background()
        self.screen.blit(self.image, (0, 0))
        self.button.draw(self.screen)

    def draw_background(self):
        for y in range(0, self.screen.get_height(), 2):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.screen.get_width(), y))

    def handle_event(self, event):
        return self.button.is_clicked(event)

