'''
General tips:

- path moves reference the position of the empty space(intuitive)
- cost of path is number of moves from start state to goal state
- Possibly write a state, solver, and board class

'''

import sys
import math
from collections import deque



'''START ALGORITHM'''



class Solver:
	'''
	board: int list given by the user
	method: String specifying which search type
	'''

	def __init__(self, board, method):
		self.board = board
		self.method = method
		self.n = int(math.sqrt(len(board))) # ensure this isnt a double for indexing reasons


	def main(self):
		#Find the zero's index in the array
		zeroIndex = None
		for i in range(0, len(self.board)):
			if self.board[i] == 0:
				zeroIndex = i

		# Instantiate our RootNode or initialState
		# Pass in None for parent & previous action of the root
		# Find the 0 and pass in as blank index to work with
		initState = State(None, self.board, zeroIndex, None)

		self.bfsSearch(initState)





	def spawnChildrenStates(self, pState):
		"""
		pState: parent state
		*In order: UDLR, we append in this order, and so it will be iterated 
			this way when appending to the neighbor set
		*Method to branch every possible way from parent state
		*Return: list of child states refering to their parent
		*Branch factor is minimum 2 and maximum 4
		*Question: 
		*Should we spawn all, & then have garbage collection grab 
			useless ones if they are deemed to exist already?
			Is there a more efficient way of achieving this?
		"""
		childStates = []

		blankIndex = pState.blankIndex

		#Up check (i is not in top row, then we can swap up)
		if blankIndex > self.n-1:
			action = "U"
			#pState : parent state
			upState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(upState)
		#Down check (i is not in bottom row, then we can swap down)
		if blankIndex < (len(pState.boardConfig) - self.n):
			action = "D"
			downState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(downState)

		#Left check (i is not in first column, then we can swap left)
		if blankIndex % self.n != 0:
			action = "L"
			leftState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(leftState)

		#Right check
		if blankIndex % (self.n-1) !=0:
			action = "R"
			rightState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(rightState)

		return childStates


	#def buildNewState(parentState, blankIndex, newBlankIndex):
	def buildNewState(self, parentState, blankIndex, action):
		"""
		Method to take an action branch from the parent State to the new State
		"""
		#IMPORTANT: the assignment is by reference unless you splice with [:]
		newConfig = parentState.boardConfig[:]


		#Determine which way we are swapping based on "action"
		#Linear(1 Dimensional) representaion of grid movement(2-D)

		if action == "U":
			newBlankIndex = blankIndex - self.n
		elif action == "D":
			newBlankIndex = blankIndex + self.n
		elif action == "L":
			newBlankIndex = blankIndex - 1
		else:
			newBlankIndex = blankIndex + 1 #right



		
		newConfig[blankIndex] = newConfig[newBlankIndex]
		newConfig[newBlankIndex] = 0

		#Return a State node with this new information
		return State(parentState, newConfig, newBlankIndex, action)


	def goalTest(self, boardConfiguration):

		for i in range(0, len(boardConfiguration)):
			if boardConfiguration[i] != i:
				return False

		return True


	def getPath(self, state, pathCost):

		#pathCost = 0

		if(state.parent.parent != None):
			return self.getPath(state.parent, pathCost+1)
			
		print(state.action)
		print(state.boardConfig)
		return pathCost

		#return pathCost


	def formatPrint(self, initState):
		print("Reached Goal State Configuration.")
		print() 
		print()
		print("Initial State:")
		print(initState.boardConfig)
		print("Path:")


	"""Different search algorithms"""

	def bfsSearch(self, initState):
		"""
		BFS search: uses a FIFO queue with a deque implementation
		board configurations are represented as strings, as to allow hashing
		"""

		frontier = deque()
		frontier.appendleft(initState)
		explored = set()

		pathCost = 0

		while len(frontier) != 0:
			state = frontier.pop()

			explored.add(str(state.boardConfig))

			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				#Recursively find parent path
				pathCost = self.getPath(state, pathCost)
				print("Path Cost: ", pathCost)
				print("End of AI search")
				return

			childStates = self.spawnChildrenStates(state)


			for child in childStates:

				#Use convert int[] to string to handle in sets
				if str(child.boardConfig) not in frontier and str(child.boardConfig) not in explored:
					frontier.appendleft(child) 

		print("failed bfs")
		return



	"""DONT MOVE ON UNTIL FIGURE OUT ALL OF BFS LIKE PATH COST!!!"""
	def dfsSearch(self, initState):
		"""
		DFS search: uses a FILO stack with a deque implemtation
		pop from the left and append left to implement Stack
		"""
		frontier = deque()
		frontier.appendleft(initState)
		explored = set()

		while len(frontier) != 0:
			state = frontier.popleft()

			explored.add(str(state.boardConfig))

			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				#Recursively find parent path
				self.getPath(state)
				print("End of AI search")
				return

			childStates = self.spawnChildrenStates(state)

			for child in childStates:
				#Use convert int[] to string to handle in sets
				if str(child.boardConfig) not in frontier and str(child.boardConfig) not in explored:
					frontier.appendleft(child) 

		print("failed dfs")
		return















class State:
	'''
	boardConfig:   ordered list of tile numbers
	parent:       State object
	action:       String constrained to "U", "D", "L", "R"
	'''

	def __init__(self, parent, boardConfig, blankIndex, action):

		self.parent = parent
		self.boardConfig = boardConfig
		self.blankIndex = blankIndex
		self.action = action





































# class State:
# 	'''
# 	boardConfig:   ordered list of tile numbers
# 	parent:       State object
# 	action:       String constrained to "U", "D", "L", "R"
# 	'''
# 	#Do I really have to pass in n each time? or calc it each time?
# 	def __init__(self, lastBoardConfig, lastPathCost, lastBlankIndex, action):

# 		self.parent = parent
# 		self.boardConfig = lastBoardConfig
# 		self.n = math.sqrt(len(lastBoardConfig)) #GLOBAL Is this necessary?? Repetative?

# 		self.blankIndex = lastBlankIndex
# 		self.pathCost = lastPathCost + 1




























argList = sys.argv

#Cause program name is argList[0]?
method = argList[1]

#The board is a comma seperated list of integers containing now spaces
boardString = argList[2]
board = []

#Store the board into a int array
for char in boardString:
	if(char != ','):
		board.append(int(char))
print()
print("***Created Artificial Intelligence***")
print()
ai = Solver(board, "bfs")
ai.main()
print("AI is has completed its task.")







'''END ALGORITHM'''



























































































# '''BFS'''

# def bfsSearch(initState, goalTest):
# 	'''
# 	initState: starting State object
# 	goalTest:  a int list representing a board configuration
# 	'''


# 	#You can hash whole lists

# 	#the left side append and pop from right
# 	#append the initial state to the board, frontier is a queue
# 	frontier = deque(board)
# 	explored = set()

# 	#While the frontier is not empty
# 	while not len(frontier) == 0:
# 		state = frontier.pop()
# 		explored.add(state)






# #board is an int list, method is a string

# class Solver(board, method):

# 	#Queue implementation
# 	self.queue = []


# 	#Find the index of the blank space
# 	blankIndex = None

# 	for i in range(0, board):
# 		if(i == 0):
# 			blankIndex = i


# 	#Create our root node or initial board state
# 	root = State(originalBoard, 0, )














	

# '''-----------------General classes-----------------'''

# class State:
# 	'''
# 	boardConfig:   ordered list of tile numbers
# 	parent:       State object
# 	action:       String constrained to "U", "D", "L", "R"
# 	'''

# 	#Do I really have to pass in n each time? or calc it each time?
# 	def __init__(self, lastBoardConfig, lastPathCost, lastBlankIndex, action):

# 		self.parent = parent
# 		self.boardConfig = lastBoardConfig
# 		self.n = math.sqrt(len(lastBoardConfig)) #GLOBAL Is this necessary?? Repetative?

# 		self.blankIndex = lastBlankIndex
# 		self.pathCost = lastPathCost + 1








































































# '''-----------------General classes-----------------'''

# class State:
# 	'''
# 	stateOrder:   ordered list of tile numbers
# 	parent:       State object
# 	action:       String constrained to "U", "D", "L", "R"
# 	'''

# 	#Do I really have to pass in n each time? or calc it each time?
# 	def __init__(self, stateOrder, parent, action):

# 		self.parent = parent
# 		self.stateOrder = parent.stateOrder
# 		self.n = math.sqrt(stateOrder) #GLOBAL Is this necessary?? Repetative?

# 		self.blankIndex = parent.blankIndex
# 		self.pathCost = parent.pathCost + 1 #uniform ++??
		
# 		#Construct a new ordering based on the action
# 		stateOrder = parent.stateOrder
# 		self.buildNewState(action)
		


# 	def buildNewState(self, action):
# 		'''Is this pass by reference method okay???'''
# 		#This is a single swap of the blank with any adjecent tile
# 		#Linear(1 Dimensional) representaion of grid movement(2-D)

# 		#blankIndex = parent.blankIndex
# 		#gridList = parent.stateOrder

# 		if action == "U":
# 			newIndex = blankIndex - n
# 		elif action == "D":
# 			newIndex = blankIndex + n
# 		elif action == "L":
# 			newIndex = blankIndex - 1
# 		else:
# 			newIndex = blankIndex + 1


# 		#I like to think of it as moving "into" the empty space, 
# 		# and then simply leaving a void behind (constructed this way)

# 		#Shift the value into the blank space (now a duplicate)
# 		self.stateOrder[blankIndex] = self.stateOrder[newIndex]
# 		#Remove the duplicate (now the leftover void)
# 		self.stateOrder[newIndex] = 0



# 	def spawnChildren():
# 		print("hello")
# 	#????
# 	#Does this now call U D L R on this base board and create 
# 	# three new instances?
# 	#Where is the BFS coming in?or is the BFS algo calling this spawn function--
# 	# I think it is. So should the BFS be in here?



# '''Solver class'''














# '''BFS implementation'''

















































#Sample input could be: $python driver.py bfs 0,3,2,1



#Write results to a file called output.txt
outputFile = open('output.txt', 'w')

#Use .write to write variables out to the file
#print("The method is: ", method)
#print("The board is: ", board, ". It is of type: ",type(board))

outputFile.write("hello")

