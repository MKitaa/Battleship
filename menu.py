import pygame


class Menu:
    def __init__(self, screen, image_path, start_button, exit_button):
        self.screen = screen
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (1200, 852))
        self.start_button = start_button
        self.exit_button = exit_button
        self.winner_message = ""
        self.winner_color = (255, 255, 255)  # Default color white

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (0, 0))
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)

        if self.winner_message:
            font = pygame.font.SysFont(None, 74)
            text = font.render(self.winner_message, True, self.winner_color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 100))

    def handle_event(self, event):
        if self.start_button.is_clicked(event):
            return True
        if self.exit_button.is_clicked(event):
            pygame.quit()
            sys.exit()
        return False

    def set_winner_message(self, message, color):
        self.winner_message = message
        self.winner_color = color
