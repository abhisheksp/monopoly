import game_phases.game_phase
from game_state.action import Action


class BSMT(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        players = list(game_state.players)
        players.insert(0, players.pop(players.index(game_state.current_player)))  # Give preference to current player
        decision_type, decision = game_state.current_player.agent.bsmt_decision(game_state)
        if decision_type == Action.BUY_HOUSE:
            game_context.phase = game_context.get_phase('BuyHouse')
            return game_context, decision
        if not game_state.current_player.double_roll():
            game_state.next_player()
        game_context.phase = game_context.get_phase('DiceRoll')
        return game_context, None

    def __repr__(self):
        return 'BSMT Phase'
