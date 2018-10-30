
# heuristic: tim ra ket noi tieu hao nang luong lon nhat
# GA: tim ra ca the co tieu hao nang luong nho nhat

import random, time, os, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from .heuristic import *


GEN = 100
CP = 0.8
MP = 0.05
NUM_OF_INDIVIDUALS = 500
TERMINATE = 50

def random_init_individual(num_relay):
    "Initial individual with any num of relay"
    indi = []
    Y = random.randint(1, num_relay)
    xs = Y/num_relay
    count_relay = 0
    for i in range(0, num_relay):
        xx = random.random()
        if xx < xs:
            indi.append(1)
        else:
            indi.append(0)
    return indi

def count_current_relay(individual):
    sum = 0
    for g in individual:
        if g == 1:
            sum += 1
    return sum

# mom and dad instead of parent1 and parent2 =)
def cross(mom, dad):
    num_relay = len(mom)
    mid = random.randint(0, num_relay-1)
    child1 = mom[:mid] + dad[mid:]
    child2 = dad[:mid] + mom[mid:]
    return child1, child2


def mutate(original):
    fake = original[:]
    ll = len(fake)
    count1 = 0
    count2 = 0
    id1 = random.randint(0, ll-1)
    while fake[id1] == 0:
        count1 += 1
        id1 = random.randint(0, ll-1)
        if count1 >= 10:
            break
    id2 = random.randint(0, ll-1)
    while fake[id2] == 1:
        count2 += 1
        id2 = random.randint(0, ll-1)
        if count2 >= 10:
            break
    fake[id1], fake[id2] = fake[id2], fake[id1]
    return fake

def GA(inp: WusnInput) -> int:
    # Khoi tao quan the
    individuals = []

    # Cac ca the da duoc tinh toan
    calculated = {}

    max_value = -float("inf")
    max_num_relay = -float("inf")

    for i in range (0, NUM_OF_INDIVIDUALS):
        indi = random_init_individual(inp.num_of_relays)
        config, value, final_num_relay = heuristic(inp, indi)
        if value > max_value and value != 9999:
            max_value = value
        if final_num_relay > max_num_relay and final_num_relay!= 9999:
            max_num_relay = final_num_relay
        calculated[str(indi)] = [config, value, final_num_relay]
        individuals.append([indi, config, value, final_num_relay])

    print(individuals[0])
    
    count_stable = 0
    max_c = individuals[0][2]
    prev_max = individuals[0][2]

    # Iterate through generations
    for it in range(0, GEN):
        start = time.time()
        none = 0
        not_none = 0
        # Crossover and mutation
        for id1 in range(0, NUM_OF_INDIVIDUALS):
            id2 = 0
            xx = random.random()
            if xx < CP:
                id2 = random.randint(0, NUM_OF_INDIVIDUALS-1)
                while id2 == id1:
                    id2 = random.randint(0, NUM_OF_INDIVIDUALS-1)
                son, daughter = cross(individuals[id1][0], individuals[id2][0])

                if str(son) in calculated:
                    config1 = calculated[str(son)][0]
                    cost1 = calculated[str(son)][1]
                    final_num_relay1 = calculated[str(son)][2]
                else:
                    s = time.time()
                    config1, cost1, final_num_relay1 = heuristic(inp, son)
                    t = time.time()
                    
                if str(daughter) in calculated:
                    config2 = calculated[str(daughter)][0]
                    cost2 = calculated[str(daughter)][1]
                    final_num_relay2 = calculated[str(daughter)][2]
                else:
                    s = time.time()
                    config2, cost2, final_num_relay2 = heuristic(inp, daughter)
                    t = time.time()

                if cost1 > max_value and cost1 != 9999:
                    max_value = cost1
                if cost2 > max_value and cost2 != 9999:
                    max_value = cost2
                if final_num_relay1 > max_value and final_num_relay1 != 9999:
                    max_num_relay = final_num_relay1
                if final_num_relay2 > max_value and final_num_relay2 != 9999:
                    max_num_relay = final_num_relay2

                if config1 == None:
                    none += 1
                else: 
                    not_none += 1
                if config2 == None:
                    none += 1
                else:
                    not_none += 1

                # config1, cost1 = tabu_search(inp, son)
                # config2, cost2 = tabu_search(inp, daughter)
                individuals.append([son, config1, cost1, final_num_relay1])
                individuals.append([daughter, config2, cost2, final_num_relay2])
                xx2 = random.random()
                if xx2 < MP:
                    grand_child1 = mutate(son)
                    grand_child2 = mutate(daughter)
                    m_config1, m_cost1, m_final_num_relay1 = heuristic(inp, grand_child1)
                    m_config2, m_cost2, m_final_num_relay2 = heuristic(inp, grand_child2)
                    if m_cost1 > max_value and m_cost1 != 9999:
                        max_value = m_cost1
                    if m_cost2 > max_value and m_cost2 != 9999:
                        max_value = m_cost2
                    if m_final_num_relay1 > max_value and m_final_num_relay1 != 9999:
                        max_num_relay = m_final_num_relay1
                    if m_final_num_relay2 > max_value and m_final_num_relay2 != 9999:
                        max_num_relay = m_final_num_relay2
                    individuals.append([grand_child1, m_config1, m_cost1, m_final_num_relay1])
                    individuals.append([grand_child2, m_config2, m_cost2, m_final_num_relay2])
        print(max_value)
        individuals2 = sorted(individuals, key=lambda x: (x[2]/max_value + x[3]/max_num_relay))
        individuals = individuals2[:NUM_OF_INDIVIDUALS]
        if individuals[0][2] < max_c:
            max_c = individuals[0][2]
        if individuals[0][2] == prev_max:
            count_stable += 1
        else:
            count_stable = 0
        if count_stable == TERMINATE:
            print("TERMINATE")
            break
        prev_max = individuals[0][2]
        end = time.time()
        print("none: %d, not_none: %d" % (none, not_none))
        print("Gen: %d, time: %fs, min: %f %f" % (it, end - start, individuals[0][2]/max_value+individuals[0][3]/max_num_relay, individuals[NUM_OF_INDIVIDUALS-1][2]/max_value+individuals[NUM_OF_INDIVIDUALS-1][3]/max_num_relay))
    # print(max_c)
    return individuals[0]

# Bo sung dieu kien SN va RN co ket noi duoc voi nhau hay khong bang cach them ban kinh sn va rn
