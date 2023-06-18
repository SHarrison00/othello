
from board import Board
from board import SquareType
from player import Player

class Game:
    """
    Main orchestrator, managing overall game flow.    
    """

    def __init__(self, player_black, player_white):
        self.board = Board()
        self.is_finished = False

        # Player instances are inputs 
        self.player_black = Player(player_black, SquareType.BLACK)
        self.player_white = Player(player_white, SquareType.WHITE)

        # Black always starts
        self.active = self.player_black
        self.inactive = self.player_white


    def change_turn(self):
        self.active, self.inactive = self.inactive, self.active


    def is_valid_move(self, row, col):
        """
        Checks the validity of a move. Involves traversing in different 
        directions on the board, and checking the traversed sequence of discs.

        Args:
            row (int): The row coordinate of the move.
            col (int): The column coordinate of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        # Move is invalid if the cell is not empty 
        if self.board.state[row, col] != SquareType.EMPTY:
            return False

        # Traversable directions; up, down, left, right and all diagonals
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Traverse board in specified direction
        for direction in DIRECTIONS:
            d_row, d_col = direction
            r, c = row + d_row, col + d_col
            found_opposing_disc = False
            
            # While within boundaries
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board.state[r, c] == SquareType.EMPTY:
                    break

                if self.board.state[r, c] == self.active.disc_color:
                    if found_opposing_disc:
                        # Sequence of opponent's (inactive) discs starting/
                        # ending with player's (active) own discs
                        return True
                    break

                if self.board.state[r, c] == self.inactive.disc_color:
                    # Next disc in traversed sequence is found to be opponents
                    found_opposing_disc = True

                # Else traverse one more step
                r += d_row
                c += d_col

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
    

    def reset_valid_moves(self):
        """
        Reset all valid moves on the board to empty. 
        """

        for row in self.board.state:
            for cell in row: 
                if cell.name == "VALID":
                    cell = SquareType.EMPTY

                    # maybe its not replacing properply...

                    # this function fails

                    # this functions will help fix other failing function 


    def update_valid_moves(self, valid_moves):
        """
        Updates the valid moves on the game board. 
        """

        if len(valid_moves) == 0:
            pass
        
        else: 
            for move in valid_moves:
                self.board.state[move[0], move[1]] = SquareType.VALID
            
        



    def is_game_finished(self):
        pass
