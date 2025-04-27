import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7

class Board:
    def __init__(self, board=None):
        if board:
            self.board = [row[:] for row in board]
        else:
            self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

    def get_available_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == " ":
                return r
        return None

    def available_moves(self):
        return [c for c in range(COLS) if self.board[0][c] == " "]

    def make_move(self, col, player):
        row = self.get_available_row(col)
        if row is not None:
            self.board[row][col] = player
        return row

    def is_full(self):
        return all(self.board[0][c] != " " for c in range(COLS))

    def check_winner(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != player:
                    continue
                # horizontal
                if c + 3 < COLS and all(self.board[r][c+i] == player for i in range(4)):
                    return True
                # vertical
                if r + 3 < ROWS and all(self.board[r+i][c] == player for i in range(4)):
                    return True
                # positive diagonal
                if r + 3 < ROWS and c + 3 < COLS and all(self.board[r+i][c+i] == player for i in range(4)):
                    return True
                # negative diagonal
                if r - 3 >= 0 and c + 3 < COLS and all(self.board[r-i][c+i] == player for i in range(4)):
                    return True
        return False

class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four: Human vs AI")
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.buttons = []
        self.current_player = "X"
        self.ai_player = "O"

        self.create_board()

        self.restart_button = tk.Button(self.root, text="Restart Game", font=("Helvetica", 16),
                                        command=self.restart_game)
        self.restart_button.grid(row=ROWS, column=0, columnspan=COLS, sticky="nsew", pady=(10, 0))

    def create_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(self.root, text=" ", font=("Helvetica", 24), height=2, width=4,
                                command=lambda c=c: self.make_move(c))
                btn.grid(row=r, column=c)
                self.buttons.append(btn)

    def make_move(self, col):
        if not self.is_game_over():
            row = self.get_available_row(col)
            if row is not None:
                self.board[row][col] = self.current_player
                self.update_gui()
                if self.check_winner(row, col, self.current_player):
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
        board_copy = Board(self.board)
        move = minimax(board_copy, 4, -float('inf'), float('inf'), True, self.ai_player, self.current_player)["column"]
        if move is not None:
            row = self.get_available_row(move)
            if row is not None:
                self.board[row][move] = self.ai_player
                self.update_gui()
                if self.check_winner(row, move, self.ai_player):
                    messagebox.showinfo("Game Over", f"{self.ai_player} wins!")
                    self.disable_all()
                elif self.is_full():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.disable_all()


    def restart_game(self):
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        for btn in self.buttons:
            btn.config(text=" ", state="normal")

    def update_gui(self):
        for r in range(ROWS):
            for c in range(COLS):
                idx = r * COLS + c
                self.buttons[idx].config(text=self.board[r][c])

    def get_available_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == " ":
                return r
        return None

    def is_full(self):
        return all(self.board[0][c] != " " for c in range(COLS))

    def is_game_over(self):
        return self.is_full() or self.get_winner() is not None

    def get_winner(self):
        for r in range(ROWS):
            for c in range(COLS):
                for player in ["X", "O"]:
                    if self.check_winner(r, c, player):
                        return player
        return None

    def check_winner(self, row, col, player):
        if self.board[row][col] != player:
            return False
        # Check horizontal
        count = 0
        for c in range(max(0, col-3), min(COLS, col+4)):
            if self.board[row][c] == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        # Check vertical
        count = 0
        for r in range(max(0, row-3), min(ROWS, row+4)):
            if self.board[r][col] == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        # Check positive diagonal
        count = 0
        for d in range(-3, 4):
            r, c = row+d, col+d
            if 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == player:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    count = 0
        # Check negative diagonal
        count = 0
        for d in range(-3, 4):
            r, c = row-d, col+d
            if 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == player:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    count = 0
        return False

    def available_moves(self):
        return [c for c in range(COLS) if self.board[0][c] == " "]

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state="disabled")

def minimax(board, depth, alpha, beta, maximizing, ai_player, human_player):
    valid_locations = board.available_moves()

    if depth == 0 or board.check_winner(ai_player) or board.check_winner(human_player) or board.is_full():
        if board.check_winner(ai_player):
            return {"column": None, "score": 1000000}
        elif board.check_winner(human_player):
            return {"column": None, "score": -1000000}
        else:
            return {"column": None, "score": 0}

    if maximizing:
        value = -float('inf')
        best_col = None
        for col in valid_locations:
            temp_board = Board(board.board)
            temp_board.make_move(col, ai_player)
            new_score = minimax(temp_board, depth-1, alpha, beta, False, ai_player, human_player)["score"]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return {"column": best_col, "score": value}
    else:
        value = float('inf')
        best_col = None
        for col in valid_locations:
            temp_board = Board(board.board)
            temp_board.make_move(col, human_player)
            new_score = minimax(temp_board, depth-1, alpha, beta, True, ai_player, human_player)["score"]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return {"column": best_col, "score": value}


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()
