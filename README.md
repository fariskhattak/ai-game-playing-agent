# AI Game Playing Agents: Connect Four & Tic-Tac-Toe

This project implements two classic games:
- **Connect Four** with AI using **Minimax Algorithm + Alpha-Beta Pruning**
- **Tic-Tac-Toe** with AI using **basic Minimax**

Both games have a **Tkinter GUI**.

---

## Features
- **Connect Four:**
  - Play against an AI that looks 4 moves ahead using minimax with alpha-beta pruning.
  - GUI-based board (6 rows × 7 columns).
  - Restart button to play again without restarting the program.

- **Tic-Tac-Toe:**
  - Play against a perfect AI using basic minimax (no alpha-beta needed due to small board).
  - GUI-based board (3 × 3 grid).
  - Restart button included.

---

## How to Run

1. Make sure you have **Python 3** installed.
2. Install Tkinter if it's not already installed (usually comes by default):
   ```bash
   pip install tk
   ```
3. Run the desired game:
   - For Connect Four:
     ```bash
     python connect_four.py
     ```
   - For Tic-Tac-Toe:
     ```bash
     python tic_tac_toe.py
     ```

---

## Project Structure
| File | Description |
|:-----|:------------|
| `connect_four.py` | Connect Four game with Minimax + Alpha-Beta Pruning |
| `tic_tac_toe.py`  | Tic-Tac-Toe game with simple Minimax |

---

## How the AI Works
- **Minimax Algorithm**: Simulates all possible future moves assuming both players play optimally.
- **Alpha-Beta Pruning (Connect Four only)**: Cuts off unnecessary branches in the decision tree to optimize performance.
- **Depth-Limited Search (Connect Four)**: The AI looks ahead up to 4 moves to balance speed and intelligence.

---

## Future Improvements (Ideas)
- Add difficulty levels (Easy, Medium, Hard).
- Highlight winning pieces.
- Add move history or undo feature.
- Improve AI with heuristic evaluation for better mid-game play in Connect Four.

---