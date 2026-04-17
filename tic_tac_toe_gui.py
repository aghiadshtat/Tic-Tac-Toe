import tkinter as tk
from tkinter import messagebox


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False

        self.status_var = tk.StringVar(value="Player X's turn")
        self.status_label = tk.Label(
            root, textvariable=self.status_var, font=("Arial", 14, "bold"), pady=10
        )
        self.status_label.pack()

        self.grid_frame = tk.Frame(root, padx=10, pady=10)
        self.grid_frame.pack()

        self.buttons = []
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                button = tk.Button(
                    self.grid_frame,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 24, "bold"),
                    command=lambda idx=index: self.make_move(idx),
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                self.buttons.append(button)

        self.controls_frame = tk.Frame(root, pady=10)
        self.controls_frame.pack()

        tk.Button(
            self.controls_frame,
            text="Restart",
            width=10,
            command=self.restart_game,
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            self.controls_frame,
            text="Quit",
            width=10,
            command=self.root.destroy,
        ).grid(row=0, column=1, padx=5)

    def make_move(self, index: int) -> None:
        if self.game_over or self.board[index]:
            return

        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player, state=tk.DISABLED)

        winner = self.get_winner()
        if winner:
            self.game_over = True
            self.status_var.set(f"Player {winner} wins!")
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            return

        if self.is_draw():
            self.game_over = True
            self.status_var.set("It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_var.set(f"Player {self.current_player}'s turn")

    def get_winner(self) -> str | None:
        win_conditions = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in win_conditions:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        return all(cell for cell in self.board)

    def restart_game(self) -> None:
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.status_var.set("Player X's turn")
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)


def main() -> None:
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
