# The purpose of the views.py file is to store the main views or URL endpoints 
# for the front-end aspect of the website. It contains the code responsible for 
# handling requests and rendering the appropriate responses to the users.

from flask import (
    Blueprint, render_template, request, 
    jsonify, session, redirect, url_for
)

import pickle
import logging 
import random
logging.basicConfig(level=logging.DEBUG)

from game import Game
from board import SquareType
from player import Player, PlayerType

views = Blueprint("views", __name__)


@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/about")
def about():
    return render_template('about.html')


@views.route('/play_game', methods=['GET', 'POST'])
def play_game():
    if request.method == 'POST':
        # Handling POST request: Retrieve the user-selected color, initialize 
        # the game accordingly store the game state in the session, and 
        # redirect to the same endpoint to handle the GET request.
        color = request.form.get('color')
        session['user_color'] = color
        
        # Create Player instances based on the selected color
        if color == 'BLACK':
            user_player = Player(PlayerType.USER, SquareType.BLACK)
            ai_player = Player(PlayerType.RANDOM, SquareType.WHITE)
        else:
            user_player = Player(PlayerType.USER, SquareType.WHITE)
            ai_player = Player(PlayerType.RANDOM, SquareType.BLACK)
        
        # Initialize the game with the created player instances
        game = Game(user_player, ai_player)
        
        serialized_game = pickle.dumps(game)
        session['game_instance'] = serialized_game
        session['game_started'] = True
        
        return redirect(url_for('views.play_game'))
    
    else:
        # Handle GET request: Retrieve color and game instance from session, 
        # deserialize if exists, and render. Else, create default game instance
        color = session.get('user_color')
        serialized_game = session.get('game_instance')
        
        if serialized_game:
            game = pickle.loads(serialized_game)
        else:
            # Default game instance
            game = Game(PlayerType.USER, PlayerType.RANDOM)
            serialized_game = pickle.dumps(game)
            session['game_instance'] = serialized_game
        
        return render_template('play_game.html', game=game, user_color=color, 
                               game_started=session.get('game_started', False))


@views.route('/user_move', methods=['POST'])
def user_move():
    data = request.get_json()
    row = data['row']
    col = data['col']
    
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        # Deserialize the game instance
        logging.debug(f"Received move: row={row}, col={col}")
        game = pickle.loads(serialized_game)

        # User's move, and game-flow mechanics
        game.next_move = (row, col) # Bespoke for front-end
        game.make_move()
        game.change_turn()
        game.update_valid_moves()
        game.check_finished()

        # Update serialized game instance in the session
        session['game_instance'] = pickle.dumps(game)

        # If game has ended, include in response to frontend
        if game.is_finished:
            response = {'message': 'Game over', 'game_over': True}
        else:
            response = {'message': 'User move received', 'game_over': False}

        return jsonify(response)
    else:
        return jsonify({'message': 'Game instance not found'})
    

@views.route('/agent_move', methods=['POST'])
def agent_move():
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        # Deserialize the game instance
        game = pickle.loads(serialized_game)

        # Agent's move, and game-flow mechanics
        game.get_player_move()
        game.make_move()
        game.change_turn()
        game.update_valid_moves()
        game.check_finished()

        # Update serialized game instance in the session
        session['game_instance'] = pickle.dumps(game)

        # If game has ended, include in response to frontend
        if game.is_finished:
            response = {'message': 'Game over', 'game_over': True}
        else:
            response = {'message': 'Agent move received', 'game_over': False}

        return jsonify(response)
    else:
        return jsonify({'message': 'Game instance not found'})
    

@views.route('/get_game_state', methods=['GET'])
def get_game_state():
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        # Deserialize the game instance
        game = pickle.loads(serialized_game)

        # Convert the game state to a list of lists with string representations
        # to make it serializable for JSON response.
        game_state = [[cell.name for cell in row] for row in game.board.state]

        # Create a dictionary with the game state
        response = {'game_state': game_state}
        return jsonify(response)
    else:
        return jsonify({'message': 'Game instance not found'})
    

@views.route('/get_random_quote')
def get_random_quote():
    with open('quotes.txt', 'r') as file:
        quotes = file.readlines()
    random_quote = random.choice(quotes).strip()
    return jsonify({"quote": random_quote})