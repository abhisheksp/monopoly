import game_phases.game_phase
from game_state.action import Action


class BSMT(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def _next_action(self, decision, decision_type, game_state):
        if decision is None or decision_type == Action.MORTGAGE_PROPERTY:
            return decision
        property_number, count = decision
        property_ = game_state.board.property_at(property_number)
        return property_, 'House', count

    def apply(self, game_context, action=None):
        game_context = self._bsmt_cycle(game_context)
        game_state = game_context.state
        if not game_state.current_player.double_roll():
            game_state.next_player()
        game_context.phase = game_context.get_phase('DiceRoll')
        return game_context, None

    def _bsmt_cycle(self, game_context):
        game_state = game_context.state
        end_bsmt = False
        while not end_bsmt:
            decisions = []
            for player in game_state.get_players():
                game_context, decision = self._player_bsmt(game_context, player)
                decisions.append(decision)
            end_bsmt = not any(decisions)
        return game_context

    def _player_bsmt(self, game_context, player):
        game_state = game_context.state
        decision_type, decision = player.agent.bsmt_decision(game_state)
        next_action = self._next_action(decision, decision_type, game_state)
        if decision_type == Action.BUY_HOUSE:
            buy_house_phase = game_context.get_phase('BuyHouse')
            game_context = buy_house_phase.apply(game_context, next_action)
        elif decision_type == Action.SELL_HOUSE:
            sell_house_phase = game_context.get_phase('SellHouse')
            game_context = sell_house_phase.apply(game_context, next_action)
        elif decision_type == Action.MORTGAGE_PROPERTY:
            mortgage_property_phase = game_context.get_phase('MortgageProperty')
            game_context = mortgage_property_phase.apply(game_context, next_action)
        return game_context, decision

    def __repr__(self):
        return 'BSMT Phase'
