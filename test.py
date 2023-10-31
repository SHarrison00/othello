
import unittest
import numpy as np
from game import Game
from board import Board
from board import SquareType
from player import Player
from player import PlayerType
from state_evaluation import StateEvaluator

class TestGame(unittest.TestCase):
    """
    Test functionality for the Game class.
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


    def test_get_offline_move(self):
        pass


    def test_is_finished(self):
        game1 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        game1.next_move = (2, 3)
        game1.check_finished()
        assert not game1.is_finished, "Basic fail."

        game2 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        game2.next_move = None
        game2.prev_move = None
        game2.check_finished()
        assert game2.is_finished, "'Neither move' fail."

        game3 = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
        for row in range(8):
            for col in range(8):
                game3.board.state[row, col] = SquareType.BLACK
        game3.check_finished()
        assert game3.is_finished, "Full board fail."


    def test_no_valid_moves(self):
        game = Game(PlayerType.RANDOM, PlayerType.RANDOM)

        NO_VALID_MOVES_BOARD = [
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.BLACK] * 8,
            [SquareType.EMPTY] * 8 
        ]

        game.board.state = np.array(NO_VALID_MOVES_BOARD)

        # Assert next_move is set to None
        game.get_player_move()
        self.assertIsNone(game.next_move)


    def test_get_valid_moves_by_color(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)

        # Expected valid moves for black and white
        EXPECTED_BLACK_VALID_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
        EXPECTED_WHITE_VALID_MOVES = [(2, 4), (3, 5), (4, 2), (5, 3)]


        # Fetch valid moves using the function
        black_valid_moves = game.get_valid_moves_by_color(SquareType.BLACK)
        white_valid_moves = game.get_valid_moves_by_color(SquareType.WHITE)

        # Assert the fetched moves match the expected moves
        self.assertListEqual(black_valid_moves, EXPECTED_BLACK_VALID_MOVES)
        self.assertListEqual(white_valid_moves, EXPECTED_WHITE_VALID_MOVES)




class TestStateEvaluator(unittest.TestCase):
    """
    Test functionality for the StateEvaluator class.
    """

    def test_count_valid_moves(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        evaluator = StateEvaluator()

        # Expected valid moves for black and white
        EXPECTED_BLACK_VALID_MOVES_COUNT = 4
        EXPECTED_WHITE_VALID_MOVES_COUNT = 4

        # Fetch valid moves count using the function
        black_valid_moves_count = evaluator.count_valid_moves(game, SquareType.BLACK)
        white_valid_moves_count = evaluator.count_valid_moves(game, SquareType.WHITE)

        # Assert the fetched moves count match the expected count
        self.assertEqual(black_valid_moves_count, EXPECTED_BLACK_VALID_MOVES_COUNT)
        self.assertEqual(white_valid_moves_count, EXPECTED_WHITE_VALID_MOVES_COUNT)


    def test_count_discs(self):
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        evaluator = StateEvaluator()

        # Expected disc count for black and white
        EXPECTED_BLACK_DISC_COUNT = 2
        EXPECTED_WHITE_DISC_COUNT = 2

        # Fetch disc count using the function
        black_disc_count = evaluator.count_discs(game, SquareType.BLACK)
        white_disc_count = evaluator.count_discs(game, SquareType.WHITE)

        # Assert the fetched disc count match the expected count
        self.assertEqual(black_disc_count, EXPECTED_BLACK_DISC_COUNT)
        self.assertEqual(white_disc_count, EXPECTED_WHITE_DISC_COUNT)


if __name__ == '__main__':
    unittest.main(verbosity=2)