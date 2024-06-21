import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val=0, max_val=1, initial_val=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.dragging = False
        self.slider_pos = x + (initial_val - min_val) / (max_val - min_val) * width

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Background
        pygame.draw.rect(screen, (200, 200, 200), (self.slider_pos - 5, self.rect.y, 10, self.rect.height))  # Knob

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.slider_pos = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.val = self.min_val + (self.slider_pos - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.val
