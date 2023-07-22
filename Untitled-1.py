# untitled.py

from game import Game
from board import Board
from player import PlayerType

game = Game(PlayerType.OFFLINE, PlayerType.OFFLINE)

# Get move, make move, change turns, get valid moves
game.board.display()
game.get_player_move()
game.make_move()
game.change_turn()
game.update_valid_moves()

# Get move, make move, change turns, get valid moves
game.board.display()
game.get_player_move()
game.make_move()
game.change_turn()
game.update_valid_moves()
