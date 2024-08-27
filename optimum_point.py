import random
import matplotlib.pyplot as plt
import numpy as np

# City data (replace the previous cities list with this)
cities = [
    ("Aberdeen", -2, 57),
    ("Adelaide", 139, -35),
    ("Algiers", 3, 37),
    ("Amsterdam", 5, 52),
    ("Ankara", 33, 40),
    ("Asunción", -58, -25),
    ("Athens", 24, 38),
    ("Auckland", 175, -37),
    ("Bangkok", 100, 14),
    ("Barcelona", 2, 41),
    ("Beijing", 116, 40),
    ("Belém", -48, -1),
    ("Belfast", -6, 55),
    ("Belgrade", 21, 45),
    ("Berlin", 13, 52),
    ("Birmingham", -2, 52),
    ("Bogotá", -74, 5),
    ("Bombay", 73, 19),
    ("Bordeaux", -1, 45),
    ("Bremen", 9, 53),
    ("Brisbane", 153, -27),
    ("Bristol", -3, 51),
    ("Brussels", 4, 51),
    ("Bucharest", 26, 44),
    ("Budapest", 19, 48),
    ("Buenos Aires", -58, -35),
    ("Cairo", 31, 30),
    ("Calcutta", 88, 23),
    ("Canton", 113, 23),
    ("Cape Town", 18, -34),
    ("Caracas", -67, 10),
    ("Cayenne", -52, 5),
    ("Chihuahua", -106, 29),
    ("Chongqing", 107, 30),
    ("Copenhagen", 13, 56),
    ("Córdoba", -64, -31),
    ("Dakar", -17, 15),
    ("Darwin", 131, -12),
    ("Djibouti", 43, 11),
    ("Dublin", -6, 53),
    ("Durban", 31, -30),
    ("Edinburgh", -3, 56),
    ("Frankfurt", 9, 50),
    ("Georgetown", -58, 7),
    ("Glasgow", -4, 56),
    ("Guatemala City", -91, 15),
    ("Guayaquil", -80, -2),
    ("Hamburg", 10, 54),
    ("Hammerfest", 24, 71),
    ("Havana", -82, 23),
    ("Helsinki", 25, 60),
    ("Hobart", 147, -43),
    ("Hong Kong", 114, 22),
    ("Iquique", -70, -20),
    ("Irkutsk", 104, 52),
    ("Jakarta", 107, -6),
    ("Johannesburg", 28, -26),
    ("Kingston", -77, 18),
    ("Kinshasa", 15, -4),
    ("Kuala Lumpur", 102, 3),
    ("La Paz", -68, -16),
    ("Leeds", -1, 54),
    ("Lima", -77, -12),
    ("Lisbon", -9, 39),
    ("Liverpool", -3, 53),
    ("London", 0, 52),
    ("Lyons", 5, 46),
    ("Madrid", -4, 40),
    ("Manchester", -2, 53),
    ("Manila", 121, 15),
    ("Marseilles", 5, 43),
    ("Mazatlán", -106, 23),
    ("Mecca", 40, 21),
    ("Melbourne", 145, -38),
    ("Mexico City", -99, 19),
    ("Milan", 9, 45),
    ("Montevideo", -56, -35),
    ("Moscow", 38, 56),
    ("Munich", 12, 48),
    ("Nagasaki", 130, 33),
    ("Nagoya", 137, 35),
    ("Nairobi", 37, -1),
    ("Nanjing", 119, 32),
    ("Naples", 14, 41),
    ("New Delhi", 77, 29),
    ("Newcastle-on-Tyne", -2, 55),
    ("Odessa", 31, 46),
    ("Osaka", 135, 35),
    ("Oslo", 11, 60),
    ("Panama City", -80, 9),
    ("Paramaribo", -55, 6),
    ("Paris", 2, 49),
    ("Perth", 116, -32),
    ("Plymouth", -4, 50),
    ("Port Moresby", 147, -9),
    ("Prague", 14, 50),
    ("Rangoon", 96, 17),
    ("Reykjavík", -22, 64),
    ("Rio de Janeiro", -43, -23),
    ("Rome", 12, 42),
    ("Salvador", -38, -13),
    ("Santiago", -71, -33),
    ("St. Petersburg", 30, 60),
    ("São Paulo", -47, -24),
    ("Shanghai", 121, 31),
    ("Singapore", 104, 1),
    ("Sofia", 23, 43),
    ("Stockholm", 18, 59),
    ("Sydney", 151, -34),
    ("Tananarive", 48, -19),
    ("Teheran", 52, 36),
    ("Tokyo", 140, 36),
    ("Tripoli", 13, 33),
    ("Venice", 12, 45),
    ("Veracruz", -96, 19),
    ("Vienna", 16, 48),
    ("Vladivostok", 132, 43),
    ("Warsaw", 21, 52),
    ("Wellington", 175, -41),
    ("Zürich", 9, 47),
    ("Albany", -73.75, 42.67),
    ("Albuquerque", -106.65, 35.08),
    ("Amarillo", -101.83, 35.18),
    ("Anchorage", -149.90, 61.22),
    ("Atlanta", -84.38, 33.75),
    ("Austin", -97.73, 30.27),
    ("Baker", -117.83, 44.78),
    ("Baltimore", -76.63, 39.30),
    ("Bangor", -68.78, 44.80),
    ("Birmingham, AL", -86.83, 33.50),
    ("Bismarck", -100.78, 46.80),
    ("Boise", -116.22, 43.60),
    ("Boston", -71.08, 42.35),
    ("Buffalo", -78.83, 42.92),
    ("Calgary", -114.02, 51.02),
    ("Carlsbad", -104.25, 32.43),
    ("Charleston, SC", -79.93, 32.78),
    ("Charleston, WV", -81.63, 38.35),
    ("Charlotte", -80.83, 35.23),
    ("Cheyenne", -104.87, 41.15),
    ("Chicago", -87.62, 41.83),
    ("Cincinnati", -84.50, 39.13),
    ("Cleveland", -81.62, 41.47),
    ("Columbia, SC", -81.03, 34.00),
    ("Columbus, OH", -83.02, 40.00),
    ("Dallas", -96.77, 32.77),
    ("Denver", -105.00, 39.75),
    ("Des Moines", -93.62, 41.58),
    ("Detroit", -83.05, 42.33),
    ("Dubuque", -90.67, 42.52),
    ("Duluth", -92.08, 46.82),
    ("Eastport", -67.00, 44.90),
    ("Edmonton", -113.47, 53.57),
    ("El Centro", -115.55, 32.63),
    ("El Paso", -106.48, 31.77),
    ("Eugene", -123.08, 44.05),
    ("Fargo", -96.80, 46.87),
    ("Flagstaff", -111.68, 35.22),
    ("Fort Worth", -97.32, 32.72),
    ("Fresno", -119.80, 36.73),
    ("Grand Junction", -108.55, 39.08),
    ("Grand Rapids", -85.67, 42.97),
    ("Havre", -109.72, 48.55),
    ("Helena", -112.03, 46.58),
    ("Honolulu", -157.83, 21.30),
    ("Hot Springs", -93.05, 34.52),
    ("Houston", -95.35, 29.75),
    ("Idaho Falls", -112.02, 43.50),
    ("Indianapolis", -86.17, 39.77),
    ("Jackson, MS", -90.20, 32.33),
    ("Jacksonville", -81.67, 30.37),
    ("Juneau", -134.40, 58.30),
    ("Kansas City", -94.58, 39.10),
    ("Key West", -81.80, 24.55),
    ("Kingston, ON", -76.50, 44.25),
    ("Klamath Falls", -121.73, 42.17),
    ("Knoxville", -83.93, 35.95),
    ("Las Vegas", -115.20, 36.17),
    ("Lewiston", -117.03, 46.40),
    ("Lincoln", -96.67, 40.83),
    ("London, ON", -81.57, 43.03),
    ("Long Beach", -118.18, 33.77),
    ("Los Angeles", -118.25, 34.05),
    ("Louisville", -85.77, 38.25),
    ("Manchester", -71.50, 43.00),
    ("Memphis", -90.05, 35.15),
    ("Miami", -80.20, 25.77),
    ("Milwaukee", -87.92, 43.03),
    ("Minneapolis", -93.23, 44.98),
    ("Mobile", -88.05, 30.70),
    ("Montgomery", -86.30, 32.35),
    ("Montpelier", -72.53, 44.25),
    ("Montreal", -73.58, 45.50),
    ("Moose Jaw", -105.52, 50.62),
    ("Nashville", -86.78, 36.17),
    ("Nelson", -117.28, 49.50),
    ("Newark", -74.17, 40.73),
    ("New Haven", -72.92, 41.32),
    ("New Orleans", -90.07, 29.95),
    ("New York", -73.97, 40.78),
    ("Nome", -165.50, 64.42),
    ("Oakland", -122.27, 37.80),
    ("Oklahoma City", -97.47, 35.43),
    ("Omaha", -95.93, 41.25),
    ("Ottawa", -75.72, 45.40),
    ("Philadelphia", -75.17, 39.95),
    ("Phoenix", -112.07, 33.48),
    ("Pierre", -100.35, 44.37),
    ("Pittsburgh", -79.95, 40.45),
    ("Portland, ME", -70.25, 43.67),
    ("Portland, OR", -122.68, 45.52),
    ("Providence", -71.40, 41.83),
    ("Quebec", -71.18, 46.82),
    ("Raleigh", -78.65, 35.77),
    ("Reno", -119.82, 39.50),
    ("Richfield", -112.08, 38.77),
    ("Richmond", -77.48, 37.55),
    ("Roanoke", -79.95, 37.28),
    ("Sacramento", -121.50, 38.58),
    ("St. John", -66.17, 45.30),
    ("St. Louis", -90.20, 38.58),
    ("Salt Lake City", -111.90, 40.77),
    ("San Antonio", -98.55, 29.38),
    ("San Diego", -117.17, 32.70),
    ("San Francisco", -122.43, 37.78),
    ("San Jose", -121.88, 37.33),
    ("San Juan", -66.17, 18.50),
    ("Santa Fe", -105.95, 35.68),
    ("Savannah", -81.08, 32.08),
    ("Seattle", -122.33, 47.62),
    ("Shreveport", -93.70, 32.47),
    ("Sioux Falls", -96.73, 43.55),
    ("Sitka", -135.25, 57.17),
    ("Spokane", -117.43, 47.67),
    ("Springfield, IL", -89.63, 39.80),
    ("Springfield, MA", -72.57, 42.10),
    ("Springfield, MO", -93.28, 37.22),
    ("Syracuse", -76.13, 43.03),
    ("Tampa", -82.45, 27.95),
    ("Toledo", -83.55, 41.65),
    ("Toronto", -79.40, 43.67),
    ("Tulsa", -95.98, 36.15),
    ("Vancouver", -123.10, 49.22),
    ("Victoria", -123.35, 48.42),
    ("Virginia Beach", -75.97, 36.85),
    ("Washington D.C.", -77.03, 38.88),
    ("Wichita", -97.28, 37.72),
    ("Wilmington", -77.95, 34.23),
    ("Winnipeg", -97.12, 49.90)
]

POINTS_POP = 100
EPOCHS = 10000

ALL_POINTS = [(city[1], city[2]) for city in cities]


# Function to find the closest city to a given point
def find_closest_city(x, y, cities):
    closest_city = min(cities, key=lambda city: (city[1] - x)**2 + (city[2] - y)**2)
    return closest_city[0]

def find_city_coordinates(city_name, cities):
    for name, x, y in cities:
        if name.lower() == city_name.lower():
            return (x, y)
    return None

def get_user_input_cities():
    chosen_cities = []
    print("Enter up to 15 cities (or 'done' when finished, 'list' to see all cities):")
    while len(chosen_cities) < 15:
        city = input(f"Enter city #{len(chosen_cities) + 1} (or 'done'/'list'): ").strip()
        if city.lower() == 'done':
            if len(chosen_cities) < 2:
                print("Please enter at least 2 cities.")
                continue
            break
        if city.lower() == 'list':
            print("\n".join(sorted(city[0] for city in cities)))
            continue
        coords = find_city_coordinates(city, cities)
        if coords:
            chosen_cities.append((city, coords))
        else:
            print(f"City '{city}' not found. Please try again.")
    return chosen_cities

print("Please enter up to 15 cities to start with.")
user_chosen_cities = get_user_input_cities()

# Set CURR_POINTS based on user input
CURR_POINTS = [coords for _, coords in user_chosen_cities]

# Find the names of the chosen cities
chosen_cities = [find_closest_city(x, y, cities) for x, y in CURR_POINTS]

class Point():
    def __init__(self, x, y):
        global CURR_POINTS
        self.x = x
        self.y = y
        self.fitness = self.calculate_fitness(CURR_POINTS)

    def calculate_fitness(self, points):
        return sum(self.get_distance(point[0], point[1]) for point in points)
    
    def get_distance(self, x2, y2):
        return ((x2 - self.x)**2 + (y2 - self.y)**2)
    
    def crossover(self, other):
        global ALL_POINTS
        prob = random.random()
        
        if prob < 0.45:
            x, y = self.x, other.y
        elif 0.45 <= prob < 0.8:
            x, y = other.x, self.y
        else:
            x, y = random.choice(ALL_POINTS)

        return Point(x, y)

point_pool = [Point(p[0], p[1]) for p in random.choices(ALL_POINTS, k=POINTS_POP)]
gens = [point_pool[0]]

for gen in range(EPOCHS):
    sorted_pool = sorted(point_pool, key=lambda p: p.fitness)
    next_pool = sorted_pool[:10]
    
    for _ in range(90):
        parent_set_1 = random.choice(sorted_pool[:50])
        parent_set_2 = random.choice(sorted_pool[:50])
        child_p = parent_set_1.crossover(parent_set_2)
        next_pool.append(child_p)

    point_pool = next_pool

    if gen % 100 == 0:
        gens.append(sorted_pool[0])
    
    print(f"Generation: {gen+1}\nFitness: {sorted_pool[0].fitness}\nPoint: ({sorted_pool[0].x}, {sorted_pool[0].y})")

print(f"Final Generation: {EPOCHS}\nFitness: {sorted_pool[0].fitness}\nPoint: ({sorted_pool[0].x}, {sorted_pool[0].y})")

# Find the name of the city closest to the final point
final_city = find_closest_city(sorted_pool[0].x, sorted_pool[0].y, cities)

# Plotting
plt.figure(figsize=(20, 12))

# Plot all cities
city_x, city_y = zip(*ALL_POINTS)
plt.scatter(city_x, city_y, color='blue', s=10, label='All Cities')

# Plot selected points
selected_x, selected_y = zip(*CURR_POINTS)
plt.scatter(selected_x, selected_y, color='green', s=50, label='Selected Points')

# Label selected points
for i, (x, y) in enumerate(CURR_POINTS):
    plt.annotate(chosen_cities[i], (x, y), xytext=(5, 5), textcoords='offset points')

# Plot changes and draw orange lines
gen_x = [p.x for p in gens]
gen_y = [p.y for p in gens]
plt.scatter(gen_x[1:-1], gen_y[1:-1], color='orange', s=50, label='Intermediate Points')

# Draw orange lines from green points to orange points
for i, (x, y) in enumerate(zip(gen_x[1:-1], gen_y[1:-1])):
    for sx, sy in CURR_POINTS:
        plt.plot([sx, x], [sy, y], color='orange', alpha=0.7, linewidth=0.5)

# Plot final point and draw red lines
plt.scatter(gens[-1].x, gens[-1].y, color='red', s=50, label='Final Point')

# Label final point
plt.annotate(final_city, (gens[-1].x, gens[-1].y), xytext=(5, 5), textcoords='offset points')

# Draw red lines from green points to the final red point
for sx, sy in CURR_POINTS:
    plt.plot([sx, gens[-1].x], [sy, gens[-1].y], color='red', linewidth=1.5)

plt.title('World Cities with Genetic Algorithm Results', fontsize=20)
plt.xlabel('Longitude', fontsize=14)
plt.ylabel('Latitude', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
plt.legend()

# Add text box with information
info_text = f"Selected Cities:\n"
for city in chosen_cities:
    info_text += f"• {city}\n"
info_text += f"\nFinal Closest City:\n• {final_city}"

plt.text(0.02, 0.02, info_text, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()
