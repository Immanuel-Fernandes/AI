import tkinter as tk
from tkinter import Canvas, simpledialog

class HanoiGUI:
    def __init__(self, root, numDisks):
        self.root = root
        self.numDisks = numDisks
        self.disk_height = 20
        self.poles = [[], [], []]
        self.selected_disk = None
        self.selected_pole = None
        self.moves = 0
        self.min_moves = (2 ** numDisks) - 1

        self.canvas = Canvas(root, width=600, height=300, bg="light blue")
        self.canvas.pack()
        self.move_counter = tk.Label(root, text="Moves: 0", font=("Helvetica", 16))
        self.move_counter.pack()
        self.min_move_label = tk.Label(root, text=f"Minimum Moves: {self.min_moves}", font=("Helvetica", 16))
        self.min_move_label.pack()

        self.canvas.create_line(100, 80, 100, 300, width=15)
        self.canvas.create_line(300, 80, 300, 300, width=15)
        self.canvas.create_line(500, 80, 500, 300, width=15)

        self.setupDisks(numDisks)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def setupDisks(self, numDisks):
        for i in range(numDisks, 0, -1):
            width = i * 30
            x1, y1, x2, y2 = self.getDiskCoords(width, 0)
            disk = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="disk")
            self.poles[0].append((disk, width))

    def getDiskCoords(self, width, pole):
        x_center = 100 + 200 * pole
        y_base = 300 - self.disk_height * len(self.poles[pole])
        x1 = x_center - width // 2
        y1 = y_base - self.disk_height
        x2 = x_center + width // 2
        y2 = y_base
        return (x1, y1, x2, y2)

    def on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if "disk" in self.canvas.gettags(item):
            for pole in range(3):
                if self.poles[pole] and self.poles[pole][-1][0] == item[0]:
                    self.selected_disk = self.poles[pole].pop()
                    self.selected_pole = pole
                    self.canvas.tag_raise(self.selected_disk[0])
                    break

    def on_drag(self, event):
        if self.selected_disk:
            self.canvas.coords(self.selected_disk[0], event.x - self.selected_disk[1] // 2, event.y - self.disk_height // 2, event.x + self.selected_disk[1] // 2, event.y + self.disk_height // 2)

    def on_drop(self, event):
        if self.selected_disk:
            closest_pole = min(range(3), key=lambda i: abs(event.x - (100 + 200 * i)))
            if not self.poles[closest_pole] or self.poles[closest_pole][-1][1] > self.selected_disk[1]:
                self.poles[closest_pole].append(self.selected_disk)
                self.canvas.coords(self.selected_disk[0], self.getDiskCoords(self.selected_disk[1], closest_pole))
                self.moves += 1
                self.update_move_counter()
            else:
                self.poles[self.selected_pole].append(self.selected_disk)
                self.canvas.coords(self.selected_disk[0], self.getDiskCoords(self.selected_disk[1], self.selected_pole))
            self.selected_disk = None
            self.selected_pole = None

    def update_move_counter(self):
        self.move_counter.config(text=f"Moves: {self.moves}")

def get_num_disks():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    num_disks = simpledialog.askinteger("Input", "Enter the number of disks:", minvalue=2, maxvalue=6)
    root.destroy()
    return num_disks

numDisks = get_num_disks()
if numDisks:
    root = tk.Tk()
    root.title("Tower of Hanoi")
    HanoiGUI(root, numDisks)
    root.mainloop()