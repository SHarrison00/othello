
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
        

    def disc_diff(self, board_state):
        """
        Calculates normalized disc difference between black and white player.
        
        Returns a value between -1 and 1, indicating an advantage for black 
        (positive) or white (negative).
        """
        black_discs = np.count_nonzero(board_state == SquareType.BLACK)
        white_discs = np.count_nonzero(board_state == SquareType.WHITE)
        
        # Avoid division by zero
        if black_discs + white_discs == 0:
            return 0

        return (black_discs - white_discs) / (black_discs + white_discs)