
import numpy as np
from enum import Enum, auto
from .board import SquareType

class HeuristicType(Enum):
    DISC_DIFF = auto()
    MOBILITY = auto()
    CORNERS = auto()


class StateEvaluator:
    """
    State evaluation using a weighted combination of heuristic components.
    """

    def __init__(self, weights=None):
        """
        Initialises the evaluator with specified heuristic weights.
        """

        self.heuristic_methods = {
            HeuristicType.DISC_DIFF: self.disc_diff_heuristic,
            HeuristicType.MOBILITY: self.mobility_heuristic,
            HeuristicType.CORNERS: self.corner_heuristic,
        }

        # Default weights, if not provided
        default_weights = {
            HeuristicType.DISC_DIFF: 0.5,
            HeuristicType.MOBILITY: 0.5,
            HeuristicType.CORNERS: 0
        }

        self.weights = weights if weights else default_weights

        # Check if weights sum to 1
        if not np.isclose(sum(self.weights.values()), 1):
            raise ValueError("Heuristic weights must sum to 1.")
        
        
    def evaluate(self, game):
        """
        Evaluate a game state using a weighted combination of heuristics.
 
        If the game has ended, assign +1 for Black win, and and -1 for White 
        win. Otherwise, evaluate using weighted heuristic components.

        Returns:
            float: The value of the game state or terminal state.
        """

        # If terminal state
        if game.is_finished:
            game.determine_winner()
            if game.game_result == "Black Wins":
                return 1
            elif game.game_result == "Draw":
                return 0
            elif game.game_result == "White Wins":
                return -1

        # If not terminal state
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
        """

        max_discs = self.count_discs(game, SquareType.BLACK)
        min_discs = self.count_discs(game, SquareType.WHITE)

        # Avoid division by zero
        if max_discs + min_discs == 0:
            return 0

        return (max_discs - min_discs) / (max_discs + min_discs)
    

    def count_corners(self, game, disc_color):

        CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
        count = 0
        for row, col in CORNERS:
            if game.board.state[row, col] == disc_color:
                count += 1

        return count


    def corner_heuristic(self, game):
        """
        Compute the corner control heuristic for the current state of the game. 
        """
        
        max_corners = self.count_corners(game, SquareType.BLACK)
        min_corners = self.count_corners(game, SquareType.WHITE)

        # Avoid division by zero
        if max_corners + min_corners == 0:
            return 0

        return (max_corners - min_corners) / (max_corners + min_corners)