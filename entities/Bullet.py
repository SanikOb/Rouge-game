from tools import *
from math import *

class Bullet:
    def __init__(self, canvas, room, x, y, v, ang):
        self.canvas = canvas
        self.oval = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow", outline="grey", width=0)
        self.room = room
        self.v = v
        self.ang = ang
        self.deflect = False

    def move(self):
        dx = self.v * cos(self.ang)
        dy = self.v * sin(self.ang)

        self.canvas.move(self.oval, dx, dy)
        wall = check_entities_collision(self.canvas, self.oval, self.room.walls)
        if wall:
            self.room.bullets.remove(self)
            self.canvas.delete(self.oval)
'''
        self.canvas.move(self.oval, dx, 0)
        wall = check_entities_collision(self.canvas, self.oval, self.room.walls)
        if wall:
            bullet_coords = self.canvas.coords(self.oval)
            wall_coords = self.canvas.coords(wall.rect)
            if dx > 0:
                self.canvas.move(self.oval, wall_coords[0] - bullet_coords[2], 0)
            else:
                self.canvas.move(self.oval, wall_coords[2] - bullet_coords[0], 0)
            self.ang = pi - self.ang
        self.canvas.move(self.oval, 0, dy)
        wall = check_entities_collision(self.canvas, self.oval, self.room.walls)
        if wall:
            bullet_coords = self.canvas.coords(self.oval)
            wall_coords = self.canvas.coords(wall.rect)
            if dy > 0:
                self.canvas.move(self.oval, 0, wall_coords[1] - bullet_coords[3])
            else:
                self.canvas.move(self.oval, 0, wall_coords[3] - bullet_coords[1])
            self.ang = -self.ang
'''