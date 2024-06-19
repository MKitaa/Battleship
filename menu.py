import pygame
import sys


class Menu:
    def __init__(self, screen, image_path, start_button, exit_button):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (1250, 840))
        self.start_button = start_button
        self.exit_button = exit_button

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (0, 0))
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def handle_event(self, event):
        if self.start_button.is_clicked(event):
            return True
        if self.exit_button.is_clicked(event):
            pygame.quit()
            sys.exit()
        return False
