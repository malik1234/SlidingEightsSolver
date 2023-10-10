import time
# import signal
from PuzzleSolver import *
import matplotlib.pyplot as plt
import manhattan

# def handler(signum, frame):
#     raise TimeoutError



def steps_for_solutions(n, m, num_trials=100):
    steps = []
    for _ in range(num_trials):
        initialState = random_solvable_state(n, m)
        _, moves = manhattan.manhattan_search(initialState, n, m)
        steps.append(len(moves))
    return steps

def measure_average_steps_and_std_dev():
    sizes = []
    avg_steps = []
    std_devs = []
    
    for n in range(3, 7):  # For sizes from 3x3 to 5x5
        m = n
        sizes.append(n)
        
        steps = steps_for_solutions(n, m)
        avg = sum(steps) / len(steps)
        avg_steps.append(avg)
        
        variance = sum((x - avg) ** 2 for x in steps) / len(steps)
        std_dev = variance ** 0.5
        std_devs.append(std_dev)
        
    return sizes, avg_steps, std_devs

def plot_average_steps():
    sizes, avg_steps, std_devs = measure_average_steps_and_std_dev()

    plt.figure(figsize=(10, 6))
    plt.errorbar(sizes, avg_steps, yerr=std_devs, marker='o', capsize=5)
    plt.title('Average Steps to Solution vs. Grid Size with Standard Deviation')
    plt.xlabel('Grid Size (NxN)')
    plt.ylabel('Average Steps')
    
    plt.xticks(sizes)
    plt.grid(True)
    
    plt.savefig("average_steps_vs_grid_size_with_std_dev.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_average_steps()
