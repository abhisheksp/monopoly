import constants

class GreedyBuyAndMortgageAgent:
	def __init__(self, id):
		self.id = id
		self.PLAYER_TURN_INDEX = 0
		self.PROPERTY_STATUS_INDEX = 1
		self.PLAYER_POSITION_INDEX = 2
		self.PLAYER_CASH_INDEX = 3
		self.PHASE_NUMBER_INDEX = 4
		self.PHASE_PAYLOAD_INDEX = 5
	
	
	def getBSMTDecision(self, state):
		property_multiplier=1
		current_player = state[0] % 2
		if current_player==1:
			property_multiplier=-1
		playerCash = state[3][current_player]
		playerDebt = state[6][(2*current_player)+1]

		if current_player==0:
			if playerCash-playerDebt<100:
				properties=state[1]
				max_houses_property_owned=max(properties)
				if max_houses_property_owned==0:
					return None
				elif max_houses_property_owned==1:
					max_houses_property_number=0
					while properties[max_houses_property_number]!=max_houses_property_owned:
						max_houses_property_number=max_houses_property_number+1
					if properties[max_houses_property_number]==max_houses_property_owned:
						#print("###############MORTGAGED#################",max_houses_property_number)
						return ('M',[max_houses_property_number])
						
					
							
			elif playerCash-playerDebt>350:
				properties=state[1]
				max_houses_property_owned=max(properties)
				if max_houses_property_owned==7:
					max_houses_property_number=0
					while properties[max_houses_property_number]!=max_houses_property_owned:
						max_houses_property_number=max_houses_property_number+1	
					if properties[max_houses_property_number]==max_houses_property_owned:
						#print("###############UNMORTGAGED#################",max_houses_property_number)
						return ('M',[max_houses_property_number])
					
	
					
			else:
				return None
				
		elif current_player==1:
			if playerCash-playerDebt<100:
				properties=state[1]
				max_houses_property_owned=min(properties)
				if max_houses_property_owned==0:
					return None
				elif max_houses_property_owned==-1:
					max_houses_property_number=0
					while properties[max_houses_property_number]!=max_houses_property_owned:
						max_houses_property_number=max_houses_property_number+1
					if properties[max_houses_property_number]==max_houses_property_owned:
						#print("###############MORTGAGED#################",max_houses_property_number)
						return ('M',[max_houses_property_number])
						
					
							
			elif playerCash-playerDebt>350:
				properties=state[1]
				max_houses_property_owned=min(properties)
				if max_houses_property_owned==-7:
					max_houses_property_number=0
					while properties[max_houses_property_number]!=max_houses_property_owned:
						max_houses_property_number=max_houses_property_number+1	
					if properties[max_houses_property_number]==max_houses_property_owned:
						#print("###############UNMORTGAGED#################",max_houses_property_number)
						return ('M',[max_houses_property_number])
	
					
			else:
				return None				
				
				
				

	def respondTrade(self, state):
		pass


	def buyProperty(self, state):
		
		return True
		
		#current_player = state[0] % 2
		#playerCash = state[3][current_player]
		#playerDebt = state[6][(2*current_player)+1]
		#
		#if playerCash-playerDebt>350:
		#	return True
		#else:
		#	return False
		#

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
		
