
import unittest
import numpy as np
from old import Board

class TestBoard(unittest.TestCase):

    def test_valid_moves_initial_board(self):
        """
        Test for valid moves on the initial board configuration. Assumes 
        implicitly the player is black and the opponent is white.
        """
        board = Board()
        valid_moves = board.get_valid_moves()
        expected_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(set(valid_moves), set(expected_moves))

    def test_valid_moves_near_full_board(self):
        """
        Test for valid moves on a board configuration that is nearly full. 
        Assumes implicitly the player is black and the opponent is white.
        """
        board = Board()
        
        # Initialise nearly full board configuration, with two empty spaces
        nearly_full_board = [
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', ' ', 'O', 'O', 'O', 'O', 'O', ' '],
        ]
        board.board = np.array(nearly_full_board)
        
        valid_moves = board.get_valid_moves()
        expected_moves = [(7, 1), (7, 7)]
        self.assertEqual(set(valid_moves), set(expected_moves))

    def test_valid_moves_full_board(self):
        """
        Test for valid moves on a completely full board configuration.
        Assumes implicitly the player is black and the opponent is white.
        """
        board = Board()
        
        # Initialise a completely full board configuration
        full_board = [
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ]
        board.board = np.array(full_board)
        
        valid_moves = board.get_valid_moves()
        self.assertEqual(valid_moves, [])

    def test_valid_moves_black_dominating(self):
        pass
   


if __name__ == '__main__':
    unittest.main(verbosity=2)