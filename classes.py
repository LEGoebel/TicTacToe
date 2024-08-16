import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        #Game Modes (vs. Human, vs. Computer (Einfach), vs. Computer (Schwer))
        self.opponent = tk.StringVar(value="Mensch")
        opponent_menu = tk.OptionMenu(self.root, self.opponent, "Mensch", "Computer (Einfach)", "Computer (Schwer)")
        opponent_menu.grid(row=3, column=0, columnspan=1)

        #Set up blank board
        self.board = [" " for i in range(9)]
        self.current_winner = None
        self.current_player = "X"

        # Create buttons in a 3x3 grid using floor division, modulo for the correct position.
        # Used the lambda function to define the correct "_ButtonCommand"
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
                if self.opponent.get() != "Mensch" and self.current_player == "O":
                    self.computer_move()

    def check_winner_static(board, player):
        # List of all win conditions (not many here in TicTacToe) to be able to compare the current state against them
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Reihen
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
                          (0, 4, 8), (2, 4, 6)]             # Diagonalen
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
                return True
        return False
        
    def check_winner(self, player):
        return TicTacToeGUI.check_winner_static(self.board, player)
        
    def reset_board(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.current_winner = None
        self.current_player = random.choice(["X", "O"])
        if self.opponent.get() != "Mensch" and self.current_player == "O":
            self.computer_move()
        print("Game was resetted.")
            
    def computer_move(self):
        level = "einfach" if self.opponent.get() == "Computer (Einfach)" else "schwer"
        computer = ComputerPlayer(level)
        index = computer.make_move(self.board, self.current_player)
        self.make_move(index, self.current_player)
        self.check_game_over()
        
    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)
        
    def check_game_over(self):
        if self.check_winner(self.current_player):
            self.current_winner = self.current_player
            messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
            self.reset_board()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_board()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

class ComputerPlayer:
    def __init__(self, level = "einfach"):
          self.level = level
    
    def make_move(self, board, player):
        if (self.level == "einfach"):
            return self.simple_move(board)
        elif (self.level == "schwer"):
            return self.optimal_move(board, player)
        
    def simple_move(self, board):
        available_moves = [i for i in range(9) if board[i] == " "]
        return random.choice(available_moves)
    
    def optimal_move(self, board, player):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, 0, False, player)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing, player):
        opponent = "O" if player == "X" else "X"
        if TicTacToeGUI.check_winner_static(board, player):
            return 1
        elif TicTacToeGUI.check_winner_static(board, opponent):
            return -1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = player
                    score = self.minimax(board, depth + 1, False, player)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = opponent
                    score = self.minimax(board, depth + 1, True, player)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score