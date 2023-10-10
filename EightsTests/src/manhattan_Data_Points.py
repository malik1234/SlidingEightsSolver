import csv
import time
import manhattan
import matplotlib.pyplot as plt
from PuzzleSolver import *
from statistics import mean, stdev
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

def steps_and_execution_time_for_solutions(n, m, num_trials=5):
    steps_list = []
    execution_times = []
    for _ in range(num_trials):
        start_time = time.process_time()
        
        initialState = random_solvable_state(n, m)
        _, moves = manhattan.manhattan_search(initialState, n, m)
        
        end_time = time.process_time()
        
        steps_list.append(len(moves))
        execution_times.append(end_time - start_time)
    return steps_list, execution_times

def measure_steps_and_execution_times():
    sizes = []
    avg_steps = []
    std_dev_steps = []
    avg_times = []
    std_dev_times = []

    for n in range(3, 7):
        m = n
        sizes.append(n)
        
        steps, execution_times = steps_and_execution_time_for_solutions(n, m)
        
        avg_steps.append(mean(steps))
        std_dev_steps.append(stdev(steps))
        
        avg_times.append(mean(execution_times))
        std_dev_times.append(stdev(execution_times))

    return sizes, avg_steps, std_dev_steps, avg_times, std_dev_times

def plot_exponential_graph(sizes, avg_times):
    # Fitting an exponential curve: y = a * e^(bx)
    coefficients = np.polyfit(sizes, np.log(avg_times), 1)
    a = np.exp(coefficients[1])
    b = coefficients[0]

    # Generate fitted values
    fitted_y = a * np.exp(b * np.array(sizes))

    # Interpolate for a smoother curve
    xnew = np.linspace(min(sizes), max(sizes), 300)
    spl = make_interp_spline(sizes, avg_times, k=2)  # type: BSpline
    ynew = spl(xnew)

    # Plotting
    plt.scatter(sizes, avg_times, color='blue', label='Data points')
    plt.plot(xnew, ynew, color='green', label='Interpolated Curve')
    plt.plot(sizes, fitted_y, color='red', label=f'Fit: y = {a:.2f} * e^({b:.2f}x)')
    plt.xlabel('Board Size')
    plt.ylabel('Average CPU Time (s)')
    plt.title('Average Execution Time vs. Board Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('execution_time_vs_board_size.png')
    plt.show()

def write_to_csv():
    sizes, avg_steps, std_dev_steps, avg_times, std_dev_times = measure_steps_and_execution_times()

    with open('manhattan_pure_data_points.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header
        csv_writer.writerow(['Grid Size', 'Avg Steps', 'Std Dev Steps', 'Avg CPU Time (s)', 'Std Dev CPU Time (s)'])
        
        for size, avg_step, std_dev_step, avg_time, std_dev_time in zip(sizes, avg_steps, std_dev_steps, avg_times, std_dev_times):
            csv_writer.writerow([f"{size}x{size}", avg_step, std_dev_step, avg_time, std_dev_time])

    # Generate the plot after writing to CSV
    plot_exponential_graph(sizes, avg_times)

if __name__ == "__main__":
    write_to_csv()
