
import time
from game import Game
from player import PlayerType

# Ask the user to choose their color
print("Do you want to play as black or white?")
color = input("Enter: ").lower()
while color not in ['black', 'white']:
    print("Do you want to play as black or white?")
    color = input("Enter: ").lower()

# Initialize game instance
if color == 'black':
    game = Game(PlayerType.OFFLINE, PlayerType.RANDOM)
else:
    game = Game(PlayerType.RANDOM, PlayerType.OFFLINE)

while not game.is_finished:
    # Display the board
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

    # Get the player's move and make it
    time.sleep(1)
    game.get_player_move()
    game.make_move()

    # Change turns and update game info
    game.change_turn()
    game.update_valid_moves()
    game.update_scores()

    # Before carrying on, check game has not ended
    game.check_finished()
    time.sleep(1.5)

# Display final game board
game.board.display()
# Message to acknowledge end of game 
print("Game over.")

# Morning tasks,

    # 1. Add print statements "Black to move.", "White to move."
    # 2. Can we make the offline player choose their colour?
        # Do this feature enhance anything, or?


# python play_othello_console.py (find a better name)
# Enter a move: D3 (improve clarity of print message)
# <Update board>
# White to move etc.

# Turn program into GIF
    # Demonstrates console development