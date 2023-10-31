
import numpy as np
from board import SquareType

class StateEvaluator:
    """
    Evaluates game states using a combination of weighted heuristic components.
    """

    def __init__(self, weights=None, heuristics=None):
        """
        Initialises the evaluator with specified weights and heuristic
        components for assessing game states.

        Args:
            weights (dict, optional): Dictionary of weights for each heuristic.
            heuristics (list, optional): List of heuristic components to use.
        """
        # Default weights, if not provided
        default_weights = {
            "disc_diff": 0.5,
            "mobility": 0.5
        }

        self.weights = weights if weights else default_weights
        self.heuristics = heuristics if heuristics else []

        if sum(self.weights.values()) != 1:
            raise ValueError("Heuristic weights must sum to 1.")
        

    def count_valid_moves(self, game, disc_color):
        return len(game.get_valid_moves_by_color(disc_color))
    

    def count_discs(self, game, disc_color):
        if disc_color == SquareType.BLACK:
            return game.black_score
        elif disc_color == SquareType.WHITE:
            return game.white_score
        else:
            raise ValueError("Invalid color specified.")
