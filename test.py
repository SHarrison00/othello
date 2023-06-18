
import unittest
import numpy as np

from game import Game
from board import Board
from board import SquareType
from player import Player

class TestGame(unittest.TestCase):
    """
    Test functionality for the Game base class.
    """

    def test_player_colors(self):
        game = Game("Sam", "Alistair")

        # Check first player is black and the second is white
        self.assertEqual(game.player_black.disc_color, SquareType.BLACK)
        self.assertEqual(game.player_white.disc_color, SquareType.WHITE)


    def test_change_turn(self):
        game = Game("Sam", "Alistair")
        game.change_turn()

        # After changing turns, active player should be white
        self.assertEqual(game.active, game.player_white)
        self.assertEqual(game.inactive, game.player_black)


    def test_reset_valid_moves(self):
        game = Game("Sam", "Alistair")
        game.reset_valid_moves()

        EXPECTED_BOARD_STATE = np.full((8, 8), SquareType.EMPTY)
        EXPECTED_BOARD_STATE[3, 3] = SquareType.WHITE
        EXPECTED_BOARD_STATE[3, 4] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 3] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 4] = SquareType.WHITE

        game.board.display()

        # After reseting valid moves, we should expect the board state above
        assert np.array_equal(game.board.state, EXPECTED_BOARD_STATE) 


    def test_valid_moves_initial_board(self):
        """
        Test for valid moves on the initial board configuration. Assumes 
        implicitly the player is black, and the opponent is white.
        """

        game = Game("Sam", "Alistair")
        valid_moves = game.get_valid_moves()
        
        EXPECTED_VALID_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(set(valid_moves), set(EXPECTED_VALID_MOVES))


    def test_valid_moves_near_full_board(self):
        """
        Test for valid moves on a board configuration that is nearly full. 
        Assumes implicitly the player is black, and the opponent is white.
        """

        game = Game("Sam", "Alistair")
        valid_moves = game.get_valid_moves()

        # Initialise nearly full board configuration, with two empty spaces
        NEARLY_FULL_BOARD = [
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 7 + [SquareType.EMPTY],
        ]

        game.board.state = np.array(NEARLY_FULL_BOARD)

        valid_moves = game.get_valid_moves()

        EXPECTED_VALID_MOVES = [(7, 7)]
        self.assertEqual(set(valid_moves), set(EXPECTED_VALID_MOVES))

    
    def test_update_valid_moves(self):
        """
        Test that the update valid modes function correctly updates the board
        state when called. 
        """

        game = Game("Sam", "Alistair")

        # Initialise nearly full board configuration, with two empty spaces
        NEARLY_FULL_BOARD = [
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 8,
            [SquareType.WHITE] * 7 + [SquareType.EMPTY],
        ]

        game.board.state = np.array(NEARLY_FULL_BOARD)

        VALID_MOVES = [(7, 7)]
        game.update_valid_moves(VALID_MOVES)
        self.assertEqual(game.board.state[7,7], SquareType.VALID)


if __name__ == '__main__':
    unittest.main(verbosity=2)