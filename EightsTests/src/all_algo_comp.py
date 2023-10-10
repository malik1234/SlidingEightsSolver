import csv
import time
import manhattan
import astar
import price
from PuzzleSolver import random_solvable_state
import matplotlib.pyplot as plt

def format_time_to_sci(time_value):
    """Format time to scientific notation with two significant figures."""
    return "{:.2e}".format(time_value)

def gather_data(n, m, num_trials=1000): #change num_trials to whatever you want
    data = []
    for _ in range(num_trials):
        initialState = random_solvable_state(n, m)

        start_time = time.process_time()
        _, manhattan_moves = manhattan.manhattan_search(initialState, n, m)
        manhattan_time = format_time_to_sci(time.process_time() - start_time)

        start_time = time.process_time()
        _, astar_moves = astar.astar(initialState, n, m)
        astar_time = format_time_to_sci(time.process_time() - start_time)

        start_time = time.process_time()
        _, price_moves,_placeholder = price.price(initialState, n, m)
        price_time = format_time_to_sci(time.process_time() - start_time)

        data.append((len(manhattan_moves), manhattan_time, len(astar_moves), astar_time, len(price_moves), price_time))

    data.sort(key=lambda x: x[0])  # sort by number of steps from manhattan_search

    with open('allalgocomparison.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Manhattan_Steps", "Manhattan_Time(s)", "AStar_Steps", "AStar_Time(s)", "Price_Steps", "Price_Time(s)"])
        writer.writerows(data)

    # Plot
    manhattan_steps, manhattan_times, astar_steps, astar_times, price_steps, price_times = zip(*data)
    
    plt.figure(figsize=(10, 6))
    plt.plot(manhattan_steps, [float(t) for t in manhattan_times], label="Manhattan")
    plt.plot(astar_steps, [float(t) for t in astar_times], label="A*")
    plt.plot(price_steps, [float(t) for t in price_times], label="Price")
    plt.xlabel('Number of Steps to Solution')
    plt.ylabel('Execution Time  of all algo(s in scientific notation)')
    plt.legend()
    plt.grid(True)
    plt.savefig("comparison_graph.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    gather_data(3, 3)






# import csv
# import time
# import matplotlib.pyplot as plt
# from PuzzleSolver import random_solvable_state
# import manhattan  
# import astar
# import price  # This is the assumed module for the price algorithm

# def compute_solutions():
#     data = []
#     for _ in range(1000):
#         initial_state = random_solvable_state(3, 3)

#         start_time = time.process_time()
#         _, manhattan_moves = manhattan.manhattan_search(initial_state, 3, 3)
#         manhattan_time = round(time.process_time() - start_time, 2)

#         start_time = time.process_time()
#         _, astar_moves = astar.astar(initial_state, 3, 3)
#         astar_time = round(time.process_time() - start_time, 2)

#         start_time = time.process_time()
#         _, price_moves = price.price(initial_state, 3, 3)  # Assuming a similar function signature for price search
#         price_time = round(time.process_time() - start_time, 2)

#         data.append({
#             "manhattan_steps": len(manhattan_moves),
#             "manhattan_time": manhattan_time,
#             "astar_steps": len(astar_moves),
#             "astar_time": astar_time,
#             "price_steps": len(price_moves),
#             "price_time": price_time
#         })

#     return sorted(data, key=lambda x: x["manhattan_steps"])

# def create_csv(data, filename="all_parts_comparison.csv"):
#     with open(filename, 'w', newline='') as csvfile:
#         fieldnames = ["manhattan_steps", "manhattan_time", "astar_steps", "astar_time", "price_steps", "price_time"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)

# data = compute_solutions()
# create_csv(data)

# def plot_graph(filename="all_parts_comparison.csv"):
#     manhattan_steps, manhattan_time, astar_time, price_time = [], [], [], []

#     with open(filename, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             manhattan_steps.append(int(row["manhattan_steps"]))
#             manhattan_time.append(float(row["manhattan_time"]))
#             astar_time.append(float(row["astar_time"]))
#             price_time.append(float(row["price_time"]))

#     plt.figure(figsize=(12, 7))
#     plt.plot(manhattan_steps, manhattan_time, marker='o', label='Manhattan Search Time')
#     plt.plot(manhattan_steps, astar_time, marker='x', label='A* Search Time')
#     plt.plot(manhattan_steps, price_time, marker='s', label='Price Search Time')

#     plt.title('Execution Time vs. Number of Steps to Solution')
#     plt.xlabel('Number of Steps (from Manhattan Search)')
#     plt.ylabel('Execution Time (s)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# plot_graph()