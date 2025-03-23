from entities.Enemy import *

class Bat(Enemy):
    def move(self):
        dx = self.v * cos(self.ang)
        dy = self.v * sin(self.ang)
        self.canvas.move(self.rect, dx, 0)
        self.x1 += dx
        self.x2 += dx
        if self.canvas.coords(self.rect)[0] < 0:
            if not self.targeted:
                self.ang = pi - self.ang
            self.canvas.move(self.rect, - self.canvas.coords(self.rect)[0], 0)
            self.x1 += - self.canvas.coords(self.rect)[0]
            self.x2 += - self.canvas.coords(self.rect)[0]
        elif self.canvas.coords(self.rect)[2] > 600:
            if not self.targeted:
                self.ang = pi - self.ang
            self.canvas.move(self.rect, 600 - self.canvas.coords(self.rect)[2], 0)
            self.x1 += 600 - self.canvas.coords(self.rect)[2]
            self.x2 += 600 - self.canvas.coords(self.rect)[2]
        self.canvas.move(self.rect, 0, dy)
        self.y1 += dy
        self.y2 += dy
        if self.canvas.coords(self.rect)[1] < 0:
            if not self.targeted:
                self.ang = - self.ang
            self.canvas.move(self.rect, 0, - self.canvas.coords(self.rect)[1])
            self.y1 += - self.canvas.coords(self.rect)[1]
            self.y2 += - self.canvas.coords(self.rect)[1]
        elif self.canvas.coords(self.rect)[3] > 600:
            if not self.targeted:
                self.ang = - self.ang
            self.canvas.move(self.rect, 0, 600 - self.canvas.coords(self.rect)[3])
            self.y1 +=  600 - self.canvas.coords(self.rect)[3]
            self.y2 +=  600 - self.canvas.coords(self.rect)[3]


    def behave(self, player):
        if self.calm:
            self.v = randint(1,2)
            self.ang = random() * 2 * pi
            self.calm = False
        player_coords = self.canvas.coords(player.rect)
        enemy_coords = self.canvas.coords(self.rect)
        if self.targeted: 
            self.ang = objects_angel(enemy_coords, player_coords)
            if objects_distance(player_coords, enemy_coords) >= 200:
                self.targeted = False
                self.v = randint(1,2)
        else:
            count = 0
            if objects_distance(player_coords, enemy_coords) <= 100:
                self.targeted = True
                self.v = randint(3,6)
                self.ang = objects_angel(enemy_coords, player_coords)
            else:
                if count % 30 == 0:
                    self.ang += random()*0.5 - 0.25 