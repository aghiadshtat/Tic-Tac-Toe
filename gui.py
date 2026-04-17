import tkinter as tk
from tkinter import messagebox

from game_logic import BotAI, TicTacToeGame


class TicTacToeGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("520x660")
        self.root.minsize(420, 560)
        self.root.configure(bg="#141625")

        self.game: TicTacToeGame | None = None
        self.bot_ai: BotAI | None = None
        self.bot_difficulty = "easy"

        self.status_text = tk.StringVar(value="Welcome to Tic-Tac-Toe")

        self.container = tk.Frame(self.root, bg="#141625")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.start_frame = tk.Frame(self.container, bg="#141625")
        self.game_frame = tk.Frame(self.container, bg="#141625")
        for frame in (self.start_frame, self.game_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self._build_start_page()
        self._build_game_page()
        self._show_page(self.start_frame)

    def _build_start_page(self) -> None:
        frame = self.start_frame
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=2)
        frame.grid_rowconfigure(3, weight=5)
        frame.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            frame,
            text="Tic-Tac-Toe",
            font=("Arial", 34, "bold"),
            fg="#7ae3ff",
            bg="#141625",
        )
        title.grid(row=1, column=0, pady=(20, 5))

        subtitle = tk.Label(
            frame,
            text="Choose a mode to start",
            font=("Arial", 14),
            fg="#d0d3ff",
            bg="#141625",
        )
        subtitle.grid(row=2, column=0, pady=(0, 20))

        controls = tk.Frame(frame, bg="#141625")
        controls.grid(row=3, column=0, sticky="n", padx=24)
        controls.grid_columnconfigure(0, weight=1)

        self._styled_button(
            controls, "Start vs Player", lambda: self.start_game(vs_bot=False)
        ).grid(row=0, column=0, sticky="ew", pady=6)
        self._styled_button(
            controls, "Start vs Bot", self.toggle_bot_options
        ).grid(row=1, column=0, sticky="ew", pady=6)
        self._styled_button(controls, "Exit", self.root.destroy).grid(
            row=2, column=0, sticky="ew", pady=6
        )

        self.bot_options = tk.Frame(controls, bg="#141625")
        self.bot_options.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        self.bot_options.grid_remove()

        self._styled_button(
            self.bot_options,
            "Hard",
            lambda: self.start_game(vs_bot=True, difficulty="hard"),
        ).grid(row=0, column=0, sticky="ew", pady=4)
        self._styled_button(
            self.bot_options,
            "Medium",
            lambda: self.start_game(vs_bot=True, difficulty="medium"),
        ).grid(row=1, column=0, sticky="ew", pady=4)
        self._styled_button(
            self.bot_options,
            "Easy",
            lambda: self.start_game(vs_bot=True, difficulty="easy"),
        ).grid(row=2, column=0, sticky="ew", pady=4)

    def _build_game_page(self) -> None:
        frame = self.game_frame
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        top = tk.Frame(frame, bg="#1b1e35", padx=12, pady=12)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(1, weight=1)

        self._styled_button(top, "Menu", self.go_to_menu, width=10).grid(
            row=0, column=0, padx=(0, 8)
        )

        tk.Label(
            top,
            textvariable=self.status_text,
            font=("Arial", 13, "bold"),
            fg="#f2f3ff",
            bg="#1b1e35",
        ).grid(row=0, column=1, sticky="w")

        indicator_wrap = tk.Frame(top, bg="#1b1e35")
        indicator_wrap.grid(row=0, column=2, sticky="e")
        self.turn_indicator = tk.Canvas(
            indicator_wrap,
            width=24,
            height=24,
            bg="#1b1e35",
            bd=0,
            highlightthickness=0,
        )
        self.turn_indicator.grid(row=0, column=0, padx=(8, 0))
        self.indicator_dot = self.turn_indicator.create_oval(
            5, 5, 19, 19, fill="#1ed760", outline=""
        )

        board_container = tk.Frame(frame, bg="#141625", padx=14, pady=14)
        board_container.grid(row=1, column=0, sticky="nsew")
        board_container.grid_rowconfigure(0, weight=1)
        board_container.grid_columnconfigure(0, weight=1)

        self.board_frame = tk.Frame(board_container, bg="#141625")
        self.board_frame.grid(row=0, column=0, sticky="nsew")
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1, uniform="board")
            self.board_frame.grid_columnconfigure(i, weight=1, uniform="board")

        self.cells: list[tk.Button] = []
        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 28, "bold"),
                    bg="#282c4a",
                    fg="#f4f5ff",
                    activebackground="#32375d",
                    activeforeground="#ffffff",
                    bd=0,
                    command=lambda i=idx: self.on_cell_click(i),
                )
                button.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
                self.cells.append(button)

        bottom = tk.Frame(frame, bg="#141625", pady=8)
        bottom.grid(row=2, column=0, sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)
        self._styled_button(bottom, "Restart", self.restart_game, width=16).grid(
            row=0, column=0
        )

    def _styled_button(
        self, parent: tk.Widget, text: str, command, width: int = 22
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            width=width,
            command=command,
            font=("Arial", 12, "bold"),
            bg="#5f6fff",
            fg="white",
            activebackground="#7483ff",
            activeforeground="white",
            relief="flat",
            padx=8,
            pady=8,
            cursor="hand2",
        )

    def toggle_bot_options(self) -> None:
        if self.bot_options.winfo_ismapped():
            self.bot_options.grid_remove()
        else:
            self.bot_options.grid()

    def start_game(self, vs_bot: bool, difficulty: str = "easy") -> None:
        self.bot_difficulty = difficulty
        if vs_bot:
            players = [{"name": "Player", "sym": "X"}, {"name": "Bot", "sym": "O"}]
            self.game = TicTacToeGame(players=players, vs_bot=True, bot_player_index=1)
            self.bot_ai = BotAI(difficulty=difficulty)
        else:
            players = [{"name": "Player 1", "sym": "X"}, {"name": "Player 2", "sym": "O"}]
            self.game = TicTacToeGame(players=players, vs_bot=False)
            self.bot_ai = None

        self._reset_board_ui()
        self._update_turn_ui()
        self._show_page(self.game_frame)
        self.root.after(120, self._maybe_bot_turn)

    def _show_page(self, page: tk.Frame) -> None:
        page.tkraise()

    def _set_indicator_color(self) -> None:
        if not self.game:
            return
        color = "#1ed760" if self.game.current_player == 0 else "#ff3b3b"
        self.turn_indicator.itemconfig(self.indicator_dot, fill=color)

    def _update_turn_ui(self) -> None:
        if not self.game:
            return
        player = self.game.players[self.game.current_player]
        if self.game.vs_bot:
            mode = f"Bot: {self.bot_difficulty.capitalize()}"
            self.status_text.set(f"{player['name']}'s turn ({player['sym']}) • {mode}")
        else:
            self.status_text.set(f"{player['name']}'s turn ({player['sym']})")
        self._set_indicator_color()

    def _play_move_sound(self) -> None:
        self.root.bell()

    def on_cell_click(self, index: int) -> None:
        if not self.game:
            return
        if self.game.vs_bot and self.game.current_player == self.game.bot_player_index:
            return
        self._apply_move(index)

    def _apply_move(self, index: int) -> None:
        if not self.game or not self.game.make_move(index):
            return

        self.cells[index].config(
            text=self.game.board[index],
            fg="#86f0a1" if self.game.board[index] == "X" else "#ff9ea7",
            state="disabled",
            disabledforeground="#86f0a1" if self.game.board[index] == "X" else "#ff9ea7",
        )
        self._play_move_sound()
        self._refresh_after_move()

    def _refresh_after_move(self) -> None:
        if not self.game:
            return

        if self.game.game_over:
            if self.game.winner:
                self.status_text.set(f"{self.game.winner['name']} wins!")
                messagebox.showinfo("Game Over", f"{self.game.winner['name']} wins!")
            else:
                self.status_text.set("It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
            self._set_indicator_color()
            self._disable_board()
            return

        self._update_turn_ui()
        self.root.after(260, self._maybe_bot_turn)

    def _maybe_bot_turn(self) -> None:
        if (
            not self.game
            or not self.game.vs_bot
            or self.game.game_over
            or self.game.current_player != self.game.bot_player_index
            or not self.bot_ai
        ):
            return
        move = self.bot_ai.choose_move(self.game)
        self._apply_move(move)

    def _disable_board(self) -> None:
        for cell in self.cells:
            cell.config(state="disabled")

    def _reset_board_ui(self) -> None:
        for cell in self.cells:
            cell.config(text="", state="normal", fg="#f4f5ff")

    def restart_game(self) -> None:
        if not self.game:
            return
        self.game.restart()
        self._reset_board_ui()
        self._update_turn_ui()
        self.root.after(120, self._maybe_bot_turn)

    def go_to_menu(self) -> None:
        self.status_text.set("Welcome to Tic-Tac-Toe")
        self._show_page(self.start_frame)

    def run(self) -> None:
        self.root.mainloop()
