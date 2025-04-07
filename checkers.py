from tools import check_entities_collision
from math import pi

def check_healthpacks_collision(game):
    healthpack = check_entities_collision(game.canvas, game.player.rect, game.room.healthpacks)
    if healthpack:
        game.player.health = 100
        game.canvas_int.itemconfig(game.health_bar, text= f"Здоровье: {game.player.health}")
        game.room.healthpacks.remove(healthpack)
        game.canvas.delete(healthpack.rect)
    
def check_bullet_collision(game):
    player_coords = game.canvas.coords(game.player.rect)
    for bullet in game.room.bullets:
        bullet_coords =  game.canvas.coords(bullet.oval)
        if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
            player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
            if game.player.health - 20 <= 0:
                game.game_over()
            else:
                game.player.health -= 20
                game.canvas_int.itemconfig(game.health_bar, text= f"Здоровье: {game.player.health}")
            game.room.bullets.remove(bullet)
            game.canvas.delete(bullet.oval)
            return
        if not bullet.deflect and check_entities_collision(game.canvas, bullet.oval, game.room.attacks):
            bullet.deflect = True
            bullet.ang = bullet.ang + pi 
        if bullet.deflect:
            enemy = check_entities_collision(game.canvas, bullet.oval, game.room.enemies)
            if enemy:
                game.room.bullets.remove(bullet)
                game.canvas.delete(bullet.oval)
                game.room.enemies.remove(enemy)
                game.canvas.delete(enemy.rect)

def check_enemy_collision(game):
    player_coords = game.canvas.coords(game.player.rect)
    for enemy in game.room.enemies:
        enemy_coords =  game.canvas.coords(enemy.rect)
        if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
            player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
            if game.player.health - 1 <= 0:
                game.game_over()
            else:
                game.player.health -= 1
                game.canvas_int.itemconfig(game.health_bar, text= f"Здоровье: {game.player.health}")
        if check_entities_collision(game.canvas, enemy.rect, game.room.attacks) and not enemy.health_cooldown:
            enemy.health -= 50
            enemy.health_cooldown += 1
            if enemy.health <= 0:
                game.room.enemies.remove(enemy)
                game.canvas.delete(enemy.rect)

def check_room_change(game):
        player = game.player
        player_coords = game.canvas.coords(player.rect)
        if player_coords[1] <= 1:
            room_change(game, -8)
            player.rect = game.canvas.create_rectangle(290, 570, 310, 590, fill="cyan")
            return True
        if player_coords[3] >= 599:
            room_change(game, 8)
            player.rect = game.canvas.create_rectangle(290, 10, 310, 30, fill="cyan")
            return True
        if player_coords[0] <= 1:
            room_change(game, -1)
            player.rect = game.canvas.create_rectangle(570, 290, 590, 310, fill="cyan")
            return True
        if player_coords[2] >= 599:
            room_change(game, 1)
            player.rect = game.canvas.create_rectangle(10, 290, 30, 310, fill="cyan")
            return True
        return False

def room_change(game, i):
    game.clear_room(game.room)
    game.room = game.rooms[game.room_index + i]
    game.render_room(game.room)
    game.room_index = game.room_index + i
    game.player.room = game.room
    