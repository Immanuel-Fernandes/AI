import tkinter as tk
from collections import deque

class WaterJugSolver:
    def __init__(self, root, m, n, d):
        self.root = root
        self.m = m
        self.n = n
        self.d = d

        self.current_state = (0, 0)
        self.visited = set()
        self.visited.add((0, 0))

        self.create_gui()
        self.selected_jug = None

    def create_gui(self):
        self.root.title("Water Jug Problem")
        self.root.geometry("500x500")
        self.root.configure(bg="light green")

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="light green")
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="Drag the jugs to move water.", font=("Arial", 16), bg="light green")
        self.status_label.pack()

        self.jug1 = self.canvas.create_rectangle(50, 50, 150, 250, outline="black", width=2)
        self.jug2 = self.canvas.create_rectangle(250, 50, 350, 250, outline="black", width=2)

        self.jug1_water = self.canvas.create_rectangle(50, 250, 150, 250, fill="light blue")
        self.jug2_water = self.canvas.create_rectangle(250, 250, 350, 250, fill="light blue")

        self.auto_solve_button = tk.Button(self.root, text="Auto Solve", command=self.auto_solve)
        self.auto_solve_button.pack()

        self.canvas.tag_bind(self.jug1, "<B1-Motion>", self.move_jug1)
        self.canvas.tag_bind(self.jug2, "<B1-Motion>", self.move_jug2)
        self.canvas.tag_bind(self.jug1, "<ButtonRelease-1>", self.release_jug)
        self.canvas.tag_bind(self.jug2, "<ButtonRelease-1>", self.release_jug)

        self.update_jugs(self.current_state)

    def is_valid_state(self, state):
        return 0 <= state[0] <= self.m and 0 <= state[1] <= self.n

    def get_next_states(self, state):
        next_states = []
        a, b = state

        # Fill jug1
        next_states.append((self.m, b))

        # Fill jug2
        next_states.append((a, self.n))

        # Empty jug1
        next_states.append((0, b))

        # Empty jug2
        next_states.append((a, 0))

        # Pour water from jug1 to jug2 until jug2 is full or jug1 is empty
        pour = min(a, self.n - b)
        next_states.append((a - pour, b + pour))

        # Pour water from jug2 to jug1 until jug1 is full or jug2 is empty
        pour = min(b, self.m - a)
        next_states.append((a + pour, b - pour))

        return next_states

    def update_jugs(self, state):
        a, b = state
        self.canvas.coords(self.jug1_water, 50, 250 - (a * 200 / self.m), 150, 250)
        self.canvas.coords(self.jug2_water, 250, 250 - (b * 200 / self.n), 350, 250)
        self.root.update()
        self.status_label.config(text=f"Current State: {state}")

    def move_jug1(self, event):
        if 1 <= event.x <= 30:
            self.current_state = (self.m, self.current_state[1])
        elif 60 <= event.x <= 90:
            self.current_state = (0, self.current_state[1])
        self.update_jugs(self.current_state)

    def move_jug2(self, event):
        if 1 <= event.x <= 30:
            self.current_state = (self.current_state[0], self.n)
        elif 60 <= event.x <= 90:
            self.current_state = (self.current_state[0], 0)
        self.update_jugs(self.current_state)

    def release_jug(self, event):
        if self.selected_jug is None:
            self.selected_jug = event.widget
        else:
            if self.selected_jug == self.jug1:
                self.transfer_water(1)
            else:
                self.transfer_water(2)
            self.selected_jug = None
        self.check_goal()

    def transfer_water(self, from_jug):
        if from_jug == 1 and self.current_state[0] > 0:
            pour = min(self.current_state[0], self.n - self.current_state[1])
            self.current_state = (self.current_state[0] - pour, self.current_state[1] + pour)
        elif from_jug == 2 and self.current_state[1] > 0:
            pour = min(self.current_state[1], self.m - self.current_state[0])
            self.current_state = (self.current_state[0] + pour, self.current_state[1] - pour)
        self.update_jugs(self.current_state)

    def auto_solve(self):
        self.queue = deque([(0, 0)])
        self.visited = set()
        self.visited.add((0, 0))
        self.root.after(500, self.solve)

    def solve(self):
        if not self.queue:
            self.status_label.config(text="No solution exists")
            return

        current_state = self.queue.popleft()
        self.update_jugs(current_state)

        if current_state[0] == self.d or current_state[1] == self.d:
            self.status_label.config(text=f"Solution found: {current_state}")
            return

        for next_state in self.get_next_states(current_state):
            if next_state not in self.visited and self.is_valid_state(next_state):
                self.visited.add(next_state)
                self.queue.append(next_state)

        self.root.after(500, self.solve)

    def check_goal(self):
        if self.current_state[0] == self.d or self.current_state[1] == self.d:
            self.status_label.config(text=f"Solution found: {self.current_state}")

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        self.create_input_gui()

    def create_input_gui(self):
        self.root.title("Water Jug Problem")
        self.root.geometry("300x200")
        self.root.configure(bg="light green")

        self.instructions = tk.Label(self.root, text="Enter the capacities and goal:", bg="light green")
        self.instructions.pack()

        self.jug1_label = tk.Label(self.root, text="Jug 1 Capacity:", bg="light green")
        self.jug1_label.pack()
        self.jug1_entry = tk.Entry(self.root)
        self.jug1_entry.pack()

        self.jug2_label = tk.Label(self.root, text="Jug 2 Capacity:", bg="light green")
        self.jug2_label.pack()
        self.jug2_entry = tk.Entry(self.root)
        self.jug2_entry.pack()

        self.goal_label = tk.Label(self.root, text="Goal Amount:", bg="light green")
        self.goal_label.pack()
        self.goal_entry = tk.Entry(self.root)
        self.goal_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_solver)
        self.start_button.pack()

    def start_solver(self):
        m = int(self.jug1_entry.get())
        n = int(self.jug2_entry.get())
        d = int(self.goal_entry.get())

        self.instructions.pack_forget()
        self.jug1_label.pack_forget()
        self.jug1_entry.pack_forget()
        self.jug2_label.pack_forget()
        self.jug2_entry.pack_forget()
        self.goal_label.pack_forget()
        self.goal_entry.pack_forget()
        self.start_button.pack_forget()

        WaterJugSolver(self.root, m, n, d)

def main():
    root = tk.Tk()
    WaterJugApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
