import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class AOStarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AO* Game")
        self.start = (0, 0)
        self.goal = (4, 4)
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="lightblue")
        self.canvas.pack(side=tk.LEFT)
        
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        tk.Label(self.controls_frame, text="Grid Size:").pack()
        self.grid_size_var = tk.StringVar(value="5x5")
        self.grid_size_dropdown = ttk.Combobox(self.controls_frame, textvariable=self.grid_size_var)
        self.grid_size_dropdown['values'] = ["5x5", "10x10", "15x15", "20x20"]
        self.grid_size_dropdown.pack()
        self.grid_size_dropdown.bind("<<ComboboxSelected>>", self.update_grid_size)
        
        self.find_path_button = tk.Button(self.controls_frame, text="Find Path", command=self.start_pathfinding)
        self.find_path_button.pack(pady=20)
        
        self.police_image = ImageTk.PhotoImage(Image.open("Car.png").resize((10, 10), Image.LANCZOS))
        self.thief_image = ImageTk.PhotoImage(Image.open("House.png").resize((10, 10), Image.LANCZOS))
        
        self.update_grid_size()
        self.canvas.bind("<Button-1>", self.toggle_wall)

    def update_grid_size(self, event=None):
        size_str = self.grid_size_var.get()
        rows, cols = map(int, size_str.split('x'))
        self.rows, self.cols = rows, cols
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.goal = (self.rows - 1, self.cols - 1)
        self.grid_size = min(300 // self.rows, 300 // self.cols)
        self.police_image = ImageTk.PhotoImage(Image.open("Car.png").resize((self.grid_size, self.grid_size), Image.LANCZOS))
        self.thief_image = ImageTk.PhotoImage(Image.open("House.png").resize((self.grid_size, self.grid_size), Image.LANCZOS))
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) == self.start:
                    self.canvas.create_image(j * self.grid_size, i * self.grid_size, anchor=tk.NW, image=self.police_image)
                elif (i, j) == self.goal:
                    self.canvas.create_image(j * self.grid_size, i * self.grid_size, anchor=tk.NW, image=self.thief_image)
                elif self.grid[i][j] == 1:
                    self.canvas.create_rectangle(
                        j * self.grid_size, i * self.grid_size,
                        (j + 1) * self.grid_size, (i + 1) * self.grid_size,
                        fill="lightgreen", outline="darkgreen"  
                    )
                else:
                    self.canvas.create_rectangle(
                        j * self.grid_size, i * self.grid_size,
                        (j + 1) * self.grid_size, (i + 1) * self.grid_size,
                        fill="lightblue", outline="blue"  
                    )

    def toggle_wall(self, event):
        x, y = event.x // self.grid_size, event.y // self.grid_size
        if 0 <= y < self.rows and 0 <= x < self.cols and (x, y) != self.start and (x, y) != self.goal:
            self.grid[y][x] = 1 - self.grid[y][x]
            self.draw_grid()

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def start_pathfinding(self):
        self.open_set = [(self.start, [])]
        self.visited = set()
        self.path = None
        self.find_path_step()

    def find_path_step(self):
        if not self.open_set:
            return
        
        current, path = self.open_set.pop(0)
        
        if current == self.goal:
            self.path = path + [current]
            self.draw_path()
            return
        
        if current in self.visited:
            self.root.after(100, self.find_path_step)
            return
        
        self.visited.add(current)
        neighbors = [(current[0] + i, current[1] + j) for i, j in [(-1,0), (1,0), (0,-1), (0,1)]]
        neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0]
        
        for neighbor in neighbors:
            self.open_set.append((neighbor, path + [current]))

        if current != self.start and current != self.goal:
            self.canvas.create_rectangle(
                current[1] * self.grid_size, current[0] * self.grid_size,
                (current[1] + 1) * self.grid_size, (current[0] + 1) * self.grid_size,
                fill="seagreen", outline="darkolivegreen"  
            )
        
        self.root.after(100, self.find_path_step)

    def draw_path(self):
        for (x, y) in self.path:
            if (x, y) == self.start or (x, y) == self.goal:
                continue
            self.canvas.create_rectangle(
                y * self.grid_size, x * self.grid_size,
                (y + 1) * self.grid_size, (x + 1) * self.grid_size,
                fill="black", outline="lightgreen"  
            )

root = tk.Tk()
app = AOStarApp(root)
root.mainloop()
