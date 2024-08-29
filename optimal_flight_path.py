import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from collections import defaultdict

PLANES = [

    ("P1", 15000, 1000, 8),
    ("P2", 20000, 1200, 10),
    ("P3", 15000, 1500, 12),
    ("P4", 17000, 2000, 18),
    ("P5", 8000, 900, 8)

]

REFUEL = [

    ("REFUEL_1", 13, 15, 20),
    ("REFUEL_2", 78, 52, 10),
    ("REFUEL_3", 44, 60, 30),
    ("REFUEL_4", 31, 58, 15),
    ("REFUEL_5", 32, 7, 10)

]

PORTS = [

    ("PORT_1", 4, 88),
    ("PORT_2", 56, 29),
    ("PORT_3", 62, 17),
    ("PORT_4", 37, 95),
    ("PORT_5", 59, 84),
    ("PORT_6", 18, 42),
    ("PORT_7", 69, 38),
    ("PORT_8", 22, 52),
    ("PORT_9", 10, 65),
    ("PORT_10", 12, 48)

]

POP_SIZE = 500
EPOCHS = 30000
SINGLE_TRIP_BUDGET = 62000
INORDER = True

class Flight():

    def __init__(self, depart, path, plane):

        self.depart = depart
        self.depart_name = depart[0]
        self.depart_x, self.depart_y = depart[1], depart[2]
        self.path = path
        self.plane = plane
        self.plane_name = plane[0]
        self.plane_rent = plane[1]
        self.plane_totalfuel = plane[2]
        self.plane_currfuel = self.plane_totalfuel
        self.plane_fuel_per_m = plane[3]

        self.cost, self.final = self.getCost()

    def getCost(self):

        global REFUEL
        global PORTS
        global INORDER

        cost = self.plane_rent

        final_path = []

        currx, curry = self.depart_x, self.depart_y

        if INORDER == False:
            if random.random() < 0.55:
                path_ = self.path[1:len(self.path)-1]
                random.shuffle(path_)
                path_.append(self.path[-1])
                path_.insert(0, self.path[0])
                self.path = path_
        
        for p in self.path:

            flag = 0

            while flag == 0:

                fuelflag = 0

                dist = self.getDistance((p[1], p[2]), (currx, curry))

                fuel_use = self.plane_fuel_per_m * dist

                left = self.plane_currfuel - fuel_use

                if left <= int(self.plane_totalfuel/5):

                    prob = random.random()

                    if prob < 0.8:

                        refuel_point = random.choice(REFUEL)
                        stopn, stopx, stopy, refuel_cost = refuel_point[0], refuel_point[1], refuel_point[2], refuel_point[3]

                        fuelflag = 1

                    else:

                        port_point = random.choice(PORTS)
                        stopn, stopx, stopy = port_point[0], port_point[1], port_point[2]

                    dist = self.getDistance((stopx, stopy), (currx, curry))

                    fuel_use = self.plane_fuel_per_m * dist

                    left = self.plane_currfuel - fuel_use

                    if left <= 0:
                        cost += 200000000
                        return cost, final_path
                    
                    else:

                        self.plane_currfuel = left

                        currx, curry = stopx, stopy
                        
                        if fuelflag == 1:
                            cost += refuel_cost * (self.plane_totalfuel - self.plane_currfuel)
                            self.plane_currfuel = self.plane_totalfuel

                        final_path.append(stopn)

                else:

                    flag = 1

            self.plane_currfuel = left

            currx, curry = p[1], p[2]

            final_path.append(p[0])

        return cost, final_path

    def crossover(self, par1):

        global PLANES

        prob = random.random()

        if prob < 0.3:

            pn = par1.plane_name
            pc = par1.plane_rent
            pt = par1.plane_totalfuel
            pf = par1.plane_fuel_per_m

        elif 0.3 <= prob < 0.6:

            pn = self.plane_name
            pc = self.plane_rent
            pt = self.plane_totalfuel
            pf = self.plane_fuel_per_m

        else:

            pn, pc, pt, pf = random.choice(PLANES)


        return Flight(self.depart, self.path, (pn, pc, pt, pf))

    @staticmethod
    def getDistance(point_1, point_2):
        return int(((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5)
    

path = [PORTS[0], PORTS[6],
        PORTS[1], PORTS[3],
        PORTS[7], PORTS[1],
        PORTS[9], PORTS[4],
        PORTS[8], PORTS[3],
        PORTS[0]]

if INORDER == False:
    path_ = list(set(path[1:len(path)-1]))
    path_.append(path[-1])
    path_.insert(0, path[0])
    path = path_


all_flights = []

for _ in range(POP_SIZE):
    fl = Flight(path[0], path, random.choice(PLANES))
    all_flights.append(fl)

gen = 0

while True:

    sorted_flights = sorted(all_flights, key=lambda x: x.cost)

    if gen == EPOCHS or sorted_flights[0].cost < SINGLE_TRIP_BUDGET:
        break

    next_flights = sorted_flights[:50]

    for i in range(450):

        f1 = random.choice(sorted_flights[:250])
        f2 = random.choice(sorted_flights[:250])

        newf = f1.crossover(f2)

        next_flights.append(newf)

    all_flights = next_flights

    gen += 1
    
    if gen%500 == 0:
        print(f"Generation: {gen}\nCost: {all_flights[0].cost}\nPlane: {all_flights[0].plane}")


def get_coordinates(stop_name):
    for stop in PORTS + REFUEL:
        if stop[0] == stop_name:
            return stop[1], stop[2]
    return None

print(f"\nPlane: {sorted_flights[0].plane_name}")
print(f"Plane rent: {sorted_flights[0].plane_rent}\n")
print(f"Stops:\n\n{' -> '.join(p[0] for p in path)}\n")
print(f"Path to take:\n\n{' -> '.join(sf for sf in sorted_flights[0].final)}\n")
print(f"Fuel left: {sorted_flights[0].plane_currfuel}/{sorted_flights[0].plane_totalfuel}")
print(f"Final Cost: {sorted_flights[0].cost}\n")

port_x = [port[1] for port in PORTS]
port_y = [port[2] for port in PORTS]

refuel_x = [station[1] for station in REFUEL]
refuel_y = [station[2] for station in REFUEL]

plt.figure(figsize=(12, 8))

# Plot ports and refuel stations
plt.scatter(port_x, port_y, color='red', marker='o')
plt.scatter(refuel_x, refuel_y, color='green', marker='o')

# Create a dictionary to store visit orders for each stop
visit_orders = defaultdict(list)

# Populate visit_orders dictionary
path = sorted_flights[0].final
for i, stop in enumerate(path[1:], start=1):  # Start from 1 for the second stop
    visit_orders[stop].append(str(i))

# Draw arrows and label stops
for i in range(len(sorted_flights[0].final) - 1):
    start = get_coordinates(sorted_flights[0].final[i])
    end = get_coordinates(sorted_flights[0].final[i+1])
    
    if start and end:
        arrow = FancyArrowPatch(
            start, end,
            arrowstyle='->,head_width=1.5,head_length=2',
            color='blue',
            linewidth=1.5,
            alpha=0.7,
            connectionstyle="arc3,rad=0.1"
        )
        plt.gca().add_patch(arrow)

# Label stops with visit orders
for stop, orders in visit_orders.items():
    coords = get_coordinates(stop)
    if coords:
        label = ",".join(orders)
        plt.annotate(label, coords, xytext=(5, 5), textcoords='offset points',
                     fontsize=9, color='purple', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', fc='yellow', ec='none', alpha=0.7))

# Add stop names
for stop in PORTS + REFUEL:
    plt.annotate(stop[0], (stop[1], stop[2]), xytext=(5, -10), textcoords='offset points')

plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Flight Path: Ports and Refuel Stations')
plt.legend(['Ports', 'Refuel Stations'])

plt.grid(True)
plt.show()
