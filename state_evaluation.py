
import numpy as np
from board import SquareType
from enum import Enum, auto

class HeuristicType(Enum):
    DISC_DIFF = auto()
    MOBILITY = auto()


class StateEvaluator:
    """
    Evaluates game states using combination of weighted heuristic components.
    """

    def __init__(self, weights=None):
        """
        Initialises the evaluator with specified weights for each heuristic.
        """

        self.heuristic_methods = {
            HeuristicType.DISC_DIFF: self.disc_diff_heuristic,
            HeuristicType.MOBILITY: self.mobility_heuristic,
        }

        # Default weights, if not provided
        default_weights = {
            HeuristicType.DISC_DIFF: 0.5,
            HeuristicType.MOBILITY: 0.5
        }

        self.weights = weights if weights else default_weights

        # Check if weights sum to 1
        if not np.isclose(sum(self.weights.values()), 1):
            raise ValueError("Heuristic weights must sum to 1.")
        
        
    def evaluate(self, game):
        """
        Evaluate game state by combining the results of weighted heuristics.

        If the game has finished, assign +1 for Black win, 0 for draw, and -1 
        for White win. Otherwise, compute the game state's evaluation by 
        summing the weighted scores of each heuristic.

        Args:
            game (Game): The current game state.

        Returns:
            float: The weighted evaluation of the game state or the value of the
            terminal state.
        """
        # If terminal state, assign numerical values 
        if game.is_finished:
            game.determine_winner()
            if game.game_result == "Black":
                return 1
            elif game.game_result == "Draw":
                return 0
            elif game.game_result == "White":
                return -1

        # If not terminal state, calculate heuristic score
        score = 0.0
        for heuristic_type, weight in self.weights.items():
            method = self.heuristic_methods.get(heuristic_type)
            if method is not None:
                score += weight * method(game)
            else:
                raise ValueError(f"Can't find {heuristic_type} method.")
        return score

        
    def count_valid_moves(self, game, disc_color):
        return len(game.get_valid_moves_by_color(disc_color))
    
        
    def mobility_heuristic(self, game):
        """
        Compute the mobility heuristic for the current state of the game. 
        Mobility is defined as the normalized difference between the number of 
        valid moves for the MAX (black) player and the MIN (white) player.
        """
        max_moves = self.count_valid_moves(game, SquareType.BLACK)
        min_moves = self.count_valid_moves(game, SquareType.WHITE)

        # Avoid division by zero 
        if max_moves + min_moves == 0:
            return 0

        return (max_moves - min_moves) / (max_moves + min_moves)
    

    def count_discs(self, game, disc_color):
        if disc_color == SquareType.BLACK:
            return game.black_score
        elif disc_color == SquareType.WHITE:
            return game.white_score
        else:
            raise ValueError("Invalid color specified.")
    

    def disc_diff_heuristic(self, game):
        """
        Compute the disc difference heuristic for current state of the game.
        Disc difference is defined as the normalized difference between the
        number of discs for the MAX (black) player and the MIN (white) player.
        """
        max_discs = self.count_discs(game, SquareType.BLACK)
        min_discs = self.count_discs(game, SquareType.WHITE)

        # Avoid division by zero
        if max_discs + min_discs == 0:
            return 0

        return (max_discs - min_discs) / (max_discs + min_discs)
    

    def count_corners(self, game, disc_color):
        pass


    def corner_heuristic(self, game):
        pass