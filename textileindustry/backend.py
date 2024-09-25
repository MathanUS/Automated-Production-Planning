import random
import sqlite3

def main(user_id):
# Establish connection
    conn = sqlite3.connect('Industry.db')
    cursor = conn.cursor()
    global tasks
    class Task:
        def __init__(self, id, machine, duration):
            self.id = id
            self.machine = machine
            self.duration = duration

    class Chromosome:
        def __init__(self, sequence=None):
            self.sequence = sequence if sequence else self.initialize_sequence()

        def initialize_sequence(self):
            return random.sample(tasks, len(tasks))

        def mutate(self):
            if len(self.sequence) < 2:
                return
            index1, index2 = random.sample(range(len(self.sequence)), 2)
            self.sequence[index1], self.sequence[index2] = self.sequence[index2], self.sequence[index1]

        def crossover(self, other):
            
            if len(self.sequence) <= 1:
                return self

            crossover_point = random.randint(1, len(self.sequence) - 1)
            child_sequence = self.sequence[:crossover_point] + [gene for gene in other.sequence if gene not in self.sequence[:crossover_point]]
            return Chromosome(child_sequence)

    population_size = 1000
    mutation_rate = 0.1
    crossover_rate = 0.8
    generations = 500


    def create_task_from_db(row):
        task_id, machine, duration = row
        return Task(task_id, machine, duration)

    def get_tasks_from_db(user_id):
        cursor.execute("SELECT taskId, machineId, duration FROM TASK WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        tasks = [create_task_from_db(row) for row in rows]
        return tasks

    # Fetch tasks from the database
    tasks = get_tasks_from_db(user_id)



    population = [Chromosome() for _ in range(population_size)]

    def evaluate(chromosome):
        makespan = 0
        unique_machines = set(task.machine for task in tasks)
        num_machines = max(unique_machines)  # Assuming machine IDs start from 1 and are continuous

        current_time_on_machines = [0] * num_machines
        
        for task in chromosome.sequence:
            machine_time = current_time_on_machines[task.machine - 1]
            current_time_on_machines[task.machine - 1] += task.duration
            makespan = max(makespan, machine_time + task.duration)
        
        return makespan

    for generation in range(generations):
        fitness_scores = {chromosome: evaluate(chromosome) for chromosome in population}
        selected_parents = random.choices(population, weights=[1 / (fitness_scores[chromosome] + 1) for chromosome in population], k=population_size)

        new_population = []
        for i in range(0, len(selected_parents), 2):
            parent1, parent2 = selected_parents[i], selected_parents[i + 1]

            if random.random() < crossover_rate:
                offspring = parent1.crossover(parent2)
            else:
                offspring = parent1 if fitness_scores[parent1] < fitness_scores[parent2] else parent2

            if random.random() < mutation_rate:
                offspring.mutate()

            new_population.append(offspring)
        population = new_population

    best_schedule = min(population, key=lambda x: evaluate(x))
    print(f"Best schedule makespan: {evaluate(best_schedule)}")
    print(f"Best schedule sequence: {[task.id for task in best_schedule.sequence]}")

    data_makespan=evaluate(best_schedule)
    data_taskseq=[task.id for task in best_schedule.sequence]
    return [data_makespan,data_taskseq]

if __name__=='__main__':
    main()
    
    
'''

import random
import sqlite3
from flask import Flask, jsonify

class Task:
    def __init__(self, id, machine, duration):
        self.id = id
        self.machine = machine
        self.duration = duration

class Chromosome:
    def __init__(self, sequence=None):
        self.sequence = sequence if sequence else self.initialize_sequence()

    def initialize_sequence(self):
        return random.sample(tasks, len(tasks))

    def mutate(self):
        index1, index2 = random.sample(range(len(self.sequence)), 2)
        self.sequence[index1], self.sequence[index2] = self.sequence[index2], self.sequence[index1]

    def crossover(self, other):
        crossover_point = random.randint(1, len(self.sequence) - 1)
        child_sequence = self.sequence[:crossover_point] + [gene for gene in other.sequence if gene not in self.sequence[:crossover_point]]
        return Chromosome(child_sequence)

app = Flask(__name__)

conn = sqlite3.connect('Industry.db')
cursor = conn.cursor()

def create_task_from_db(row):
    task_id, machine, duration = row
    return Task(task_id, machine, duration)

def get_tasks_from_db():
    cursor.execute("SELECT taskId, machineId, duration FROM TASK")
    rows = cursor.fetchall()
    tasks = [create_task_from_db(row) for row in rows]
    return tasks

tasks = get_tasks_from_db()

@app.route('/get_best_schedule', methods=['GET'])
def get_best_schedule():
    population_size = 1000
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

    for generation in range(generations):
        fitness_scores = {chromosome: evaluate(chromosome) for chromosome in population}
        selected_parents = random.choices(population, weights=[1 / (fitness_scores[chromosome] + 1) for chromosome in population], k=population_size)

        new_population = []
        for i in range(0, len(selected_parents), 2):
            parent1, parent2 = selected_parents[i], selected_parents[i + 1]

            if random.random() < crossover_rate:
                offspring = parent1.crossover(parent2)
            else:
                offspring = parent1 if fitness_scores[parent1] < fitness_scores[parent2] else parent2

            if random.random() < mutation_rate:
                offspring.mutate()

            new_population.append(offspring)
        population = new_population

    best_schedule = min(population, key=lambda x: evaluate(x))
    makespan = evaluate(best_schedule)
    sequence = [task.id for task in best_schedule.sequence]

    conn.close()

    data = {
        "makespan": makespan,
        "sequence": sequence
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
'''
