import tkinter as tk
import random

class NQueensGUI:
    def __init__(self, master, size=8):
        self.master = master
        self.size = size
        self.cell_size = 60
        self.board = [random.randint(0, self.size - 1) for _ in range(self.size)]
        
        self.canvas = tk.Canvas(master, width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.canvas.pack()
        
        self.draw_board()
        self.place_queens()

        self.solve_button = tk.Button(master, text="Solve with Hill Climbing", command=self.hill_climbing)
        self.solve_button.pack()

    def draw_board(self):
        for row in range(self.size):
            for col in range(self.size):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * self.cell_size, row * self.cell_size,
                    (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                    fill=color
                )

    def place_queens(self):
        self.canvas.delete("queen")  
        for col, row in enumerate(self.board):
            self.canvas.create_oval(
                col * self.cell_size + 10, row * self.cell_size + 10,
                (col + 1) * self.cell_size - 10, (row + 1) * self.cell_size - 10,
                fill="red", tags="queen"
            )
    
    def attacking_pairs(self, board):
        pairs = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                    pairs += 1
        return pairs

    def get_neighbors(self):
        neighbors = []
        for col in range(self.size):
            for row in range(self.size):
                if row != self.board[col]:
                    neighbor = self.board[:]
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors

    def hill_climbing(self):
        restart_count = 0
        while True:
            current_cost = self.attacking_pairs(self.board)

            if current_cost == 0:
                self.place_queens()
                print(f"Solved with {restart_count} restarts!")
                break

            neighbors = self.get_neighbors()
            next_board = None
            next_cost = current_cost

            for neighbor in neighbors:
                cost = self.attacking_pairs(neighbor)
                if cost < next_cost:
                    next_board = neighbor
                    next_cost = cost

            if next_board is None or next_cost >= current_cost:
                self.board = [random.randint(0, self.size - 1) for _ in range(self.size)]
                restart_count += 1
                print(f"Restarting... Attempt {restart_count}")
            else:
                self.board = next_board  
                self.place_queens()  
                self.master.update()  

if __name__ == "__main__":
    root = tk.Tk()
    root.title("N-Queens Hill Climbing")
    
    game = NQueensGUI(root, size=8)  
    
    root.mainloop()
