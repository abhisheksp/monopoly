from game_state.action import Action


class Agent:
    """
    Adapter to external Agent
    """

    def __init__(self, external_agent=None):
        self.external_agent = external_agent

    def buy_property(self, state):
        return self.external_agent.buyProperty(state)

    def bsmt_decision(self, state):
        ext_decision = self.external_agent.getBMSTDecision(state)
        if ext_decision[0] == 'M':
            action_type = Action.MORTGAGE_PROPERTY
            property_ = state.board.property_at(ext_decision[1][0])
            return action_type, property_
        return ext_decision

    def auction_property(self, state):
        return self.external_agent.auctionProperty(state)

    def jail_decision(self, state):
        return self.external_agent.jailDecision(state)

    def respond_trade(self, state):
        return self.external_agent.respondTrade(state)

    def respond_mortgage(self, state):
        return self.external_agent.respondMortgage(state)

    def receive_state(self, state):
        self.external_agent.receiveState(state)
        return
