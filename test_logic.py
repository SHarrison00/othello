
import unittest
import numpy as np
from logic import Board

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
        """
        Test for valid moves on a board configuration where black is dominating 
        and there is only one space left for a valid move for black. There are 
        no moves possible for white.
        """
        board = Board()
        
        # Initialise a board configuration where black is dominating
        board.board = np.full((8, 8), 'X')
        board.board[6, 1] = 'O' # Require to avoid game already being over
        board.board[7, 1] = ' '
        board.display()
        
        valid_moves_black = board.get_valid_moves()
        expected_moves = [(7, 1)]
        
        # Check the valid moves for the player that is black
        self.assertEqual(set(valid_moves_black), set(expected_moves), 
            "The only valid move for black should be (7, 1).")
        
        # Check there are no valid moves for the player that is white
        board.switch_players()
        valid_moves_white = board.get_valid_moves()
        self.assertEqual(valid_moves_white, [],
            "There should be no valid moves for white.")


if __name__ == '__main__':
    unittest.main(verbosity=2)