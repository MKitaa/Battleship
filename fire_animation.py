import pygame


class FireAnimation:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.frames = []
        self.load_frames()
        self.current_frame = 0
        self.animation_speed = 5
        self.counter = 0
        self.position = (0, 0)
        self.active = False

    def load_frames(self):
        for i in range(12):
            frame = pygame.image.load(f"assets/fireloop/fire1_{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (self.cell_size, self.cell_size))
            self.frames.append(frame)

    def start(self, position):
        self.position = position
        self.current_frame = 0
        self.counter = 0
        self.active = True

    def update(self):
        if self.active:
            self.counter += 1
            if self.counter >= self.animation_speed:
                self.counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0

    def draw(self, screen):
        if self.active:
            screen.blit(self.frames[self.current_frame], self.position)
