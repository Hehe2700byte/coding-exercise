from abc import ABC, abstractmethod
from typing import Any, Self
from enum import Enum
from copy import deepcopy


class Color(Enum):
    BLACK = 'X'
    WHITE = 'O'


class Dir(Enum):
    CLOCKWISE = 'C'
    ANTICLOCKWISE = 'A'


class Player(ABC):
    """Abstract base class for a game participant.

    Attributes:
        color (Color): The piece color assigned to the player.
    """
    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def get_move(self) -> Any:
        """Abstract method to get the input of the player's next move."""
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Player {self.color.value}"


class HumanPlayer(Player):
    """A human player of Pentago that provides moves via console input.

    Attributes:
    lines (int): The count of lines (contiguous pieces) made by the player.
    """
    def __init__(self, color: Color):
        super().__init__(color)
        self.lines = 0

    def get_move(self) -> tuple[int, int, Dir, int]:
        """
        Prompts user for move input, validates format, and returns move data.
        """
        while True:
            try:
                move = input(f"Player {self.color.value}'s turn: ")
                move = move.upper()
                parts = move.split()
                if len(parts) != 2:
                    raise ValueError
                address, rotate = parts
                y = int(address[1:]) - 1
                x = ord(address[0]) - ord('A')
                dir = Dir(rotate[0])
                quar = int(rotate[1:])
                if quar not in range(1, 5):
                    raise ValueError
                return y, x, dir, quar
            except (ValueError, KeyError, IndexError) :
                print("Invalid format! Enter [Cell][Space][Dir][Quad]")

class Matrix:
    """A class to represent and manipulate a 2D grid of elements.

    Attributes:
        m (int): The number of rows in the matrix.
        n (int): The number of columns in the matrix.
        cells (list[list[Any]]): The underlying 2D list storing matrix data.

    Example:
        >>> m = Matrix(2, 2, data=[[1, 2], [3, 4]])
        >>> print(m)
        [[ 1  2]
         [ 3  4]]
    """
    def __init__(self, m: int, n: int, data: list[list[Any]] = None):
        """Initializes a matrix of size m x n with optional initial data."""
        self.m = m  # rows
        self.n = n  # columns
        self.cells = data if data else [[None] * n for _ in range(m)]

    def sub_matrix(self,
                   row_start: int, row_end: int,
                   col_start: int, col_end: int) -> Self:
        """
        Returns a new Matrix object representing a sliced portion of the
        current one.
        """
        matrix_slice = [[self.cells[i][j] for j in range(col_start, col_end)] for i in range(row_start, row_end)]
        return Matrix(row_end - row_start, col_end - col_start, matrix_slice)


    def transpose(self) -> None:
        """Flips the matrix over its diagonal, switching rows and columns."""
        self.m, self.n = self.n, self.m
        self.cells = [list(row) for row in zip(*self.cells)]

    def reverse(self, rowwise: bool = True) -> None:
        """Reverses the order of elements either row-wise or column-wise."""
        if rowwise:
            for i in range(self.m):
                self.cells[i].reverse()
        else:
            self.transpose()
            for j in range(self.m):
                self.cells[j].reverse()
            self.transpose()
        

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if not self.cells or not self.cells[0]:
            return "[]"
        flat_cells = [str(item) for row in self.cells for item in row]
        max_len = max(len(s) for s in flat_cells)
        formatted_rows = []
        for row in self.cells:
            row_str = " ".join(f"{str(item):>{max_len}}" for item in row)
            formatted_rows.append(f" [{row_str}]")
        body = "\n".join(formatted_rows)
        return f"[{body[1:]}]"


class BoardGame(ABC):
    """Abstract base class for a tabletop board game.

    Attributes:
        players (list[Player]): The participants in the game.
        num_players (int): Total number of players.
        current_player_index (int): Index of the player whose turn it is.
        winner (Player): The player who won the game. Defaults to None.
    """
    def __init__(self, players: list[Player]):
        """Sets up the game with a list of players and sets who plays first."""
        self.players = players
        self.num_players = len(players)
        self.current_player_index = 0
        self.winner = None

    @abstractmethod
    def is_game_over(self) -> bool:
        """
        Abstract method to check if the game has reached a terminal state.
        """
        pass

    def get_winner(self) -> int:
        """Returns the Player object that won, or None if the game is onging
        or draw."""
        return self.winner

    @abstractmethod
    def run(self) -> None:
        """Abstract method to execute the main game loop."""
        pass

    @property
    def current_player(self) -> Player:
        """Returns the actual Player object whose turn it is."""
        return self.players[self.current_player_index]

    def switch_player(self) -> None:
        """Cycles through the Player objects."""
        i = (self.current_player_index + 1) % self.num_players
        self.current_player_index = i


class Marble:
    """A class that represents a physical game piece on the board.

    Attributes:
        color (Color): The color of the marble.
    """
    def __init__(self, color):
        self.color = color

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.color.value


class Pentago(BoardGame, Matrix):
    """The concrete class that implements the Pentago board game, borrowing the
    operations provided by the Matrix class to simplify some board logic, e.g.,
    quadrant rotation = matrix transpose + reversing matrix elements.

    Attributes:
        line_len (int): The number of marbles required in a line to win.
    """
    def __init__(self, n: int = 6):
        self.n = n
        self.players = [HumanPlayer(Color.BLACK), HumanPlayer(Color.WHITE)]
        super().__init__(self.players)
        super(BoardGame, self).__init__(n, n)
        self.line_len = n - 1


    def initialize_board(self, board: list[list[Marble]]) -> None:
        """Overwrites the current cells with a provided 2D list of Marbles."""
        assert self.m == len(board) and all(
            self.n == len(board[i]) for i in range(len(board))
        ), "Board cannot be initialized due to dimension mismatch!"
        self.cells = board

    def rotate_quadrant(
            self, quadrant: int, direction: Dir = Dir.CLOCKWISE) -> None:
        """Rotates one of the four board quadrants 90 degrees in a given
        direction."""
        reverse_bool = True if direction == Dir.CLOCKWISE else False
        mid = self.n // 2
        row_start, row_end = (0, mid) if quadrant in [1, 2] else (mid, self.n)
        col_start, col_end = (0, mid) if quadrant in [1, 3] else (mid, self.n)
        rotate_matrix = self.sub_matrix(row_start, row_end, col_start, col_end)
        rotate_matrix.transpose()
        rotate_matrix.reverse(reverse_bool)
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                self.cells[i][j] = rotate_matrix.cells[i-row_start][j-col_start]
        print(f"Quadrant {quadrant} rotated {direction.name.lower()}")
                        

    def get_marble(self, y: int, x: int) -> Marble | None:
        """Returns a marble at (y, x) or returns None if out of bounds."""
        if 0 <= y < self.m and 0 <= x < self.n:
            return self.cells[y][x]

    def count_blanks(self) -> int:
        """Returns the total number of empty cells remaining on the board."""
        return sum(row.count(None) for row in self.cells)

    def count_lines(self, p: Player) -> int:
        """
        Returns the number of lines (sequences of n-1 consecutive marbles) of
        the specified player's color.
        """
        num_lines = 0
        #horizontally
        for i in range(self.n):
            for j in range(self.n - self.line_len + 1):
                cell_slice = self.cells[i][j:j+self.line_len]
                values = [cell.color.value if cell else None for cell in cell_slice]
                if values == [p.color.value] * self.line_len:
                    num_lines += 1

        #vertibally
        cells_copy = Matrix(self.n, self.n, self.cells)
        cells_copy.transpose()
        for i in range(self.n):
            for j in range(self.n - self.line_len + 1):
                cell_slice = cells_copy.cells[i][j:j+self.line_len]
                values = [cell.color.value if cell else None for cell in cell_slice]
                if values == [p.color.value] * self.line_len:
                    num_lines += 1
        #diagonal
        diagonals1 = [self.cells[i][i] for i in range(self.n)]
        diagonals2 = [self.cells[i][self.n - i - 1] for i in range(self.n)]
        values1 = [cell.color.value if cell else None for cell in diagonals1]
        values2 = [cell.color.value if cell else None for cell in diagonals2]
        for i in range(self.n - self.line_len + 1):
            if values1[i:i+self.line_len] == [p.color.value] * self.line_len:
                num_lines += 1
            if values2[i:i+self.line_len] == [p.color.value] * self.line_len:
                num_lines += 1
        
        return num_lines

    def is_valid_move(self, y: int, x: int) -> bool:
        """Checks if a move is valid, i.e., the specified coordinates are
        within bounds and currently empty."""
        return 0 <= y < self.m and 0 <= x < self.n and self.cells[y][x] is None

    def make_move(self, y: int, x: int, p: Player) -> None:
        """Places a marble of the player's color at the specified coordinates
        on the board."""
        self.cells[y][x] = Marble(p.color)

    def is_game_over(self) -> bool:
        """
        Updates player line counts and checks if a win or draw has occurred.
        """
        self.players[0].lines = self.count_lines(self.players[0])
        self.players[1].lines = self.count_lines(self.players[1])
        if self.players[0].lines > self.players[1].lines:
            self.winner = self.players[0]
        elif self.players[0].lines < self.players[1].lines:
            self.winner = self.players[1]
        else:
            self.winner = None
        if self.players[0].lines >= 1 or self.players[1].lines >= 1 or not self.count_blanks():
            return True
        else:
            return False
        

    def print_board(self) -> None:
        """
        Displays the current board state in the console with quadrant dividers.
        """
        board = self.cells
        N = len(board)
        mid = N // 2
        pad = " " * 2 if N <= 9 else " " * 3
        h_rule = f"{pad}+{'-' * (N + 1)}+{'-' * (N + 1)}+"
        cols = [chr(65 + j) for j in range(N)]  # ASCII of 'A': 65
        print(f"{pad}  {' '.join(cols[:mid])}   {' '.join(cols[mid:])}")
        print(h_rule)
        for i, row in enumerate(board):
            if i == mid:
                print(h_rule)
            left = " ".join(map(lambda x: str(x) if x else '.', row[:mid]))
            right = " ".join(map(lambda x: str(x) if x else '.', row[mid:]))
            print(f"{i + 1:>{len(pad)-1}} | {left} | {right} |")
        print(h_rule)

    def run(self) -> None:
        """
        Executes the main game loop, handling turns, moves, and rotations.
        """
        self.initialize_board([[None for _ in range(self.n)] for _ in range(self.n)])
        round_num = 1
        while True:
            print(f"Round {round_num}:")
            round_num += 1
            self.print_board()
            Current_player = self.current_player
            while True:
                move = Current_player.get_move()
                if self.is_valid_move(move[0], move[1]):
                    break
                print("Invalid move!")  
            self.make_move(move[0], move[1], Current_player)
            if self.is_game_over():
                break
            self.rotate_quadrant(move[3], move[2])
            if self.is_game_over():
                break
            self.switch_player()

        print("Game over:")
        self.print_board()
        print(f"Player X: {self.players[0].lines} line(s); Player O: {self.players[1].lines} line(s)")
        print("Draw game!") if self.winner == None else print(f"Player {self.winner.color.value} wins!")


# Sample client code
if __name__ == "__main__":
    board_size = int(input("Enter board size [default 6]: ") or 6)
    game = Pentago(n=board_size)
    game.run()
