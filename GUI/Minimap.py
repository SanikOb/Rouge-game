from tkinter import Canvas

class Minimap:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.canvas = Canvas(self.root, width=150, height=150, bg="black")
        self.canvas.pack(side="left")
        self.rooms = []
        for i in range(size):
            for j in range(size):
                self.rooms.append(self.canvas.create_rectangle(j * (150 / size), i * (150 / size), (j + 1) * (150 / size), (i + 1) * (150 / size), fill="black"))
        self.player = self.canvas.create_rectangle(70, 70, 80, 80, fill="cyan")

    def show_room(self, room_index):
        self.canvas.itemconfig(self.rooms[room_index], fill="grey") 

    def change_current_room(self, room_index):
        x = room_index % self.size
        y = room_index // self.size
        self.canvas.coords(self.player, 150 / self.size * x + 5, 150 / self.size * y + 5, 150 / self.size * (x + 1) - 5, 150 / self.size * (y + 1) - 5)
