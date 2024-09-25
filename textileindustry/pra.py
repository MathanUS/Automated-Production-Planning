import random
import sqlite3
import matplotlib.pyplot as plt
import time

# Your Task and Chromosome classes here

# Flask setup and database functions here

def run_genetic_algorithm(population_size):
    conn = sqlite3.connect('Industry.db')
    cursor = conn.cursor()

    tasks = get_tasks_from_db()  # Ensure this function retrieves tasks from the database

    mutation_rate = 0.1
    crossover_rate = 0.8
    generations = 500

    population = [Chromosome() for _ in range(population_size)]

    def evaluate(chromosome):
        makespan = 0
        current_time_on_machines = [0] * len(set(task.machine for task in tasks))
        
        for task in chromosome.sequence:
            machine_time = current_time_on_machines[task.machine - 1]
            current_time_on_machines[task.machine - 1] += task.duration
            makespan = max(makespan, machine_time + task.duration)
        
        return makespan

    start_time = time.time()
    for generation in range(generations):
        # Genetic algorithm operations (same as previous code)
        pass

        if generation == 199:  # Stop the loop at generation 200
            break

    end_time = time.time()
    runtime = end_time - start_time
    conn.close()
    return runtime

if __name__ == '__main__':
    population_sizes = [100, 500, 1000, 2000]  # Define different population sizes to test
    runtimes = []

    for size in population_sizes:
        runtime = run_genetic_algorithm(size)
        runtimes.append(runtime)
        print(f"Population Size: {size}, Runtime: {runtime} seconds")

    # Plotting the graph for time complexity
    plt.plot(population_sizes, runtimes, marker='o')
    plt.xlabel('Population Size')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Time Complexity Analysis for Different Population Sizes')
    plt.grid(True)
    plt.show()

    


