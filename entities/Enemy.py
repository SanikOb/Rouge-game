from math import *
from tools import *
from random import *
from entities.Bullet import Bullet
class Enemy:
    def __init__(self, canvas, room, x, y):
        self.canvas = canvas
        self.x1 = x - 10
        self.y1 = y - 10
        self.x2 = x + 10
        self.y2 = y + 10
        self.room = room
        self.v = 0
        self.ang = 0
        self.health = 100
        self.health_cooldown = 0
        self.targeted = False
        self.calm = True
        self.is_shooting = True
        self.shoot_cooldown = 0

    def move(self):
        dx = self.v * cos(self.ang)
        dy = self.v * sin(self.ang)
        self.canvas.move(self.rect, dx, 0)
        self.x1 += dx
        self.x2 += dx
        wall = check_entities_collision(self.canvas, self.rect, self.room.walls)
        if wall:
            if not self.targeted:
                self.ang = pi - self.ang
            enemy_coords = self.canvas.coords(self.rect)
            wall_coords = self.canvas.coords(wall.rect)
            if dx > 0:
                self.canvas.move(self.rect, wall_coords[0] - enemy_coords[2] - 1, 0)
                self.x1 += wall_coords[0] - enemy_coords[2] - 1
                self.x2 += wall_coords[0] - enemy_coords[2] - 1
            else:
                self.canvas.move(self.rect, wall_coords[2] - enemy_coords[0] + 1, 0)
                self.x1 += wall_coords[2] - enemy_coords[0] + 1
                self.x2 += wall_coords[2] - enemy_coords[0] + 1
        self.canvas.move(self.rect, 0, dy)
        self.y1 += dy
        self.y2 += dy
        wall = check_entities_collision(self.canvas, self.rect, self.room.walls)
        if wall:
            if not self.targeted:
                self.ang = -self.ang
            enemy_coords = self.canvas.coords(self.rect)
            wall_coords = self.canvas.coords(wall.rect)
            if dy > 0:
                self.canvas.move(self.rect, 0, wall_coords[1] - enemy_coords[3] - 1)        
                self.y1 += wall_coords[1] - enemy_coords[3] - 1
                self.y2 += wall_coords[1] - enemy_coords[3] - 1
            else:
                self.canvas.move(self.rect, 0, wall_coords[3] - enemy_coords[1] + 1)
                self.y1 += wall_coords[3] - enemy_coords[1] + 1
                self.y2 += wall_coords[3] - enemy_coords[1] + 1

    def behave(self, player):
        if self.calm:
            self.v = randint(1,2)
            self.ang = random() * 2 * pi
            self.calm = False
        player_coords = self.canvas.coords(player.rect)
        enemy_coords = self.canvas.coords(self.rect)
        if self.health_cooldown:
            self.health_cooldown += 1
            if self.health_cooldown >= 6:
                self.health_cooldown = 0
        if self.targeted: 
            self.ang = objects_angel(enemy_coords, player_coords)
            if objects_distance(player_coords, enemy_coords) >= 100:
                self.targeted = False
                self.v = randint(1,2)
            if self.is_shooting:
                self.room.bullets.append(Bullet(self.canvas, self.room, (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2, v = 6, ang = objects_angel(enemy_coords, player_coords) + random()*(1/10)-1/20))
                self.is_shooting = False
            else:
                self.shoot_cooldown += 1
                if self.shoot_cooldown >= 30:
                    self.is_shooting = True
                    self.shoot_cooldown = 0
        else:
            count = 0
            if objects_distance(player_coords, enemy_coords) <= 100:
                self.targeted = True
                self.v = randint(2,4)
                self.ang = objects_angel(enemy_coords, player_coords)
            else:
                if count % 30 == 0:
                    self.ang += random()*0.5 - 0.25 