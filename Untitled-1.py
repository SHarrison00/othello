# untitled.py

import time

from game import Game
from board import Board
from player import PlayerType

game = Game(PlayerType.RANDOM, PlayerType.RANDOM)

# print(game.is_finished())

while not game.is_finished:
    
    game.board.display()
    game.get_player_move()
    
    game.make_move()

    game.change_turn()
    game.update_valid_moves()
    game.update_scores()
    print(game.black_score)
    print(game.white_score)
    game.check_finished()

    time.sleep(0.1)

game.board.display()
print("game end.")