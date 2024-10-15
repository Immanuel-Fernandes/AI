import tkinter as tk
from collections import deque

class WaterJugSolver:
    def __init__(self, root, m, n, d):
        self.root = root
        self.m = m
        self.n = n
        self.d = d

        self.queue = deque([(0, 0)])
        self.visited = set([(0, 0)])

        self.create_gui()

    def create_gui(self):
        self.root.title("Water Jug Problem")
        self.root.geometry("400x400")
        self.root.configure(bg="light green")

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="light green")
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="Solving...", font=("Arial", 16), bg="light green")
        self.status_label.pack()

        self.jug1 = self.canvas.create_rectangle(50, 50, 150, 250, outline="black", width=2)
        self.jug2 = self.canvas.create_rectangle(250, 50, 350, 250, outline="black", width=2)
        
        self.jug1_water = self.canvas.create_rectangle(50, 250, 150, 250, fill="light blue")
        self.jug2_water = self.canvas.create_rectangle(250, 250, 350, 250, fill="light blue")

        self.solve()

    def is_valid_state(self, state):
        return 0 <= state[0] <= self.m and 0 <= state[1] <= self.n

    def get_next_states(self, state):
        a, b = state
        return [
            (self.m, b), (a, self.n), (0, b), (a, 0),
            (a - min(a, self.n - b), b + min(a, self.n - b)),
            (a + min(b, self.m - a), b - min(b, self.m - a))
        ]

    def update_jugs(self, state):
        a, b = state
        self.canvas.coords(self.jug1_water, 50, 250 - a * 200 / self.m, 150, 250)
        self.canvas.coords(self.jug2_water, 250, 250 - b * 200 / self.n, 350, 250)
        self.root.update()

    def solve(self):
        if not self.queue:
            self.status_label.config(text="No solution exists")
            return

        current_state = self.queue.popleft()
        self.update_jugs(current_state)
        self.status_label.config(text=f"Current State: {current_state}")

        if current_state[0] == self.d or current_state[1] == self.d:
            self.status_label.config(text=f"Solution found: {current_state}")
            return

        for next_state in self.get_next_states(current_state):
            if next_state not in self.visited and self.is_valid_state(next_state):
                self.visited.add(next_state)
                self.queue.append(next_state)

        self.root.after(500, self.solve)

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        self.create_input_gui()

    def create_input_gui(self):
        self.root.title("Water Jug Problem")
        self.root.geometry("300x200")
        self.root.configure(bg="light green")

        tk.Label(self.root, text="Enter the capacities and goal:", bg="light green").pack()
        self.jug1_entry = self.create_entry("Jug 1 Capacity:")
        self.jug2_entry = self.create_entry("Jug 2 Capacity:")
        self.goal_entry = self.create_entry("Goal Amount:")

        tk.Button(self.root, text="Start", command=self.start_solver).pack()

    def create_entry(self, label_text):
        tk.Label(self.root, text=label_text, bg="light green").pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    def start_solver(self):
        m = int(self.jug1_entry.get())
        n = int(self.jug2_entry.get())
        d = int(self.goal_entry.get())

        for widget in self.root.winfo_children():
            widget.pack_forget()

        WaterJugSolver(self.root, m, n, d)

def main():
    root = tk.Tk()
    WaterJugApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
