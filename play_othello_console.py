
import time
from src.game import Game
from src.player import Player, PlayerType
from src.board import SquareType

# Ask offline user to choose their color
print("Do you want to play as black or white?")
color = input("Enter: ").lower()
while color not in ['black', 'white']:
    print("Do you want to play as black or white?")
    color = input("Enter: ").lower()

if color == 'black':
    player_black = Player(PlayerType.OFFLINE, SquareType.BLACK)
    player_white = Player(PlayerType.RANDOM, SquareType.WHITE)
else:
    player_black = Player(PlayerType.RANDOM, SquareType.BLACK)
    player_white = Player(PlayerType.OFFLINE, SquareType.WHITE)

# Initialise game
game = Game(player_black, player_white)

while not game.is_finished:
    print("\n\n")
    game.board.display()
    time.sleep(1.5)

    if game.active == game.player_black:
        if game.prev_move != None:
            print("White has moved.")
            time.sleep(1)
        print("Black to move.")
    else:
        if game.prev_move != None:
            print("Black has moved.")
            time.sleep(1)
        print("White to move.")

    time.sleep(1)
    game.get_player_move()
    game.make_move()
    game.change_turn()
    game.update_valid_moves()
    game.update_scores()

    game.check_finished()
    time.sleep(1.5)

# Display final game board
game.board.display()
print("Game over.")