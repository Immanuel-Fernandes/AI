import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import random
import pygame
from tkinter import messagebox, Toplevel

pygame.mixer.init()

def create_board():
    return np.zeros((3, 3), dtype=int)

def check_winner(board, player):
    for i in range(3):
        if np.all(board[i, :] == player) or np.all(board[:, i] == player):
            return True
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False

def evaluate(board):
    for player in [1, 2]:
        if check_winner(board, player):
            return player
    if np.all(board != 0):
        return -1
    return 0

def possibilities(board):
    return list(zip(*np.where(board == 0)))

def random_place(board, player):
    selection = possibilities(board)
    if selection:
        current_loc = random.choice(selection)
        board[current_loc] = player
    return board

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("515x550")  
        
        self.board = create_board()
        self.current_player = 1
        self.labels = {
            1: "Conservationist",
            2: "Polluter"
        }
        self.win_messages = {
            1: "The Ecofreaks have successfully Defeated a Nature Exploiter and conserved the Earth.",
            2: "The Exploiter has successfully polluted the Earth."
        }
        self.win_images = {
            1: Image.open("Victory.jpg").resize((200, 200)),
            2: Image.open("Defeat.jpg").resize((200, 200))
        }
        self.images = {
            1: ctk.CTkImage(dark_image=Image.open("X.jpg").resize((120, 120)), size=(120, 120)),
            2: ctk.CTkImage(dark_image=Image.open("O.jpg").resize((120, 120)), size=(120, 120))
        }
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.play_with_computer = False
        
        self.create_widgets()
        
    def create_widgets(self):
        menu = ctk.CTkOptionMenu(self.root, values=["2 Players", "Play Against a Nature Exploiter"], command=self.set_game_mode)
        menu.grid(row=0, column=0, columnspan=3, pady=10)  
        
        for i in range(3):
            for j in range(3):
                button = ctk.CTkButton(self.root, width=150, height=150, text="", command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i+2, column=j, padx=10, pady=10)  
                self.buttons[i][j] = button

    def set_game_mode(self, choice):
        self.play_with_computer = (choice == "Play Against a Nature Exploiter")
        self.reset_game()

    def play_sound(self, player):
        sound_file = f"{player}.mp3"
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        
    def make_move(self, row, col):
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_player
            self.buttons[row][col].configure(image=self.images[self.current_player], state='disabled')
            self.play_sound(self.current_player)
            if evaluate(self.board) == self.current_player:
                self.show_winner(self.current_player)
            elif evaluate(self.board) == -1:
                self.show_winner(-1)
            else:
                self.current_player = 3 - self.current_player
                if self.play_with_computer and self.current_player == 2:
                    self.root.after(500, self.computer_move)
    
    def computer_move(self):
        self.board = random_place(self.board, 2)
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 2 and self.buttons[i][j].cget('state') != 'disabled':
                    self.buttons[i][j].configure(image=self.images[2], state='disabled')
                    break
        self.play_sound(2)
        if evaluate(self.board) == 2:
            self.show_winner(2)
        elif evaluate(self.board) == -1:
            self.show_winner(-1)
        else:
            self.current_player = 1

    def show_winner(self, winner):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(state='disabled')
        
        if winner == -1:
            messagebox.showinfo("Game Over", "The outcome results in a balanced environmental impact")
        else:
            result_message = self.win_messages[winner]
            result_image = ImageTk.PhotoImage(self.win_images[winner])
            
            win_window = Toplevel(self.root)
            win_window.title("Game Over")
            
            label_image = ctk.CTkLabel(win_window, image=result_image)
            label_image.image = result_image 
            label_image.pack()
            
            label_message = ctk.CTkLabel(win_window, text=result_message, font=('Helvetica', 14), pady=10)
            label_message.pack()
            
            button_ok = ctk.CTkButton(win_window, text="OK", command=win_window.destroy)
            button_ok.pack(pady=10)
        
        self.reset_game()

    def reset_game(self):
        self.board = create_board()
        self.current_player = 1
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(image='', state='normal')

if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToeGUI(root)
    root.mainloop()
