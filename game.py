
import numpy as np

from board import Board
from board import SquareType
from player import Player, PlayerType

class Game:
    """
    Handles the overall game flow, creating a Board() instance and two Player() 
    instances for black and white, respectively.   
    """

    def __init__(self, player_type_black, player_type_white):
        self.board = Board()
        self.is_finished = False

        # Player instances are inputs 
        self.player_black = Player(player_type_black, SquareType.BLACK)
        self.player_white = Player(player_type_white, SquareType.WHITE)

        # Black always starts
        self.active = self.player_black
        self.inactive = self.player_white

        # Move history
        self.next_move = None
        self.prev_move = None

        # Scores, and winner
        self.black_score = 2
        self.white_score = 2
        self.winner = None


    def change_turn(self):
        self.active, self.inactive = self.inactive, self.active


    def update_scores(self):
        self.black_score = np.count_nonzero(self.board.state == SquareType.BLACK)
        self.white_score = np.count_nonzero(self.board.state == SquareType.WHITE)    


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

        # Before doing anything, reset any moves on the board that are still
        # displayed as valid
        self.reset_valid_moves()

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

        for row in range(8):
            for col in range(8):
                if self.board.state[row, col] == SquareType.VALID:
                    self.board.state[row, col] = SquareType.EMPTY


    def update_valid_moves(self):
        """
        Updates the valid moves on the game board. 
        """

        # Reset previous valid moves
        self.reset_valid_moves()

        # Get all valid moves for the current active player
        valid_moves = self.get_valid_moves()

        if not valid_moves:
            return
        
        # Update
        for move in valid_moves:
            row, col = move
            self.board.state[row, col] = SquareType.VALID

    
    def get_player_move(self):
        """
        Retrieve player's move by identifying player type.
        """

        if self.active.player_type == PlayerType.OFFLINE:
            row, col = self.active.get_offline_move(self)

        elif self.active.player_type == PlayerType.RANDOM:
            move = self.active.get_random_move(self)
            if move is None:
                return
            row, col = move

        self.next_move = (row, col)


    def discs_to_flip(self, row, col):
        """
        For a given move, determine the discs that need to be flipped.
        """

        # Initialize store discs to flip
        discs_to_flip = []

        # Traversable DIRECTIONS; up, down, left, right and all diagonals
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Traverse board in specified direction
        for direction in DIRECTIONS:
            d_row, d_col = direction
            r, c = row + d_row, col + d_col

            # Sequence of other player discs
            seq_discs = []

            # Flag to indicate if there exists discs to flip
            flip_flag = False

            # Continue traversing in the current direction
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board.state[r, c] == self.inactive.disc_color:
                    seq_discs.append((r, c))
                    flip_flag = True

                elif self.board.state[r, c] == self.active.disc_color:
                    if flip_flag:
                        discs_to_flip.extend(seq_discs)
                    break
                else:
                    break

                # Traverse another step
                r += d_row
                c += d_col

        return discs_to_flip
    

    def flip(self):
        """
        For the next move flip the discs, updating the board.
        """

        # For next move, identify discs to flip
        row, col = self.next_move[0], self.next_move[1]
        discs = self.discs_to_flip(row, col)

        # Update the board state
        for disc in discs:
            self.board.state[disc[0], disc[1]] = self.active.disc_color


    def make_move(self):
        """
        Make the next move, flipping opponent's discs. 
        """

        if self.next_move is None:
            return

        # Place chosen disc
        row, col = self.next_move[0], self.next_move[1]
        self.board.state[row, col] = self.active.disc_color
        
        # Flip other discs
        self.flip() 

        # Update history
        self.prev_move = self.next_move


    def is_board_full(self):
        
        for row in range(8):
            for col in range(8):
                cell_state = self.board.state[row, col]
                if cell_state in [SquareType.EMPTY, SquareType.VALID]:
                    return False
        return True
    

    def check_finished(self):

        # Game ends if neither player can move
        if self.next_move is None and self.prev_move is None:
            self.is_finished = True

        # Game ends if board is full 
        if self.is_board_full():
            self.is_finished = True