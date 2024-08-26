import random

POP_SIZE = 200

POSSIBLE_TIMES = [((i/60)) for i in range(360, 1431, 15)]
POSSIBLE_DAYS = ['Su', 'M', 'T', 'W', 'Th', 'F', 'Sa']

# Sample restrictions

RESTRICTED_TIMES = POSSIBLE_TIMES[:8]

MW_RESTRICTIONS = POSSIBLE_TIMES[16:24]
MW_RESTRICTIONS.extend(POSSIBLE_TIMES[32:40])
MW_RESTRICTIONS.extend(RESTRICTED_TIMES)

TT_RESTRICTIONS = POSSIBLE_TIMES[24:32]
TT_RESTRICTIONS.extend(POSSIBLE_TIMES[40:48])
TT_RESTRICTIONS.extend(RESTRICTED_TIMES)

RESTRICTIONS = {
    'Su': RESTRICTED_TIMES,
    'M': MW_RESTRICTIONS,
    'T': TT_RESTRICTIONS,
    'W': MW_RESTRICTIONS,
    'Th': TT_RESTRICTIONS,
    'F': RESTRICTED_TIMES,
    'Sa': RESTRICTED_TIMES
}

DESIRED_HRS = int(input("Desired number of hours: "))
DESIRED_DAY = input("Desired day: ")
DESIRED_START = float(input("Desired start time: "))

MAX_EPOCHS = 1000

class Event():

    def __init__(self, day, start, end):

        self.day = day
        self.start = start
        self.end = end
        self.cost = self.get_cost()

    def get_cost(self):

        global RESTRICTIONS
        global DESIRED_HRS
        global DESIRED_DAY
        global DESIRED_START
        global POSSIBLE_TIMES

        cost = 0

        if self.start != DESIRED_START:
            cost += (self.start - DESIRED_START)**2 + 5

        hrs = self.end - self.start

        if hrs != DESIRED_HRS:
            cost += (hrs - DESIRED_HRS)**2 + 5

        if self.day != DESIRED_DAY:
            cost += (POSSIBLE_DAYS.index(self.day) - POSSIBLE_DAYS.index(DESIRED_DAY))**2

        if self.start in RESTRICTIONS[self.day]:
            cost += 30

        if self.start == self.end:
            cost += 20

        return cost
    
    def crossover(self, parent):

        global POSSIBLE_DAYS
        global POSSIBLE_TIMES

        prob = random.random()

        child_day = self.day
        child_start = self.start
        child_end = self.end

        if prob < 0.3:
            child_day = parent.day
        elif 0.3 <= prob < 0.5:
            child_start = parent.start
        elif 0.5 <= prob < 0.8:
            child_end = parent.end
        else:
            child_start = random.choice(POSSIBLE_TIMES)
            child_day = random.choice(POSSIBLE_DAYS)
            child_end = random.choice(POSSIBLE_TIMES)

        return child_day, child_start, child_end
    
event_pool = []

for _ in range(POP_SIZE):
    event_pool.append(Event(random.choice(POSSIBLE_DAYS), random.choice(POSSIBLE_TIMES), random.choice(POSSIBLE_TIMES)))

gen = 0

while True:

    sorted_event_pool = sorted(event_pool, key=lambda e: abs(e.cost))

    if sorted_event_pool[0].cost == 0 or gen == MAX_EPOCHS:
        break

    new_event_pool = sorted_event_pool[:20]

    for i in range(180):
        par1 = random.choice(sorted_event_pool[:100])
        par2 = random.choice(sorted_event_pool[:100])
        child_day, child_start, child_end = par1.crossover(par2)
        new_event_pool.append(Event(child_day, child_start, child_end))

    event_pool = new_event_pool

    gen += 1

    print(f"Generation: {gen}\nCost: {event_pool[0].cost}\n")

name = "Lunch"

ddrs = []
bdrs = []

bd = sorted_event_pool[0].day

for ddr, bdr in zip(sorted(RESTRICTIONS[DESIRED_DAY]), sorted(RESTRICTIONS[sorted_event_pool[0].day])):
    ddr, bdr = str(ddr), str(bdr)
    timing_d, timing_b = ddr.split('.'), bdr.split('.')
    h_d, h_b = timing_d[0], timing_b[0]
    m_d, m_b = timing_d[1].replace('0', '00'), timing_b[1].replace('0', '00')
    m_d, m_b = m_d.replace('5', '30'), m_b.replace('5', '30')
    m_d, m_b = m_d.replace('230', '15'), m_b.replace('230', '15')
    m_d, m_b = m_d.replace('730', '45'), m_b.replace('730', '45')
    ddrs.append(f"{h_d}:{m_d}")
    bdrs.append(f"{h_b}:{m_b}")

ddrstr = '\n'.join(d for d in ddrs)
bdrstr = '\n'.join(b for b in bdrs)

st, e = str(sorted_event_pool[0].start), str(sorted_event_pool[0].end)
timing_st, timing_e = st.split('.'), e.split('.')
h_s, h_e = timing_st[0], timing_e[0]
m_s, m_e = timing_st[1].replace('0', '00'), timing_e[1].replace('0', '00')
m_s, m_e = m_s.replace('5', '30'), m_e.replace('5', '30')
m_s, m_e = m_s.replace('230', '15'), m_e.replace('230', '15')
m_s, m_e = m_s.replace('730', '45'), m_e.replace('730', '45')
stt = f"{h_s}:{m_s}"
edt = f"{h_e}:{m_e}"

print(f"Desired day [{DESIRED_DAY}] restrictions:\n{ddrstr}\n")

print(f"Best day [{bd}] restrictions:\n{bdrstr}\n")

print(f"""Name: {name}\nBest day: {bd}
Best time: {stt} to {edt}""")
