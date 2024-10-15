import tkinter as tk
import math

board = [' ' for _ in range(9)]

def is_winner(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  
                      (0, 4, 8), (2, 4, 6)]             
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)

def is_board_full():
    return ' ' not in board

def alpha_beta_pruning(is_maximizing, alpha, beta):
    if is_winner('X'):
        return 1 
    elif is_winner('O'):
        return -1  
    elif is_board_full():
        return 0  

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = alpha_beta_pruning(False, alpha, beta)
                board[i] = ' '  
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = alpha_beta_pruning(True, alpha, beta)
                board[i] = ' '  
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break 
        return min_eval

def best_move():
    best_value = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            move_value = alpha_beta_pruning(False, -math.inf, math.inf)
            board[i] = ' '  
            if move_value > best_value:
                best_value = move_value
                move = i
    return move

def on_click(index):
    if board[index] == ' ' and not is_winner('X') and not is_winner('O'):
        board[index] = 'O'
        buttons[index].config(text='O', state=tk.DISABLED)

        if is_winner('O'):
            status_label.config(text="Player O wins!")
            disable_all_buttons()
            return
        elif is_board_full():
            status_label.config(text="It's a draw!")
            return

        ai_move = best_move()
        board[ai_move] = 'X'
        buttons[ai_move].config(text='X', state=tk.DISABLED)

        if is_winner('X'):
            status_label.config(text="AI (X) wins!")
            disable_all_buttons()
        elif is_board_full():
            status_label.config(text="It's a draw!")

def disable_all_buttons():
    for button in buttons:
        button.config(state=tk.DISABLED)

def reset_game():
    global board
    board = [' ' for _ in range(9)]
    for button in buttons:
        button.config(text='', state=tk.NORMAL)
    status_label.config(text="Player O's Turn")

window = tk.Tk()
window.title("Tic-Tac-Toe")

buttons = []
for i in range(9):
    button = tk.Button(window, text='', width=10, height=4, font=('Arial', 20), command=lambda i=i: on_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

status_label = tk.Label(window, text="Player O's Turn", font=('Arial', 15))
status_label.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(window, text='Reset', command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3)

window.mainloop()