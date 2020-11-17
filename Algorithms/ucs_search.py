

from queue import PriorityQueue

def move(puzzle, tile):
  puzzle_copy = puzzle.copy()
  empty_tile_index = puzzle.index(tile)
  puzzle_copy[puzzle_copy.index(0)] = puzzle_copy[empty_tile_index]
  puzzle_copy[empty_tile_index] = 0
  return puzzle_copy

def check_move_cost(puzzle, tile):
  tile_index = puzzle.index(tile)
  # easy way to classify the puzzle into top and bottom rows
  row_length = len(puzzle)/2
  
  # if "0" and the tile are on either top or bottom row together
  if ((((puzzle.index(0) < row_length and tile_index < row_length)
    or (puzzle.index(0) >= row_length and tile_index >= row_length))
  # and "0" and the tile is next to each other in the same row, it's a regular move
    and abs(puzzle.index(0) - tile_index) == 1)
  # OR "0" and the tile are in different row    
  # if "0" is above or below the tile, it's a regular move
    or (abs(puzzle.index(0) - tile_index) == row_length)):
    return 1
  
  # if "0" and the tile are on either top or bottom row together
  # and they are in the 2 ends of the same row
  # it's a wrapping move
  # absolute because it could be either top row or bottom row
  elif (((puzzle.index(0) < row_length and tile_index < row_length)
    or (puzzle.index(0) >= row_length and tile_index >= row_length))
    and abs(puzzle.index(0) - tile_index) == (row_length-1)):
    return 2
  
  # "0" and the tile are in different row    
  # if "0" if diagonally adjacent to the tile, it's a diagonal moves
  elif (abs(puzzle.index(0) - tile_index) == {1, 3, 5, 7, 9}):
    return 3  

def uniform_cost_search(puzzle_input):
  fringe=[]
  fringe.append(create_puzzle_node(puzzle_input,None,None,0))
  current_node=fringe.pop(0)
  path=[]
  while current_node.state != {[1, 2, 3, 4, 5, 6, 7, 0], [1, 3, 5, 7, 2, 4, 6 ,0]}:
    tree_root=create_child_nodes(current_node)
    for child_node in tree_root:
      child_node.cost+=tree_root.cost
      fringe.append(child_node)
    fringe.sort(key =lambda x: x.cost)
    current_node=fringe.pop(0)

  while(current_node.parent!=None):
    path.insert(0,current_node.operator)
    current=current.parent
  return path

def create_puzzle_node(state, parent, cost):
  return Node(state, parent, cost)

def create_child_nodes(current_node):
  child_nodes = []
  empty_tile_index = current_node.state.index(0)
  
  if (empty_tile_index == {0, 3, 4, 7}):
    child_nodes.append(create_puzzle_node(move_vert(current_node.state)), current_node, 1)
    child_nodes.append(create_puzzle_node(move_left_or_right(current_node.state)), current_node, 1)
    child_nodes.append(create_puzzle_node(wrap_move_left_or_right(current_node.state)), current_node, 2)
    child_nodes.append(create_puzzle_node(diagonal_move_left(current_node.state)), current_node, 3)
    child_nodes.append(create_puzzle_node(diagonal_move_right(current_node.state)), current_node, 3)
  else:
    child_nodes.append(create_puzzle_node(move_vert(current_node.state)), current_node, 1)
    child_nodes.append(create_puzzle_node(move_left(current_node.state)), current_node, 1)
    child_nodes.append(create_puzzle_node(move_right(current_node.state)), current_node, 2)
    child_nodes.append(create_puzzle_node(diagonal_move_left(current_node.state)), current_node, 3)
    child_nodes.append(create_puzzle_node(diagonal_move_right(current_node.state)), current_node, 3)

  return child_nodes
  
def move_vert(state):
  new_state = state[:]
  if (new_state.index(0) == {0, 1, 2, 3}):
    new_state[new_state.index(0)], new_state[new_state.index(0) + 4] = new_state[new_state.index(0) + 4], new_state[new_state.index(0)]
  else: 
    new_state[new_state.index(0)], new_state[new_state.index(0) - 4] = new_state[new_state.index(0) - 4], new_state[new_state.index(0)]

  return new_state

def move_left_or_right(state):
  new_state = state[:]
  if (new_state.index(0) == {0, 4}):
    new_state[new_state.index(0)], new_state[new_state.index(0) + 1] = new_state[new_state.index(0) + 1], new_state[new_state.index(0)]
  else: 
    new_state[new_state.index(0)], new_state[new_state.index(0) - 1] = new_state[new_state.index(0) - 1], new_state[new_state.index(0)]

  return new_state

def move_left(state):
  new_state = state[:]
  new_state[new_state.index(0)], new_state[new_state.index(0) - 1] = new_state[new_state.index(0) - 1], new_state[new_state.index(0)]

  return new_state

def move_right(state):
  new_state = state[:]
  new_state[new_state.index(0)], new_state[new_state.index(0) + 1] = new_state[new_state.index(0) + 1], new_state[new_state.index(0)]

  return new_state

def wrap_move_left_or_right(state):
  new_state = state[:]
  if (new_state.index(0) == {0, 4}):
    new_state[new_state.index(0)], new_state[new_state.index(0) + 3] = new_state[new_state.index(0) + 3], new_state[new_state.index(0)]
  else: 
    new_state[new_state.index(0)], new_state[new_state.index(0) - 3] = new_state[new_state.index(0) - 3], new_state[new_state.index(0)]

  return new_state

def diagonal_move_left(state):
  new_state = state[:]
  if (new_state.index(0) == {0, 4}):
    new_state[new_state.index(0)], new_state[abs(new_state.index(0) -7)] = new_state[abs(new_state.index(0) -7)], new_state[new_state.index(0)]
  else:
    new_state[new_state.index(0)], new_state[(new_state.index(0) + 3) // 8] = new_state[(new_state.index(0) + 3) // 8], new_state[new_state.index(0)]

  return new_state

def diagonal_move_right(state):
  new_state = state[:]
  if (new_state.index(0) == {3, 7}):
    new_state[new_state.index(0)], new_state[abs(new_state.index(0) -7)] = new_state[abs(new_state.index(0) -7)], new_state[new_state.index(0)]
  else:
    new_state[new_state.index(0)], new_state[(new_state.index(0) + 5) // 8] = new_state[(new_state.index(0) + 5) // 8], new_state[new_state.index(0)]

  return new_state

class Node:
  def __init__(self, state, parent, cost):
    # state of the node, aka puzzle 
    self.state = state
    # parent to get the path
    self.parent = parent
    # path cost of this node from root node
    self.cost = cost

def read_input(file):
  input_puzzles = []
  file_open = open(file, "r")
  for line in file_open:
    a = line.split()
    input_puzzles.append(a)
      
  return input_puzzles
