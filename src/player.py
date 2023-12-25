
import random
from enum import Enum
from .board import SquareType
from .state_evaluation import StateEvaluator

class PlayerType(Enum):
    USER = 'user'
    OFFLINE = 'offline'
    RANDOM = 'random_agent'
    MINIMAX = 'minimax'


class Player:
    """
    Represents a player, e.g player type and disc color etc.
    """

    def __init__(self, 
                 player_type: PlayerType, 
                 disc_color: SquareType, 
                 state_eval: StateEvaluator = None,
                 depth: int = 2):
        """
        Initialises a player with a type, disc color etc.

        Args:
            player_type (PlayerType): The type of the player (e.g., user, AI).
            disc_color (SquareType): The color of the player's disc.
            state_eval (StateEvaluator, optional): Strategy state evaluation.
            depth (int, optional): Depth for the Minimax algorithm.
        """

        self.player_type = player_type
        self.disc_color = disc_color
        self.state_eval = state_eval if state_eval else StateEvaluator()
        self.depth = depth

    
    def get_offline_move(self, game):
        """
        Get the offline player's move.
        """

        while True:
            try:
                move = input("Enter your move: ")
                col = ord(move[0].lower()) - ord('a')
                row = int(move[1]) - 1
                
                if game.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move. Try again.")

            except (ValueError, IndexError):
                print("Invalid input. Enter the move in the format 'e4'.")


    def get_random_move(self, game):
        """
        Get a random agent's move.
        """

        valid_moves = []
        for row in range(8):
            for col in range(8):
                if game.board.state[row, col] == SquareType.VALID:
                    valid_moves.append((row, col))

        if not valid_moves:
            return None
        
        # Randomly choose a move
        row, col = random.choice(valid_moves)

        return row, col
    

    def minimax(self, game, depth, maximizing_player):
        """
        Calculates the Minimax value for a given game state.

        Args:
            game (Game): The current state of the game.
            depth (int): The maximum depth to explore in the game tree.
            maximizing_player (bool): True if current player is maximizing; 
                                      otherwise, False.

        Returns:
            float: The optimal score a maximizing player can obtain, or the 
                optimal score a minimizing player can concede.
        """

        # Base case. Return board's value if reach max-depth or game over
        if depth == 0 or game.is_finished:
            return self.state_eval.evaluate(game)            

        if maximizing_player:
            max_eval = float('-inf')
            # Iterate across all moves for the active player
            for move in game.get_valid_moves_by_color(game.active.disc_color):
                simulated_game = game.simulate_move(move)

                # Evaluate and update
                eval = self.minimax(simulated_game, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            # Iterate across all moves for the active player
            for move in game.get_valid_moves_by_color(game.active.disc_color):
                simulated_game = game.simulate_move(move)

                # Evaluate and update
                eval = self.minimax(simulated_game, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
        

    def minimax_evaluate_moves(self, game):
        """
        Evaluate valid moves according to Minimax.

        Returns:
            List[Tuple[Tuple[int, int], float]]: A list of tuples, each 
            containing a valid move and its associated minimax value.
        """

        moves_with_values = []

        valid_moves = game.get_valid_moves_by_color(self.disc_color)

        if not valid_moves:
            return moves_with_values
        
        for move in valid_moves:
            simulated_game = game.simulate_move(move)

            # Compute the minimax value
            minimax_value = self.minimax(
                simulated_game, 
                self.depth - 1, 
                self.disc_color == SquareType.BLACK
            )

            # Add minimax value to list
            moves_with_values.append((move, minimax_value))

        return moves_with_values


    def get_minimax_move(self, game):
        """
        Get the best move using the Minimax algorithm.

        Returns:
            Tuple[int, int]: The row and column of the best move.
        """
        evaluated_moves = self.minimax_evaluate_moves(game)

        if not evaluated_moves:
            return None
        
        if self.disc_color == SquareType.BLACK:
            # Maximize the minimax value for Black.
            best_move = max(evaluated_moves, key=lambda item: item[1])[0]
        else:
            # Minimize the minimax value for White.
            best_move = min(evaluated_moves, key=lambda item: item[1])[0]

        return best_move