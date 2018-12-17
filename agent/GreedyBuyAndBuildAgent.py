import constants

class GreedyBuyAndBuildAgent:
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
			if playerCash-playerDebt>500:
				properties=state[1]
				new_properties=[]
				for y in range(len(properties)):
					if y in [1,3,5,6,8,9,11,12,13,14,15,16,18,19,21,23,24,25,26,27,28,29,31,32,34,35,37,39]:
						new_properties.append(properties[y])
				
				greater_than_0=[]
				for x in new_properties:
					if x>0 and x<6:
						greater_than_0.append(x)
				if len(greater_than_0)==0:
					return None
				min_houses_property_owned=min(greater_than_0)

				min_houses_property_number=0
				while properties[min_houses_property_number]!=min_houses_property_owned:
					min_houses_property_number=min_houses_property_number+1
				if properties[min_houses_property_number]==min_houses_property_owned:
					#print("############### HOUSE BOUGHT#################",min_houses_property_number)
					return ('B',[(min_houses_property_number,1)])
					
					
							
			elif playerCash-playerDebt<200:
				properties=state[1]
				new_properties=[]
				for y in range(len(properties)):
					if y in [1,3,5,6,8,9,11,12,13,14,15,16,18,19,21,23,24,25,26,27,28,29,31,32,34,35,37,39]:
						new_properties.append(properties[y])
				greater_than_0=[]
				for x in new_properties:
					if x>1 and x<7:
						greater_than_0.append(x)
				if len(greater_than_0)==0:
					return None
				max_houses_property_owned=max(greater_than_0)

				max_houses_property_number=0
				while properties[max_houses_property_number]!=max_houses_property_owned:
					max_houses_property_number=max_houses_property_number+1
				if properties[max_houses_property_number]==max_houses_property_owned:
					#print("############### HOUSE SOLD #################",max_houses_property_number)
					return ('S',[(max_houses_property_number,1)])
					
	
					
			else:
				return None

				
				
				
		elif current_player==1:
			if playerCash-playerDebt>500:
				properties=state[1]
				new_properties=[]
				for y in range(len(properties)):
					if y in [1,3,5,6,8,9,11,12,13,14,15,16,18,19,21,23,24,25,26,27,28,29,31,32,34,35,37,39]:
						new_properties.append(properties[y])
				
				less_than_0=[]
				for x in new_properties:
					if x>-6 and x<0:
						less_than_0.append(x)
				if len(less_than_0)==0:
					return None
				min_houses_property_owned=max(less_than_0)

				min_houses_property_number=0
				while properties[min_houses_property_number]!=min_houses_property_owned:
					min_houses_property_number=min_houses_property_number+1
				if properties[min_houses_property_number]==min_houses_property_owned:
					#print("############### HOUSE BOUGHT#################",min_houses_property_number)
					return ('B',[(min_houses_property_number,1)])
					
					
							
			elif playerCash-playerDebt<200:
				properties=state[1]
				new_properties=[]
				for y in range(len(properties)):
					if y in [1,3,5,6,8,9,11,12,13,14,15,16,18,19,21,23,24,25,26,27,28,29,31,32,34,35,37,39]:
						new_properties.append(properties[y])
				less_than_0=[]
				for x in new_properties:
					if x>-7 and x<-1:
						less_than_0.append(x)
				if len(less_than_0)==0:
					return None
				max_houses_property_owned=min(less_than_0)

				max_houses_property_number=0
				while properties[max_houses_property_number]!=max_houses_property_owned:
					max_houses_property_number=max_houses_property_number+1
				if properties[max_houses_property_number]==max_houses_property_owned:
					#print("############### HOUSE SOLD #################",max_houses_property_number)
					return ('S',[(max_houses_property_number,1)])
					
	
					
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
		
