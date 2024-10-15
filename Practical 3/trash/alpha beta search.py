import tkinter as tk
from tkinter import messagebox

tree = [[[5, 1, 2], [8, -8, -9]], [[9, 4, 5], [-3, 4, 3]]]
root = 0
pruned = 0

def children(branch, depth, alpha, beta):
    global pruned
    i = 0
    for child in branch:
        if isinstance(child, list):
            (nalpha, nbeta) = children(child, depth + 1, alpha, beta)
            if depth % 2 == 1:
                beta = min(nalpha, beta)
            else:
                alpha = max(nbeta, alpha)
            branch[i] = alpha if depth % 2 == 0 else beta
            i += 1
        else:
            if depth % 2 == 0 and alpha < child:
                alpha = child
            if depth % 2 == 1 and beta > child:
                beta = child
        if alpha >= beta:
            pruned += 1
            break
    return (alpha, beta)

def run_alpha_beta():
    global pruned
    global root
    alpha = float('-inf')
    beta = float('inf')
    (alpha, beta) = children(tree, root, alpha, beta)
    
    result_str = f"(alpha, beta): ({alpha}, {beta})\n"
    result_str += f"Result: {tree}\n"
    result_str += f"Times pruned: {pruned}"
    messagebox.showinfo("Alpha-Beta Result", result_str)

def create_gui():
    root = tk.Tk()
    root.title("Alpha-Beta Pruning Game")

    tk.Label(root, text="Alpha-Beta Pruning", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Run Alpha-Beta", command=run_alpha_beta, font=("Helvetica", 14)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
