
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


        Computes the game state's evaluation by summing the weighted scores of 
        each heuristic in self.weights dictionary. Each heuristic score is 
        calculated by its method and multiplied by its weight.

        Returns:
            float: The weighted evaluation of the game state.
        """
        # Initialize the score to zero.
        score = 0.0

        # Iterate through all selected heuristics and weights
        for heuristic_type, weight in self.weights.items():
            # Find heuristic method in dictionary
            method = self.heuristic_methods.get(heuristic_type)

            if method is not None:
                # Calculate weighted heuristic and add to score.
                score += weight * method(game)
            else:
                # Raise error if heuristic method not found in dictionary
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