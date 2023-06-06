
import numpy as np

class Board:
    """
    Handles the game board, its state, and valid moves.
    """

    def __init__(self):
        self.state = np.full((8, 8), ' ')
        self.state[3, 3] = 'O'
        self.state[3, 4] = 'X'
        self.state[4, 3] = 'X'
        self.state[4, 4] = 'O'

    def display(self):
        print(self.board)

