import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Human vs AI")
        self.board = [" "] * 9
        self.buttons = []
        self.current_player = "X"
        self.ai_player = "O"

        self.create_board()

        self.restart_button = tk.Button(self.root, text="Restart Game", font=("Helvetica", 16),
                                        command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.root, text=" ", font=("Helvetica", 32), height=2, width=5,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def make_move(self, index):
        if self.board[index] == " " and not self.is_game_over():
            self.board[index] = self.current_player
            self.update_gui()
            if self.winner(index, self.current_player):
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.disable_all()
                return
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.disable_all()
                return
            # AI turn
            self.root.after(500, self.ai_move)

    def ai_move(self):
        move = minimax(self, self.ai_player, True)["position"]
        if move is not None:
            self.board[move] = self.ai_player
            self.update_gui()
            if self.winner(move, self.ai_player):
                messagebox.showinfo("Game Over", f"{self.ai_player} wins!")
                self.disable_all()
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.disable_all()

    def restart_game(self):
        self.board = [" "] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text=" ", state="normal")

    def update_gui(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

    def is_full(self):
        return " " not in self.board

    def is_game_over(self):
        return self.is_full() or self.get_winner() is not None

    def get_winner(self):
        for player in ["X", "O"]:
            for i in range(9):
                if self.board[i] == player and self.winner(i, player):
                    return player
        return None

    def winner(self, square, player):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == player for s in row]):
            return True

        col_ind = square % 3
        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == player for s in col]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == player for s in diagonal1]) or all([s == player for s in diagonal2]):
                return True

        return False

    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state="disabled")

def minimax(game, player, maximizing):
    opponent = "O" if player == "X" else "X"
    available = game.available_moves()

    winner = game.get_winner()
    if winner == player:
        return {"position": None, "score": 1}
    elif winner == opponent:
        return {"position": None, "score": -1}
    elif game.is_full():
        return {"position": None, "score": 0}

    best = {"position": None, "score": float("-inf") if maximizing else float("inf")}

    for move in available:
        game.board[move] = player if maximizing else opponent
        sim_score = minimax(game, player, not maximizing)
        game.board[move] = " "
        sim_score["position"] = move

        if maximizing:
            if sim_score["score"] > best["score"]:
                best = sim_score
        else:
            if sim_score["score"] < best["score"]:
                best = sim_score

    return best


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
