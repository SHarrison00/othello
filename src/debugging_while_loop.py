from game import Game
from board import SquareType
from player import Player, PlayerType
from state_evaluation import StateEvaluator, HeuristicType

# Agents dictionary
agents = {}
depth = 1

# Agent 1: Disc difference
custom_weights = {HeuristicType.DISC_DIFF: 1.0}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_1'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 2: Mobility
custom_weights = {HeuristicType.MOBILITY: 1.0}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_2'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 3: Corners
custom_weights = {HeuristicType.CORNERS: 1.0}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_3'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 4: Disc difference & Corners
custom_weights = {HeuristicType.DISC_DIFF: 0.5, HeuristicType.CORNERS: 0.5}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_4'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 5: Disc difference & Mobility
custom_weights = {HeuristicType.DISC_DIFF: 0.5, HeuristicType.MOBILITY: 0.5}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_5'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 6: Mobility & Corners
custom_weights = {HeuristicType.MOBILITY: 0.5, HeuristicType.CORNERS: 0.5}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_6'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

# Agent 7: All Heuristics
custom_weights = {
    HeuristicType.DISC_DIFF: 1/3,
    HeuristicType.MOBILITY: 1/3,
    HeuristicType.CORNERS: 1/3
}
state_eval = StateEvaluator(weights=custom_weights)
agents['agent_7'] = {
    'black': Player(PlayerType.MINIMAX, SquareType.BLACK, state_eval, depth),
    'white': Player(PlayerType.MINIMAX, SquareType.WHITE, state_eval, depth)
}

def simulate_match(agent_black_name, agent_white_name):
    # Get agent using dictionary
    agent_black = agents.get(agent_black_name)
    agent_white = agents.get(agent_white_name)
    
    # Instantiate game instance
    player_black = agent_black["black"]
    player_white = agent_white["white"]
    game = Game(player_black, player_white)

    game.board.display()

    move_num = 0
    
    while not game.is_finished:

        if move_num <= 57:
            game.get_player_move() 
            game.make_move()
            game.change_turn()
            game.update_valid_moves()
            game.update_scores()
            game.check_finished()
            game.board.display()
        else:
            game.get_player_move() # This should make .next_move 'None', but it does not...
            game.make_move()
            game.change_turn()
            game.update_valid_moves()
            game.update_scores()
            game.check_finished()
            game.board.display() 
        
        move_num += 1

    game.determine_winner()

    return {
        'game_result': game.game_result,
        'black_score': game.black_score,
        'white_score': game.white_score,
        'agent_black': agent_black_name,
        'agent_white': agent_white_name
    }

simulate_match("agent_2", "agent_6")