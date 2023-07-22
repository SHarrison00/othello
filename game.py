
from board import Board
from board import SquareType
from player import Player, PlayerType

class Game:
    """
    Main orchestrator, managing overall game flow.    
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

        # Initialize next move to None
        self.next_move = None


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
        Retrieve the player's move by identifying the type of player.
        """

        if self.active.player_type == PlayerType.OFFLINE:
            row, col = self.active.get_offline_user_move(self)

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

        # Place the disc for the next move
        row, col = self.next_move[0], self.next_move[1]
        self.board.state[row, col] = self.active.disc_color
        
        # Flip the opponent's discs
        self.flip() 


    def is_game_finished(self):
        pass
