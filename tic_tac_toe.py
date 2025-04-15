class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9  # 3x3 board flattened
        self.current_winner = None

    def print_board(self):
        # Show position numbers in empty spots
        display = [str(i) if cell == " " else cell for i, cell in enumerate(self.board)]
        for row in [display[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")


    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, square, player):
        if self.board[square] == " ":
            self.board[square] = player
            if self.winner(square, player):
                self.current_winner = player
            return True
        return False

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

    def is_full(self):
        return " " not in self.board

    def is_game_over(self):
        return self.current_winner or self.is_full()

def minimax(board, player, maximizing, depth=0):
    opponent = "O" if player == "X" else "X"
    available = board.available_moves()

    if board.current_winner == opponent:
        return {"position": None, "score": 1 * (len(available) + 1) if not maximizing else -1 * (len(available) + 1)}
    elif board.is_full():
        return {"position": None, "score": 0}

    best = {"position": None, "score": float("-inf") if maximizing else float("inf")}

    for move in available:
        board.make_move(move, player if maximizing else opponent)
        sim_score = minimax(board, player, not maximizing, depth + 1)
        board.board[move] = " "
        board.current_winner = None
        sim_score["position"] = move

        if maximizing:
            if sim_score["score"] > best["score"]:
                best = sim_score
        else:
            if sim_score["score"] < best["score"]:
                best = sim_score

    return best

def play():
    game = TicTacToe()
    
    # Validate user input for X or O
    while True:
        human = input("Do you want to be X or O? ").upper()
        if human in ["X", "O"]:
            break
        else:
            print("Invalid input. Please enter 'X' or 'O'.")

    ai = "O" if human == "X" else "X"
    turn = "X"  # X always goes first

    print("\nWelcome to Tic-Tac-Toe!")
    game.print_board()

    while not game.is_game_over():
        if turn == human:
            try:
                move = int(input("Choose your move (0-8): "))
                if move not in game.available_moves():
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Please enter a number between 0 and 8.")
                continue
            game.make_move(move, human)
        else:
            print("AI is thinking...")
            move = minimax(game, ai, True)["position"]
            game.make_move(move, ai)

        game.print_board()
        print()

        if game.current_winner:
            print(f"{turn} wins!")
            return
        elif game.is_full():
            print("It's a tie!")
            return

        turn = "O" if turn == "X" else "X"

if __name__ == "__main__":
    play()
