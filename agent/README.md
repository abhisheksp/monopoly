# Monopoly

Data Science Project CSE 519
RL Agent

## NN with 3 layers
We use the Keras Sequential model to build a neural network for our Deep Q-Learning. The networks all have three layers:
```
	model = Sequential()
	model.add(Dense(len(state[0]), input_dim=len(state[0]), activation='linear'))
	model.add(Dense(150, activation='sigmoid'))
	model.add(Dense(2, activation='linear'))
	model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
```

## Q-Learning algorithm
Based on the reward received and the Q values predicted by the network for the new state, we modify the Q value of previous state-action pair using the Bellman Equation:
```
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
```

### Reward Function
We define a reward function that gives a reward for a given state:
```
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

```
During training, one of the important steps is to let the RL agent explore a few actions freely, at the beginning, even if their Q values are not the best (maximum). This selection process is referred to as the  epsilon-greedySelection in the implementation of the paper[1]. We maintain a parameter epsilon which is gradually decreased as the model trains, and as the value gets smaller, the probability of picking random actions also decreases, i.e, the agent stops exploring, and sticks to picking feedback-based learned actions.
We train all the Neural Networks (we describe all of their specifications in detail below) by playing the RL agent against other agents that are described in the earlier sections. We also train them by playing one RL agent against another RL agent. We persist these NN models across multiple games, and the RL agents will learn by playing over 1000 games at once. Once the models are sufficiently trained, we freeze the Neural Network layers. At this point, the agent will predict the actions to take using the pre-trained model.
## Implementing RL Agent Class Methods
### buyProperty
The state is encoded as a python list with only relevant fields (we ignore past states). This is passed to the first layer of the Neural Network. The network predicts two actions (last layer has two units) which is the position of the maximum Q value in the output array. 0, i.e, return False or 1, i.e, return True. We use the same reward function that is discussed above.

### getBSMTDecision
The state is formatted to a list and is fed to the Neural Network. The network predicts 3 specific actions. 0 is to take no action, 1 is to Build, and 2 is to textbfSell. Note that mortgaging and unmortgaging are handled internally within these actions. This decision is further handled by a greedy agent that does the following:
#### 1
If RL agent says build, but if there are any properties mortgaged by the player, Unmortgage the property first. If all properties are unmortgaged, select the group that is 'completed' by the player, and look for the optimal property to build house/hotel.
#### 2
If RL agent says sell, look for 'completed' property groups, and select an optimal house/hotel to build.
#### 3
If RL agent says sell, but all completed groups have houses already sold, or if there are no more completed groups left, Mortgage the most profitable property owned.