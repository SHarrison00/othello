# untitled.py

from game import Game
from board import Board
from player import PlayerType

game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)

game.board.display()

# game.reset_valid_moves()
# print(game.is_valid_move(2, 3))

game.get_player_move()