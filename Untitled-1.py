# untitled.py

from game import Game
from board import Board
from player import PlayerType

game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)

game.board.display()

# game.get_player_move()
game.discs_to_be_flipped(0 , 0)
game.discs_to_be_flipped(2 , 3)
game.discs_to_be_flipped(4 , 5)
game.discs_to_be_flipped(7 , 7)
