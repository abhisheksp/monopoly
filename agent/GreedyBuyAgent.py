import constants

class GreedyBuyAgent:
	def __init__(self, id):
		self.id = id
		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
	
	
	def getBSMTDecision(self, state):
		return None

	def respondTrade(self, state):
		pass

	def buyProperty(self, state):
		return True
		

	def auctionProperty(self, state):
		return 0

	def receiveState(self, state):
		pass


	def jailDecision(self, state):
		current_player = state[self.PLAYER_TURN_INDEX] % 2
		playerCash = state[self.PLAYER_CASH_INDEX][current_player]
		
		if playerCash >= 50:
			return ("P")
		else:
			return ("R")
		
