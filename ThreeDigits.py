import sys 
import collections 
from heapq import *

def generate_children(parent, forbidden, last_changed):
	'''Generates children according to constraints.'''
	children = []
	if last_changed != "first": 
		if parent[0] != '0' and int(parent) - 100 not in forbidden: 
			child = str(int(parent) - 100)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)
			
		if parent[0] != '9' and int(parent) + 100 not in forbidden: 
			child = str(int(parent) + 100)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)
	
	if last_changed != "second": 
		if parent[1] != '0' and int(parent) - 10 not in forbidden:
			child = str(int(parent) - 10)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)

		if parent[1] != '9' and int(parent) + 10 not in forbidden:
			child = str(int(parent) + 10)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)
	
	if last_changed != "third": 
		if parent[2] != '0' and int(parent) - 1 not in forbidden:
			child = str(int(parent) - 1)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)

		if parent[2] != '9' and int(parent) + 1 not in forbidden:
			child = str(int(parent) + 1)
			if len(child) == 1:
				child = '00' + child
			if len(child) == 2: 
				child = '0' + child
			children.append(child)
	return children

def search_bfs(start, goal, forbidden): 
	'''Search for goal using BFS algorithm.'''
	expanded = []  #keeps track of nodes already visited. 
	came_from = {} #for backtracing the path. 
	fringe = []
	fringe.append([start])
	grandparent = None 
	continue_loop = False 
	path = []
	
	while fringe: 
		path = fringe.pop(0)
		parent = path[-1]
		
		last_changed = ''
		
		#get grandparent 
		if parent in came_from: 
			grandparent = came_from[parent].pop(0)
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
			
		children = generate_children(parent, forbidden, last_changed) #generate children
		#print(parent, children)
		
		for node in expanded: 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children): #check whether there are same digits. 
				continue_loop = True 
				break
				
		if continue_loop == True: 
			continue_loop = False 
			continue 
		
		expanded.append((parent,children)) #keep track of expanded nodes 
		
		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path
		
		for child in children: 
			new_path = list(path)
			new_path.append(child)
			fringe.append(new_path)
				
			if child not in came_from: #key does not exist 
				came_from[child] = []
			came_from[child].append(parent)
	
	expanded = [i[0] for i in expanded]
	return expanded, path
				
def search_dfs(start, goal, forbidden):
	'''Search for goal using DFS algorithm.'''
	expanded = []
	fringe = [] 
	fringe.append([start])
	came_from = {}
	grandparent = None 
	continue_loop = False 
	path = []
	
	while fringe: 
		path = fringe.pop()
		parent = path[-1]
		
		last_changed = ''
		
		#get grandparent 
		if parent in came_from: 
			grandparent = came_from[parent].pop() #works?
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
		
		
		children = generate_children(parent, forbidden, last_changed) #generate children
		children.reverse()
		
		for node in expanded: 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children): #check whether there are same digits. 
				continue_loop = True 
				break
				
		if continue_loop == True: 
			continue_loop = False 
			continue 
		
		expanded.append((parent,children)) #keep track of expanded nodes 
		
		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path
		
		#print(parent, children)
		
		for child in children: 
			new_path = list(path)
			new_path.append(child)
			fringe.append(new_path)
			
			if child not in came_from: #key does not exist 
				came_from[child] = []
			came_from[child].append(parent)

	expanded = [i[0] for i in expanded]
	return expanded, path

def calc_heuristic(number_a, number_b):
	'''Calculates heuristic for greedy, A* and hill climbing algorithm.'''
	first_sum = abs(int(number_a[0]) - int(number_b[0]))
	second_sum = abs(int(number_a[1]) - int(number_b[1]))
	third_sum = abs(int(number_a[2]) - int(number_b[2]))
	
	heuristic = first_sum + second_sum + third_sum
	return heuristic 
	
def search_Astar(start, goal, forbidden):
	'''Search for goal using A star algorithm.'''
	expanded = [] #closed set 
	came_from = {} 
	gscore = {start : 0} #cost of going from start to start
	fscore = {start : calc_heuristic(start, goal)}
	heap = [] #acts like a priority queue, represents the fringe 
	heappush(heap, (fscore[start], 0, [start])) 
	
	continue_loop = False 
	grandparent = None
	path = []
	
	count = -1
	
	while heap: 
		path = heappop(heap)[2]
		parent = path[-1]
		
		last_changed = ''
		
		if parent in came_from: 
			grandparent = came_from[parent].pop(0)
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
				
		children = generate_children(parent, forbidden, last_changed)
		
		for node in expanded: 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children): #check whether there are same digits. 
				continue_loop = True 
				break
				
		if continue_loop == True: 
			continue_loop = False 
			continue 
		
		expanded.append((parent,children)) #keep track of expanded nodes 
		
		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path
		for child in children: 
			#if child in expanded: 
				#continue 
				
			tentative_gscore = gscore[parent] + 1
			#print(tentative_gscore)
			#if tentative_gscore >= gscore[child]: 
				#continue #this is not a better path 
			
			#if child not in expanded:
			#This path is the best until now. Record it!
			if child not in came_from:
				came_from[child] = []
					
			new_path = list(path)
			new_path.append(child)
				
			came_from[child].append(parent)
			gscore[child] = tentative_gscore
			fscore[child] = gscore[child] + calc_heuristic(child, goal)
			heappush(heap, (fscore[child], count, new_path))
			count = count - 1
			
	expanded = [i[0] for i in expanded]
	return expanded, path

def search_greedy(start, goal, forbidden):
	'''Search for goal using greedy algorithm search.'''
	expanded = [] #closed set 
	came_from = {} 
	hscore = {start : calc_heuristic(start, goal)}
	heap = [] #acts like a priority queue, represents the fringe 
	heappush(heap, (hscore[start], 0, [start])) 
	
	grandparent = None
	continue_loop = False 
	path = []
	
	count = -1
	
	while heap: 
		path = heappop(heap)[2]
		parent = path[-1]
	
		last_changed = ''
		
		if parent in came_from: 
			grandparent = came_from[parent].pop(0)
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
				
		children = generate_children(parent, forbidden, last_changed)
		
		for node in expanded: 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children): #check whether there are same digits. 
				continue_loop = True 
				break
				
		if continue_loop == True: 
			continue_loop = False 
			continue 
		
		expanded.append((parent,children)) #keep track of expanded nodes 
		
		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path
		for child in children:
			if child not in came_from:
				came_from[child] = []
					
			new_path = list(path)
			new_path.append(child)
				
			came_from[child].append(parent)
			hscore[child] = calc_heuristic(child, goal)
			heappush(heap, (hscore[child], count, new_path))
			count = count - 1
			
	expanded = [i[0] for i in expanded]
	return expanded, path

def search_hill(start, goal, forbidden): 
	'''Search for goal using hill-climbing algorithm.'''
	expanded = [] #closed set 
	came_from = {} 
	fringe = [] 
	fringe.append([start])
	grandparent = None
	continue_loop = False 
	path = []
	
	while fringe: 
		path = fringe.pop(0)
		parent = path[-1]
		
		last_changed = ''
		
		if parent in came_from: 
			grandparent = came_from[parent].pop(0)
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
			
		children = generate_children(parent, forbidden, last_changed) #generate children
		
		for node in expanded: 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children): #check whether there are same digits. 
				continue_loop = True 
				break
				
		if continue_loop == True: 
			continue_loop = False 
			continue 
		
		expanded.append((parent,children)) #keep track of expanded nodes 
		
		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path
		
		best_eval = float("inf")
		best_child = ''
		
		for child in children: 
			eval = calc_heuristic(child, goal)
			if eval <= best_eval: 
				best_child = child 
				best_eval = eval 
				
		prev_eval = calc_heuristic(parent, goal) 
		
		if prev_eval <= best_eval: 
			expanded = [i[0] for i in expanded]
			return expanded, path
		
		new_path = list(path)
		new_path.append(best_child)
		fringe.append(new_path)
		
		if best_child not in came_from: #key does not exist 
			came_from[best_child] = []
		came_from[best_child].append(parent)
	
	expanded = [i[0] for i in expanded]
	return expanded, path

def search_ids(start, goal, forbidden, max_depth): 
	'''Search goal using iterating deepening search algorithm.'''
	expanded = []
	fringe = [] 
	fringe.append([(start, 0)])
	came_from = {}
	grandparent = None 
	curr_depth = 1
	path = None
	continue_loop = False
	
	while fringe: 
		path = fringe.pop()
		parent = path[-1][0]
		parent_depth = path[-1][1]
		curr_depth = parent_depth + 1
		
		last_changed = ''
		
		#get grandparent 
		if parent in came_from: 
			grandparent = came_from[parent].pop() #works?
		
		if grandparent != None: 
			if int(grandparent) + 100 == int(parent) or int(grandparent) - 100 == int(parent): 
				last_changed = "first"
			if int(grandparent) + 10 == int(parent) or int(grandparent) - 10 == int(parent): 
				last_changed = "second"
			if int(grandparent) + 1 == int(parent) or int(grandparent) - 1 == int(parent): 
				last_changed = "third"
		
		children = generate_children(parent, forbidden, last_changed) #generate children
		children.reverse()

		for node in expanded: #check to prevent cycles. 
			if sorted(node[0]) == sorted(parent) and sorted(node[1]) == sorted(children):
				continue_loop = True 
				break

		if continue_loop == True: 
			continue_loop = False 
			continue 
			
		expanded.append((parent,children)) #keep track of expanded nodes 

		if parent == goal or len(expanded) == 1000: #desination found. Return list of expanded nodes. 
			expanded = [i[0] for i in expanded]
			return expanded, path, curr_depth 
		
		if parent_depth < max_depth: 
			
			for child in children: 
				new_path = list(path)
				new_path.append((child, curr_depth))
				fringe.append(new_path)

				if child not in came_from: #key does not exist 
					came_from[child] = []
				came_from[child].append(parent)
	#goal was never discovered case 
	expanded = [i[0] for i in expanded]
	return expanded, path, curr_depth
	
	
def display_answer(expanded_nodes, path, goal): 
	'''Print out expanded nodes and solution path.'''
	first_line = ''
	if goal not in path: #no solution case. 
		first_line = 'No solution found.'
	else:
		for i in range(0, len(path)): 
			if i == len(path) - 1:
				first_line += path[i]
			else: 
				first_line += path[i] + ','
	print(first_line)
		
	second_line = '' #print expanded nodes. 
	for i in range(0, len(expanded_nodes)):
		if i == len(expanded_nodes) - 1:
			second_line += expanded_nodes[i]
		else: 
			second_line += expanded_nodes[i] + ','
	print(second_line)
	
def read_input(file_name): 
	'''Read text file and retrieve input.'''
	with open(file_name) as f:
		lines = f.read().splitlines()
		
	if len(lines) == 3: #case where there are forbidden numbers.
		forbidden_numbers = lines[2].split(",")
		lines[2] = forbidden_numbers
	else: 
		lines.append([]) #case where there are no forbidden numbers - append empty list.
	
	return lines 

def main(): 
	
	search_method = sys.argv[1]
	
	file_name = sys.argv[2]
	input = read_input(file_name) 
	start = input[0]
	goal = input[1]
	
	forbidden = input[2] #a list.
	forbidden = [int(i) for i in forbidden]
	
	#search with bfs
	if search_method == "B": 
		expanded_bfs, path_bfs = search_bfs(start, goal, forbidden)
		display_answer(expanded_bfs, path_bfs, goal)
	
	#search with dfs
	if search_method == "D": 
		expanded_dfs, path_dfs = search_dfs(start, goal, forbidden)
		display_answer(expanded_dfs, path_dfs, goal)
	
	#search with Astar
	if search_method == "A": 
		expanded_Astar, path_Astar = search_Astar(start, goal, forbidden)
		display_answer(expanded_Astar, path_Astar, goal)

	#search with greedy
	if search_method == "G": 
		expanded_greedy, path_greedy = search_greedy(start, goal, forbidden)
		display_answer(expanded_greedy, path_greedy, goal)
	
	#search with hill-climbing
	if search_method == "H": 
		expanded_hill, path_hill = search_hill(start, goal, forbidden)
		display_answer(expanded_hill, path_hill, goal)
	
	#search with IDS 
	if search_method == "I": 
		depth = 0
		expanded_ids_all = []
		path_ids_all = []
		while(True): 
			expanded_ids, path_ids, returned_depth = search_ids(start, goal, forbidden, depth)
			expanded_ids_all += expanded_ids 
			depth += 1 
			if path_ids[-1][0] == goal or len(expanded_ids_all) >= 1000: 
				break
		if len(expanded_ids_all) >= 1000: #stop at 1000 expanded nodes. 
			expanded_ids_all = expanded_ids_all[0:1000]
		for i in range(0, len(path_ids)): 
			path_ids_all.append(path_ids[i][0])
		display_answer(expanded_ids_all, path_ids_all, goal)

if __name__ == "__main__": 
	main() 

