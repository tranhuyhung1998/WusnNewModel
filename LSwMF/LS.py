from ortools.graph import pywrapgraph
from common.input import WusnInput
from copy import copy, deepcopy
from random import randint
from common.point import distance
import numpy as np
import math

max_iteration = 100


def get_initial_state(inp: WusnInput, max_rn_conn):
    sol = []

    max_flow = solve_max_flow(inp, max_rn_conn, inp.radius)

    for i in range(max_flow.NumArcs()):
        if max_flow.Head(i) == inp.num_of_relays + inp.num_of_sensors + 1:
            sol.append(max_flow.Flow(i))
    # print('num of rns: {}. max_rn_conn: {}. len: {}'.format(inp.num_of_relays, len(max_rn_conn), len(sol)))
    return sol, max_flow


def ifValid(max_rn_conn, sol):
    return all(sol[i] <= max_rn_conn[i] and sol[i] >= 0 for i in range(len(sol)))


def solve_max_flow(inp: WusnInput, sol, dist):
    max_flow = pywrapgraph.SimpleMaxFlow()

    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    N = inp.num_of_sensors
    M = inp.num_of_relays
    R = inp.radius

    for i in range(N):
        max_flow.AddArcWithCapacity(0, i+1, 1)

    for i in range(N):
        for j in range(M):
            if distance(sensors_arr[i], relays_arr[j]) <= 2*dist:
                max_flow.AddArcWithCapacity(i+1, j+N+1, 1)

    # print(len(sol))
    # print(M)
    for j in range(M):
        max_flow.AddArcWithCapacity(j+N+1, N+M+1, sol[j])

    if max_flow.Solve(0, N+M+1) == max_flow.OPTIMAL:
        return max_flow
    else:
        return -1


def BSR(inp: WusnInput, sol):
    R = inp.radius
    N = inp.num_of_sensors
    min_r = R
    left = 0
    right = R
    mid = (left+right)/2

    if(solve_max_flow(inp, sol, R).OptimalFlow() < N):
        return -1

    while(right-left > 1e-6):
        if(solve_max_flow(inp, sol, mid).OptimalFlow() < N):
            left = mid
        else:
            right = mid
            min_r = mid
        mid = (left + right)/2

    return solve_max_flow(inp, sol, min_r)


def cal_value(inp: WusnInput, max_flow, sol):
    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    value = -1
    sum = 0

    activated_relays = np.where(np.array(sol) > 0)[0]
    num_activated_relays = len(activated_relays)
    for i in range(len(activated_relays)):
        relay_idx = activated_relays[i]
        # print(relay_idx)
        value = max([value, inp.static_relay_loss[relays_arr[relay_idx]] +
                     sol[relay_idx]*inp.dynamic_relay_loss[relays_arr[relay_idx]]])
        sum += inp.static_relay_loss[relays_arr[relay_idx]] + \
            sol[relay_idx]*inp.dynamic_relay_loss[relays_arr[relay_idx]]
    
    for i in range(max_flow.NumArcs()):
        if max_flow.Tail(i) <= inp.num_of_sensors and max_flow.Tail(i) > 0 and max_flow.Flow(i) > 0:
            tail, head = max_flow.Tail(
                i)-1, max_flow.Head(i)-1-inp.num_of_sensors
            value = max(value, inp.sensor_loss[(
                sensors_arr[tail], relays_arr[head])])
            sum += inp.sensor_loss[(sensors_arr[tail], relays_arr[head])]

    return value, sum


def isSolvable(inp: WusnInput):
    N = inp.num_of_sensors
    M = inp.num_of_relays
    R = inp.radius

    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    for i in range(N):
        ok = False
        for j in range(M):
            if distance(sensors_arr[i], relays_arr[j]) <= 2*R:
                ok = True
                break
        if ok == False:
            return False
    return True


def LS(inp: WusnInput):
    if isSolvable(inp) == False:
        return False
    max_rn_conn = [inp.max_rn_conn[k] for k in inp.max_rn_conn]
    sol, max_flow = get_initial_state(inp, max_rn_conn)

    best_value, best_sum = cal_value(inp, max_flow, sol)
    best_sol = sol
    print('Iteration: ', 0)
    print('Best value: {}. Best sum: {}'.format(best_value, best_sum))
    print('Best solution: {}\n'.format(best_sol))
    for k in range(max_iteration):
        sol_k = best_sol
        value_k = best_value
        sum_k = best_sum
        for i in range(len(sol)):
            for j in range(len(sol)):
                if i != j:
                    solc = copy(best_sol)
                    solc[i], solc[j] = solc[i]+1, solc[j]-1

                    if ifValid(max_rn_conn, solc):
                        max_flow = BSR(inp, solc)
                        if max_flow == -1:
                            continue
                        value, sum = cal_value(inp, max_flow, solc)
                        if value < value_k:
                            sum_k = sum
                            value_k = value
                            sol_k = solc
                        else:
                            if value == value_k:
                                if sum < sum_k:
                                    sum_k = sum
                                    value_k = value
                                    sol_k = solc

        # print(value_k, sum_k)
        # print(best_value, best_sum)
        if(value_k == best_value and sum_k == best_sum):
            break
        else:
            best_sol = sol_k
            best_value = value_k
            best_sum = sum_k
        print('Iteration: ', k+1)
        print('Best value: {}. Best sum: {}'.format(best_value, best_sum))
        print('Best solution: {}\n'.format(best_sol))
    print('-------------------------')

# if __name__ == '__main__':
#     print('asd')
