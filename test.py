
import unittest
import numpy as np

from game import Game
from board import Board
from board import SquareType
from player import Player
from player import PlayerType

class TestGame(unittest.TestCase):
    """
    Test functionality for the Game base class.
    """

    def test_player_colors(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)

        # Check first player is black and the second is white
        self.assertEqual(game.player_black.disc_color, SquareType.BLACK)
        self.assertEqual(game.player_white.disc_color, SquareType.WHITE)


    def test_change_turn(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        game.change_turn()

        # After changing turns, active player should be white
        self.assertEqual(game.active, game.player_white)
        self.assertEqual(game.inactive, game.player_black)


    def test_reset_valid_moves(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        game.reset_valid_moves()

        EXPECTED_BOARD_STATE = np.full((8, 8), SquareType.EMPTY)
        EXPECTED_BOARD_STATE[3, 3] = SquareType.WHITE
        EXPECTED_BOARD_STATE[3, 4] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 3] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 4] = SquareType.WHITE

        # After reseting valid moves, we should expect the board state above
        assert np.array_equal(game.board.state, EXPECTED_BOARD_STATE) 


    def test_valid_moves_initial_board(self):
        """
        Test for valid moves on the initial board configuration. Assumes 
        implicitly the player is black, and the opponent is white.
        """

        game = Game(PlayerType.USER, PlayerType.RANDOM)

        # First, we reset the valid moves that are defined when the board is
        # instantiated at the start
        game.reset_valid_moves()

        # Then, we can test the functionality of get_valid_moves()
        valid_moves = game.get_valid_moves()
        
        EXPECTED_VALID_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(set(valid_moves), set(EXPECTED_VALID_MOVES))


    def test_valid_moves_near_full_board(self):
        """
        Test for valid moves on a board configuration that is nearly full. 
        Assumes implicitly the player is black, and the opponent is white.
        """

        game = Game(PlayerType.USER, PlayerType.RANDOM)
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
        Test valid modes are updated to the board state as intended.
        """

        game = Game(PlayerType.USER, PlayerType.RANDOM)

        # Initialise nearly full board configuration, with one empty spaces
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
        game.update_valid_moves()
        self.assertEqual(game.board.state[7,7], SquareType.VALID)

    
    def test_disc_to_flip(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        
        # Two cases to test
        self.assertEqual(game.discs_to_flip(0 , 0), [])
        self.assertEqual(game.discs_to_flip(2 , 3), [(3, 3)])


    def test_is_board_full_empty_board(self):
        game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        self.assertFalse(game.is_board_full())


    def test_is_board_full_full_board(self):
        game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)

        for row in range(8):
            for col in range(8):
                game.board.state[row, col] = SquareType.BLACK
        self.assertTrue(game.is_board_full())


    def test_get_offline_user_move(self):
        pass


    def test_is_finished(self):
        game1 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        game1.next_move = (2, 3)
        game1.is_finished()
        assert not game1.is_finished, "Basic fail."

        game2 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        game2.next_move = None
        game2.prev_move = None
        game2.is_finished()
        assert game2.is_finished, "'Neither move' fail."

        game3 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        for row in range(8):
            for col in range(8):
                game3.board.state[row, col] = SquareType.BLACK
        game3.is_finished()
        assert game3.is_finished, "Full board fail."


if __name__ == '__main__':
    unittest.main(verbosity=2)