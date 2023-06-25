
from board import SquareType
from enum import Enum

class PlayerType(Enum):
    USER = 'user'
    OFFLINE = 'offline'
    RANDOM = 'random_agent'


class Player:
    """
    Representing the player and their strategy.
    """

    def __init__(self, player_type: PlayerType, disc_color: SquareType):
        self.player_type = player_type
        self.disc_color = disc_color

    
    def get_offline_user_move(self, game):
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
            