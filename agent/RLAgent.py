import random
from config import log
import dice
import constants
from cards import Cards
import copy
import timeout_decorator
import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import InputLayer
from keras.layers import Activation
import constants

class RLAgent:
	def __init__(self, id, buyPropertyModel = None, bsmModel = None):
		self.id = id
		self.lastBuyState = None
		self.buyPropertyModel = buyPropertyModel
		self.lastBuyAction = 0
		self.gammaBuyProperty = 0.95
		self.epsilonBuyProperty = 0.5
		self.epsilonMinBuyProperty = 0.01
		self.epsilonDecayBuyProperty = 0.9
		self.buyPropertyPolicyFrozen = False

		self.lastBSMState = None
		self.bsmModel = bsmModel
		self.lastBSMAction = 0
		self.gammaBSM = 0.95
		self.epsilonBSM = 0.5
		self.epsilonMinBSM = 0.01
		self.epsilonDecayBSM = 0.9
		self.bsmPolicyFrozen = False

	def getBuyPropertyModel(self):
		return self.buyPropertyModel
	
	def getBsmModel(self):
		return self.bsmModel
	
	def moneyForState(self, state):
		agentOneCash = state[3][0]
		agentTwoCash = state[3][1]
		playerOneDebt = state[6][1]
		playerTwoDebt = state[6][3]
		agentOneCash = agentOneCash - playerOneDebt
		agentTwoCash = agentOneCash - playerTwoDebt
		agentOnePropertyWorth = 0
		agentTwoPropertyWorth = 0
		for i in constants.property_to_space_map:
			#In 0 to 39 board position range
			propertyValue =  state[1][i]
			propertyPosition = constants.board[ constants.property_to_space_map[ i ] ]
			
			if propertyValue in range(-6,0):
				agentTwoPropertyWorth += (propertyPosition['price'] + ( (abs(propertyValue)-1)*propertyPosition['build_cost'] ) )
			elif propertyValue == -7:
				agentTwoPropertyWorth += (propertyPosition['price']/2)
			elif propertyValue in range(1,7):
				agentOnePropertyWorth += (propertyPosition['price'] + ( (propertyValue-1)*propertyPosition['build_cost'] ) )
			elif propertyValue == 7:
				agentOnePropertyWorth += (propertyPosition['price']/2)
		
		if state[1][28] == -1:
			agentTwoPropertyWorth += 50
		elif state[1][28] == 1:
			agentOnePropertyWorth += 50
		
		if state[1][29] == -1:
			agentTwoPropertyWorth += 50
		elif state[1][29] == 1:
			agentOnePropertyWorth += 50
		return ((agentOnePropertyWorth,agentTwoPropertyWorth,agentOneCash,agentTwoCash))

	def rewardForAgent(self, money):
		# #print(money[0], money[1], money[2], money[3])
		x = self.id
		p = 2
		if x == 1:
			v = money[0]-money[1]
			m = money[2]/(money[2]+money[3]) if money[2]+money[3] else 0
		else:
			v = money[1]-money[0]
			m = money[3]/(money[2]+money[3]) if money[2]+money[3] else 0
		return ((v/p)/(1+abs(v/p)))+(m/p)

	def respondTrade(self, state):
		pass

	def getInputStateVector(self,  state):
		new_state = [state[0]]+ list(state[1]) + list(state[2]) + list(state[3])+ [state[4]]+ list(state[6])
		return [new_state]
	
	def buildBuyPropertyModel(self, state):
		# Neural Net for Deep-Q learning Model
		# 1 Input layers, 1 Output Layer, and 1 Hidden Layer
		#print("Building BuyPropertyModel")
		model = Sequential()
		model.add(Dense(len(state[0]), input_dim=len(state[0]), activation='linear'))
		model.add(Dense(150, activation='sigmoid'))
		model.add(Dense(2, activation='linear'))
		model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
		self.buyPropertyModel = model

	def buildBSMModel(self, state):
		# Neural Net for Deep-Q learning Model
		# 1 Input layers, 1 Output Layer, and 1 Hidden Layer
		#print("Building BSMModel")
		model = Sequential()
		model.add(Dense(len(state[0]), input_dim=len(state[0]), activation='linear'))
		model.add(Dense(150, activation='sigmoid'))
		model.add(Dense(3, activation='linear'))
		model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
		self.bsmModel = model

	def predictBuyProperty(self, state):
		a = np.array(state)
		return self.buyPropertyModel.predict(a)
	
	def predictBSM(self, state):
		a = np.array(state)
		return self.bsmModel.predict(a)

	def trainBuyProperty(self, state, qValueArray):
		a = np.array(state)
		self.buyPropertyModel.fit(a, qValueArray.reshape(-1, 2), epochs=1, verbose=0)

	def trainBSM(self, state, qValueArray):
		a = np.array(state)
		self.bsmModel.fit(a, qValueArray.reshape(-1, 3), epochs=1, verbose=0)
	
	def e_greedyBuyPropertySelection(self, qValues):
		if np.random.rand() <= self.epsilonBuyProperty:
			return random.randrange(2)
		return np.argmax(qValues)

	def e_greedyBSMSelection(self, qValues):
		if np.random.rand() <= self.epsilonBSM:
			return random.randrange(3)
		return np.argmax(qValues)
	
	def getBuyPropertyReward(self, state):
		stateWithoutHistory = state[:-1]
		money = self.moneyForState(stateWithoutHistory)
		return self.rewardForAgent(money)

	def getBSMReward(self, state):
		stateWithoutHistory = state[:-1]
		money = self.moneyForState(stateWithoutHistory)
		return self.rewardForAgent(money)
	
	def buyProperty(self, state):
		if not state:
			return False
		#convert newly received state to NN input, ie, an input vector
		newInputStateVector = self.getInputStateVector(state)
		if self.lastBuyState:
			#convert previous recorded state to NN input, ie, an input vector
			inputStateVector = self.getInputStateVector(self.lastBuyState)
			#Run NN on inputStateVector to get output, ie, list of qValues
			qValueArray = self.predictBuyProperty(inputStateVector)

			#Run NN on newInputStateVector (newly received state) to get output, ie, list of qValues
			newQValueArray = self.predictBuyProperty(newInputStateVector)
			
			#Pick an action from the list of qValue based on epsilon greedy policy
			action = self.e_greedyBuyPropertySelection(newQValueArray)

			#Also pick the maximum qvalue from the list of qvalues, this will be used in Bellman Equation later
			newQValue = np.amax(newQValueArray)

			#get the reward for new state
			reward = self.getBuyPropertyReward(state)
			
			#apply formula to get modified q value: A version of the bellman Equation
			modifiedQValue = (reward + self.gammaBuyProperty * newQValue)
			
			#Change the Q value of the previously selected action for the previous state
			qValueArray[0][self.lastBuyAction] = modifiedQValue
			
			#Train the model for previous state again with modified q value for previous action
			self.trainBuyProperty(inputStateVector, qValueArray)
		else:
			# Called BSM for the first time. No reward
			#Build a NN for the state recieved
			if not self.buyPropertyModel:
				self.buildBuyPropertyModel(newInputStateVector)
			#Run NN on newInputStateVector (newly received state) to get output, ie, list of qValues
			newQValueArray = self.predictBuyProperty(newInputStateVector)

			#Pick an action from the list of qValue based on epsilon greedy policy
			action = self.e_greedyBuyPropertySelection(newQValueArray)
		
		# #print("Buy Property Action:")
		# #print(action)
		# Record states and actions
		self.lastBuyState = state
		self.lastBuyAction =  action

		# Keep decreasing epsilon value - needed for epsilon greedy selection
		if self.epsilonBuyProperty > self.epsilonMinBuyProperty:
			self.epsilonBuyProperty *= self.epsilonDecayBuyProperty
		#If Action is 0, Return False
		#If Action is 1, Return True
		if action == 0:
			return False
		else:
			return True

	def auctionProperty(self, state):
		return 0

	def receiveState(self, state):
		pass

	def jailDecision(self, state):
		current_player = state[0] % 2
		playerCash = state[3][current_player]
		if playerCash >= 50:
			return ("P")
		else:
			return ("R")
	def unmortgageProperty(self, state):
		player = self.id
		properties = state[1]
		for i in range(40):
			if player == 1 and properties[i] == 7 and ((state[3][0] - state[6][1]) >= (constants.board[properties[i]]['price'] * 0.5)):
				return ("M", [i])
			elif player == 2 and properties[i] == -7 and ((state[3][1] - state[6][3]) >= (constants.board[properties[i]]['price'] * 0.5)):
				return ("M", [i])
		return None
	def isOwner(self, propertyIds, state):
		player = self.id
		for pid in propertyIds:
			if player == 1:
				if state[1][pid] not in [1,2,3,4,5,6]:
					return False
			elif player == 2:
				if state[1][pid] not in [-1,-2,-3,-4,-5,-6]:
					return False
		return True
	def canAfford(self, group, money):
		for p in group:
			if constants.board[p]['build_cost'] > money:
				return False
		return True
	def getCandidates(self, group, state):
		player = self.id
		if player == 1:
			minHouses = 99
			bestProp = 99
			for pid in group:
				if state[1][pid] < minHouses:
					minHouses = state[1][pid]
					bestProp = pid
			if minHouses >= 6:
				return None
			return (bestProp, constants.board[bestProp]['build_cost'])
		else:
			minHouses = -99
			bestProp = 99
			for pid in group:
				if state[1][pid] > minHouses:
					minHouses = state[1][pid]
					bestProp = pid
			if minHouses <= -6:
				return None
			return (bestProp, constants.board[bestProp]['build_cost'])

	def buidHouseOrHotel(self, state):
		colorGroups = {0:[1,3],2:[6,8,9],3:[11,13,14],5:[16,18,19],6:[21,23,24],7:[26,27,29],8:[31,32,34],9:[37,39]}
		completedGroups = []
		affordable = []
		buildCandidates = []
		player = self.id
		if player == 1:
			money =(state[3][0] - state[6][1])
		else:
			money =(state[3][1] - state[6][3])
		for groupId, propertyIds in colorGroups.items():
			if self.isOwner(propertyIds, state):
				completedGroups.append(propertyIds)
		#print("completedGroups", completedGroups)
		if not completedGroups:
			return None
		for group in completedGroups:
			if self.canAfford(group, money):
				affordable.append(group)
		#print("affordable groups", affordable)
		if not affordable:
			return None
		for group in affordable:
			t = self.getCandidates(group, state)
			if t:
				buildCandidates.append(t)
		if not buildCandidates:
			return None
		#print("Build Candidates", buildCandidates)
		maxCost = -1
		bestProp = -1
		for pid, cost in buildCandidates:
			if cost > maxCost:
				maxCost = cost
				bestProp = pid
		if maxCost == -1:
			return None
		return ("B", [(bestProp, 1)])
	
	def hasHousesOrHotels(self, state, properties):
		for pid in properties:
			if state[1][pid] not in [1, 7, -1, -7]:
				return True
		return False
	def getSellcandidate(self, state, candidateGroup):
		max_p = 0
		min_p = 99
		p = -1
		for pid in candidateGroup:
			if self.id == 1:
				if not state[1][pid] == 7:
					if state[1][pid] > max_p:
						max_p = state[1][pid]
						p = pid
			else:
				if not state[1][pid] == -7:
					if state[1][pid] < min_p:
						min_p = state[1][pid]
						p = pid
		if p == -1:
			return None
		return ("S", [(p, 1)])

	def sellHouseOrHotel(self, state):
		colorGroups = {0:[1,3],2:[6,8,9],3:[11,13,14],5:[16,18,19],6:[21,23,24],7:[26,27,29],8:[31,32,34],9:[37,39]}
		completedGroups = []
		filledGroups = []
		player = self.id
		if player == 1:
			money =(state[3][0] - state[6][1])
		else:
			money =(state[3][1] - state[6][3])
		for groupId, propertyIds in colorGroups.items():
			if self.isOwner(propertyIds, state):
				completedGroups.append(propertyIds)
		#print("completedGroups", completedGroups)
		if not completedGroups:
			return None
		for group in completedGroups:
			if self.hasHousesOrHotels(state, group):
				filledGroups.append(group)
		if not filledGroups:
			return None
		candidateGroup = filledGroups[0]
		if not candidateGroup:
			return None
		candidate = self.getSellcandidate(state, candidateGroup)
		return candidate

	def decisionToBuild(self, state):
		unmortgageAction = self.unmortgageProperty(state)
		# #print("Unmortgage Property", unmortgageAction)
		if not unmortgageAction:
			buildAction = self.buidHouseOrHotel(state)
			#print("Build Property", buildAction)
			if not buildAction:
				return None
			return buildAction
		return unmortgageAction
	def mortgageProperty(self, state):
		player = self.id
		props = state[1]
		for i in range(40):
			if player == 1 and props[i] == 1:
				return ("M", [i])
			if player == 2 and props[i] == -1:
				return ("M", [i])
		return None

	def decisionToSell(self, state):
		sellAction = self.sellHouseOrHotel(state)
		if not sellAction:
			mortgageAction = self.mortgageProperty(state)
			return mortgageAction
		return sellAction
	
	def getBSMTDecision(self, state):
		# return None
		if not state:
			return None
		#convert newly received state to NN input, ie, an input vector
		newInputStateVector = self.getInputStateVector(state)
		if self.lastBSMState:
			#convert previous recorded state to NN input, ie, an input vector
			inputStateVector = self.getInputStateVector(self.lastBSMState)

			#Run NN on newInputStateVector (newly received state) to get output, ie, list of qValues
			qValueArray = self.predictBSM(inputStateVector)
			
			#predict with new state
			newQValueArray = self.predictBSM(newInputStateVector)

			#Pick an action from the list of qValue based on epsilon greedy policy
			action = self.e_greedyBSMSelection(newQValueArray)

			#Also pick the maximum qvalue from the list of qvalues, this will be used in Bellman Equation later
			newQValue = np.amax(newQValueArray)

			#get the reward for new state
			reward = self.getBSMReward(state)
			
			#apply formula to get modified q value: A version of the bellman Equation
			modifiedQValue = (reward + self.gammaBSM * newQValue)
			
			#Change the Q value of the previously selected action for the previous state
			qValueArray[0][self.lastBSMAction] = modifiedQValue
			
			#Train the model for previous state again with modified q value for previous action
			self.trainBSM(inputStateVector, qValueArray)
		else:
			# Called BSM for the first time. No reward
			#Build a NN for the state recieved
			if not self.bsmModel:
				self.buildBSMModel(newInputStateVector)

			#Run NN on newInputStateVector (newly received state) to get output, ie, list of qValues
			newQValueArray = self.predictBSM(newInputStateVector)

			#Pick an action from the list of qValue based on epsilon greedy policy
			action = self.e_greedyBSMSelection(newQValueArray)
		
		#print("BSM Action:")
		#print(action)
		
		# Record states and actions
		self.lastBSMState = state
		self.lastBSMAction =  action
		# Keep decreasing epsilon value - needed for epsilon greedy selection
		if self.epsilonBSM > self.epsilonMinBSM:
			self.epsilonBSM *= self.epsilonDecayBSM
		#If Action is 0, Do nothing
		#If Action is 1, Build
		#If Action is 2, Sell
		if action == 0:
			return None
		elif action == 1:
			result = self.decisionToBuild(state)
			if not result:
				self.lastBSMAction = 0
			#print(result)
			return result
		else:
			result = self.decisionToSell(state)
			if not result:
				self.lastBSMAction = 0
			return result

	def run(self, state):
		return {}