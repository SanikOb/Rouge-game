import objects.Wall as Wall

class Room:
    def __init__(self, doors = [-1, -1, -1, -1], walls = [], healthpacks = []):
        self.doors = doors
        self.walls = walls
        self.enemies = []
        self.healthpacks = healthpacks
        self.bullets = []
        self.attacks = []
