import random

TARGET = "Hello, world!"

GENES = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 !@#$%^&*()., "

POPULATION = 100

class Individual():

    def __init__(self, chromosome):

        self.chromosome = chromosome
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        global TARGET
        fitness = 0
        for i in range(len(self.chromosome)):
            if self.chromosome[i] != TARGET[i]:
                fitness += 1
        
        return fitness
    
    def crossover(self, other):

        global GENES

        selfli = list(self.chromosome)
        otherli = list(other.chromosome)
        
        childli = []

        for i in range(len(self.chromosome)):
            prob = random.random()

            if prob < 0.45:
                childli.append(self.chromosome[i])
            elif 0.45 <= prob < 0.8:
                childli.append(other.chromosome[i])
            else:
                childli.append(random.choice(GENES))

        return ''.join(c for c in childli)


pool = []

for i in range(POPULATION):
    chromosome = ''.join(random.choice(GENES) for i in range(len(TARGET)))
    pool.append(Individual(chromosome))

generation = 0

while True:

    sorted_pool = sorted(pool, key=lambda x: x.fitness)

    if sorted_pool[0].fitness <= 0:
        break

    next_pool = []

    next_pool.extend(sorted_pool[:10])

    for i in range(90):
        parent_set_1 = random.choice(sorted_pool[:50])
        parent_set_2 = random.choice(sorted_pool[:50])
        child_chromosome = parent_set_1.crossover(parent_set_2)
        next_pool.append(Individual(child_chromosome))

    pool = next_pool

    generation += 1

    print(f"Generation: {generation}\Fitness: {pool[0].fitness}\nString: {pool[0].chromosome}")

print(f"Generation: {generation}\Fitness: {sorted_pool[0].fitness}\nString: {sorted_pool[0].chromosome}")