import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Updated jobs with priority (1-5, where 1 is highest priority)
jobs = [
    {"id": 1, "name": "Data Processing", "duration": 3, "deadline": 5, "machine": ["A", "B"], "priority": 3},
    {"id": 2, "name": "Web Scraping", "duration": 2, "deadline": 4, "machine": ["B", "C"], "priority": 4},
    {"id": 3, "name": "Report Generation", "duration": 4, "deadline": 7, "machine": ["A", "C"], "priority": 2},
    {"id": 4, "name": "Database Backup", "duration": 1, "deadline": 2, "machine": ["A", "B", "C"], "priority": 1},
    {"id": 5, "name": "Email Campaign", "duration": 2, "deadline": 6, "machine": ["B", "C"], "priority": 5},
    {"id": 6, "name": "Server Maintenance", "duration": 3, "deadline": 8, "machine": ["A"], "priority": 2},
    {"id": 7, "name": "ML Model Training", "duration": 5, "deadline": 10, "machine": ["C"], "priority": 4},
    {"id": 8, "name": "API Integration", "duration": 2, "deadline": 5, "machine": ["A", "B"], "priority": 3},
]

max_deadline = max(job["deadline"] for job in jobs)
min_duration = min(job["duration"] for job in jobs)

def init_machines():
    return {"A": [], "B": [], "C": []}

def get_cost(machines, max_deadline, min_duration):
    tardiness = 0
    all_overlaps = 0
    schedule_details = {machine: [] for machine in machines}
    total_gap_penalty = 0
    priority_penalty = 0
    
    # Cost factors
    gap_penalty_factor = 10
    makespan_factor = 5
    priority_factor = 15  # Weight for priority-based penalties
    
    max_makespan = 0

    for machine, machine_tasks in machines.items():
        schedule = []
        # Sort by priority (priority 1 first) then by deadline
        sorted_tasks = sorted(machine_tasks, key=lambda task: (task["priority"], task["deadline"]))

        for i, task in enumerate(sorted_tasks):
            if i == 0:
                start_time = 1
            else:
                start_time = max(schedule[-1][-1] + 1, 1)
            
            end_time = start_time + task["duration"] - 1
            time_range = list(range(start_time, end_time + 1))
            schedule.append(time_range)
            schedule_details[machine].append((task, time_range))
            
            # Calculate tardiness with priority weighting (priority 1 = highest penalty)
            task_tardiness = max(0, end_time - task["deadline"])
            tardiness += task_tardiness * (6 - task["priority"])  # Invert priority for penalty
            
            # Priority-based waiting time penalty (priority 1 = highest penalty for waiting)
            waiting_time = start_time - 1
            priority_penalty += waiting_time * (6 - task["priority"])

            if i > 0:
                gap = start_time - schedule[-2][-1] - 1
                if gap > 0:
                    total_gap_penalty += gap * gap_penalty_factor

        machine_makespan = schedule[-1][-1] if schedule else 0
        max_makespan = max(max_makespan, machine_makespan)

    cost = (tardiness + 
            all_overlaps + 
            total_gap_penalty + 
            (max_makespan * makespan_factor) + 
            (priority_penalty * priority_factor))
    
    return cost, schedule_details

def crossover(parent1, parent2):
    child = init_machines()
    for job in jobs:
        # Priority 1 jobs have higher chance to inherit from better parent
        if random.random() < 0.5 + ((6 - job["priority"]) / 10):
            for machine, tasks in parent1.items():
                if job in tasks:
                    child[machine].append(job)
                    break
        else:
            for machine, tasks in parent2.items():
                if job in tasks:
                    child[machine].append(job)
                    break
    return child

def mutate(schedule, mutation_rate=0.1):
    for job in jobs:
        # Priority 1 jobs have lower mutation rate to maintain their scheduling
        adjusted_mutation_rate = mutation_rate * job["priority"] / 5
        if random.random() < adjusted_mutation_rate:
            for machine in schedule.values():
                if job in machine:
                    machine.remove(job)
                    break
            new_machine = random.choice(job["machine"])
            schedule[new_machine].append(job)
    return schedule

def genetic_algorithm(population_size=100, generations=2000):
    population = []
    for _ in range(population_size):
        machines = init_machines()
        # Initialize population with priority consideration (priority 1 first)
        sorted_jobs = sorted(jobs, key=lambda x: (x["priority"], x["deadline"]))
        for job in sorted_jobs:
            machine = random.choice(job["machine"])
            machines[machine].append(job)
        population.append(machines)

    best_overall_schedule = None
    best_overall_cost = float('inf')
    best_schedule_details = None

    for generation in range(generations):
        population_with_costs = [(schedule, *get_cost(schedule, max_deadline, min_duration)) 
                               for schedule in population]
        population_with_costs.sort(key=lambda x: x[1])
        
        if population_with_costs[0][1] < best_overall_cost:
            best_overall_schedule, best_overall_cost, best_schedule_details = population_with_costs[0]
            print(f"Generation {generation}: New best cost = {best_overall_cost}")

        elite_size = population_size // 5
        new_population = [schedule for schedule, _, _ in population_with_costs[:elite_size]]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population_with_costs[:len(population_with_costs)//2], k=2)
            child = crossover(parent1[0], parent2[0])
            child = mutate(child)
            new_population.append(child)

        population = new_population

    return best_overall_schedule, best_overall_cost, best_schedule_details

def plot_schedule(schedule_details):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = list(mcolors.TABLEAU_COLORS.values())
    machines = list(schedule_details.keys())

    for i, (machine, tasks) in enumerate(schedule_details.items()):
        for task, time_range in tasks:
            start, end = time_range[0], time_range[-1]
            priority_text = f"P{task['priority']}"
            label = f"{task['name']} ({priority_text})"
            # Adjust color opacity based on priority (priority 1 = most opaque)
            opacity = 1 - (task['priority'] - 1) * 0.15  # Priority 1 = 1.0, Priority 5 = 0.4
            ax.barh(i, end - start + 1, left=start, height=0.5,
                   align='center', color=colors[task['id'] % len(colors)],
                   alpha=opacity, label=label)

    ax.set_yticks(range(len(machines)))
    ax.set_yticklabels(machines)
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.set_title('Job Schedule (Priority 1 = Highest)')
    
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.tight_layout()
    plt.show()

# Run the algorithm
best_schedule, best_cost, schedule_details = genetic_algorithm()
print(f"Best cost found: {best_cost}")
print("\nBest schedule:")
for machine, tasks in schedule_details.items():
    print(f"\nMachine {machine}:")
    for task, time_range in tasks:
        print(f"  Priority {task['priority']} - {task['name']}: Time range {time_range[0]}-{time_range[-1]}")

plot_schedule(schedule_details)