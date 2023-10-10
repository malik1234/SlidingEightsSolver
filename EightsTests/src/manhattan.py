
from queue import PriorityQueue
import signal
from PuzzleSolver import *

def timeout_handler(signum, frame):
    raise TimeoutError

def manhattan_search(initial_state, n, m):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # Set a 60 second timer
    try:  
        # Calculate the goal state based on dimensions
        solState = generate_goal_state(n, m)
        #  allows you tostore states with their Manhattan distances as priorities
        priority_queue = PriorityQueue()
        # Create a set to keep track of visited states
        visitedStates = set()
        # Initialize the priority queue with the initial state and its Manhattan distance
        initial_manhattan = manhattan_distance(initial_state)
        priority_queue.put((initial_manhattan, [initial_state]))

        while not priority_queue.empty():
            # Get the state with the lowest Manhattan distance
            _, current_path = priority_queue.get()
            current_state = current_path[-1]
            # Check if the current state is the goal state
            if is_complete(current_state, solState):
                return 1, extract_moves(current_path)
            # Add the current state to the visited set
            visitedStates.add(tuple(map(tuple, current_state)))
            # Generate possible next states by moving the empty space
            empty_i, empty_j, possible_moves = generate_child_nodes(current_state)
            for move_i, move_j in possible_moves:
                if 0 <= move_i < len(current_state) and 0 <= move_j < len(current_state[0]):
                    # Create a deep  copy of the current state
                    next_state = [list(row) for row in current_state]
                    # Swap the empty space and the tile to perform the move
                    next_state[empty_i][empty_j], next_state[move_i][move_j] = next_state[move_i][move_j], next_state[empty_i][empty_j]
                    # Check if the next state has been visited
                    if tuple(map(tuple, next_state)) not in visitedStates:
                        # Calculate the Manhattan distance for the next state
                        next_manhattan = manhattan_distance(next_state)

                        # Add the next state and its Manhattan distance to the priority queue
                        next_path = current_path + [next_state]
                        priority_queue.put((next_manhattan, next_path))

        # If no solution is found, return None
    except TimeoutError:
        signal.alarm(0) # Reset the alarm when catching the timeout exception
        print("timeout exception")  # message for clarity as I've run into an issue discerning between a priority queue that is empty and one that has timed out in testing
        return -1, []

    signal.alarm(0)  # Reset the alarm at the end of the function
    return -1, []

if __name__ == "__main__": 
  try:
    n, m, initial_state = extract_initial_state_from_input()
    if(is_complete(initial_state,generate_goal_state(n,m))):
        status = 1
        moves = []
        print (status,len(moves))
    
    elif not is_solvable(initial_state,m):
        status = 0
        print(status)
        SystemExit
    
    else:
        status, moves = manhattan_search(initial_state, n, m)

        if status == -1:
            print(status)
        elif status == 1:
            
            print(status, len(moves), *moves)

  except ValueError as e:
        print(f"Error: {e}")
        SystemExit

