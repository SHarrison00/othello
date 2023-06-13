
# debugging

from game import Game
from board import Board
from player import Player

game = Game("Sam", "Alistair")
valid_moves = game.is_valid_move(row = 2, col = 3)

print(game.board.state[3,3])