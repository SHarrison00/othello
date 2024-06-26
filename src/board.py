
import numpy as np
from enum import Enum

class SquareType(Enum):
    EMPTY = ' '
    BLACK = 'X'
    WHITE = 'O'
    VALID = '#'


class Board:
    """
    Represents the state of the game board.
    """

    def __init__(self):
        self.state = np.full((8, 8), SquareType.EMPTY)
        self.state[3, 3] = SquareType.WHITE
        self.state[3, 4] = SquareType.BLACK
        self.state[4, 3] = SquareType.BLACK
        self.state[4, 4] = SquareType.WHITE

        self.state[2, 3] = SquareType.VALID
        self.state[3, 2] = SquareType.VALID
        self.state[4, 5] = SquareType.VALID
        self.state[5, 4] = SquareType.VALID


    def display(self):
        """
        Display the board state in the console.
        """

        board_repr = np.array([
            [" " + square.value + " " for square in row]
            for row in self.state
        ])

        print('     A   B   C   D   E   F   G   H  ')
        print('  +' + '-' * 33 + '+')
        for i, row in enumerate(board_repr, start=1):
            row_str = '|'.join(row)
            print(f'{i} | {row_str} |')
            print('  +' + '-' * 33 + '+')