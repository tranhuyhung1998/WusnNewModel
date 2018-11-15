from ortools.graph import pywrapgraph
from common.input import WusnInput
from copy import copy, deepcopy
from random import randint
from common.point import distance
import numpy as np 
import math

max_iteration = 1

def generate_random_sol(max_rn_conn, num_of_relays, num_of_sensors):  
    sol = copy(max_rn_conn)
    while(np.sum(sol) != num_of_sensors):
        x = randint(0,num_of_relays-1)
        if sol[x] > 0:
            sol[x] -= 1
    return sol

def ifValid(max_rn_conn, sol):
    return all(sol[i] <= max_rn_conn[i] and sol[i] >= 0 for i in range(len(sol)))

def cal_cost(inp: WusnInput, sol):
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
    cost = 0
    
    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    N = inp.num_of_sensors
    M = inp.num_of_relays
    R = inp.radius

    for i in range(N):
        min_cost_flow.AddArcWithCapacityAndUnitCost(0, i+1, 1, 0)
    
    for i in range(N):
        for j in range(M):
            if distance(sensors_arr[i], relays_arr[i]) <= 2*R:
                min_cost_flow.AddArcWithCapacityAndUnitCost(i+1, j+N+1, 1, inp.sensor_loss[(sensors_arr[i], relays_arr[i])])
    
    for j in range(M):
        min_cost_flow.AddArcWithCapacityAndUnitCost(j+N+1, N+M+1, sol[j], )



    return cost



def LS(inp: WusnInput):
    max_rn_conn = [inp.max_rn_conn[k] for k in inp.max_rn_conn]
    sol = generate_random_sol(max_rn_conn, inp.num_of_relays, inp.num_of_sensors)

    best_cost = math.inf
    best_sol = sol

    for k in range(max_iteration):
        sol = best_sol
        for i in range(len(sol)):
            for j in range(len(sol)):
                if i!=j:
                    solc = copy(sol)
                    solc[i], solc[j] = solc[i]+1, solc[j]-1
                    if ifValid(max_rn_conn, solc):
                        cost = cal_cost(inp, sol)
                        if cost < best_cost:
                            best_cost = cost
                            best_sol = sol
                        return
# if __name__ == '__main__':
#     print('asd')