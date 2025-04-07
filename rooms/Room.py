class Room:
    def __init__(self, walls = [], healthpacks = [], type = 0):
        self.walls = walls
        self.healthpacks = healthpacks
        self.type = type
        self.enemies = []
        self.bullets = []
        self.attacks = []
        self.explored = False
