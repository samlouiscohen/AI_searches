'''
General tips:

- path moves reference the position of the empty space(intuitive)
- cost of path is number of moves from start state to goal state
- Possibly write a state, solver, and board class

'''

import sys
import math
import time
import resource
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



		return self.bfsSearch(initState)





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
			action = 'Up'
			#pState : parent state
			upState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(upState)
		#Down check (i is not in bottom row, then we can swap down)
		if blankIndex < (len(pState.boardConfig) - self.n):
			action = 'Down'
			downState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(downState)

		#Left column check (i is not in first column, then we can swap left)
		if blankIndex % self.n != 0:
			action = 'Left'
			leftState = self.buildNewState(pState, pState.blankIndex, action)
			childStates.append(leftState)

		#Right column check
		if (blankIndex + 1) % self.n !=0:
			action = 'Right'
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

		if action == 'Up':
			newBlankIndex = blankIndex - self.n
		elif action == 'Down':
			newBlankIndex = blankIndex + self.n
		elif action == 'Left':
			newBlankIndex = blankIndex - 1
		else: #right
			newBlankIndex = blankIndex + 1 

		#Swap blank with adjacent tile
		newConfig[blankIndex] = newConfig[newBlankIndex]
		newConfig[newBlankIndex] = 0

		#Return a State node with this new information
		return State(parentState, newConfig, newBlankIndex, action)


	def goalTest(self, boardConfiguration):

		for i in range(0, len(boardConfiguration)):
			if boardConfiguration[i] != i:
				return False

		return True


	# # def getPath(self, state, pathCost):
	# def getPath(self, state, pathCost):


	# 	#pathCost = 0

	# 	if(state.parent.parent != None):
	# 		pathCost = self.getPath(state.parent, pathCost+1)
	# 		#print("just called get path with: ", state.parent.boardConfig)
	# 		#self.getPath(state.parent)

	# 	print(state.action)
	# 	print(state.boardConfig)
	# 	return pathCost

	# 	#return pathCost

	# def getPath(self, state, pathCost):
	def getPath(self, state, pathCost, path_to_goal):
		"""
		Recursive method to print out path from initial board to end board
		Base case: if the state's parent is None
		Note: We don't want to print the init Node's state change (so extra if)

		"""


		if(state.parent != None):
			pathCost = self.getPath(state.parent, pathCost+1, path_to_goal)
		
		if state.parent == None:
			#In initial node, no action led to this. So don't print action
			return pathCost

		#print(state.action)
		#formatedStateAction = 
		#path_to_goal.append("'" + state.action + "'")
		path_to_goal.append(state.action)

		#print(state.boardConfig)
		return pathCost





	def formatPrint(self, initState):
		# print("Artificially Intelligent Agent. I live to serve.")
		# print("Master Sam, I have Reached Goal State Configuration.")
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
		data: 0: path_to_goal, 1: pathCost, 2: nodes_expanded, 3:
		"""

		#path_to_goal, cost_of_path,
		#nodes_expanded, fringe_size, max_fringe_size,
		#search_depth, max_search_depth, running_time, max_ram_usage

		data = DataContainer()
		initPathCost = 0


		frontier = deque()
		frontier.appendleft(initState)
		explored = set()

		#pathCost = 0

		while len(frontier) != 0:

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)
			#Update max search depth
			#??

			state = frontier.pop()

			#Add the current state to the explored set
			explored.add(str(state.boardConfig))

			#Test if current state is the goal state
			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				
				#Recursively find parent path with getPath method
				data.cost_of_path = self.getPath(
					state, initPathCost, data.path_to_goal)
				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)


				#Store data into stats object

				#To be an expanded node, you first have to be explored. Only 
				# the goal-state node will have returned before being explored.
				data.nodes_expanded = len(explored) - 1

				return data

			#If current node is not in goal state, expand it
			childStates = self.spawnChildrenStates(state)


			for child in childStates:

				#Use convert int[] to string to handle in sets
				if str(child.boardConfig) not in frontier and str(child.boardConfig) not in explored:
					frontier.appendleft(child) 


		data.nodes_expanded = len(explored)
		print("failed bfs")
		return data #???????????????? Do I even account for this?








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


class DataContainer:
	"""
	Object to hold statistical information about the search
	"""

	def __init__(self):

		self.path_to_goal = []
		self.cost_of_path = None
		self.nodes_expanded = None
		self.fringe_size = 0
		self.max_fringe_size = 0
		self.search_depth = None
		self.max_search_depth = None
		self.running_time = None
		self.max_ram_usage = None



















































"""RUNNING PROGRAM"""

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


start_time = time.time()

ai = Solver(board, "bfs")
data = ai.main()

data.running_time = "{0:.8f}".format(time.time() - start_time)
data.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000

#print("AI is has completed its task in: ", running_time, "seconds")
#print("AI is has completed its task with RAM use: ", max_resource/1000000, "megabytes")









#File output


print(data.path_to_goal)
print("Path Cost: ", data.cost_of_path)
print("nodes expanded: ", data.nodes_expanded)
print("fringe_size: ", data.fringe_size)
print("max_fringe_size: ", data.max_fringe_size)
print("search_depth: ", None)
print("max_search_depth: ", None)
print("running_time: ", data.running_time)
print("max_ram_usage: ", data.max_ram_usage)


print("End of AI search")
#print(data.fringe_size)


#Ask how to format properly!!!!
#Write results to a file called output.txt
#outputFile = open('output.txt', 'w')

# finalPath = "["

# for aMove in data.path_to_goal:
# 	finalPath+= "'%s' " % aMove
# finalPath
# print(finalPath)
# #print(data.path_to_goal)
# print("-------------------------------------------------")





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



# #Write results to a file called output.txt
# outputFile = open('output.txt', 'w')

# #Use .write to write variables out to the file
# #print("The method is: ", method)
# #print("The board is: ", board, ". It is of type: ",type(board))

# outputFile.write("hello")

