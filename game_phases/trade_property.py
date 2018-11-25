import game_phases.game_phase


class TradeProperty(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        trades = action
        for trade in trades:
            self._apply_trade(trade)
        return game_context

    def __repr__(self):
        return 'Mortgage Property Phase'

    def _apply_trade(self, trade):
        buyer, seller, price, properties = trade['buyer'], trade['seller'], trade['price'], trade['properties']
        buyer.deduct(price)
        seller.increment(price)
        for property_ in properties:
            property_.own(buyer)
