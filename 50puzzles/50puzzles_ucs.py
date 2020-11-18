import threading 
import time

puzzle_input = []
puzzle_index = 0
is_times_up = False
total_seconds = 0.0

average_length_solution = 0
total_length_solution = 0
average_length_search = 0
total_length_search = 0
average_no_solution = 0
total_no_solution = 0
average_cost = 0
total_cost = 0
average_time = 0
total_time = 0

def main():
  global puzzle_index
  global puzzle_input
  global is_times_up
  global total_seconds
  puzzles_read = read_input("./50puzzles/50puzzles.txt")
  puzzle_count = puzzles_read[0]
  puzzles = puzzles_read[1]
  
  for x in range(puzzle_count):
    print("\nNOW SOLVING PUZZLE " + str(x) + "\n")
    puzzle_index = x
    puzzle_input = puzzles[x]
    is_times_up = False
    total_seconds = 0
    t1 = threading.Thread(target=timer) 
    t2 = threading.Thread(target=uniform_cost_search)

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
  
  output_analysis()

def timer():
  global is_times_up
  global total_seconds
  while not is_times_up:
    time.sleep(0.1)
    total_seconds += 0.1
    if (total_seconds >= 60):
      print("TIMES UP!")
      is_times_up = True

def uniform_cost_search():
  global puzzle_input
  global is_times_up
  open_nodes=[]
  visited_node=[]
  output_gn=[]
  path=[]
  open_nodes.append(create_puzzle_node([puzzle_input, 0, ""],None,0,0))
  visited_node.append(open_nodes[0])
  current_node=open_nodes.pop(0)
  while (not (current_node.state in [[1, 2, 3, 4, 5, 6, 7, 0], [1, 3, 5, 7, 2, 4, 6, 0]]) and not is_times_up):
    childs = create_child_nodes(current_node)
    open_nodes = check_childs_in_open(childs, open_nodes, visited_node)
    visited_node.append(open_nodes[0])
    current_node=open_nodes.pop(0)

  if not is_times_up:
    print("PUZZLE SOLVED!")
  is_times_up = True

  while(current_node.parent!=None):
    path.insert(0, current_node)
    parent_node=current_node.parent
    current_node=parent_node
    
  output(path, visited_node)

def output(path, visited_node):
  global total_seconds

  global total_length_solution
  global total_length_search
  global total_no_solution
  global total_cost
  global total_time

  # solution
  if total_seconds <= 60:
    for x in path:
      total_cost += x.edge_cost
      total_length_solution += 1
    total_time += total_seconds
  else:
    total_no_solution += 1

  # search
  if total_seconds <= 60:
    for x in visited_node:
      total_length_search += 1

def output_analysis():
  global average_length_solution
  global total_length_solution
  global average_length_search
  global total_length_search
  global average_no_solution
  global total_no_solution
  global average_cost
  global total_cost
  global average_time
  global total_time
  
  average_length_solution = total_length_solution/(50 - total_no_solution)
  average_length_search = total_length_search/(50 - total_no_solution)
  average_no_solution = total_no_solution/50
  average_cost = total_cost/(50 - total_no_solution)
  average_time = total_time/(50 - total_no_solution)
  
  f = open("./50puzzles/50puzzles_ucs_analysis.txt", "w")
  f.write("average_length_solution = " + str(average_length_solution) + "\n")
  f.write("total_length_solution = " + str(total_length_solution) + "\n")
  f.write("average_length_search = " + str(average_length_search) + "\n")
  f.write("total_length_search = " + str(total_length_search) + "\n")
  f.write("average_no_solution = " + str(average_no_solution) + "\n")
  f.write("total_no_solution = " + str(total_no_solution) + "\n")
  f.write("average_cost = " + str(average_cost) + "\n")
  f.write("total_cost = " + str(total_cost) + "\n")
  f.write("average_time = " + str(average_time) + "\n")
  f.write("total_time = " + str(total_time) + "\n")
  f.close()

def check_childs_in_open(childs, open, visited_node):
  open_states = []
  for node in open:
    open_states.append(node)
  visited_node_states = []
  for node in visited_node:
    visited_node_states.append(node.state)
  
  for child_node in childs:
    if not child_node.state in visited_node_states:
      if child_node.state in open_states:
        for node in open:
          if node.state == child_node.state and node.node_cost > child_node.node_cost:
            node = child_node
      else:
        open.append(child_node)
  open.sort(key =lambda x: x.node_cost)
  return open

class Node:
  def __init__(self, state_tile, parent, node_cost, edge_cost):
    # state of the node, aka puzzle 
    self.state = state_tile[0]
    # numbered tile that the empty tile swap with
    self.num_tile = state_tile[1]
    # parent to get the path
    self.parent = parent
    # cost to reach this node from root node
    self.node_cost = node_cost
    # path cost from parent node to this node, aka move cost
    self.edge_cost = edge_cost

def create_puzzle_node(state_tile, parent, node_cost, edge_cost):
  return Node(state_tile, parent, node_cost, edge_cost)

def create_child_nodes(current_node):
  child_nodes = []
  current_node1 = current_node
  empty_tile_index = current_node.state.index(0)
  if (empty_tile_index in [0, 3, 4, 7]):
    child_nodes.append(create_puzzle_node(move_left_or_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_vert(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(wrap_move_left_or_right(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(diagonal_move_left(current_node.state), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move_right(current_node.state), current_node, current_node.node_cost + 3, 3))
  else:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_vert(current_node.state), current_node, current_node.node_cost + 1, 1))
  return child_nodes

def move_vert(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  if new_state.index(0) in [0, 1, 2, 3]:
    num_tile = new_state[index_0 + 4]
    new_state[index_0], new_state[index_0 + 4] = new_state[index_0 + 4], new_state[index_0]
  else: 
    num_tile = new_state[index_0 - 4]
    new_state[index_0], new_state[index_0 - 4] = new_state[index_0 - 4], new_state[index_0]
  return [new_state, num_tile]

def move_left_or_right(state):
  if state.index(0) in [0, 4]:
    new_state_tile = move_right(state)
  else: 
    new_state_tile = move_left(state)
  return new_state_tile

def move_left(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 1]
  new_state[index_0], new_state[index_0 - 1] = new_state[index_0 - 1], new_state[index_0]
  return [new_state, num_tile]

def move_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  num_tile = new_state[index_0 + 1]
  new_state[index_0], new_state[index_0 + 1] = new_state[index_0 + 1], new_state[index_0]
  return [new_state, num_tile]

def wrap_move_left_or_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 1]
  if new_state.index(0) in [0, 4]:
    num_tile = new_state[index_0 + 3]
    new_state[index_0], new_state[index_0 + 3] = new_state[index_0 + 3], new_state[index_0]
  else: 
    num_tile = new_state[index_0 - 3]
    new_state[index_0], new_state[index_0 - 3] = new_state[index_0 - 3], new_state[index_0]
  return [new_state, num_tile]

def diagonal_move_left(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  if new_state.index(0) in [0, 4]:
    num_tile = new_state[abs(index_0 - 7)]
    new_state[index_0], new_state[abs(index_0 - 7)] = new_state[abs(index_0 - 7)], new_state[index_0]
  else:
    num_tile = new_state[(index_0 + 3) % 8]
    new_state[index_0], new_state[(index_0 + 3) % 8] = new_state[(index_0 + 3) % 8], new_state[index_0]
  return [new_state, num_tile]

def diagonal_move_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  if new_state.index(0) in [3, 7]:
    num_tile = new_state[abs(index_0 - 7)]
    new_state[index_0], new_state[abs(index_0 - 7)] = new_state[abs(index_0 - 7)], new_state[index_0]
  else:
    num_tile = new_state[(index_0 + 5) % 8]
    new_state[index_0], new_state[(index_0 + 5) % 8] = new_state[(index_0 + 5) % 8], new_state[index_0]
  return [new_state, num_tile]

def read_input(file):
  puzzles = []
  puzzles_count = 0
  file_open = open(file, "r")
  for line in file_open:
    str_array = line.split()
    int_array = [int(numeric_string) for numeric_string in str_array]
    puzzles.append(int_array)
    puzzles_count += 1
  file_open.close()
  return [puzzles_count, puzzles]

main()