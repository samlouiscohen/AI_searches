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
		else:
			return self.idaSearch(initState)







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
				

				data.cost_of_path = self.getPath(
					state, data.path_to_goal)

				#Account a edge case of max search depth
				if data.cost_of_path == 1:
					data.max_search_depth = 1


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

		#Stack with deque implementation (append left, pop left)
		frontier = deque()
		frontier_set = set()

		frontier.appendleft(initState)
		frontier_set.add(str(initState.boardConfig))

		explored = set()


		while len(frontier) != 0:

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)


			state = frontier.popleft()
			frontier_set.remove(str(state.boardConfig))

			#Add the current state to the explored set
			explored.add(str(state.boardConfig))

			#Test if current state is the goal state
			if self.goalTest(state.boardConfig):
				self.formatPrint(initState)
				
				#Recursively find parent path with getPath method
				#data.cost_of_path = self.getPath(state, initPathCost, data.path_to_goal)
				data.cost_of_path = self.getPath(state, data.path_to_goal)

				#Account a edge case of max search depth
				if data.cost_of_path == 1:
					data.max_search_depth = 1
				
				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)

				#To be an expanded node, you first have to be explored. Only 
				# the goal-state node will have returned before being explored.
				data.nodes_expanded = len(explored) - 1

				return data

			print("stateDepth:" + str(state.depth) + " | maxdepth: " + str(data.max_search_depth))



			#If current node is not in goal state, expand it
			childStates = self.spawnChildrenStates(state)

			if state.depth > data.max_search_depth:
				data.max_search_depth  = state.depth

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





	def astSearch(self, initState):
		"""
		A-Star Search implemented using a priority queue
		Heuristic f(n) = g(n) + h(n): Manhattan priority function- 
			the sum of the distances of the tiles from their goal positions
		Note: Don't count the blank space in this summation

		g(n): cost to reach node n
		h(n): cost to get from n to the goal

		The priorityQueue stores 3-tuples: (cost, UDLR, node)
		The priorityQueue is implemented w/ a list but is formatted w/ "heapq"
		"""

		data = DataContainer()

		#Initialize the frontier as a heap
		frontier = []
		heapq.heappush(frontier, (0, 0, initState))

		#Initialize the explored & frontier sets: O(1) access & hold strings
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


			#Create the children or "neighbors" of the current node
			childStates = self.spawnChildrenStates(nodeTuple[2])


			#Create a tuple for each child to insert into the pQueue
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


				#If board is not in explored nor frontier, just add to frontier
				if str(child.boardConfig) not in explored and str(child.boardConfig) not in frontier_set:
						
					heapq.heappush(frontier, childNodeTuple)
					frontier_set.add(str(child.boardConfig))

				#If a duplicate boardConfig is in frontier, determine which of
				# the two is cheaper and keep that one
				elif str(child.boardConfig) in frontier_set:

					self.decreaseKey(frontier, childNodeTuple)



	def decreaseKey(self, frontier, childTuple):
		"""Since we're in decreaseKey method, it means that the boardConfig 
		was already in the frontier. So now we have to see if the new pathCost
		to the same config is cheaper. If so replace the old one."""

		for oldTupleNode in frontier:

			#Find the node that contains the board that we now have a duplicate of
			if oldTupleNode[2].boardConfig == childTuple[2].boardConfig:

				#Compare the costs first by heuristic, then action, then age
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



	def idaSearch(self, initState):
		
		data = DataContainer()
		print("start program")

		#A limit to stop the search tree from continuing past a certain *cost*
		costLimit = self.totalCostFunction(initState)
		print("\n\n\n\n\n\n\n\n\n\n")
		print("costLimit = ", costLimit)

		#Initially set this to inifinity so we're garunteed to get smaller value
		cheapestNodeCostOverLimit = math.inf

		#Frontier as a stack, implemented with a dequeue (push/pop on left)
		frontier = deque()

		#Initialize the frontier with the "root" of the search tree
		frontier.appendleft(initState)


		while len(frontier) != 0:

		#	print("Cost limit: " + str(costLimit))

			#Update max fringe size
			if len(frontier) > data.max_fringe_size:
				data.max_fringe_size = len(frontier)

			stateNode = frontier.popleft()

			#print(stateNode.boardConfig)
			#print(len(frontier))

			#Check if the current stateNode is the GoalState
			if self.goalTest(stateNode.boardConfig):

				data.cost_of_path = self.getPath(stateNode, data.path_to_goal)

				#Account for an edge case of max search depth
				if data.cost_of_path == 1:
					data.max_search_depth = 1
				
				#Set search_depth to pathCost as cost is number of edges (deep)
				data.search_depth = data.cost_of_path

				#Only set the current fringe_size when we found the goal state
				data.fringe_size = len(frontier)

				#To be an expanded node, you first have to be explored. Only 
				# the goal-state node will have returned before being explored.
				#data.nodes_expanded = len(explored) - 1

				return data
			data.nodes_expanded += 1
			#Update the max search depth
			if stateNode.depth + 1 > data.max_search_depth:
				data.max_search_depth  = stateNode.depth + 1


			#If current node is not in goal state, expand it
			childStates = self.spawnChildrenStates(stateNode)

			#Create a set of parent nodes for the current node to check against
			#This "explored" set prevents us from going down a branch that
			# contains a "loop" or is inefficient by doing work only to get 
			# back to a previous configuration
			#**So we dont care about multiple of a state in the frontier???????????????
			explored = set()
			
			parent = stateNode
			while parent != None:
				explored.add(str(parent.boardConfig))
				parent = parent.parent


			#Append any of the currentNode's children that lead to a new state
			for child in reversed(childStates):

				if str(child.boardConfig) not in explored:
					child.cost = self.totalCostFunction(child)
					#print("childCost = ", child.cost)

					if child.cost <= costLimit:
						frontier.appendleft(child)
					#	print("child added -->", child.boardConfig)
					#ChildCost > limit, see if its over by the smallest # yet
					elif child.cost < cheapestNodeCostOverLimit:
						cheapestNodeCostOverLimit = child.cost

			#If frontier is now empty & still no goalState, reset tree search w/ a greater limit
			if len(frontier) == 0:
				print("reset")
				frontier = deque()

				#Start over by putting the root back in the stack
				frontier.appendleft(initState)

				#Set new limit: 
				# shallowest we can go and still know we will reach new state(s) 
				costLimit = cheapestNodeCostOverLimit
				print("costLimit = ", costLimit)

				#Reset the cheapest"over"cost so all nodes can update it ??????????????????
				cheapestNodeCostOverLimit = math.inf














				

















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

		for i in range(0, len(boardConfig)):

			tileNum = boardConfig[i]

			#Dont include the 0 tile
			if tileNum == 0:
				continue

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
		col = (num) % (n)

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





class DataContainer:
	"""
	Object to hold statistical information about the search
	"""

	def __init__(self):

		self.path_to_goal = deque()
		self.cost_of_path = 0
		self.nodes_expanded = 0
		self.fringe_size = 0
		self.max_fringe_size = 0
		self.search_depth = 0
		self.max_search_depth = 0
		self.running_time = 0
		self.max_ram_usage = 0




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






























# def idaSearch(self, initState):
# 		"""
# 		IDA* search. This takes advantage of iterative deepening to reduce
# 		 space complexity and consequently time complexity.
# 		 Note: IDA* uses f-cost rather than depth as the cutoff value 
# 		"""

# 		data = DataContainer()

# 		minimum = math.inf
# 		#Set initial cost limit to the cost of the ..........
# 		cost_limit = self.totalCostFunction(initState)

# 		frontier = deque()

# 		#Run dfs until find solution
# 		while(1):

# 			#Frontier as a stack with deque implementation (append left, pop left)
			
# 			frontier_set = set()

# 			frontier.appendleft(initState)
# 			#frontier_set.add(str(initState.boardConfig))

# 			#explored = set()


# 			#Update the max "depth" or cost the dfs should reach
# 			cost_limit +=1

# 			print(cost_limit)


# 			#Run dfs
# 			while len(frontier) != 0:

# 				#Update max fringe size
# 				if len(frontier) > data.max_fringe_size:
# 					data.max_fringe_size = len(frontier)

# 				state = frontier.popleft()
# 				#frontier_set.remove(str(state.boardConfig))

# 				#Add the current state to the explored set
# 				#explored.add(str(state.boardConfig))

# 				#Test if current state is the goal state
# 				if self.goalTest(state.boardConfig):
				
# 					data.cost_of_path = self.getPath(state, data.path_to_goal)

# 					#Account for an edge case of max search depth
# 					if data.cost_of_path == 1:
# 						data.max_search_depth = 1
					
# 					#Set search_depth to pathCost as cost is number of edges (deep)
# 					data.search_depth = data.cost_of_path

# 					#Only set the current fringe_size when we found the goal state
# 					data.fringe_size = len(frontier)

# 					#To be an expanded node, you first have to be explored. Only 
# 					# the goal-state node will have returned before being explored.
# 					data.nodes_expanded = len(explored) - 1

# 					return data


# 				#If current node is not in goal state, expand it
# 				childStates = self.spawnChildrenStates(state)


# 				if state.depth + 1 > data.max_search_depth:
# 					data.max_search_depth  = state.depth + 1

				



# 				#Keep track of the min element in the stack and that
# 				# min of the thing that didnt work is the new limit
# 				#The minimum of the heuristics that were not expected and that is the new limit
				

# 					explored = set()
# 					parentNode = child.parent
# 					while parentNode != None:
# 						explored.add(str(parentNode.boardConfig))
# 						parentNode = parentNode.parent
				
# 				for child in reversed(childStates):
					


# 					child.cost = self.totalCostFunction(child)

# 					if str(child.boardConfig) not in explored:# and str(child.boardConfig) not in frontier_set:
# 						if child.cost <= cost_limit:
# 							frontier.appendleft(child)
# 							#frontier_set.add(str(child.boardConfig))

# 			#else:
# 			#newcost = min(cost_limit, child.cost)
# 			#cost_limit = newcost





	# def idaSearch(self, initState):
	# 	"""
	# 	IDA* search. This takes advantage of iterative deepening to reduce
	# 	 space complexity and consequently time complexity.
	# 	 Note: IDA* uses f-cost rather than depth as the cutoff value 
	# 	"""

	# 	data = DataContainer()

	# 	cost_limit = self.totalCostFunction(initState)

	# 	frontier = deque()

	# 	#Run dfs until find solution
	# 	while(1):

	# 		#Frontier as a stack with deque implementation (append left, pop left)
			
	# 		frontier_set = set()

	# 		frontier.appendleft(initState)
	# 		#frontier_set.add(str(initState.boardConfig))

	# 		#explored = set()


	# 		#Update the max "depth" or cost the dfs should reach
	# 		cost_limit +=1

	# 		print(cost_limit)


	# 		#Run dfs
	# 		while len(frontier) != 0:

	# 			#Update max fringe size
	# 			if len(frontier) > data.max_fringe_size:
	# 				data.max_fringe_size = len(frontier)

	# 			state = frontier.popleft()
	# 			#frontier_set.remove(str(state.boardConfig))

	# 			#Add the current state to the explored set
	# 			#explored.add(str(state.boardConfig))

	# 			#Test if current state is the goal state
	# 			if self.goalTest(state.boardConfig):
				
	# 				data.cost_of_path = self.getPath(state, data.path_to_goal)

	# 				#Account for an edge case of max search depth
	# 				if data.cost_of_path == 1:
	# 					data.max_search_depth = 1
					
	# 				#Set search_depth to pathCost as cost is number of edges (deep)
	# 				data.search_depth = data.cost_of_path

	# 				#Only set the current fringe_size when we found the goal state
	# 				data.fringe_size = len(frontier)

	# 				#To be an expanded node, you first have to be explored. Only 
	# 				# the goal-state node will have returned before being explored.
	# 				data.nodes_expanded = len(explored) - 1

	# 				return data


	# 			#If current node is not in goal state, expand it
	# 			childStates = self.spawnChildrenStates(state)


	# 			if state.depth + 1 > data.max_search_depth:
	# 				data.max_search_depth  = state.depth + 1

				



	# 			#Keep track of the min element in the stack and that
	# 			# min of the thing that didnt work is the new limit
	# 			#The minimum of the heuristics that were not expected and that is the new limit
				

	# 				explored = set()
	# 				parentNode = child.parent
	# 				while parentNode != None:
	# 					explored.add(str(parentNode.boardConfig))
	# 					parentNode = parentNode.parent

	# 			for child in reversed(childStates):
					


	# 				child.cost = self.totalCostFunction(child)

	# 				if str(child.boardConfig) not in explored:# and str(child.boardConfig) not in frontier_set:
	# 					if child.cost <= cost_limit:
	# 						frontier.appendleft(child)
	# 						#frontier_set.add(str(child.boardConfig))

	# 		#else:
	# 		#newcost = min(cost_limit, child.cost)
	# 		#cost_limit = newcost









					# elif str(child.boardConfig) in frontier_set:
					# 	if child.cost < cost_limit:

					# 		for node in frontier:
					# 			if str(node.boardConfig) == str(child.boardConfig):

					# 				if child.cost < node.cost:
					# 					node = child






