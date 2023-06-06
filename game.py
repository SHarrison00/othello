
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

    def is_game_finished(self):
        pass






