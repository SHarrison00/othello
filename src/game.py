
import numpy as np
import copy
from .board import Board, SquareType
from .player import Player, PlayerType

class Game:
    """
    Handles the overall game flow, creating a Board() instance and two Player() 
    instances for black and white, respectively.   
    """

    def __init__(self, player_black, player_white):
        self.board = Board()
        self.is_finished = False

        self.player_black = player_black
        self.player_white = player_white

        # Black always starts
        self.active = self.player_black
        self.inactive = self.player_white

        self.next_move = None
        self.prev_move = None

        # Scoring and winner
        self.black_score = 2
        self.white_score = 2
        self.game_result = None


    def change_turn(self):
        self.active, self.inactive = self.inactive, self.active


    def update_scores(self):
        self.black_score = np.count_nonzero(self.board.state == SquareType.BLACK)
        self.white_score = np.count_nonzero(self.board.state == SquareType.WHITE)    


    def is_valid_move(self, row, col):
        """
        Check the validity of a move. This involves traversing in different 
        directions on the board and checking the traversed sequence of discs.

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        # First, reset any moves on the board still displayed as valid
        self.reset_valid_moves()

        if self.board.state[row, col] != SquareType.EMPTY:
            return False

        # Traversable directions; up, down, left, right and all diagonals
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in DIRECTIONS:
            d_row, d_col = direction
            r, c = row + d_row, col + d_col

            found_opposing_disc = False
            
            # While within board boundaries
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board.state[r, c] == SquareType.EMPTY:
                    break

                if self.board.state[r, c] == self.active.disc_color:
                    if found_opposing_disc:
                        # Found sequence of opponent's (inactive player) discs
                        # starting & ending with active player's own discs
                        return True
                    break

                if self.board.state[r, c] == self.inactive.disc_color:
                    found_opposing_disc = True

                # Traverse another step in same direction
                r += d_row
                c += d_col

        # No directions yield valid sequence, hence must be invalid
        return False


    def get_valid_moves(self):
        """
        Get all valid moves for the current active player in the game.

        Returns:
            list: A list of tuples of valid moves (row, col).
        """

        return [
            (row, col)
            for row in range(8)
            for col in range(8)
            if self.is_valid_move(row, col)
        ]
    

    def get_valid_moves_by_color(self, color):
        """
        Get all valid moves for a specified color.
        
        Returns:
            list: A list of tuples of valid moves (row, col).
        """

        # Store original active and inactive players
        original_active = self.active
        original_inactive = self.inactive

        # Now, set active player based on input
        if color == SquareType.BLACK:
            self.active = self.player_black
            self.inactive = self.player_white
        elif color == SquareType.WHITE:
            self.active = self.player_white
            self.inactive = self.player_black
        else:
            raise ValueError("Invalid color specified.")

        valid_moves = [
            (row, col)
            for row in range(8)
            for col in range(8)
            if self.is_valid_move(row, col)
        ]

        # Restore original active and inactive players
        self.active = original_active
        self.inactive = original_inactive

        return valid_moves


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
        
        for move in valid_moves:

            # Update board state
            row, col = move
            self.board.state[row, col] = SquareType.VALID


    def is_valid_moves(self):

        return any(
            cell == SquareType.VALID 
            for row in self.board.state 
            for cell in row
        )    
    

    def get_player_move(self):
        """
        Get active player's move by identifying their player type.
        """

        # First, update move history
        self.prev_move = self.next_move

        if self.active.player_type == PlayerType.OFFLINE:
            row, col = self.active.get_offline_move(self)

        elif self.active.player_type == PlayerType.RANDOM:
            move = self.active.get_random_move(self)
            if move is None:
                self.next_move = None
                return
            row, col = move

        elif self.active.player_type == PlayerType.MINIMAX:            
            move = self.active.get_minimax_move(self)
            if move is None:
                self.next_move = None
                return
            row, col = move

        # Set the next move
        self.next_move = (row, col)


    def discs_to_flip(self, row, col):
        """
        Determine disc(s) that need to be flipped for a move.
        """

        discs_to_flip = []

        # Traversable DIRECTIONS; up, down, left, right and all diagonals
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in DIRECTIONS:
            d_row, d_col = direction
            r, c = row + d_row, col + d_col

            # Sequence of other player discs
            seq_discs = []

            # Flag to indicate if there exists discs to flip
            flip_flag = False

            while 0 <= r < 8 and 0 <= c < 8:
                if self.board.state[r, c] == self.inactive.disc_color:
                    # Add the opponent's disc to the sequence
                    seq_discs.append((r, c))
                    flip_flag = True

                elif self.board.state[r, c] == self.active.disc_color:
                    if flip_flag:
                        # If we encounter our own disc after already 
                        # encountering opponent's discs, extend discs_to_flip
                        discs_to_flip.extend(seq_discs)
                    break
                else:
                    break

                # Traverse another step in same direction
                r += d_row
                c += d_col

        return discs_to_flip
    

    def flip(self):
        """
        Flip discs for the next move, thereby updating the board state.
        """

        row, col = self.next_move[0], self.next_move[1]
        discs = self.discs_to_flip(row, col)

        for disc in discs:

            # Update the board state
            self.board.state[disc[0], disc[1]] = self.active.disc_color


    def make_move(self):
        """
        Make the next move, flipping opponent's discs. 
        """

        if self.next_move is None:
            return

        # Place disc
        row, col = self.next_move[0], self.next_move[1]
        self.board.state[row, col] = self.active.disc_color
        
        # Flip other discs
        self.flip()
        

    def is_board_full(self):

        for row in range(8):
            for col in range(8):
                cell_state = self.board.state[row, col]
                if cell_state in [SquareType.EMPTY, SquareType.VALID]:
                    return False
        
        return True
    

    def check_finished(self):
        """
        Checks if the game has finished and determines the winner.
        """

        # Neither player can move
        if self.next_move is None and self.prev_move is None:
            self.is_finished = True
            self.determine_winner()

        # The game board board is full 
        elif self.is_board_full():
            self.is_finished = True
            self.determine_winner()

        # One player has no discs
        elif self.black_score == 0 or self.white_score == 0:
            self.is_finished = True
            self.determine_winner()

    
    def determine_winner(self):
        """
        Determines the winner by comparing the scores of both players. 
        """

        if self.black_score > self.white_score:
            self.game_result = "Black Wins"
        elif self.white_score > self.black_score:
            self.game_result = "White Wins"
        else:
            self.game_result = "Draw"


    def simulate_move(self, move):
        """
        Simulate a move by creating a copy of the current game state.

        Returns:
            Game: A new game instance with the move applied.
        """

        # Create a deep copy of the game
        new_game = copy.deepcopy(self)

        # Apply the input move 
        new_game.next_move = move
        new_game.make_move()

        new_game.change_turn()
        new_game.update_valid_moves()
        new_game.update_scores()

        # Check if the game has ended
        new_game.check_finished()

        return new_game