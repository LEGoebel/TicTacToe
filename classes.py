import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.board = [" " for i in range(9)]
        self.current_winner = None
        self.current_player = "X"

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text = " ", font=("normal", 40), width=5, height=2,
                               command=lambda i = i: self.on_click(i))
            button.grid(row = i // 3, column = i % 3)
            self.buttons.append(button)

        restart_button = tk.Button(self.root, text="Restart", font=("normal", 20), command=self.reset_board)
        restart_button.grid(row=3, column=0, columnspan=3)

    def on_click(self, index):
            if self.board[index] == " " and not self.current_winner:
                self.board[index] = self.current_player
                self.buttons[index].config(text = self.current_player)

            if self.check_winner(self.current_player):
                self.current_winner = self.current_player
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.reset_board()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
            win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Reihen
                              (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
                              (0, 4, 8), (2, 4, 6)]  # Diagonalen
            for condition in win_conditions:
                if self.board[condition[0]]==self.board[condition[1]]==self.board[condition[2]]==player:
                    return True
            return False
        
    def reset_board(self):
            self.board = [" " for _ in range(9)]
            for button in self.buttons:
                button.config(text=" ")
            self.current_winner = None
            self.current_player = "X"
            print("Game was resetted.")
