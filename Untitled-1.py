# untitled.py

from game import Game
from board import Board
from player import PlayerType

game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)

game.board.display()

game.get_player_move()