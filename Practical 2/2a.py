import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

def get_N():
    root = tk.Tk()
    root.withdraw()  
    N = simpledialog.askinteger("Input", "Enter the number of Tiles:", minvalue=2, maxvalue=6)
    root.destroy()
    return N

N = get_N()
#N = 4 
root = tk.Tk()
root.title("4/N-Queen Game")
black_sq = Image.open("Black_sq.png")
white_sq = Image.open("White_sq.png")
queen = Image.open("Queen.png")
black_sq_img = ImageTk.PhotoImage(black_sq)
white_sq_img = ImageTk.PhotoImage(white_sq)
queen_img = ImageTk.PhotoImage(queen)

squares = [white_sq_img, black_sq_img]
board = [[0 for _ in range(N)] for _ in range(N)]

labels = [[None for _ in range(N)] for _ in range(N)]
queen_labels = [[None for _ in range(N)] for _ in range(N)]

queen_count = 0

def is_valid_placement(row, col):
    for i in range(N):
        if board[i][col] == 1:
            return False
    
    for j in range(N):
        if board[row][j] == 1:
            return False
    
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1
    
    r, c = row, col
    while r >= 0 and c < N:
        if board[r][c] == 1:
            return False
        r -= 1
        c += 1
    
    r, c = row, col
    while r < N and c >= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1
    
    r, c = row, col
    while r < N and c < N:
        if board[r][c] == 1:
            return False
        r += 1
        c += 1    
    return True

def place_queen(row, col):
    global queen_count
    if is_valid_placement(row, col):
        board[row][col] = 1
        label_x = labels[row][col].winfo_x()
        label_y = labels[row][col].winfo_y()
        label_width = labels[row][col].winfo_width()
        label_height = labels[row][col].winfo_height()
        
        # Calculate the center position
        queen_x = label_x + (label_width - queen_img.width()) // 2
        queen_y = label_y + (label_height - queen_img.height()) // 2
        
        queen_labels[row][col] = tk.Label(root, image=queen_img, bg="white")
        queen_labels[row][col].place(x=queen_x, y=queen_y)
        
        queen_count += 1
        if queen_count == 4:
            messagebox.showinfo("Congratulations", "You have successfully solved the 4 queens problem!")
        return True
    else:
        messagebox.showinfo("Game Over", "The queen can attack a previously placed queen. Game Over!")
        root.quit()
        return False

def label_click(row, col):
    if board[row][col] == 0:  
        if place_queen(row, col):
            pass  
        else:
            pass  

for i in range(N):
    for j in range(N):
        labels[i][j] = tk.Label(root, image=squares[(i + j) % 2])
        labels[i][j].grid(row=i, column=j)
        labels[i][j].bind("<Button-1>", lambda event, r=i, c=j: label_click(r, c))

messagebox.showinfo("Instructions", "Click on any square to place a queen. Queens cannot attack each other horizontally, vertically, or diagonally from their position.")
root.mainloop()