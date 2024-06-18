import pygame


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 36)
        self.color = (70, 130, 180)  # Steel blue color
        self.hover_color = (100, 149, 237)  # Cornflower blue color
        self.text_color = (255, 255, 255)  # White color
        self.border_color = (255, 255, 255)  # White color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surf, self.rect.move((self.rect.width - text_surf.get_width()) // 2,
                                              (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
