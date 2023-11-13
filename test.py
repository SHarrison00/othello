
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

    def setUp(self):
        # Create players
        self.black_player = Player(PlayerType.RANDOM, SquareType.BLACK)
        self.white_player = Player(PlayerType.RANDOM, SquareType.WHITE)
        # Initialize the game with these players
        self.game = Game(self.black_player, self.white_player)


    def test_player_colors(self):
        # Check first player is black and the second is white
        self.assertEqual(self.game.player_black.disc_color, SquareType.BLACK)
        self.assertEqual(self.game.player_white.disc_color, SquareType.WHITE)


    def test_change_turn(self):
        self.game.change_turn()
        # After changing turns, active player should be white
        self.assertEqual(self.game.active, self.game.player_white)
        self.assertEqual(self.game.inactive, self.game.player_black)


    def test_reset_valid_moves(self):
        self.game.reset_valid_moves()

        EXPECTED_BOARD_STATE = np.full((8, 8), SquareType.EMPTY)
        EXPECTED_BOARD_STATE[3, 3] = SquareType.WHITE
        EXPECTED_BOARD_STATE[3, 4] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 3] = SquareType.BLACK
        EXPECTED_BOARD_STATE[4, 4] = SquareType.WHITE

        # After reseting valid moves, we should expect the board state above
        assert np.array_equal(self.game.board.state, EXPECTED_BOARD_STATE) 


    def test_valid_moves_initial_board(self):
        """
        Test for valid moves on the initial board configuration. Assumes 
        implicitly the player is black, and the opponent is white.
        """
        # First, we reset the valid moves that are defined when the board is
        # instantiated at the start
        self.game.reset_valid_moves()

        # Then, we can test the functionality of get_valid_moves()
        valid_moves = self.game.get_valid_moves()
        
        EXPECTED_VALID_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(set(valid_moves), set(EXPECTED_VALID_MOVES))


    def test_valid_moves_near_full_board(self):
        """
        Test for valid moves on a board configuration that is nearly full. 
        Assumes implicitly the player is black, and the opponent is white.
        """
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
        self.game.board.state = np.array(NEARLY_FULL_BOARD)

        valid_moves = self.game.get_valid_moves()

        EXPECTED_VALID_MOVES = [(7, 7)]
        self.assertEqual(set(valid_moves), set(EXPECTED_VALID_MOVES))

    
    def test_update_valid_moves(self):
        """
        Test valid modes are updated to the board state as intended.
        """
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
        self.game.board.state = np.array(NEARLY_FULL_BOARD)
        self.game.update_valid_moves()
        self.assertEqual(self.game.board.state[7,7], SquareType.VALID)

    
    def test_disc_to_flip(self):        
        self.assertEqual(self.game.discs_to_flip(0 , 0), [])
        self.assertEqual(self.game.discs_to_flip(2 , 3), [(3, 3)])


    def test_is_board_full_empty_board(self):
        self.assertFalse(self.game.is_board_full())


    def test_is_board_full_full_board(self):
        self.game.board.state = np.full((8, 8), SquareType.BLACK)
        self.assertTrue(self.game.is_board_full())


    def test_is_finished(self):
        self.game.next_move = (2, 3)
        self.game.check_finished()
        assert not self.game.is_finished, "Game should not be finished."

        self.game.next_move = None
        self.game.prev_move = None
        self.game.check_finished()
        assert self.game.is_finished, \
            "Game should finnish when there are no moves for either player."

        self.game.board.state = np.full((8, 8), SquareType.BLACK)
        self.game.check_finished()
        assert self.game.is_finished, \
            "Game should be finished when the board is full."


    def test_no_valid_moves(self):
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
        self.game.board.state = np.array(NO_VALID_MOVES_BOARD)
        self.game.get_player_move()
        # Assert next_move is set to None
        self.assertIsNone(self.game.next_move, "There should be no valid moves.")


    def test_get_valid_moves_by_color(self):
        EXPECTED_BLACK_VALID_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
        EXPECTED_WHITE_VALID_MOVES = [(2, 4), (3, 5), (4, 2), (5, 3)]

        # Fetch valid moves using the function
        black_valid_moves = self.game.get_valid_moves_by_color(SquareType.BLACK)
        white_valid_moves = self.game.get_valid_moves_by_color(SquareType.WHITE)

        # Assert the fetched moves match the expected moves
        self.assertListEqual(black_valid_moves, EXPECTED_BLACK_VALID_MOVES)
        self.assertListEqual(white_valid_moves, EXPECTED_WHITE_VALID_MOVES)

    
    def test_white_wins(self):
        # Set up the game state where White is the winner
        self.game.board.state.fill(SquareType.WHITE)
        self.game.update_scores()
        
        # End the game
        self.game.check_finished()
        self.game.determine_winner()
        
        # Assert White is the winner
        self.assertEqual(self.game.game_result, "White", \
                         "White should be the winner but isn't.")
        
        
    def test_draw(self):
        # Set up the game state as a draw
        for row in range(4):
            for col in range(8):
                self.game.board.state[row, col] = SquareType.WHITE
        for row in range(4, 8):
            for col in range(8):
                self.game.board.state[row, col] = SquareType.BLACK
        self.game.update_scores()
        
        # End the game
        self.game.check_finished()
        self.game.determine_winner()
        
        # Assert the game is a draw
        self.assertEqual(self.game.game_result, "Draw", \
                         "The game should be a draw but isn't.")




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
        black_player = Player(PlayerType.MINIMAX, SquareType.BLACK, state_evaluator)
        white_player = Player(PlayerType.RANDOM, SquareType.WHITE)

        # Initialize game to use in testing evaluator methods
        game = Game(black_player, white_player)
        
        # Check StateEvaluator's methods work correctly when called from player
        valid_moves_count = black_player.state_eval.count_valid_moves(game, black_player.disc_color)
        disc_count = black_player.state_eval.count_discs(game, black_player.disc_color)
        self.assertEqual(valid_moves_count, 4)
        self.assertEqual(disc_count, 2)




class TestStateEvaluator(unittest.TestCase):
    """
    Test functionality for the StateEvaluator class.
    """

    def setUp(self):
        # Initialize a StateEvaluator with default weights
        self.evaluator = StateEvaluator()
        
        # Initialize players with the StateEvaluator
        black_player = Player(PlayerType.MINIMAX, SquareType.BLACK, self.evaluator)
        white_player = Player(PlayerType.RANDOM, SquareType.WHITE)
        
        # Initialize game to use in testing evaluator methods
        self.game = Game(black_player, white_player)


    def test_count_valid_moves(self):
        # Expected valid moves for black and white
        EXPECTED_BLACK_VALID_MOVES_COUNT = 4
        EXPECTED_WHITE_VALID_MOVES_COUNT = 4

        # Fetch valid moves count using the function
        black_valid_moves_count = self.evaluator.count_valid_moves(self.game, SquareType.BLACK)
        white_valid_moves_count = self.evaluator.count_valid_moves(self.game, SquareType.WHITE)

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
        # Custom weights for testing
        custom_weights = {
            HeuristicType.DISC_DIFF: 0.7,
            HeuristicType.MOBILITY: 0.3
        }

        # Initialize StateEvaluator with custom weights
        self.evaluator = StateEvaluator(weights=custom_weights)

        # Initialize players with the StateEvaluator
        black_player = Player(PlayerType.MINIMAX, SquareType.BLACK, self.evaluator)
        white_player = Player(PlayerType.RANDOM, SquareType.WHITE)

        # Initialize game with the players
        self.game = Game(black_player, white_player)

        # Clear the board for a custom setup
        self.game.board.state = np.full((8, 8), SquareType.EMPTY)

        # Place discs for a non-trivial state
        self.game.board.state[2, 3] = SquareType.BLACK  # Black plays D3
        self.game.board.state[3, 3] = SquareType.BLACK
        self.game.board.state[3, 4] = SquareType.BLACK
        self.game.board.state[4, 3] = SquareType.BLACK
        self.game.board.state[4, 4] = SquareType.WHITE

        # Update scores based on new board
        self.game.update_scores()


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
        

    def test_count_corners(self):
        """
        Test the count_corners function for accuracy.
        """
        # Setup a board state with specific corners occupied
        self.game.board.state[0, 0] = SquareType.BLACK
        self.game.board.state[0, 7] = SquareType.WHITE
        self.game.board.state[7, 0] = SquareType.EMPTY
        self.game.board.state[7, 7] = SquareType.BLACK

        # Count corners for both black and white
        black_corners = self.evaluator.count_corners(self.game, SquareType.BLACK)
        white_corners = self.evaluator.count_corners(self.game, SquareType.WHITE)

        # Assert that the corner counts are correct
        self.assertEqual(black_corners, 2, "Incorrect corner count for Black.")
        self.assertEqual(white_corners, 1, "Incorrect corner count for White.")

    
    def test_corner_heuristic(self):
        """
        Test the corner heuristic function for various board states.
        """
        # Set up a board state with specific corners occupied
        self.game.board.state[0, 0] = SquareType.BLACK
        self.game.board.state[0, 7] = SquareType.WHITE
        self.game.board.state[7, 0] = SquareType.EMPTY
        self.game.board.state[7, 7] = SquareType.BLACK

        # Compute the corner heuristic value
        corner_heuristic = self.evaluator.corner_heuristic(self.game)

        # Expected value: Black controls 2 corners, White controls 1 corner
        # Expected heuristic value = (2 - 1) / (2 + 1) = 1/3
        EXPECTED_VALUE = 1/3

        # Assert that the heuristic value is as expected
        self.assertAlmostEqual(corner_heuristic, EXPECTED_VALUE, \
                               msg="Corner heuristic calculated incorrectly.")


    def test_evaluate(self):
        """
        Test evaluate function with custom weighted combination of heuristics.
        """
        EXPECTED_EVALUATION_SCORE = 0.42
        evaluation_score = self.evaluator.evaluate(self.game)
        self.assertEqual(evaluation_score, EXPECTED_EVALUATION_SCORE, 
                         "Evaluate function didn't return expected score.")
        

    def test_evaluate_black_win(self):
        """
        Test evaluate function returns +1 for a Black win.
        """
        # Set up a winning board state for Black
        self.game.board.state.fill(SquareType.BLACK)
        self.game.board.state[0, 0] = SquareType.WHITE 

        # Update scores and check game had finished
        self.game.update_scores() # i.e. Black wins 63-1
        self.game.check_finished()

        # Call the evaluate function
        evaluator = StateEvaluator()
        evaluation_score = evaluator.evaluate(self.game)

        # Assert that the evaluation function returns +1 for a Black win
        self.assertEqual(evaluation_score, 1, 
                         "Evaluate function should return +1 for a Black win.")
        



class TestSimulateMove(unittest.TestCase):

    def setUp(self):
        """
        Set up an initial board state for testing the simulate_move function.
        """
        # Initialize players
        black_player = Player(PlayerType.USER, SquareType.BLACK, StateEvaluator())
        white_player = Player(PlayerType.RANDOM, SquareType.WHITE)
        
        # Initialize the game with these players
        self.game = Game(black_player, white_player)
        self.initial_board = np.copy(self.game.board.state)


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
        



class TestMinimax(unittest.TestCase):
    """
    Test the functionality of the minimax algorithm.
    """

    def setUp(self):
        """
        Set up an initial board state for testing the minimax function.
        """
        # Initialize StateEvaluator with default (or custom) weights
        state_evaluator = StateEvaluator()

        # Initialize a minimax player with the StateEvaluator
        minimax_player_black = Player(PlayerType.MINIMAX, SquareType.BLACK, state_evaluator)
        minimax_player_white = Player(PlayerType.MINIMAX, SquareType.WHITE, state_evaluator)
        
        # Initialize the game with minimax as black and random as white
        self.game = Game(minimax_player_black, minimax_player_white)


    def test_minimax_base_case(self):
        """
        Test minimax values for all possible initial moves for Black. Evaluates 
        the immediate impact of each move according to base case of Minimax. 
        """
        # Initial valid moves for Black
        initial_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        
        # Expected value (by symmetry) for each move
        EXPECTED_MINIMAX_VALUE = 0.3
        
        for move in initial_moves:
            # Simulate the move on the board
            simulated_game = self.game.simulate_move(move)

            # Calculate the minimax value for the resulting game state at the base case,
            # where depth is 0. This will invoke the heuristic evaluation directly
            # since the base case does not involve recursive lookahead.
            minimax_value = simulated_game.player_black.minimax(simulated_game, 0, True)
            
            # Assert that the minimax value is as expected
            self.assertEqual(minimax_value, EXPECTED_MINIMAX_VALUE,
                f"Minimax value for {move}  expected to be {EXPECTED_MINIMAX_VALUE}, but got {minimax_value}.")
            

    def test_minimax_recursion(self):
        """
        Test the recursive behavior of the Minimax algorithm by evaluating the 
        potential moves for White after Black plays D3, and ensuring that the 
        algorithm correctly calculates the minimax value two levels deep (i.e.
        depth = 2, where 'Black plays D3' is the initial state).
        """
        # Black plays D3 (initial state)
        simulated_game = self.game.simulate_move((2, 3))

        # Looking 2 moves ahead, i.e all possible White moves, and Black responses
        simulated_game.player_white.depth = 2
        white_moves = simulated_game.player_white.minimax_evaluate_moves(simulated_game)

        # Define the expected minimax values for White's possible moves
        EXPECTED_MINIMAX_VALUES = {
            (2, 2): 0.08928571428571427, # 5/56
            (2, 4): 0.16883116883116883, # 13/77
            (4, 2): 0.21428571428571427  # 3/14
        }

        # Check calculated minimax values match expected values
        for move, value in white_moves:
            self.assertAlmostEqual(value, EXPECTED_MINIMAX_VALUES[move],
                msg=f"Minimax value for move {move} expected to be {EXPECTED_MINIMAX_VALUES[move]}, but got {value}.")


    def test_get_minimax_move(self):
        """
        Test get_minimax_move function retrieves the best move for White 
        using the Minimax algorithm after Black plays D3.
        """
        # Black plays D3 (initial state)
        simulated_game = self.game.simulate_move((2, 3))

        # Set the depth for White's minimax evaluation
        simulated_game.player_white.depth = 2
        best_move_white = simulated_game.player_white.get_minimax_move(simulated_game)

        # Expected best move for White
        EXPECTED_BEST_MOVE = (2, 2)

        # Assert that the best move is as expected
        self.assertEqual(best_move_white, EXPECTED_BEST_MOVE,
                        f"The best minimax move for White expected to be {EXPECTED_BEST_MOVE}, but got {best_move_white}.")
        
if __name__ == '__main__':
    unittest.main(verbosity=2)