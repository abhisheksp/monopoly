import game_phases.game_phase


class Auction(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        current_player = game_state.current_player
        current_position = current_player.position
        bids = map(lambda x: (x[1], x[1].agent.auction_property()), enumerate(game_state.players))
        maximum_bidder, bid_amount = max(bids, key=lambda bid: bid[1])
        maximum_bidder.buy_property(bid_amount)
        current_position.own(maximum_bidder)
        game_context.phase = game_context.get_phase('BSMT')
        return game_context

    def __repr__(self):
        return 'Pay Rent Phase'

