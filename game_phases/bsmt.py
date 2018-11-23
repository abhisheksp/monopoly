import game_phases.game_phase
from game_state.action import Action


class BSMT(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def _next_action(self, decision, game_state):
        if decision is None:
            return None
        property_number, count = decision
        property_ = game_state.board.property_at(property_number)
        return property_, 'House', count

    def apply(self, game_context, action=None):
        game_state = game_context.state
        players = list(game_state.players)
        players.insert(0, players.pop(players.index(game_state.current_player)))  # Give preference to current player
        decision_type, decision = game_state.current_player.agent.bsmt_decision(game_state)
        next_action = self._next_action(decision, game_state)
        if decision_type == Action.BUY_HOUSE:
            game_context.phase = game_context.get_phase('BuyHouse')
            return game_context, next_action
        elif decision_type == Action.SELL_HOUSE:
            game_context.phase = game_context.get_phase('SellHouse')
            return game_context, next_action
        if not game_state.current_player.double_roll():
            game_state.next_player()
        game_context.phase = game_context.get_phase('DiceRoll')
        return game_context, None

    def __repr__(self):
        return 'BSMT Phase'
