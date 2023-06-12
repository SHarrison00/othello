
from board import Board
from player import Player

class Game:
    """
    Main orchestrator, managing overall game flow.    
    """

    def __init__(self, player_black, player_white):
        self.board = Board()
        self.is_finished = False

        # Player instances are inputs 
        self.player_black = Player(player_black, 'X')
        self.player_white = Player(player_white, 'O')

        # Black always starts
        self.active = self.player_black
        self.inactive = self.player_white

    def change_turn(self):
        self.active, self.inactive = self.inactive, self.active

    def is_valid_move(self, row, col):
        """
        Checks the validity of a move. Involves traversing in different 
        DIRECTIONS on the board, and checking the traversed sequence of discs.

        Args:
            row (int): The row coordinate of the move.
            col (int): The column coordinate of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        # Move is invalid if the cell is not empty 
        if self.board.state[row, col] != ' ':
            return False

        # Traversable directions; up, down, left, right and all diagonals
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Traverse board in specified direction
        for direction in DIRECTIONS:
            d_row, d_col = direction
            row, col = row + d_row, col + d_col
            found_opposing_disc = False
            
            # While within boundaries
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board.state[row, col] == ' ':
                    break

                if self.board.state[row, col] == self.active.disc_color:
                    if found_opposing_disc:
                        # Sequence of opponent's (inactive) discs starting/
                        # ending with player's (active) own discs
                        return True
                    break

                if self.board.state[row, col] == self.inactive.disc_color:
                    # Next disc in traversed sequence is found to be opponents
                    found_opposing_disc = True

                # Else traverse one more step
                row += d_row
                col += d_col

        # No directions yield valid sequence, hence invalid
        return False

    def get_valid_moves(self):
        """
        Get all valid moves for the current active player in the game.

        Returns:
            list: A list of tuples representing the valid moves (row, col).
        """

        return [
            (row, col)
            for row in range(8)
            for col in range(8)
            if self.is_valid_move(row, col)
        ]

    def is_game_finished(self):
        pass

    