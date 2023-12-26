# The purpose of the views.py file is to store the main views or URL endpoints 
# for the front-end. It contains the code responsible for handling requests and
# rendering responses to the users.

from flask import (
    Blueprint, render_template, request, 
    jsonify, session, redirect, url_for
)

import os 

import pickle
import logging 
import random
import numpy as np
logging.basicConfig(level=logging.DEBUG)

from src.game import Game
from src.board import SquareType
from src.player import Player, PlayerType
from src.state_evaluation import StateEvaluator, HeuristicType
 
views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route('/play_game', methods=['GET', 'POST'])
def play_game():
    if request.method == 'POST':
        color = request.form.get('color')
        session['user_color'] = color

        # OthelloAI evaluation function weights
        state_eval = StateEvaluator(weights={
            HeuristicType.DISC_DIFF: 25/60,
            HeuristicType.MOBILITY: 5/60,
            HeuristicType.CORNERS: 30/60
        })
    
        if color == 'BLACK':
            user_player = Player(PlayerType.USER, SquareType.BLACK)
            ai_player = Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, 3)
            game = Game(user_player, ai_player)
        else:
            user_player = Player(PlayerType.USER, SquareType.WHITE)
            ai_player = Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, 3)
            game = Game(ai_player, user_player)
        
        serialized_game = pickle.dumps(game)
        session['game_instance'] = serialized_game
        session['game_started'] = True
        
        return redirect(url_for('views.play_game'))
    
    else:
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
    # Move data from the JSON request
    data = request.get_json()
    row = data['row']
    col = data['col']
    
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        logging.debug(f"Received move: row={row}, col={col}")
        game = pickle.loads(serialized_game)

        game.next_move = (row, col)
        game.make_move()
        game.change_turn()
        game.update_valid_moves()
        game.update_scores()
        game.check_finished()

        # Update serialized game instance
        session['game_instance'] = pickle.dumps(game)

        response = {
            'message': 'User move received',
            'game_over': game.is_finished
        }

        return jsonify(response)
    else:
        return jsonify({'message': 'Game instance not found'})
        

@views.route('/agent_move', methods=['POST'])
def agent_move():
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        game = pickle.loads(serialized_game)

        if game.active.player_type == PlayerType.USER:
            game.change_turn()

        # Check AI has valid moves
        game.update_valid_moves()
        valid_moves = game.is_valid_moves()

        if valid_moves:
            game.get_player_move()
            game.make_move()
            agent_moved = True
        else:
            agent_moved = False

        game.change_turn()
        game.update_valid_moves()
        game.update_scores()
        game.check_finished()

        # Check User has valid moves
        user_has_moves = game.is_valid_moves()

        session['game_instance'] = pickle.dumps(game)

        response = {
            'message': 'Agent move received' if agent_moved else 'No valid move for agent',
            'game_over': game.is_finished,
            'agent_moved': agent_moved,
            'user_has_moves': user_has_moves
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'Game instance not found'})
    

@views.route('/get_game_state', methods=['GET'])
def get_game_state():
    serialized_game = session.get('game_instance')
    
    if serialized_game:
        game = pickle.loads(serialized_game)

        # Convert game state to a list of lists JSON serialisation
        game_state = [[cell.name for cell in row] for row in game.board.state]

        response = {'game_state': game_state}
        
        return jsonify(response)
    
    else:
        return jsonify({'message': 'Game instance not found'})
    

@views.route('/get_random_quote')
def get_random_quote():

    print(os.path.dirname(__file__))

    with open('data/quotes.txt', 'r') as file:
        quotes = file.readlines()
    random_quote = random.choice(quotes).strip()

    return jsonify({"quote": random_quote})


@views.route('/get_game_outcome')
def get_game_outcome():
    serialized_game = session.get('game_instance')

    if serialized_game:
        game = pickle.loads(serialized_game)
        game.determine_winner()

        outcome_message = f"Game over. {game.game_result}. Score: Black {game.black_score} - White {game.white_score}"
        return jsonify({"outcome_message": outcome_message})
    
    else:
        return jsonify({"outcome_message": "Game instance not found"})