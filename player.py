
import random
from enum import Enum
from board import SquareType
from state_evaluation import StateEvaluator

class PlayerType(Enum):
    USER = 'user'
    OFFLINE = 'offline'
    RANDOM = 'random_agent'
    MINIMAX = 'minimax'


class Player:
    """
    Represents an Othello player, detailing player type (e.g., user, or AI), 
    disc color, and any strategy for evaluating game states (e.g. Minimax).
    """

    def __init__(self, 
                 player_type: PlayerType, 
                 disc_color: SquareType, 
                 state_eval: StateEvaluator = None):
        """
        Initializes a player with a type, disc color, and an optional 
        state evaluation strategy.

        Args:
            player_type (PlayerType): The type of the player (e.g., user, AI).
            disc_color (SquareType): The color of the player's disc.
            state_eval (StateEvaluator, optional): Strategy state evaluation.
        """
        self.player_type = player_type
        self.disc_color = disc_color
        self.state_eval = state_eval if state_eval else StateEvaluator()

    
    def get_offline_move(self, game):
        """
        Retrieve the offline player's move.
        """

        while True:
            try:
                move = input("Enter your move: ")
                col = ord(move[0].lower()) - ord('a')
                row = int(move[1]) - 1
                
                # Now, use game instance itself, and Game method is_valid_move
                if game.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Enter the move in the format 'e4'.")


    def get_random_move(self, game):
        """
        Retrieve random agent's move.
        """

        # Traverse board to find all valid moves
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if game.board.state[row, col] == SquareType.VALID:
                    valid_moves.append((row, col))

        if not valid_moves:
            return None
        
        # Randomly choose a move from valid moves
        row, col = random.choice(valid_moves)

        return row, col
    

    def minimax(self, game, depth, maximizing_player):
        """
        Implementation of the Minimax algorithm that calculates the best move 
        for a given game state.

        Args:
            game (Game): The current state of the game.
            depth (int): The maximum depth to explore in the game tree.
            maximizing_player (bool): True if current player is maximizing; 
                                      otherwise, False.

        Returns:
            float: The optimal score a maximizing player can aim for, or the 
                optimal score a minimizing player can concede - in the given 
                game state.
        """
        # Base case: return board's value if reach max-depth, or game is over
        if depth == 0 or game.is_finished:
            return self.state_eval.evaluate(game)

        # Maximizing player's turn
        if maximizing_player:
            max_eval = float('-inf')
            for move in game.get_valid_moves_by_color(self.disc_color):
                simulated_game = game.simulate_move(move)
                eval = self.minimax(simulated_game, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval

        # Minimizing player's turn
        else:
            min_eval = float('inf')
            for move in game.get_valid_moves_by_color(self.disc_color):
                simulated_game = game.simulate_move(move)
                eval = self.minimax(simulated_game, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

