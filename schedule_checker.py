import random

POP_SIZE = 200

POSSIBLE_TIMES = [((i/60)) for i in range(360, 1431, 15)]
POSSIBLE_DAYS = ['Su', 'M', 'T', 'W', 'Th', 'F', 'Sa']

# Sample restrictions

RESTRICTED_TIMES = [6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75]

SU_RESTRICTIONS = []
M_RESTRICTIONS = []
T_RESTRICTIONS = []
W_RESTRICTIONS= []
TH_RESTRICTIONS = []
F_RESTRICTIONS = []
SA_RESTRICTIONS = []

MW_CLASS_1 = [12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75]
MW_CLASS_2 = [16.0, 16.25, 16.5, 16.75, 17.0, 17.25, 17.5, 17.75]

M_TUTORING = [18.0, 18.25, 18.5, 18.75]

TT_CLASS_1 = [10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75]
TT_CLASS_2 = [14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75]

TH_CLUB = [18.0, 18.25, 18.5, 18.75, 19.0, 19.25, 19.5]

SU_RESTRICTIONS.append(RESTRICTED_TIMES)

M_RESTRICTIONS.append(RESTRICTED_TIMES)
M_RESTRICTIONS.append(MW_CLASS_1)
M_RESTRICTIONS.append(MW_CLASS_2)
M_RESTRICTIONS.append(M_TUTORING)

T_RESTRICTIONS.append(RESTRICTED_TIMES)
T_RESTRICTIONS.append(TT_CLASS_1)
T_RESTRICTIONS.append(TT_CLASS_2)

W_RESTRICTIONS.append(RESTRICTED_TIMES)
W_RESTRICTIONS.append(MW_CLASS_1)
W_RESTRICTIONS.append(MW_CLASS_2)

TH_RESTRICTIONS.append(RESTRICTED_TIMES)
TH_RESTRICTIONS.append(TT_CLASS_1)
TH_RESTRICTIONS.append(TT_CLASS_2)
TH_RESTRICTIONS.append(TH_CLUB)

F_RESTRICTIONS.append(RESTRICTED_TIMES)

SA_RESTRICTIONS.append(RESTRICTED_TIMES)

RESTRICTIONS = {
    'Su': SU_RESTRICTIONS,
    'M': M_RESTRICTIONS,
    'T': T_RESTRICTIONS,
    'W': W_RESTRICTIONS,
    'Th': TH_RESTRICTIONS,
    'F': F_RESTRICTIONS,
    'Sa': SA_RESTRICTIONS
}

DESIRED_HRS = float(input("Desired number of hours: "))
DESIRED_DAY = input("Desired day: ")
NEXT_BEST_DAY = input("Next best day: ")
DESIRED_START = float(input("Desired start time: "))

MAX_EPOCHS = 3000

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
        global NEXT_BEST_DAY

        cost = 0

        if self.day != DESIRED_DAY:
            cost += ((POSSIBLE_DAYS.index(self.day) - POSSIBLE_DAYS.index(DESIRED_DAY))**2)*10
            if self.day != NEXT_BEST_DAY:
                cost += ((POSSIBLE_DAYS.index(self.day) - POSSIBLE_DAYS.index(NEXT_BEST_DAY))**2)*5
            elif self.day == NEXT_BEST_DAY:
                cost = -5
        elif self.day == DESIRED_DAY:
            cost = -10

        if self.start != DESIRED_START:
            cost += ((self.start - DESIRED_START)**2)*10 + 5

        time_range = [i/100 for i in range(int(self.start*100), int(self.end*100+25), 25)]

        hrs = self.end - self.start

        if hrs != DESIRED_HRS:
            cost += ((hrs - DESIRED_HRS)**2)*100 + 5

        if hrs > DESIRED_HRS:
            cost += ((hrs - DESIRED_HRS)**2)*1000 + 5

        for re in RESTRICTIONS[self.day]:
            for tr in time_range:
                if tr in re:
                    cost += 500

        if self.start >= self.end:
            cost += 500

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

bd = sorted_event_pool[0].day

bdtimings = []

for r in RESTRICTIONS[sorted_event_pool[0].day]:
    bdrs = []
    for bdr in sorted(r):
        bdr = str(bdr)
        timing_b = bdr.split('.')
        h_b = timing_b[0]
        m_b = timing_b[1].replace('0', '00')
        m_b = m_b.replace('5', '30')
        m_b = m_b.replace('230', '15')
        m_b = m_b.replace('730', '45')
        bdrs.append(f"{h_b}:{m_b}")
    bdrstr = '\n'.join(b for b in bdrs)
    bdtimings.append(bdrstr+'\n')


st, e = str(sorted_event_pool[0].start), str(sorted_event_pool[0].end)
timing_st, timing_e = st.split('.'), e.split('.')
h_s, h_e = timing_st[0], timing_e[0]
m_s, m_e = timing_st[1].replace('0', '00'), timing_e[1].replace('0', '00')
m_s, m_e = m_s.replace('5', '30'), m_e.replace('5', '30')
m_s, m_e = m_s.replace('230', '15'), m_e.replace('230', '15')
m_s, m_e = m_s.replace('730', '45'), m_e.replace('730', '45')
stt = f"{h_s}:{m_s}"
edt = f"{h_e}:{m_e}"

bdall = '\n'.join(b for b in bdtimings)

print(f"Best day [{bd}] restrictions:\n{bdall}\n")

print(f"""Best day: {bd}
Best time: {stt} to {edt}""")
