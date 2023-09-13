# The purpose of the views.py file is to store the main views or URL endpoints 
# for the front-end aspect of the website. It contains the code responsible for 
# handling requests and rendering the appropriate responses to the users.

from flask import Blueprint, render_template, request, jsonify, session
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


@views.route('/play_game')
def play_game():
    serialized_game = session.get('game_instance')

    if serialized_game:
        # Deserialize the game instance
        game = pickle.loads(serialized_game)
    else:
        # Create a new game instance
        game = Game(PlayerType.USER, PlayerType.RANDOM)
        serialized_game = pickle.dumps(game)
        session['game_instance'] = serialized_game

    return render_template('play_game.html', game=game)


@views.route('/make_move', methods=['POST'])
def make_move():
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
        response_data = {'message': 'Move received'}
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
