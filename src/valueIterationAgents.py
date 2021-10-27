# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
import copy


from learningAgents import ValueEstimationAgent

NORTH = 'north'
SOUTH = 'south'
EAST  = 'east'
WEST  = 'west'
STOP  = 'stop'
EXIT  = 'exit'

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.sum = 0

        self.values1 = util.Counter()

        # Write value iteration code here
        states = mdp.getStates()

        for i in range(iterations):
            states = mdp.getStates()

            for state in states:
                action = self.computeActionFromValues(state)
                if(self.mdp.isTerminal(state)):
                    continue
                self.values1[state] = mdp.getReward(state, None, None) + discount * self.sum

            self.values = copy.deepcopy(self.values1)


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):

        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        if(action not in self.mdp.getPossibleActions(state)):
            #self.values[state] = 0
            return 0

        ALPHA = 0.5

        nextState = state
        
        if(self.mdp.isTerminal(state)):
            nextState = (state[0], state[1])
        elif action == NORTH:
             nextState = (state[0], state[1] + 1)
        elif action == SOUTH:
             nextState = (state[0], state[1] - 1)
        elif action == EAST:
             nextState = (state[0] + 1, state[1])
        elif action == WEST:
             nextState = (state[0] - 1, state[1])
        
        max = -1
        max_key = ""

        for key in self.values:
            print("Chave:", key, "Valor:", self.values[key])
            if(self.values[key] > max):
                max_key = key
                max = self.values[key]

        sortedRewards = self.values.argMax()
        print("=====>", max), max_key

        self.values1[state] = (1 - ALPHA) * self.getValue(state) + ALPHA * (self.mdp.getReward(state, nextState, action) + 0.9 * max)
        
        return self.values[state]

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        possibleActions = self.mdp.getPossibleActions(state)
        largestSum = 0
        best_action = 0

        
        if(len(possibleActions) == 0):
            return None

        for action in possibleActions:
            probStates = self.mdp.getTransitionStatesAndProbs(state, action)
            sum = 0

            #Calculo para cada ação
            for probState in probStates:
                sum += self.getValue(probState[0]) * probState[1]
            
            if sum > largestSum:
                largestSum = sum
                best_action = action

        self.sum = largestSum

        if(best_action == 0):
            best_action = EXIT

        #print("$$$$$", best_action, type(best_action))
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
