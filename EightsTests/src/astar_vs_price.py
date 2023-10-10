import csv
import time
from PuzzleSolver import random_solvable_state
import astar
import price

def gather_data(n, m, num_trials=100):
    data = []
    for _ in range(num_trials):
        initialState = random_solvable_state(n, m)
        
        _, astar_moves = astar.astar(initialState, n, m)
        _, price_moves, price_move_sum = price.price(initialState, n, m)
        
        astar_path_length = len(astar_moves)
        price_path_length = len(price_moves)
        
        astar_move_sum = sum(astar_moves)
        
        difference = astar_path_length - price_path_length
        
        data.append((initialState, astar_path_length, astar_move_sum, price_path_length, price_move_sum, difference))

    with open('pricecomparison.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["State", "AStar_PathLength", "AStar_MoveSum", "Price_PathLength", "Price_MoveSum", "Difference"])
        writer.writerows(data)

if __name__ == "__main__":
    gather_data(3, 3)
