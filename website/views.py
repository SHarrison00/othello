# The purpose of the views.py file is to store the main views or URL endpoints 
# for the front-end aspect of the website. It contains the code responsible for 
# handling requests and rendering the appropriate responses to the users.

from flask import Blueprint, render_template
from game import Game

views = Blueprint("views", __name__)


@views.route("/home")
def home():
    return render_template("home.html")


@views.route('/play_game')
def play_game():

    # Instantiate a game instance
    game_instance = Game("Sam", "Alistair")

    return render_template('play_game.html', game = game_instance)


@views.route("/about")
def about():
    return render_template('about.html')
 