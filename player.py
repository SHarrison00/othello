
import random

from board import SquareType
from enum import Enum

class PlayerType(Enum):
    USER = 'user'
    OFFLINE = 'offline'
    RANDOM = 'random_agent'
    MINIMAX = 'minimax'


class Player:
    """
    Represents each Othello player, storing information about the type of 
    player (e.g., user, or AI) and disc colour.
    """

    def __init__(self, player_type: PlayerType, disc_color: SquareType):
        self.player_type = player_type
        self.disc_color = disc_color

    
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
    

    def get_minimax_move(self, game):
        """
        Retrieve minimax agent's move.
        """


