import tkinter as tk
from tkinter import messagebox, simpledialog


class TicTacToeGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.setup_cancelled = False

        self.players = [
            {"name": "Player 1", "sym": "X"},
            {"name": "Player 2", "sym": "O"},
        ]
        self.current_player = 0
        self.board = [""] * 9
        self.game_over = False

        self.status_text = tk.StringVar()
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_text,
            font=("Arial", 14, "bold"),
            padx=12,
            pady=12,
        )
        self.status_label.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.buttons: list[tk.Button] = []
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                button = tk.Button(
                    self.root,
                    text="",
                    width=8,
                    height=4,
                    font=("Arial", 20, "bold"),
                    command=lambda i=index: self.make_move(i),
                )
                button.grid(row=row + 1, column=col, padx=5, pady=5)
                self.buttons.append(button)

        controls = tk.Frame(self.root, pady=8)
        controls.grid(row=4, column=0, columnspan=3)
        tk.Button(controls, text="Restart", width=12, command=self.restart_game).grid(
            row=0, column=0, padx=6
        )
        tk.Button(controls, text="Quit", width=12, command=self.root.destroy).grid(
            row=0, column=1, padx=6
        )

        if not self.setup_players():
            self.setup_cancelled = True
            self.root.destroy()
            return
        self.update_status()

    def setup_players(self) -> bool:
        for index in range(2):
            default_name = self.players[index]["name"]
            while True:
                name = simpledialog.askstring(
                    "Player Setup",
                    f"Enter name for player {index + 1}:",
                    initialvalue=default_name,
                    parent=self.root,
                )
                if name is None:
                    return False
                name = name.strip()
                if name:
                    self.players[index]["name"] = name
                    break
                messagebox.showerror("Invalid Name", "Please enter a valid name.")

        first_symbol = self.ask_symbol(self.players[0]["name"], "X")
        if first_symbol is None:
            return False
        self.players[0]["sym"] = first_symbol

        while True:
            second_symbol = self.ask_symbol(self.players[1]["name"], "O")
            if second_symbol is None:
                return False
            if second_symbol != self.players[0]["sym"]:
                self.players[1]["sym"] = second_symbol
                break
            messagebox.showerror(
                "Invalid Symbol",
                "Player 2 must choose a different symbol from Player 1.",
            )
        return True

    def ask_symbol(self, player_name: str, default_symbol: str) -> str | None:
        while True:
            symbol = simpledialog.askstring(
                "Player Setup",
                f"{player_name}, choose one letter as your symbol:",
                initialvalue=default_symbol,
                parent=self.root,
            )
            if symbol is None:
                return None
            symbol = symbol.strip().upper()
            if len(symbol) == 1 and symbol.isalpha():
                return symbol
            messagebox.showerror(
                "Invalid Symbol", "Symbol must be exactly one alphabetic character."
            )

    def make_move(self, index: int) -> None:
        if self.game_over or self.board[index]:
            return

        player = self.players[self.current_player]
        self.board[index] = player["sym"]
        self.buttons[index].config(text=player["sym"], state="disabled")

        winner = self.get_winner()
        if winner is not None:
            self.game_over = True
            self.status_text.set(f"{winner['name']} wins!")
            self.disable_board()
            messagebox.showinfo("Game Over", f"{winner['name']} wins!")
            return

        if all(self.board):
            self.game_over = True
            self.status_text.set("It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.current_player = 1 - self.current_player
        self.update_status()

    def get_winner(self) -> dict | None:
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
                symbol = self.board[a]
                return next(
                    player for player in self.players if player["sym"] == symbol
                )
        return None

    def disable_board(self) -> None:
        for button in self.buttons:
            button.config(state="disabled")

    def restart_game(self) -> None:
        self.board = [""] * 9
        self.current_player = 0
        self.game_over = False
        for button in self.buttons:
            button.config(text="", state="normal")
        self.update_status()

    def update_status(self) -> None:
        player = self.players[self.current_player]
        self.status_text.set(f"{player['name']}'s turn ({player['sym']})")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    if not app.setup_cancelled:
        app.run()
