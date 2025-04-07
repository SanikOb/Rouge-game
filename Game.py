import tkinter as tk
from random import randint, choice
from checkers import *

from GUI.Minimap import Minimap

from entities.Player import Player

from rooms.room_list import room_list

from PIL import Image, ImageTk, ImageFilter


class Game:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, width=600, height=150)
        self.canvas_int = tk.Canvas(self.frame, width=450, height=150, bg="grey")
        self.canvas_map = Minimap(self.frame, 8)
        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas_int.pack(side="right")
        self.frame.pack()
        self.canvas.pack()

        self.rooms = [0 for i in range(64)]
        self.map, self.room_index = self.generate_map(15)
        self.generate_rooms(self.map)
        self.room = self.rooms[self.room_index]
        self.render_room(self.room)
        self.explore_room()
        self.canvas_map.change_current_room(self.room_index)
        
        #img = Image.open("sprytes/player.png").resize((50,50), Image.Resampling.LANCZOS)
        #img = img.rotate(90) // img.crop((100,100,110,110)) // img.filter(ImageFilter.BoxBlur(5))
        #self.player_image = ImageTk.PhotoImage(img)

        self.player = Player(self.canvas, self.room, 300, 300) #self.player_image)
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

    def generate_map(self, n):
            map = [0 for i in range(64)]
            i = randint(0, 63)
            map[i] = 1
            k = i
            for j in range(n - 1):
                while True:
                    c = [-8, -1, 1, 8]
                    if k % 8 == 0:
                        c.remove(-1)
                    if k % 8 == 7:
                        c.remove(1)
                    if k > 55:
                        c.remove(8)
                    if k < 8:
                        c.remove(-8)
                    k += choice(c)
                    if not map[k]:
                        break
                map[k] = 1   
            return(map, i)
        
    def generate_rooms(self, map):
        for i in range(64):
            if map[i]:
                string = ''
                for j in [-8, -1, 1, 8]:
                    try:
                        string += str(map[i + j])
                    except:
                        string += '0'
                result = int(string, 2)
                self.rooms[i] = choice([room for room in room_list if room.type == result])

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

    def explore_room(self):
        room_index = self.room_index
        if not self.room.explored:
            self.canvas_map.show_room(room_index)
            for i in [-8, -1, 1, 8]:
                if (room_index % 8 == 0 and i == -1) or (room_index % 8 == 7 and i == 1): continue
                try:
                    if self.rooms[room_index + i]:
                        self.canvas_map.show_room(room_index + i)
                except: pass

    def render_room(self, room):
        for wall in room.walls:
            wall.rect = self.canvas.create_rectangle(wall.x1, wall.y1, wall.x2, wall.y2, fill="grey", outline="grey")
        for enemy in room.enemies:
            enemy.rect = self.canvas.create_rectangle(enemy.x1, enemy.y1, enemy.x2, enemy.y2, fill="red")
        for healthpack in room.healthpacks:
            healthpack.rect = self.canvas.create_rectangle(healthpack.x1, healthpack.y1, healthpack.x2, healthpack.y2, fill = "green", outline = "green")

    def update_game(self):
        if self.game_on:
            self.player.update()
            check_healthpacks_collision(self)
            self.enemy_update()
            check_enemy_collision(self)
            self.bullet_update()
            check_bullet_collision(self)
            self.attacks_update()
            if check_room_change(self):
                self.canvas_map.change_current_room(self.room_index)
                self.explore_room()
            self.root.after(16, self.update_game)