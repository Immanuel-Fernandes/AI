import tkinter as tk
from tkinter import ttk
from heapq import heappush, heappop
from PIL import Image, ImageTk

class AStarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Game")
        
        self.start = (0, 0)
        self.goal = (4, 4)
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="lightblue")
        self.canvas.pack(side=tk.LEFT)        
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(self.controls_frame, text="Grid Size:").pack()
        self.grid_size_var = tk.StringVar(value="3x3")
        self.grid_size_dropdown = ttk.Combobox(self.controls_frame, textvariable=self.grid_size_var)
        self.grid_size_dropdown['values'] = ["3x3", "5x5", "10x10", "15x15", "20x20", "25x25", "30x30"]
        self.grid_size_dropdown.pack()
        self.grid_size_dropdown.bind("<<ComboboxSelected>>", self.update_grid_size)

        self.find_path_button = tk.Button(self.controls_frame, text="Find Path", command=self.find_path)
        self.find_path_button.pack(pady=20)
        
        self.dog_image = ImageTk.PhotoImage(Image.open("dog.png").resize((15, 15), Image.LANCZOS))
        self.food_image = ImageTk.PhotoImage(Image.open("food.png").resize((15, 15), Image.LANCZOS))
        self.update_grid_size()        
        self.canvas.bind("<Button-1>", self.toggle_wall)

    def update_grid_size(self, event=None):
        size_str = self.grid_size_var.get()
        rows, cols = map(int, size_str.split('x'))
        self.rows, self.cols = rows, cols
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.goal = (self.rows - 1, self.cols - 1)
        self.grid_size = min(300 // self.rows, 300 // self.cols)
        self.dog_image = ImageTk.PhotoImage(Image.open("dog.png").resize((self.grid_size, self.grid_size), Image.LANCZOS))
        self.food_image = ImageTk.PhotoImage(Image.open("food.png").resize((self.grid_size, self.grid_size), Image.LANCZOS))
        
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white"
                if (i, j) == self.start:
                    self.canvas.create_image(j * self.grid_size, i * self.grid_size, anchor=tk.NW, image=self.dog_image)
                elif (i, j) == self.goal:
                    self.canvas.create_image(j * self.grid_size, i * self.grid_size, anchor=tk.NW, image=self.food_image)
                elif self.grid[i][j] == 1:  
                    color = "lightcyan"
                    self.canvas.create_rectangle(j * self.grid_size, i * self.grid_size,
                                                 (j + 1) * self.grid_size, (i + 1) * self.grid_size,
                                                 fill=color, outline="lightseagreen")
                else:  
                    self.canvas.create_rectangle(j * self.grid_size, i * self.grid_size,
                                                 (j + 1) * self.grid_size, (i + 1) * self.grid_size,
                                                 fill="lightsteelblue", outline="lightgrey")

    def toggle_wall(self, event):
        x, y = event.x // self.grid_size, event.y // self.grid_size
        if 0 <= y < self.rows and 0 <= x < self.cols and (x, y) != self.start and (x, y) != self.goal:
            self.grid[y][x] = 1 - self.grid[y][x]
            self.draw_grid()

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        self.path = []
        open_set = []
        heappush(open_set, (0, self.start))
        came_from = {}

        g_score = { (i, j): float('inf') for i in range(self.rows) for j in range(self.cols) }
        g_score[self.start] = 0
        
        f_score = { (i, j): float('inf') for i in range(self.rows) for j in range(self.cols) }
        f_score[self.start] = self.heuristic(self.start, self.goal)

        while open_set:
            _, current = heappop(open_set)

            if current == self.goal:
                while current in came_from:
                    self.path.append(current)
                    current = came_from[current]
                self.path.append(self.start)
                self.path.reverse()
                self.draw_path()
                return

            neighbors = [(current[0] + i, current[1] + j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0]

            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))

    def draw_path(self):
        for (x, y) in self.path:
            if (x, y) == self.start or (x, y) == self.goal:
                continue
            self.canvas.create_rectangle(y * self.grid_size, x * self.grid_size,
                                         (y + 1) * self.grid_size, (x + 1) * self.grid_size,
                                         fill="lightblue", outline="lightsteelblue")

root = tk.Tk()
app = AStarApp(root)
root.mainloop()
