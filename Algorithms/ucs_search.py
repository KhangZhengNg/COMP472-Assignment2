import threading 
import time

puzzle_input = []
puzzle_index = 0
is_times_up = False
total_seconds = 0.0

def main():
  global puzzle_index
  global puzzle_input
  global is_times_up
  global total_seconds
  puzzles_read = read_input("samplePuzzles.txt")
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
  while (current_node.state != [1, 2, 3, 4, 5, 6, 7, 0] and not is_times_up):
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
  global puzzle_index
  global total_seconds
  # output to Solution File
  print("OUTPUTTING TO SOLUTION FILE NOW")
  output_source_file = open("./Output/" + str(puzzle_index) + "_ucs_solution.txt", "w")
  if total_seconds <= 60:
    total_cost = 0
    for x in path:
      total_cost += x.edge_cost
      output = (str(x.num_tile) + "_" + str(x.edge_cost) + "_" + str(x.state) + "\n").replace(" ", "").replace(",","_").replace("[", "").replace("]","")
      output_source_file.write(output)
    formatted_time = "{:.2f}".format(total_seconds)
    output_source_file.write(("\n\n"+ str(total_cost) + "_" + str(formatted_time)))
  else:
    output_source_file.write("NO SOLUTION")
  output_source_file.close()
  # output to Search File
  print("OUTPUTTING TO SOLUTION FILE NOW")
  output_search_file = open("./Output/" + str(puzzle_index) + "_ucs_search.txt", "w")
  if total_seconds <= 60:
    for x in visited_node:
      output = ("0_" + str(x.node_cost) + "_0_" + str(x.state) + "\n").replace(" ", "").replace(",","_").replace("[", "").replace("]","")
      output_search_file.write(output)
  else:
    output_search_file.write("NO SOLUTION")
  output_search_file.close()

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
    child_nodes.append(create_puzzle_node(diagonal_move_left(current_node.state), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move_right(current_node.state), current_node, current_node.node_cost + 3, 3))
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
  if (new_state.index(0) == {0, 4}):
    num_tile = new_state[abs(index_0 - 7)]
    new_state[index_0], new_state[abs(index_0 - 7)] = new_state[abs(index_0 - 7)], new_state[index_0]
  else:
    num_tile = new_state[(index_0 + 3) % 8]
    new_state[index_0], new_state[(index_0 + 3) % 8] = new_state[(index_0 + 3) % 8], new_state[index_0]
  return [new_state, num_tile]

def diagonal_move_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  if new_state.index(0) == [3, 7]:
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
  return [puzzles_count, puzzles]

main()