
import unittest
from game import Game
from board import Board
from player import Player

class TestGame(unittest.TestCase):
    """
    Test functionality for the Game base class.
    """

    def test_player_colors(self):
        game = Game("Sam", "Alistair")

        # Check first player is black and the second is white
        self.assertEqual(game.player_black.disc_color, 'X')
        self.assertEqual(game.player_white.disc_color, 'O')


    def test_change_turn(self):
        game = Game("Sam", "Alistair")
        game.change_turn()

        # After changing turns, active player should be white
        self.assertEqual(game.active, game.player_white)
        self.assertEqual(game.inactive, game.player_black)


if __name__ == '__main__':
    unittest.main(verbosity=2)