from copy import deepcopy
import signal
import random

def timeout_handler(signum, frame):
    raise TimeoutError
#based on the code provided in the lectures
def count_inversions(values):
    inv_count = 0
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            if values[j] and values[i] and values[i] > values[j]:
                inv_count += 1
    return inv_count

def is_solvable(goal, m):
    # Flatten the 2D goal into a 1D list
    values = [cell for row in goal for cell in row]

    inv_count = count_inversions(values)
    zero_pos = values.index(0)
    # Calculate the row index of the 0 value
    zero_row = zero_pos // m
    if m % 2 == 1:  # For odd width, the number of inversions must be even for it to be solvable
        return inv_count % 2 == 0
    else:
        if zero_row % 2 == 1 and inv_count % 2 == 0:
            return True
        if zero_row % 2 == 0 and inv_count % 2 == 1:
            return True
        return False
       
def manhattan_distance(state): # gives the total distance for each tile on the board
    distance = 0
    n = len(state)
    m = len(state[0])
    for i in range(n):
        for j in range(m):
            value = state[i][j]
            if value != 0:  #0 doesn't really have a manhattan distance so we can ignore
                goal_i = (value - 1) // m 
                goal_j = (value - 1) % m   
                distance += abs(i - goal_i) + abs(j - goal_j) # absolute value used in case we have a 3,2,1 situation 
                #where 1 is 2 away from its correct position, but without abs it would cause the overall distance to shrink by 2
    return distance
# Helper function to find the position of a value in the goal
def find_position(value, goal):
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            if goal[i][j] == value:
                return i, j
    return None

def is_complete(state, goal):  # Check if the current state matches the goal state
    return state == goal

def generate_goal_state(n, m):
    goal_state = [[m * i + j + 1 for j in range(m)] for i in range(n)]
    goal_state[-1][-1]= 0  # Set the last element to 0 (empty space)
    return goal_state


def extract_moves(solution_path):
    moves = []
    for i in range(1, len(solution_path)):
        prev_state = solution_path[i-1]
        current_state = solution_path[i]
        curr_zero_i, curr_zero_j = find_position(0, current_state)  
        # The tile that moved into the empty space
        moved_tile = prev_state[curr_zero_i][curr_zero_j]
        moves.append(moved_tile)
    return moves

def generate_child_nodes(current_state):
    empty_i, empty_j = find_position(0, current_state)
    possible_moves = [(empty_i - 1, empty_j), (empty_i + 1, empty_j),
                              (empty_i, empty_j - 1), (empty_i, empty_j + 1)]
                      
    return empty_i,empty_j,possible_moves

def extract_initial_state_from_input():
    # Reading n, m, and goal values
    input_values = list(map(int, input().split()))

    n, m = input_values[0], input_values[1]
    values = input_values[2:]

    # Convert flat list to 2D goal (initial state)
    initial_state = [values[i * m : i * m + m] for i in range(n)]
    return n, m, initial_state

#This is mainly used as a helper function to verify solutions produced by my algorithms in testing; it applies their output to the initial state to see if it matches the goal state
def apply_moves_to_state(initial_state, moves):
    current_state = deepcopy(initial_state)
    for move in moves:
        empty_i, empty_j = find_position(0, current_state)
        tile_i, tile_j = find_position(move, current_state)
        # Swap tile with the empty position
        current_state[empty_i][empty_j], current_state[tile_i][tile_j] = current_state[tile_i][tile_j], current_state[empty_i][empty_j]
    return current_state


# I use this function to generate a solvable state which is compatible with stacscheck verification for ease of use, as well as allowing my results to be reproducible
def random_solvable_state(n, m):
    while True:
        
        # Flatten the grid and shuffle it
        flat_grid = list(range(1, n * m)) + [0]
        random.shuffle(flat_grid)
        
        grid = [flat_grid[i * m : i * m + m] for i in range(n)]
        
        if is_solvable(grid, m):
            
           # Prepare a single list starting with n, m and followed by flattened grid elements
            #result = [n, m] + flat_grid
            
            # Print the result in the desired format
            #print(" ".join(map(str, result)))
            
            return grid


""" This section of PuzzleSolver is specifically for input validation purposes. Given more time I would have made a seperate file for this but due to time constraints I have left it here."""



def validate_dimensions(n, m):
    #makes sure n and m are integers and a reasonable size( although anything above 5 is techincally unsolvable)
    if not (isinstance(n, int) and isinstance(m, int)):
        raise ValueError("Both n and m must be integers.")
    if not (1 <= n <= 100 and 1 <= m <= 100):
        raise ValueError("Both n and m should be between 1 and 10.")

def validate_initial_state(initial_state, n, m):
    #  Extra Check if the initial state has the correct structure (2D list of size n x m)
    if not isinstance(initial_state, list) or len(initial_state) != n:
        raise ValueError("Initial state must be a list of n rows.")
    
    for row in initial_state:
        if not isinstance(row, list) or len(row) != m:
            raise ValueError(f"Each row in the initial state must have {m} columns.")

    # Check if the initial state has all expected values exactly once
    expected_values = set(range(n * m))
    actual_values = {cell for row in initial_state for cell in row}
    
    if actual_values != expected_values:
        missing_values = expected_values - actual_values
        extra_values = actual_values - expected_values
        messages = []
        
        if missing_values:
            messages.append(f"Missing values: {', '.join(map(str, missing_values))}")
        if extra_values:
            messages.append(f"Extra values: {', '.join(map(str, extra_values))}")
        
        raise ValueError(". ".join(messages))
def validate_values(values, n, m):
    if not len(values) == n * m:
        raise ValueError("Mismatch in the number of values!")
    expected_values = set(range(n * m))
    if set(values) != expected_values:
        raise ValueError("Values mismatch!")

