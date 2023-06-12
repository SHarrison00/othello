
import numpy as np

class Board:
    """ Class representation of the game board."""

    def __init__(self):
        self.player_disc = 'X' # 'X' is black
        self.opposing_disc = 'O' # 'O' is black
        self.board = np.full((8, 8), ' ')
        self.board[3, 3] = 'O'
        self.board[3, 4] = 'X'
        self.board[4, 3] = 'X'
        self.board[4, 4] = 'O'

    def display(self):
        print(self.board)

    def switch_players(self):
        """
        Switches players' roles. This method changes the current perspective on 
        player roles, where the current player becomes the opposing player, and 
        the opposing player becomes the current player.
        """
        self.player_disc, self.opposing_disc = (
            self.opposing_disc,
            self.player_disc
        )
        
    def is_terminal(self):
        "Has the game ended?"

        pass 

    def is_valid_move(self, row, col):
        """
        Checks the validity of a move. This involves traversing in different 
        directions on the board, and checking the traversed sequence of discs.

        Args:
            row (int): The row coordinate of the move.
            col (int): The column coordinate of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Move is invalid if the cell is not empty 
        if self.board[row, col] != ' ':
            return False

        # Possible directions; up, down, left, right and all diagonals
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            d_row, d_col = direction
            current_row, current_col = row + d_row, col + d_col
            found_opposing_disc = False

            # Traverse board in specified direction while within boundaries
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                if self.board[current_row, current_col] == ' ':
                    break

                # If cell is player's disc and an opponent's disc has been 
                # found, then the move "out-flanks" the opponent hence is valid
                if self.board[current_row, current_col] == self.player_disc:
                    if found_opposing_disc:
                        return True
                    break

                # If cell is opponent's disc update "found opponent" disc flag 
                if self.board[current_row, current_col] == self.opposing_disc:
                    found_opposing_disc = True

                # Else traverse one more step in same direction
                current_row += d_row
                current_col += d_col

        return False

    def get_valid_moves(self):
        """
        Finds all valid moves on the board utilising the method is_valid_move() 
        and using list comprehension.

        Returns:
            List[tuple[int, int]]: A list of tuples containing all valid moves.
        """

        # Iteratively find all valid moves on the board
        valid_moves = [(row, col) for row in range(8) 
                       for col in range(8) 
                       if self.is_valid_move(row, col)]
        
        return valid_moves