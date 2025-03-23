from objects.Attack import Attack
from tools import check_entities_collision

class Player:
    def __init__(self, canvas, room, x, y): #image
        self.canvas = canvas
        self.room = room
        self.rect = canvas.create_rectangle(x-10,y-10,x+10,y+10, fill="cyan")
        #self.sprite = canvas.create_image(x,y, image = image)
        #self.image = image
        self.keys_pressed = set()
        self.health = 100
        self.dx = 0
        self.dy = 0
        self.move_top = False
        self.move_bottom = False
        self.move_right = False
        self.move_left = False
        self.can_attack = True
        self.attack_dir = ""
        self.attack_cooldown = 0

    def move(self):
        if self.attack_cooldown < 4 and self.attack_cooldown != 0:
            return
        if self.move_top != self.move_bottom:
            dy = -5 if self.move_top else 5
        else:
            dy = 0
        if self.move_left != self.move_right:
            dx = -5 if self.move_left else 5
        else:
            dx = 0
        if abs(dx) == abs(dy) and dx:
            dx = 3.5 if dx > 0 else -3.5
            dy = 3.5 if dy > 0 else -3.5
        self.canvas.move(self.rect, dx, 0)
        wall = check_entities_collision(self.canvas, self.rect, self.room.walls)
        if wall:
            obj_coords = self.canvas.coords(self.rect)
            wall_coords = self.canvas.coords(wall.rect)
            if dx > 0:
                self.canvas.move(self.rect, wall_coords[0] - obj_coords[2] - 1, 0)
            else:
                self.canvas.move(self.rect, wall_coords[2] - obj_coords[0] + 1, 0)
        self.canvas.move(self.rect, 0, dy)
        wall = check_entities_collision(self.canvas, self.rect, self.room.walls)
        if wall:
            obj_coords = self.canvas.coords(self.rect)
            wall_coords = self.canvas.coords(wall.rect)
            if dy > 0:
                self.canvas.move(self.rect, 0, wall_coords[1] - obj_coords[3] - 1)
            else:
                self.canvas.move(self.rect, 0, wall_coords[3] - obj_coords[1] + 1)

    def attack(self):
        if self.attack_dir:
            player_coords = self.canvas.coords(self.rect)
            if self.attack_dir == "up": 
                self.room.attacks.append(Attack(self.canvas, player_coords[0] - 2, player_coords[1], player_coords[2] + 2, player_coords[1] - 25))
            elif self.attack_dir == "down": 
                self.room.attacks.append(Attack(self.canvas, player_coords[0] - 2, player_coords[3] + 25, player_coords[2] + 2, player_coords[3]))
            elif self.attack_dir == "left": 
                self.room.attacks.append(Attack(self.canvas, player_coords[0] - 25, player_coords[1] - 2, player_coords[0], player_coords[3] + 2))
            else: 
                self.room.attacks.append(Attack(self.canvas, player_coords[2], player_coords[1] - 2, player_coords[2] + 25, player_coords[3] + 2))
        

    '''
    def update_sprite_position(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.canvas.coords(self.sprite, center_x, center_y)

    def remove_sprite(self):
        
    '''
