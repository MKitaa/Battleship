from ship import Ship


class PatrolBoat(Ship):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, cell_size, "assets/ships/patrolBoat/patrolBoat.png")


class Cruiser(Ship):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, cell_size * 2, "assets/ships/cruiser/cruiser.png")


class Destroyer(Ship):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, cell_size * 3, "assets/ships/destroyer/destroyer.png")


class Submarine(Ship):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, cell_size * 4, "assets/ships/submarine/submarine.png")


class Carrier(Ship):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, cell_size * 5, "assets/ships/carrier/carrier.png")
