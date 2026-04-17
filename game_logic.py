import random

WIN_CONDITIONS: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class TicTacToeGame:
    def __init__(
        self,
        players: list[dict[str, str]],
        vs_bot: bool = False,
        bot_player_index: int | None = None,
    ) -> None:
        self.players = players
        self.vs_bot = vs_bot
        self.bot_player_index = bot_player_index if vs_bot else None
        self.board = [""] * 9
        self.current_player = 0
        self.game_over = False
        self.winner: dict[str, str] | None = None
        self.is_draw = False

    def restart(self) -> None:
        self.board = [""] * 9
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.is_draw = False

    def available_moves(self) -> list[int]:
        return [index for index, value in enumerate(self.board) if not value]

    def make_move(self, index: int) -> bool:
        if self.game_over or self.board[index]:
            return False

        symbol = self.players[self.current_player]["sym"]
        self.board[index] = symbol

        winner_symbol = self.check_winner_symbol(self.board)
        if winner_symbol:
            self.game_over = True
            self.winner = next(
                player for player in self.players if player["sym"] == winner_symbol
            )
            return True

        if all(self.board):
            self.game_over = True
            self.is_draw = True
            return True

        self.current_player = 1 - self.current_player
        return True

    @staticmethod
    def check_winner_symbol(board: list[str]) -> str | None:
        for a, b, c in WIN_CONDITIONS:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return None


class BotAI:
    def __init__(self, difficulty: str) -> None:
        self.difficulty = difficulty

    def choose_move(self, game: TicTacToeGame) -> int:
        if self.difficulty == "easy":
            return random.choice(game.available_moves())
        if self.difficulty == "medium":
            return self._choose_medium(game)
        return self._choose_hard(game)

    def _choose_medium(self, game: TicTacToeGame) -> int:
        if game.bot_player_index is None:
            return random.choice(game.available_moves())
        bot_symbol = game.players[game.bot_player_index]["sym"]
        human_symbol = game.players[1 - game.bot_player_index]["sym"]
        moves = game.available_moves()

        for move in moves:
            trial_board = game.board[:]
            trial_board[move] = bot_symbol
            if TicTacToeGame.check_winner_symbol(trial_board) == bot_symbol:
                return move

        for move in moves:
            trial_board = game.board[:]
            trial_board[move] = human_symbol
            if TicTacToeGame.check_winner_symbol(trial_board) == human_symbol:
                return move

        if 4 in moves:
            return 4

        corners = [m for m in moves if m in (0, 2, 6, 8)]
        if corners:
            return random.choice(corners)

        return random.choice(moves)

    def _choose_hard(self, game: TicTacToeGame) -> int:
        if game.bot_player_index is None:
            return random.choice(game.available_moves())
        bot_symbol = game.players[game.bot_player_index]["sym"]
        human_symbol = game.players[1 - game.bot_player_index]["sym"]

        best_score = float("-inf")
        best_move = game.available_moves()[0]

        for move in game.available_moves():
            board = game.board[:]
            board[move] = bot_symbol
            score = self._minimax(
                board=board,
                depth=0,
                maximizing=False,
                bot_symbol=bot_symbol,
                human_symbol=human_symbol,
            )
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _minimax(
        self,
        board: list[str],
        depth: int,
        maximizing: bool,
        bot_symbol: str,
        human_symbol: str,
    ) -> int:
        winner_symbol = TicTacToeGame.check_winner_symbol(board)
        if winner_symbol == bot_symbol:
            return 10 - depth
        if winner_symbol == human_symbol:
            return depth - 10
        if all(board):
            return 0

        available = [index for index, value in enumerate(board) if not value]
        if maximizing:
            best = float("-inf")
            for move in available:
                score = self._minimax(
                    board=board[:move] + [bot_symbol] + board[move + 1 :],
                    depth=depth + 1,
                    maximizing=False,
                    bot_symbol=bot_symbol,
                    human_symbol=human_symbol,
                )
                best = max(best, score)
            return int(best)

        best = float("inf")
        for move in available:
            score = self._minimax(
                board=board[:move] + [human_symbol] + board[move + 1 :],
                depth=depth + 1,
                maximizing=True,
                bot_symbol=bot_symbol,
                human_symbol=human_symbol,
            )
            best = min(best, score)
        return int(best)
