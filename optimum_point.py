import random
import matplotlib.pyplot as plt
import numpy as np

POINTS_POP = 100

ALL_POINTS = []

EPOCHS = 10000

gens = []

for x in range(-180, 181):
    for y in range(-90, 91):
        ALL_POINTS.append((x,y))

CURR_POINTS = [(77,12), (0, 51), (-104, 39)]

class Point():

    def __init__(self, x, y):

        global CURR_POINTS

        self.x = x
        self.y = y
        self.fitness = self.calculate_fitness(CURR_POINTS)

    def calculate_fitness(self, points):

        total_distance = 0

        for point in points:

            distance = self.get_distance(point[0], point[1])
            total_distance += distance

        return total_distance
    
    def get_distance(self, x2, y2):

        x1 = self.x
        y1 = self.y

        return ((x2 - x1)**2 + (y2 - y1)**2)
    
    def crossover(self, other):

        global ALL_POINTS
        prob = random.random()
        
        if prob < 0.45:
            x = self.x
            y = other.y

        elif 0.45 <= prob < 0.8:
            x = other.x
            y = self.y

        else:
            x,y = random.choice(ALL_POINTS)

        return Point(x, y)
    
point_pool = []

for j in range(POINTS_POP):
    random_point = random.choice(ALL_POINTS)
    point_pool.append(Point(random_point[0], random_point[1]))

gens.append((point_pool[0].x, point_pool[0].y))

gen = 0

while True:
    
    sorted_pool = sorted(point_pool, key=lambda p: p.fitness)

    if gen == EPOCHS:
        break

    next_pool = []

    next_pool.extend(sorted_pool[:10])

    for i in range(90):
        parent_set_1 = random.choice(sorted_pool[:50])
        parent_set_2 = random.choice(sorted_pool[:50])
        child_p = parent_set_1.crossover(parent_set_2)
        next_pool.append(child_p)

    point_pool = next_pool

    gen += 1

    if gen//100 == 0:
        gens.append((point_pool[0].x, point_pool[0].y))

    print(f"Generation: {gen}\nFitness: {point_pool[0].fitness}\nPoint: ({point_pool[0].x}, {point_pool[0].y})")

print(f"Generation: {gen}\nFitness: {sorted_pool[0].fitness}\nPoint: ({sorted_pool[0].x}, {sorted_pool[0].y})")

xs = []
ys = []

gxs = []
gys = []

for cp in CURR_POINTS:
    xs.append(cp[0])
    ys.append(cp[1])

for g in gens:
    gxs.append(g[0])
    gys.append(g[1])

cpx = np.array(xs)
cpy = np.array(ys)

ogx = np.array(gxs)
ogy = np.array(gys)

plt.scatter(cpx, cpy)
plt.scatter(ogx, ogy)
plt.plot(sorted_pool[0].x, sorted_pool[0].y, '-ro')
plt.show()
