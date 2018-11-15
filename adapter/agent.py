class Agent:
    """
    Adapter to external Agent
    """

    def __init__(self, external_agent=None):
        self.external_agent = external_agent

    def buy_property(self, state):
        return self.external_agent.buyProperty(state)

    def bsmt_decision(self, state):
        return self.external_agent.getBMSTDecision(state)

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
