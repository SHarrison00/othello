
import unittest
import numpy as np
from game import Game
from board import Board
from board import SquareType
from player import Player
from player import PlayerType
from state_evaluation import StateEvaluator, HeuristicType

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




class TestPlayer(unittest.TestCase):
    """
    Test functionality related to the Player class.
    """

    def test_state_evaluator_integration_with_player(self):
        # Initialize a StateEvaluator with custom weights
        custom_weights = {
            "disc_diff": 0.7,
            "mobility": 0.3
        }
        state_evaluator = StateEvaluator(weights=custom_weights)
        
        # Initialize a player with this StateEvaluator
        player = Player(PlayerType.MINIMAX, SquareType.BLACK, state_evaluator)
        
        # Initialize game to use in testing evaluator methods
        game = Game(player, PlayerType.RANDOM)
        
        # Check StateEvaluator's methods work correctly when called from player
        valid_moves_count = player.state_eval.count_valid_moves(game, player.disc_color)
        disc_count = player.state_eval.count_discs(game, player.disc_color)
        self.assertEqual(valid_moves_count, 4)
        self.assertEqual(disc_count, 2)




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




class TestHeuristics(unittest.TestCase):
    """
    Test functionality of any heuristic functions.
    """
        
    def setUp(self):
        """
        Set up a non-trivial board state for testing.
        """
        self.game = Game(PlayerType.USER, PlayerType.RANDOM)

        # Clear the board for a custom setup
        self.game.board.state = np.full((8, 8), SquareType.EMPTY)

        # Place discs for a non-trivial state, 
        # e.g. Black plays D3 
        self.game.board.state[2, 3] = SquareType.BLACK
        # Initial Othello "square" then looks like,
        self.game.board.state[3, 3] = SquareType.BLACK
        self.game.board.state[3, 4] = SquareType.BLACK
        self.game.board.state[4, 3] = SquareType.BLACK
        self.game.board.state[4, 4] = SquareType.WHITE

        # Update scores based on new board
        self.game.update_scores()

        # Custom weights for testing
        custom_weights = {
            HeuristicType.DISC_DIFF: 0.7,
            HeuristicType.MOBILITY: 0.3
        }
        
        # Initialize StateEvaluator
        self.evaluator = StateEvaluator(weights=custom_weights)


    def test_disc_diff_heuristic(self):
        """
        Test the disc difference heuristic on a non-trivial board state.
        """
        EXPECTED_DISC_DIFF = 0.6
        disc_diff = self.evaluator.disc_diff_heuristic(self.game)
        self.assertEqual(disc_diff, EXPECTED_DISC_DIFF, 
                         "Disc difference heuristic evaluated incorrectly.")


    def test_mobility_heuristic(self):
        """
        Test the mobility heuristic on a non-trivial board state.
        """
        EXPECTED_MOBILITY = 0.0
        mobility = self.evaluator.mobility_heuristic(self.game)
        self.assertEqual(mobility, EXPECTED_MOBILITY, 
                         "Mobility heuristic evaluated incorrectly.")
        

    def test_evaluate(self):
        """
        Test evaluate function with custom weighted combination of heuristics.
        """
        EXPECTED_EVALUATION_SCORE = 0.42
        evaluation_score = self.evaluator.evaluate(self.game)
        self.assertEqual(evaluation_score, EXPECTED_EVALUATION_SCORE, 
                         "Evaluate function didn't return expected score.")
        



class TestSimulateMove(unittest.TestCase):

    def setUp(self):
        """
        Set up an initial board state for testing the simulate_move function.
        """
        self.game = Game(PlayerType.USER, PlayerType.RANDOM)
        self.initial_board = self.game.board.state.copy()


    def test_simulate_move_d3(self):
        """
        Test simulate_move correctly simulates a move when black plays D3.
        """
        # Black plays D3
        move = (2, 3)
        simulated_game = self.game.simulate_move(move)
        
        # Check if the simulated game's board state has changed correctly
        self.assertFalse(np.array_equal(self.initial_board, simulated_game.board.state),
                         "The board state should have changed after simulating the move.")
        
        # Check if the move at D3 has been played by black
        self.assertEqual(simulated_game.board.state[move], SquareType.BLACK,
                         "D3 should be occupied by black.")
        
        # Check if the active player has changed to white after black's move
        self.assertEqual(simulated_game.active.disc_color, SquareType.WHITE,
                         "The active player should now be white.")

        # Check that the number of valid moves for white has been updated
        white_valid_moves = simulated_game.get_valid_moves_by_color(SquareType.WHITE)
        self.assertTrue(len(white_valid_moves) == 3,
                        "White should have at least three valid moves after black plays D3.")

        # Check that the scores have been updated correctly
        # Assuming that black's D3 move flips one white disc to black
        self.assertEqual(simulated_game.black_score, 4,
                         "Black should have a score of 4 after playing D3.")
        self.assertEqual(simulated_game.white_score, 1,
                         "White should have a score of 1 after black plays D3.")
        

if __name__ == '__main__':
    unittest.main(verbosity=2)