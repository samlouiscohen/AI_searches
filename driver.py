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
import queue
import heapq



'''START ALGORITHM'''


#uniqueID = 0

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
		#initState.depth = 0 #Test this for finding max depth


		#Decide which search to perform
		if method == "bfs":
			return self.bfsSearch(initState)
		elif method == "dfs":
			return self.dfsSearch(initState)
		elif method == "ast":
			return self.astSearch(initState)
		#else:
		#	return self.idaSearch(initState)







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

		#Update the ID for this new node

		global uniqueID
		uniqueID +=1

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


	# def getPath(self, state, pathCost, path_to_goal):
	# 	"""
	# 	Recursive method to print out path from initial board to end board
	# 	Base case: if the state's parent is None
	# 	Note: We don't want to print the init Node's state change (so extra if)

	# 	"""
		# if(state.parent != None):
		# 	pathCost = self.getPath(state.parent, pathCost+1, path_to_goal)
		# else:
		# 	#Init node, no action led here. Don't further recurse nor append.
		# 	return pathCost


		# path_to_goal.append(state.action)
		# return pathCost
	def getPath(self, state, path_to_goal):
		"""
		method to print out path from initial board to end board
		Base case: if the state's parent is None
		Note: We don't want to print the init Node's state change (so extra if)

		"""
		pathCost = 0

		while(state.parent != None):

			path_to_goal.appendleft(state.action)
			pathCost += 1
			#print(state.parent.boardConfig)
			state = state.parent

		return pathCost






	def formatPrint(self, initState):
		# print("Artificially Intelligent Agent. I live to serve.")
		# print("Master Sam, I have Reached Goal State Configuration.")
		print("Initial State:")
		print(initState.boardConfig)





	"""Different search algorithms"""

	def bfsSearch(self, initState):
		"""
		BFS search: uses a FIFO queue with a deque implementation
		board configurations are represented as strings, as to allow hashing
		data: 0: path_to_goal, 1: pathCost, 2: nodes_expanded, 3:
		"""


		data = DataContainer()
		initPathCost = 0


		frontier = deque()
		frontier.appendleft(initState)
		explored = set()
		frontier_set = set()
		frontier_set.add(str(initState.boardConfig))


		while len(frontier) != 0:

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)

			state = frontier.pop()
			frontier_set.remove(str(state.boardConfig))

			#Add the current state to the explored set
			explored.add(str(state.boardConfig))

			#Test if current state is the goal state
			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				
				#Recursively find parent path with getPath method
				# data.cost_of_path = self.getPath(
				# 	state, initPathCost, data.path_to_goal)

				data.cost_of_path = self.getPath(
					state, data.path_to_goal)


				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)


				#To be an expanded node, you first have to be explored. Only 
				# the goal-state node will have returned before being explored.
				data.nodes_expanded = len(explored) - 1

				return data

			#If current node is not in goal state, expand it
			childStates = self.spawnChildrenStates(state)

			if state.depth + 1 > data.max_search_depth:
				data.max_search_depth  = state.depth + 1

			for child in childStates:

				#Use convert int[] to string to handle in sets
				if str(child.boardConfig) not in explored and str(child.boardConfig) not in frontier_set:
				#if str(child.boardConfig) not in frontier and str(child.boardConfig) not in explored:
					frontier.appendleft(child) 
					frontier_set.add(str(child.boardConfig))


		data.nodes_expanded = len(explored)
		print("failed bfs")
		return data #???????????????? Do I even account for this?


	def dfsSearch(self, initState):
		"""
		DFS search: uses a FILO stack with a deque implementation
		board configurations are represented as strings, as to allow hashing
		data: 0: path_to_goal, 1: pathCost, 2: nodes_expanded, 3:
		"""

		data = DataContainer()
		#initPathCost = 0


		frontier = deque()
		frontier.appendleft(initState) #appends to the right side


		explored = set()
		frontier_set = set()
		frontier_set.add(str(initState.boardConfig))

		while len(frontier) != 0:

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)


			state = frontier.popleft() #pops from the right side
			frontier_set.remove(str(state.boardConfig))

			#Add the current state to the explored set
			explored.add(str(state.boardConfig))

			#Test if current state is the goal state
			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				
				#Recursively find parent path with getPath method
				#data.cost_of_path = self.getPath(state, initPathCost, data.path_to_goal)
				data.cost_of_path = self.getPath(state, data.path_to_goal)

				
				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)

				#To be an expanded node, you first have to be explored. Only 
				# the goal-state node will have returned before being explored.
				data.nodes_expanded = len(explored) - 1

				return data


			#if state.depth + 1 > data.max_search_depth:
			#	data.max_search_depth  = state.depth + 1

			if state.depth > data.max_search_depth:
				data.max_search_depth  = state.depth

			#If current node is not in goal state, expand it
			childStates = self.spawnChildrenStates(state)

			#Reverse childstates-- push backwards order, and pop correct order
			for child in reversed(childStates):

				#Use convert int[] to string to handle in sets
				#if ((str(child.boardConfig) not in frontier) and (str(child.boardConfig) not in explored)):
				if str(child.boardConfig) not in explored and str(child.boardConfig) not in frontier_set:
	
					frontier.appendleft(child) 
					frontier_set.add(str(child.boardConfig))


		data.nodes_expanded = len(explored)
		print("failed dfs")
		return data



	"""--------------------------"""

	def astSearch(self, initState):
		"""
		use 2-tuples: (cost, UDLR, node). The direction is in the node.
		"""


		data = DataContainer()

		frontier = []
		heapq.heappush(frontier, (0, 0, initState))

		explored = set()

		frontier_set = set()
		frontier_set.add(str(initState.boardConfig))



		while len(frontier) != 0:

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)

			#Pop cheapest node, add it to explored & remove it from frontier set
			nodeTuple = heapq.heappop(frontier)
			frontier_set.remove(str(nodeTuple[2].boardConfig))
			explored.add(str(nodeTuple[2].boardConfig))



			#Check if this popped state is the goal state
			if self.goalTest(nodeTuple[2].boardConfig):
				
				data.cost_of_path = self.getPath(nodeTuple[2], data.path_to_goal)

				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)

				#To be an expanded node, you first have to be explored. However,
				# the goalNode will increment explored, but wont be expanded
				data.nodes_expanded = len(explored) - 1

				return data

			#Update the max search depth
			if nodeTuple[2].depth + 1 > data.max_search_depth:
				data.max_search_depth  = nodeTuple[2].depth + 1

			childStates = self.spawnChildrenStates(nodeTuple[2])

			for child in childStates:

				childNodeTuple = None

				if child.action == 'Up':
					child.cost = self.totalCostFunction(child)
					childNodeTuple = (child.cost, 1, child)
					
				elif child.action == 'Down':
					child.cost = self.totalCostFunction(child)
					childNodeTuple = (child.cost, 2, child)
					
				elif child.action == 'Left':
					child.cost = self.totalCostFunction(child)
					childNodeTuple = (child.cost, 3, child)
					
				else:
					child.cost = self.totalCostFunction(child)
					childNodeTuple = (child.cost, 4, child)


				if str(child.boardConfig) not in explored and str(child.boardConfig) not in frontier_set:
						
					heapq.heappush(frontier, childNodeTuple)

					frontier_set.add(str(child.boardConfig))

				elif str(child.boardConfig) in frontier_set:
					#print("hello")
					#pass
					self.decreaseKey(frontier, childNodeTuple)





	def decreaseKey(self, frontier, childTuple):
		"""Since we're in decreaseKey method, it means that the boardConfig 
		was already in the frontier. So now we have to see if the new pathCost
		to the same config is cheaper. If so replace the old one."""

		for oldTupleNode in frontier:

			#Find the node that contains the board that we now have a duplicate of
			if oldTupleNode[2].boardConfig == childTuple[2].boardConfig:

				#Compare the costs
				if childTuple[0] < oldTupleNode[0]:
					#oldTupleNode = childTuple
					del frontier[frontier.index(oldTupleNode)]
					heapq.heappush(frontier, childTuple)



				elif childTuple[1] < oldTupleNode[1]:
					#oldTupleNode = childTuple
					del frontier[frontier.index(oldTupleNode)]
					heapq.heappush(frontier, childTuple)

				else: #The first two were equal and so we look to first in, and so the old will always win (dont do anything)
					break

		#heapq.heapify(frontier)


	"""--------------------------"""


	#def ida























	# def astSearch(self, initState):
	# 	"""
	# 	A-Star Search implemented using a priority queue.
	# 	Heuristic: Manhattan priority function- 
	# 		the sum of the distances of the tiles from their goal positions.
	# 	Note: Don't count the blank space in this summation

	# 	g(n): cost to reach node n
	# 	h(n): cost to get from n to the goal
	# 	f(n) = g(n) + h(n)

	# 	ALGORITHM:
	# 	1. Use a tuple: (distance, udlr, uniqueID) within the priorityQueue
	# 		-The priority queue orders by the 1st value, then proceeds if same
	# 	2. UDLR: 0,1,2,3

	# 	"""
	# 	#Container object to send out all data after A-Star ends
	# 	data = DataContainer()

	# 	#Unique ID to determine the order in case dupliacte node was entered
	# 	#uniqueID = 0

	# 	#Use a priority queue for the frontier list. This takes tuples
	# 	frontier = [] #queue.PriorityQueue()

	# 	#Dictionary to map a UniqueID from the frontier tuple to an actual node
	# 	boardDictionary = dict()


	# 	#Note: dictIDtoNode maps-- int : Node
	# 	dictIDtoNode = dict()
	# 	#Note: dictBoardToID maps-- String : int
	# 	dictBoardToID = dict()

	# 	#Initialize the Priority Queue (frontier) with the root state
	# 	heapq.heappush(frontier, (0, None, uniqueID))

	# 	#boardDictionary[uniqueID] = initState

	# 	dictIDtoNode[uniqueID] = initState
	# 	dictBoardToID[str(initState.boardConfig)] = uniqueID



	# 	explored = set()
	# 	frontier_set = set()


	# 	while len(frontier) != 0:

	# 		# for k, v in dictIDtoNode.items():
	# 		# 	print(k, v.boardConfig)
	# 		# 	print("")

	# 		stateCosts = heapq.heappop(frontier)
	# 		#frontier_set.remove(stateCosts[2])
	# 		#state = boardDictionary[stateCosts[2]]
	# 		state = dictIDtoNode[stateCosts[2]]

	# 		#Add the current state to the explored set
	# 		explored.add(str(state.boardConfig))


	# 		#Goal test
	# 		if self.goalTest(state.boardConfig):
	# 			data.cost_of_path = self.getPath(state, data.path_to_goal)
	# 			return data

	# 		#If current node is not in goal state, expand it
	# 		childStates = self.spawnChildrenStates(state)

	# 		#Use this to assign correct ID's to each child in the cluster
	# 		idAdjust = len(childStates) - 1
			



	# 		for child in childStates:

	# 			#Assign the proper uniqueID to each child after blindly incrementing
	# 			actualID = uniqueID - idAdjust
	# 			#boardDictionary[actualID] = child
	# 			dictIDtoNode[actualID] = child
	# 			#dictBoardToID[child.boardConfig] = uniqueID #This will add a duplicate right???????

	# 			idAdjust -= 1
	# 			costTuple = None

	# 			if child.action == 'Up':
	# 				costTuple = (self.totalCostFunction(child), 1, actualID)
					
	# 			elif child.action == 'Down':
	# 				costTuple = (self.totalCostFunction(child), 2, actualID)
					
	# 			elif child.action == 'Left':
	# 				costTuple = (self.totalCostFunction(child), 3, actualID)
					
	# 			else:
	# 				costTuple = (self.totalCostFunction(child), 4, actualID)




	# 			if str(child.boardConfig) not in explored and str(child.boardConfig) not in frontier_set:
					
	# 				heapq.heappush(frontier, costTuple)

	# 				frontier_set.add(str(child.boardConfig))
	# 				dictBoardToID[str(child.boardConfig)] = uniqueID

	# 			elif str(child.boardConfig) in frontier_set:

	# 				self.decreaseKey(frontier, dictIDtoNode, dictBoardToID, costTuple, child)


	# 	data.nodes_expanded = len(explored)
	# 	print("failed ast")
	# 	return data




	# def decreaseKey(self, frontier, dictIDtoNode, dictBoardToID, newCost, newNode):
	# 	"""
	# 	Since we're in decreaseKey method, it means that the boardConfig 
	# 	was already in the frontier. So now we have to see if the new pathCost
	# 	to the same config is cheaper. If so replace the old one.

	# 	**Does it make sense to store the f-function cost in the nodes???

	# 	Algorithm:
	# 	1. We know the boardConfig, and the new one is not added to the frontier yet.
	# 	2. 


	# 	Whats the benifit of a dictionary with uniqueID: object rather than

	# 	"""

	# 	for k, v in dictIDtoNode.items():
	# 		print(k, v)
		
	# 	uniqueID = newCost[2]

	# 	oldID = dictBoardToID[str(newNode.boardConfig)]

	# 	oldNode = dictIDtoNode[oldID]


	# 	#Search the heap for the cost associated with the oldID

	# 	for costTuple in frontier:

	# 		#Search for the oldID corresponding to the duplicate boardConfig
	# 		if costTuple[2] == oldID:

	# 			#Check to see which of the paths is cheaper

	# 			#If the new cost is cheaper, than replace the old path
	# 			if newCost[0] < costTuple[0]:

	# 				#Update both dictionaries, the frontier, NOT the sets
	# 				costTuple = newCost #??????PROPER UPDATE-- set the new tuple like this??????

	# 				#Delete the old ID key and add the new ID-state pair
	# 				dictIDtoNode[uniqueID] = dictIDtoNode.pop(oldID)
	# 				#dictIDtoNode[uniqueID] = dictIDtoNode[oldID]
	# 				#dictIDtoNode.pop(oldID)




	# 				dictBoardToID[str(newNode.boardConfig)] = uniqueID


	# 			elif newCost[1] < costTuple[1]:
	# 				#print("\n------------- found old ID----------\n")
	# 				# for aTuple in frontier:
	# 				# 	if(aTuple[2] == uniqueID):
	# 				# 		print("\n------------- found old ID----------\n")


	# 				costTuple = newCost
	# 				dictIDtoNode[uniqueID] = dictIDtoNode.pop(oldID)
	# 				#dictIDtoNode[uniqueID] = dictIDtoNode[oldID]

	# 				dictBoardToID[str(newNode.boardConfig)] = uniqueID

	# 			else: #Tie goes to the older node then so just break and dont do anything-- dont add the new node at all.
	# 				break



	# 			heapq.heapify(frontier)




















	def totalCostFunction(self, node):
		"""
		Method to calculate the f(n) total cost of the current node.
		returns g(n) + h(n)
		"""
		return node.depth + self.calcManhattanDist(node.boardConfig)

	def calcManhattanDist(self, boardConfig):
		"""
		Manhattan priority function- Calculate the sum of 
			the distances of the tiles from their goal positions.
		boardConfig: type list, series of tile numbers
		This treats the 0 tile as a blank (non-tile)
		**Dnt calc for 0
		"""
		distanceSum = 0
		for i in range(1, len(boardConfig)): #Dont include the 0 tile

			tileNum = boardConfig[i]

			iRowCol = self.calcRowCol(i, self.n)

			tRowCol = self.calcRowCol(tileNum, self.n)

			distanceSum += abs(tRowCol[0]-iRowCol[0]) + abs(tRowCol[1]-iRowCol[1])

		return distanceSum

	def calcRowCol(self, num, n):
		"""
		Find the 2-D row and column of an index in a 1-D list
		"""

		#Find the row of a number
		row = 0
		rowMultiplier = 1
		while((num // (n*rowMultiplier)) != 0):
			row +=1
			rowMultiplier +=1

		#Find the column of a number
		col = num % n

		return row,col





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
		self.depth = parent.depth + 1 if parent else 0
		self.cost = 0

	def __lt__(self, other):
		return self.cost < other.cost

# class HeapState:
# 	'''
# 	boardConfig:   ordered list of tile numbers
# 	parent:       State object
# 	action:       String constrained to "U", "D", "L", "R"
# 	'''

# 	def __init__(self, parent, boardConfig, blankIndex, action):

# 		self.parent = parent
# 		self.boardConfig = boardConfig
# 		self.blankIndex = blankIndex
# 		self.action = action
# 		self.depth = parent.depth + 1 if parent else 0

# 	def __lt__(self, other):

# 		return self.cost < other.cost

# class heapState:
# 	def __init__(self, parent, boardConfig, blankIndex, action):
# 		self.parent = parent
# 		self.boardConfig = boardConfig
# 		self.blankIndex = blankIndex
# 		self.action = action
# 		self.depth = parent.depth + 1 if parent else 0

# 		self.ID
# 		self.cost = None

# 	def __lt__(self, other):

# 		if self.cost == other.cost:
# 			if direction == other direction:
# 				return other

# 			else:



# 		self.cost == other.cost:

# 			return compareDirections

		









class DataContainer:
	"""
	Object to hold statistical information about the search
	"""

	def __init__(self):

		self.path_to_goal = deque()
		self.cost_of_path = None
		self.nodes_expanded = None
		self.fringe_size = 0
		self.max_fringe_size = 0
		self.search_depth = 0
		self.max_search_depth = 0
		self.running_time = None
		self.max_ram_usage = None



















































"""RUNNING PROGRAM"""

argList = sys.argv



#Unique ID to determine the order in case dupliacte node was entered
global uniqueID
uniqueID = 0


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

#calcRowCol(4,3)
#i = 0
#tileNum = 4
#iRowCol = calcRowCol(i, 3)
#tRowCol = calcRowCol(tileNum, 3)
#distanceSum = abs(tRowCol[0]-iRowCol[0]) + abs(tRowCol[1]-iRowCol[1])
#print("DISTANCE::::" + str(distanceSum))


ai = Solver(board, method)
data = ai.main()

data.running_time = "{0:.8f}".format(time.time() - start_time)
data.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000






#Output to terminal
print("path_to_goal: ", list(data.path_to_goal))
print("cost_of_path: ", data.cost_of_path)
print("nodes expanded: ", data.nodes_expanded)
print("fringe_size: ", data.fringe_size)
print("max_fringe_size: ", data.max_fringe_size)
print("search_depth: ", data.search_depth)
print("max_search_depth: ", data.max_search_depth)
print("running_time: ", data.running_time)
print("max_ram_usage: ", data.max_ram_usage)
print("End of AI search. \n")


#Output to file
outputFile = open('output.txt', 'w')

outputFile.write("path_to_goal: " + str(list(data.path_to_goal)) + "\n")
outputFile.write("cost_of_path: " + str(data.cost_of_path) + "\n")
outputFile.write("nodes_expanded: " + str(data.nodes_expanded) + "\n")
outputFile.write("fringe_size: " + str(data.fringe_size) + "\n")
outputFile.write("max_fringe_size: " + str(data.max_fringe_size) + "\n")
outputFile.write("search_depth: " + str(data.search_depth) + "\n")
outputFile.write("max_search_depth: " + str(data.max_search_depth) + "\n")
outputFile.write("running_time: " + str(data.running_time) + "\n")
outputFile.write("max_ram_usage: " + str(data.max_ram_usage))

outputFile.close()








'''END ALGORITHM'''

























































"""
		A-Star Search implemented using a priority queue.
		Heuristic: Manhattan priority function- 
			the sum of the distances of the tiles from their goal positions.
		Note: Blank space is not considered an actual tile here.
		Note: state.boardConfig is of type list.
	

	
		ALGORITHM:

		G Function: The physical euclidean distance function. Calculates the 
			number of steps from the root-node to the current state.

		H Function: The Heuristic function. This calculates the 
			Euclidean(Manhattan) distance of each ith tile to the ith index.
			This is clearly imperfect information as each distance calculation 
			doesn't account for the other tiles movement. This is to say that it
			 is an optimistic Heuristic, in that the actual path cost could 
			 likely be more expensive than the summation of distances.

		g(n): cost to reach node n
		h(n): cost to get from n to the goal
		f(n) = g(n) + h(n)








		1. Spawn children nodes. Check the f function of each node and insert 
			into the priority queue.

		2. Use decreaseKey

		3. Check for duplicate states

		In the PriorityQueue order by this tuple: (distance, udlr, uniqueID)

		Note: G is provided by ManhattanDist, H is provided by depth.



		Structure:

		Use a tuple within the priority queue uniqueID within the 


		"""

































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

