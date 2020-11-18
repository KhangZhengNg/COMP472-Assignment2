import threading 
import time
import random

puzzle_input = []
puzzle_index = 0
is_puzzle_solved = False
goal_states = [[1, 2, 3, 4, 5, 6 , 7, 8, 9, 10, 11, 0], [1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 0]]
new_puzzles = []
new_puzzle = 0

average_length_solution = 0
total_length_solution = 0
average_length_search = 0
total_length_search = 0
average_cost = 0
total_cost = 0
average_time = 0
total_time = 0

def main():
  global puzzle_index
  global new_puzzles
  global new_puzzle
  # generate_2x4_puzzle() to generate random puzzle
  new_puzzles = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 11],
                 [1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 8],
                 [1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 11, 7],
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11]]
  
  # change the value in range()
  for x in range(4):
    puzzle_index = x
    new_puzzle = new_puzzles[x]
    print("\nNOW SOLVING PUZZLE " + str(new_puzzle))
    t1 = threading.Thread(target=stopwatch) 
    t2 = threading.Thread(target=uniform_cost_search)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
  
  output_analysis()

def stopwatch():
  global is_puzzle_solved
  global total_time
  while not is_puzzle_solved:
    time.sleep(0.1)
    total_time += 0.1

def uniform_cost_search():
  global new_puzzle
  global is_puzzle_solved
  open_nodes=[]
  visited_node=[]
  output_gn=[]
  path=[]
  open_nodes.append(create_puzzle_node([new_puzzle, 0, ""],None,0,0))
  visited_node.append(open_nodes[0])
  current_node=open_nodes.pop(0)
  while (not (current_node.state in goal_states)):
    childs = create_child_nodes(current_node)
    open_nodes = check_childs_in_open(childs, open_nodes, visited_node)
    visited_node.append(open_nodes[0])
    current_node=open_nodes.pop(0)

  print("PUZZLE SOLVED!")
  is_puzzle_solved = True

  while(current_node.parent!=None):
    path.insert(0, current_node)
    parent_node=current_node.parent
    current_node=parent_node
    
  output(path, visited_node)

def output(path, visited_node):
  global total_time
  global new_puzzle
  
  global total_length_solution
  global total_length_search
  global total_cost
  global total_time
  
  # output to Solution File
  global puzzle_index
  print("OUTPUTTING TO SOLUTION FILE NOW")
  output_solution_file = open("./ScaledUpPuzzle/" + str(puzzle_index) + "_scaled_up_3x4_puzzle_ucs_solution.txt", "w")
  output_solution_file.write("Puzzle = " + str(new_puzzle) + "\n")
  for x in path:
    total_cost += x.edge_cost
    total_length_solution += 1
    output = (str(x.num_tile) + "_" + str(x.edge_cost) + "_" + str(x.state) + "\n").replace(" ", "").replace(",","_").replace("[", "").replace("]","")
    output_solution_file.write(output)
  formatted_time = "{:.2f}".format(total_time)
  output_solution_file.write(("\n\n"+ str(total_cost) + "_" + str(formatted_time)))
  output_solution_file.close()
  # output to Search File
  print("OUTPUTTING TO SOLUTION FILE NOW")
  output_search_file = open("./ScaledUpPuzzle/" + str(puzzle_index) + "_scaled_up_3x4_puzzle_ucs_search.txt", "w")
  output_search_file.write("Puzzle = " + str(new_puzzle) + "\n")
  for x in visited_node:
    total_length_search += 1
    output = ("0_" + str(x.node_cost) + "_0_" + str(x.state) + "\n").replace(" ", "").replace(",","_").replace("[", "").replace("]","")
    output_search_file.write(output)
  output_search_file.close()
  
def output_analysis():
  global average_length_solution
  global total_length_solution
  global average_length_search
  global total_length_search
  global average_cost
  global total_cost
  global average_time
  global total_time
  
  average_length_solution = total_length_solution/5
  average_length_search = total_length_search/5
  average_cost = total_cost/5
  average_time = total_time/5
  
  f = open("./ScaledUpPuzzle/" + str(puzzle_index) + "_scaled_up_3x4_puzzle_ucs_analysis.txt", "w")
  f.write("average_length_solution = " + str(average_length_solution) + "\n")
  f.write("total_length_solution = " + str(total_length_solution) + "\n")
  f.write("average_length_search = " + str(average_length_search) + "\n")
  f.write("total_length_search = " + str(total_length_search) + "\n")
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
  
  if empty_tile_index == 0:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(wrap_move_up(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(wrap_move_left(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 0, 9), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 0, 11), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 0, 7), current_node, current_node.node_cost + 3, 3))
  elif empty_tile_index in [1, 2]:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
  elif empty_tile_index == 3:
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(wrap_move_right(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(wrap_move_up(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 3, 8), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 3, 4), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 3, 10), current_node, current_node.node_cost + 3, 3))
  elif empty_tile_index == 4:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
  elif empty_tile_index in [5, 6]:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
  elif empty_tile_index == 7:
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_down(current_node.state), current_node, current_node.node_cost + 1, 1))
  elif empty_tile_index == 8:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(wrap_move_left(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(wrap_move_down(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 8, 1), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 8, 7), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 8, 3), current_node, current_node.node_cost + 3, 3))
  elif empty_tile_index in [9, 10]:
    child_nodes.append(create_puzzle_node(move_right(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
  elif empty_tile_index == 11:
    child_nodes.append(create_puzzle_node(move_up(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(move_left(current_node.state), current_node, current_node.node_cost + 1, 1))
    child_nodes.append(create_puzzle_node(wrap_move_right(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(wrap_move_down(current_node.state), current_node, current_node.node_cost + 2, 2))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 11, 4), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 11, 0), current_node, current_node.node_cost + 3, 3))
    child_nodes.append(create_puzzle_node(diagonal_move(current_node.state, 11, 2), current_node, current_node.node_cost + 3, 3))
  return child_nodes

def diagonal_move(state, index1, index2):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - index1 + index2]
  new_state[index_0], new_state[index_0 - index1 + index2] = new_state[index_0 - index1 + index2], new_state[index_0]
  return [new_state, num_tile]

def wrap_move_down(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 8]
  new_state[index_0], new_state[index_0 - 8] = new_state[index_0 - 8], new_state[index_0]
  return [new_state, num_tile]

def wrap_move_left(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 + 3]
  new_state[index_0], new_state[index_0 + 3] = new_state[index_0 + 3], new_state[index_0]
  return [new_state, num_tile]

def wrap_move_up(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 + 8]
  new_state[index_0], new_state[index_0 + 8] = new_state[index_0 + 8], new_state[index_0]
  return [new_state, num_tile]

def wrap_move_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 3]
  new_state[index_0], new_state[index_0 - 3] = new_state[index_0 - 3], new_state[index_0]
  return [new_state, num_tile]

def move_down(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 + 4]
  new_state[index_0], new_state[index_0 + 4] = new_state[index_0 + 4], new_state[index_0]
  return [new_state, num_tile]

def move_left(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 1]
  new_state[index_0], new_state[index_0 - 1] = new_state[index_0 - 1], new_state[index_0]
  return [new_state, num_tile]

def move_up(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  empty_tile = new_state[index_0]
  num_tile = new_state[index_0 - 4]
  new_state[index_0], new_state[index_0 - 4] = new_state[index_0 - 4], new_state[index_0]
  return [new_state, num_tile]

def move_right(state):
  new_state = state[:]
  index_0 = new_state.index(0)
  num_tile = new_state[index_0 + 1]
  new_state[index_0], new_state[index_0 + 1] = new_state[index_0 + 1], new_state[index_0]
  return [new_state, num_tile]

def generate_2x4_puzzle():
  global new_puzzles
  new_puzzles = []
  
  l = list(range(12))

  # change the value of 1 in range(1) in order to generate # puzzles
  for x in range(1):
    global goal_states
    lr = random.sample(l, len(l))
    while (((lr in new_puzzles)) and (lr in goal_states)):
      lr = random.sample(l, len(l))
    new_puzzles.append(lr)
  

# main
main()