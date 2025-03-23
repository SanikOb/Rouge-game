import tkinter as tk
from objects.Room import Room
from math import *
from random import *
from tools import check_entities_collision

from objects.Wall import Wall
from objects.Healthpack import Healthpack
from objects.Attack import Attack

from entities.Bullet import Bullet
from entities.Player import Player
from entities.Enemy import Enemy

from entities.enemies.Bat import Bat
from entities.enemies.Tryclop import Tryclop

from PIL import Image, ImageTk, ImageFilter


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas_int = tk.Canvas(root, width = 600, height = 150, bg = "grey")
        self.canvas_int.pack()
        self.canvas = tk.Canvas(root, width = 600, height = 600, bg = "black")
        self.canvas.pack()

        self.room_list = [
            Room([-1,-1,1,1],
            [
                Wall(self.canvas, 0, 0, 600, 50),
                Wall(self.canvas, 0, 0, 50, 275),
                Wall(self.canvas, 0, 325, 50, 600),
                Wall(self.canvas, 0, 550, 600, 600),
                Wall(self.canvas, 550, 0, 600, 275),
                Wall(self.canvas, 550, 325, 600, 600),

                Wall(self.canvas, 100, 100, 200, 350),
                Wall(self.canvas, 200, 100, 350, 250),
                Wall(self.canvas, 250, 300, 350, 400),
                Wall(self.canvas, 400, 50, 500, 350),
                Wall(self.canvas, 100, 400, 500, 500),
                Wall(self.canvas, 50, 400, 100, 450),

                Wall(self.canvas, -50, 275, 0, 325),
                Wall(self.canvas, 600, 275, 650, 325)
            ],
            [
                Healthpack(self.canvas, 520, 300)
            ]),
            Room([-1,-1, 0, 0],
            [
                Wall(self.canvas, 0, 0, 600, 50),
                Wall(self.canvas, 0, 0, 50, 275),
                Wall(self.canvas, 0, 325, 50, 600),
                Wall(self.canvas, 0, 550, 600, 600),
                Wall(self.canvas, 550, 0, 600, 275),
                Wall(self.canvas, 550, 325, 600, 600),

                Wall(self.canvas, -50, 275, 0, 325),
                Wall(self.canvas, 600, 275, 650, 325)
            ],
            [
                Healthpack(self.canvas, 520, 300)
            ])
        ]

        
        self.room_list[0].enemies.append(choice([Enemy(self.canvas, self.room_list[0], 80, 150), Bat(self.canvas, self.room_list[0], 80, 150)]))
        self.room_list[0].enemies.append(choice([Enemy(self.canvas, self.room_list[0], 370, 350), Bat(self.canvas, self.room_list[0], 370, 350)]))
        self.room_list[0].enemies.append(choice([Enemy(self.canvas, self.room_list[0], 450, 380), Bat(self.canvas, self.room_list[0], 450, 380)]))

        self.room_list[1].enemies.append(Tryclop(self.canvas, self.room_list[1], 300, 300))
        

        self.room = self.room_list[0]

        self.render_room(self.room)
        
        #img = Image.open("sprytes/player.png").resize((50,50), Image.Resampling.LANCZOS)
        #img = img.rotate(90) // img.crop((100,100,110,110)) // img.filter(ImageFilter.BoxBlur(5))
        #self.player_image = ImageTk.PhotoImage(img)

        self.player = Player(self.canvas, self.room, 20, 300) #self.player_image)
        self.health_bar = self.canvas_int.create_text(300, 50, text=f"Здоровье: {self.player.health}", font =("Arial", 14), fill="black") 

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        self.game_on = True
        self.update_game()    

    def key_press(self, event):
        key = event.keysym.lower()
        if key in ("w","a","s","d","up","left","right","down"):
            self.player.keys_pressed.add(key)

    def key_release(self, event):
        key = event.keysym.lower()
        if key in ("w","a","s","d","up","left","right","down"):
            self.player.keys_pressed.discard(key)

    def game_over(self):
        self.canvas_int.create_text(300, 70, text="Зачет у Аллы Григорьевны", font =("Arial",14), fill="red")
        self.canvas_int.itemconfig(self.health_bar, text= f"Здоровье: 0")
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")
        self.game_on = False    

    def check_healthpacks_collision(self):
        healthpack = check_entities_collision(self.canvas, self.player.rect, self.room.healthpacks)
        if healthpack:
            self.player.health = 100
            self.canvas_int.itemconfig(self.health_bar, text= f"Здоровье: {self.player.health}")
            self.room.healthpacks.remove(healthpack)
            self.canvas.delete(healthpack.rect)
    
    def check_bullet_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        for bullet in self.room.bullets:
            bullet_coords =  self.canvas.coords(bullet.oval)
            if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
                player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
                if self.player.health - 20 <= 0:
                    self.game_over()
                else:
                    self.player.health -= 20
                    self.canvas_int.itemconfig(self.health_bar, text= f"Здоровье: {self.player.health}")
                self.room.bullets.remove(bullet)
                self.canvas.delete(bullet.oval)
                return
            if not bullet.deflect and check_entities_collision(self.canvas, bullet.oval, self.room.attacks):
                bullet.deflect = True
                bullet.ang = bullet.ang + pi 
            if bullet.deflect:
                enemy = check_entities_collision(self.canvas, bullet.oval, self.room.enemies)
                if enemy:
                    self.room.bullets.remove(bullet)
                    self.canvas.delete(bullet.oval)
                    self.room.enemies.remove(enemy)
                    self.canvas.delete(enemy.rect)

    def check_enemy_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.room.enemies:
            enemy_coords =  self.canvas.coords(enemy.rect)
            if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
                player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
                if self.player.health - 1 <= 0:
                    self.game_over()
                else:
                    self.player.health -= 1
                    self.canvas_int.itemconfig(self.health_bar, text= f"Здоровье: {self.player.health}")
            if check_entities_collision(self.canvas, enemy.rect, self.room.attacks) and not enemy.health_cooldown:
                enemy.health -= 50
                enemy.health_cooldown += 1
                if enemy.health <= 0:
                    self.room.enemies.remove(enemy)
                    self.canvas.delete(enemy.rect)
        

    def player_update(self):
        player = self.player
        for key in player.keys_pressed:
                if key == "w":
                    player.move_top = True
                elif key == "s":
                    player.move_bottom = True
                elif key == "a":
                    player.move_left = True
                elif key == "d":
                    player.move_right = True
                elif key == "up" and player.can_attack:
                    player.attack_dir = key
                    player.can_attack = False
                elif key == "down" and player.can_attack:
                    player.attack_dir = key
                    player.can_attack = False
                elif key == "left" and player.can_attack:
                    player.attack_dir = key
                    player.can_attack = False
                elif key == "right" and player.can_attack:
                    player.attack_dir = key
                    player.can_attack = False
        player.move()
        player.attack()
        player.move_top = False
        player.move_bottom = False
        player.move_left = False
        player.move_right = False
        player.attack_dir = ""
        if not player.can_attack:
            player.attack_cooldown += 1
            if player.attack_cooldown >= 20:
                player.can_attack = True
                player.attack_cooldown = 0

    def enemy_update(self):
        for enemy in self.room.enemies:
            enemy.behave(self.player)
            enemy.move()

    def bullet_update(self):
        for bullet in self.room.bullets:
            bullet.move()

    def attacks_update(self):
        for attack in self.room.attacks:
            attack.timer += 1
            if attack.timer >= 5:
                self.room.attacks.remove(attack)
                self.canvas.delete(attack.rect)


    def clear_room(self, room):
        for wall in room.walls:
            self.canvas.delete(wall.rect)
        for enemy in room.enemies:
            self.canvas.delete(enemy.rect) 
        for healthpack in room.healthpacks:
            self.canvas.delete(healthpack.rect) 
        for bullet in room.bullets:
            self.canvas.delete(bullet.oval)
            self.room.bullets.remove(bullet)
        self.canvas.create_rectangle(0, 0, 600, 600, fill="black")

    def render_room(self, room):
        for wall in room.walls:
            wall.rect = self.canvas.create_rectangle(wall.x1, wall.y1, wall.x2, wall.y2, fill="grey", outline="grey")
        for enemy in room.enemies:
            enemy.rect = self.canvas.create_rectangle(enemy.x1, enemy.y1, enemy.x2, enemy.y2, fill="red")
        for healthpack in room.healthpacks:
            healthpack.rect = self.canvas.create_rectangle(healthpack.x1, healthpack.y1, healthpack.x2, healthpack.y2, fill = "green", outline = "green")

    def check_room_change(self):
        player = self.player
        player_coords = self.canvas.coords(player.rect)
        if player_coords[1] <= 0:
            self.clear_room(self.room)
            self.room = self.room_list[self.room.doors[0]]
            self.render_room(self.room)
            player.room = self.room
            player.rect = self.canvas.create_rectangle(290, 570, 310, 590, fill="cyan")
        if player_coords[3] >= 599:
            self.clear_room(self.room)
            self.room = self.room_list[self.room.doors[1]]
            self.render_room(self.room)
            player.room = self.room
            player.rect = self.canvas.create_rectangle(290, 10, 310, 590, fill="cyan")
        if player_coords[0] <= 1:
            self.clear_room(self.room)
            self.room = self.room_list[self.room.doors[2]]
            self.render_room(self.room)
            player.room = self.room
            player.rect = self.canvas.create_rectangle(570, 290, 590, 310, fill="cyan")
        if player_coords[2] >= 599:
            self.clear_room(self.room)
            self.room = self.room_list[self.room.doors[3]]
            self.render_room(self.room)
            player.room = self.room
            player.rect = self.canvas.create_rectangle(10, 290, 30, 310, fill="cyan")
    
    def update_game(self):
        if self.game_on:
            self.player_update()
            self.check_healthpacks_collision()
            self.enemy_update()
            self.check_enemy_collision()
            self.bullet_update()
            self.check_bullet_collision()
            self.attacks_update()
            self.check_room_change()
            self.root.after(16, self.update_game)