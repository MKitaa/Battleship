import pygame


class Ship:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)


class ShipManager:
    def __init__(self):
        self.ships = self.create_ships()

    def create_ships(self):
        ships = [
            Ship(50, 500, 100, 25),
            Ship(160, 500, 80, 25),
            Ship(250, 500, 60, 25),
            Ship(320, 500, 40, 25),
            Ship(380, 500, 20, 25)
        ]
        return ships

    def draw(self, screen):
        for ship in self.ships:
            ship.draw(screen)
