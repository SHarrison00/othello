# The purpose of the views.py file is to store the main views or URL endpoints 
# for the front-end aspect of the website. It contains the code responsible for 
# handling requests and rendering the appropriate responses to the users.

from flask import (
    Blueprint, render_template, request, 
    jsonify, session, redirect, url_for
)

import pickle
import logging 
logging.basicConfig(level=logging.DEBUG)

from game import Game
from player import PlayerType

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
        
        if color == 'BLACK':
            game = Game(PlayerType.USER, PlayerType.RANDOM)
        else:
            game = Game(PlayerType.RANDOM, PlayerType.USER)
        
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

        # Return a JSON response indicating success or any relevant data
        response_data = {'message': 'User move received'}
        return jsonify(response_data)
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

        # Return a JSON response with the agent's move
        response_data = {'message': 'Agent move received'}
        return jsonify(response_data)
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
        response_data = {'game_state': game_state}
        return jsonify(response_data)
    else:
        return jsonify({'message': 'Game instance not found'})
