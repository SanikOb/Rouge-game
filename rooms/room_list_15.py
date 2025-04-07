from Room import Room
from ..objects.Wall import Wall
from ..objects.Healthpack import Healthpack
from ..entities.enemies.Bat import Bat
from ..entities.enemies.Tryclop import Tryclop

room_list_15 = [
            Room(
            [
                Wall(0, 0, 275, 50),
                Wall(325, 0, 600, 50),
                Wall(550, 50, 600, 275),
                Wall(550, 325, 600, 600),
                Wall(0, 50, 50, 275),
                Wall(0, 325, 50, 600),
                Wall(50, 550, 275, 600),
                Wall(325, 550, 550, 600),

                Wall(275, -50, 325, 0),
                Wall(-50, 275, 0, 325),
                Wall(600, 275, 650, 325),
                Wall(275, 600, 325, 650)
            ],
            [], 15),

            Room(
            [
                Wall(0, 0, 275, 50),
                Wall(325, 0, 600, 50),
                Wall(550, 50, 600, 275),
                Wall(550, 325, 600, 600),
                Wall(0, 50, 50, 275),
                Wall(0, 325, 50, 600),
                Wall(50, 550, 275, 600),
                Wall(325, 550, 550, 600),

                Wall(275, -50, 325, 0),
                Wall(-50, 275, 0, 325),
                Wall(600, 275, 650, 325),
                Wall(275, 600, 325, 650),

                Wall(50, 50, 300, 300),
                Wall(350, 50, 550, 350),
                Wall(50, 350, 350, 550),
                Wall(350, 350, 550, 50)

            ],
            [], 15)
            ]
