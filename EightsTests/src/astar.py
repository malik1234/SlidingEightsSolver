from queue import PriorityQueue
from copy import deepcopy
import signal
from PuzzleSolver import *

def astar(initial_state, n, m):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60) 
    try:  
        goal_state = generate_goal_state(n, m)
        priority_queue = PriorityQueue()
        visited = set()

        # Start with cost of 0 and heuristic value for initial state
        g_initial = 0
        h_initial = manhattan_distance(initial_state)
        priority_queue.put((g_initial + h_initial, g_initial, [initial_state]))

        while not priority_queue.empty():
            f_current, g_current, current_path = priority_queue.get()
            current_state = current_path[-1]

            if is_complete(current_state, goal_state):
                return 1, extract_moves(current_path)

            visited.add(tuple(map(tuple, current_state)))

            empty_i, empty_j, possible_moves = generate_child_nodes(current_state)

            for move_i, move_j in possible_moves:
                if 0 <= move_i < n and 0 <= move_j < m:
                    next_state = [list(row) for row in current_state]
                    next_state[empty_i][empty_j], next_state[move_i][move_j] = next_state[move_i][move_j], next_state[empty_i][empty_j]
                    
                    # Calculate the cost to move to the next state
                    g_next = g_current + 1
                    h_next = manhattan_distance(next_state)

                    if tuple(map(tuple, next_state)) not in visited:
                        f_next = g_next + h_next
                        next_path = current_path + [next_state]
                        priority_queue.put((f_next, g_next, next_path))

    except TimeoutError:
        signal.alarm(0) 
        print("timeout exception")
        return -1, []

    signal.alarm(0)  
    return -1, []




if __name__ == "__main__":
  try:
    n, m, initial_state = extract_initial_state_from_input()
    validate_dimensions(n, m)
    validate_initial_state(initial_state, n, m)  
    if(is_complete(initial_state,generate_goal_state(n,m))):
        status = 1
        moves = []
        print (status,len(moves))
    
    elif not is_solvable(initial_state,m):
        status = 0
        print(status)
        SystemExit
    
    else:
        status, moves = astar(initial_state, n, m)
        if status == -1:
            print(status)
        elif status == 1:
         print(status, len(moves),*moves)

  except ValueError as e:
        print(f"Error: {e}")
        SystemExit