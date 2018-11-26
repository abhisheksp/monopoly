import game_phases.game_phase
from game_state.action import Action


class BSMT(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_context = self._bsmt_cycle(game_context)
        game_context.phase = game_context.get_phase('TurnEnd')
        return game_context, None

    def _next_action(self, player, decision, decision_type, game_state):
        if decision is None or decision_type == Action.MORTGAGE_PROPERTY:
            return decision
        if decision_type == Action.TRADE_PROPERTY:
            trades = []
            selling_price, selling_properties, requesting_price, requesting_properties = decision
            other_player = game_state.other_player(player)
            if len(selling_properties) > 0:
                trade = {
                    'buyer': other_player,
                    'seller': player,
                    'price': selling_price,
                    'properties': selling_properties
                }
                trades.append(trade)
            if len(requesting_properties) > 0:
                trade = {
                    'buyer': player,
                    'seller': other_player,
                    'price': requesting_price,
                    'properties': requesting_properties
                }
                trades.append(trade)
            return trades
        property_number, count = decision
        property_ = game_state.board.property_at(property_number)
        return property_, 'House', count

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
        next_action = self._next_action(player, decision, decision_type, game_state)
        if decision_type == Action.BUY_HOUSE:
            buy_house_phase = game_context.get_phase('BuyHouse')
            game_context, _ = buy_house_phase.apply(game_context, next_action)
        elif decision_type == Action.SELL_HOUSE:
            sell_house_phase = game_context.get_phase('SellHouse')
            game_context, _ = sell_house_phase.apply(game_context, next_action)
        elif decision_type == Action.MORTGAGE_PROPERTY:
            mortgage_property_phase = game_context.get_phase('MortgageProperty')
            game_context, _ = mortgage_property_phase.apply(game_context, next_action)
        elif decision_type == Action.TRADE_PROPERTY:
            player_1, player_2 = game_state.get_players()
            other_player = player_2 if player is player_1 else player_1
            other_player_decision, _ = other_player.agent.respond_trade(game_context)
            if other_player_decision:
                trade_property_phase = game_context.get_phase('TradeProperty')
                game_context, _ = trade_property_phase.apply(game_context, next_action)
        return game_context, decision

    def __repr__(self):
        return 'BSMT Phase'
