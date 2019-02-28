import os
import time
from ortools.graph import pywrapgraph
from common.input import WusnInput
from copy import copy, deepcopy
from random import randint
from common.point import distance
import numpy as np
import math
from common.output import WusnOutput
from argparse import ArgumentParser

max_iteration = 100


def get_initial_state(inp: WusnInput, max_rn_conn):
    sol = []

    max_flow = solve_max_flow(inp, max_rn_conn, inp.radius)

    for i in range(max_flow.NumArcs()):
        if max_flow.Head(i) == inp.num_of_relays + inp.num_of_sensors + 1:
            sol.append(max_flow.Flow(i))
    return sol, max_flow

def ifValid(inp: WusnInput, max_rn_conn, sol, best_value, alpha=0.5):
    value = -float('inf')
    
    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    activated_relays = np.where(np.array(sol) > 0)[0]
    num_activated_relays = len(activated_relays)
    
    for i in range(len(activated_relays)):
        relay_idx = activated_relays[i]
        value = max([value, inp.static_relay_loss[relays_arr[relay_idx]] +
                     sol[relay_idx]*inp.dynamic_relay_loss[relays_arr[relay_idx]]])

    return all(sol[i] <= max_rn_conn[i] and sol[i] >= 0 for i in range(len(sol))) and num_activated_relays * alpha / inp.num_of_relays + value * (1 - alpha) / inp.e_max <= best_value

def solve_max_flow(inp: WusnInput, sol, dist):
    max_flow = pywrapgraph.SimpleMaxFlow()

    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    N, M, R = inp.num_of_sensors, inp.num_of_relays, inp.radius

    for i in range(N):
        max_flow.AddArcWithCapacity(0, i+1, 1)

    for i in range(N):
        for j in range(M):
            if distance(sensors_arr[i], relays_arr[j]) <= 2*dist:
                max_flow.AddArcWithCapacity(i+1, j+N+1, 1)

    for j in range(M):
        max_flow.AddArcWithCapacity(j+N+1, N+M+1, sol[j])

    if max_flow.Solve(0, N+M+1) == max_flow.OPTIMAL:
        return max_flow
    else:
        return -1


def BSR(inp: WusnInput, sol):
    R, N = inp.radius, inp.num_of_sensors
    min_r, left, right = R, 0, R

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


def cal_value(inp: WusnInput, max_flow, sol, alpha):
    sensors_arr = [k for k in inp.sensors]
    relays_arr = [k for k in inp.relays]

    value = -float('inf')
    sum = 0

    activated_relays = np.where(np.array(sol) > 0)[0]
    num_activated_relays = len(activated_relays)

    for i in range(len(activated_relays)):
        relay_idx = activated_relays[i]
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

    # out = WusnOutput(inp)
    # for i in range(max_flow.NumArcs()):
    #     if max_flow.Tail(i) <= inp.num_of_sensors and max_flow.Tail(i) > 0 and max_flow.Flow(i) > 0:
    #         tail, head = max_flow.Tail(
    #             i)-1, max_flow.Head(i)-1-inp.num_of_sensors
    #         out.assign(relays_arr[head], sensors_arr[tail])

    return num_activated_relays * alpha / inp.num_of_relays + value * (1 - alpha) / inp.e_max, sum


def isSolvable(inp: WusnInput):
    N, M, R = inp.num_of_sensors, inp.num_of_relays, inp.radius

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


def LS(inp: WusnInput, alpha):
    if isSolvable(inp) == False:
        return False
    max_rn_conn = [inp.max_rn_conn[k] for k in inp.max_rn_conn]
    sol, max_flow = get_initial_state(inp, max_rn_conn)

    best_value, best_sum = cal_value(inp, max_flow, sol, alpha)
    best_sol = sol
    print('Iteration: ', 0)
    print('Best value: {}. Best sum: {}'.format(best_value, best_sum))
    print('Best solution: {}\n'.format(best_sol))
    for k in range(max_iteration):
        sol_k = best_sol
        value_k = best_value
        sum_k = best_sum
        #move 1 connection
        for i in range(len(sol)):
            for j in range(len(sol)):
                if i != j:
                    solc = copy(best_sol)
                    solc[i], solc[j] = solc[i]+1, solc[j]-1

                    if ifValid(inp, max_rn_conn, solc, best_value, alpha):
                        max_flow = BSR(inp, solc)
                        if max_flow == -1:
                            continue
                        value, sum = cal_value(
                            inp, max_flow, solc, alpha)
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
        
        #swap connections
        for i in range(len(sol)):
            for j in range(len(sol)):
                if i < j:
                    solc = copy(best_sol)
                    if solc[i] == solc[j]:
                        continue
                    solc[i], solc[j] = solc[j], solc[i]

                    if ifValid(inp, max_rn_conn, solc, best_value, alpha):
                        max_flow = BSR(inp, solc)
                        if max_flow == -1:
                            continue
                        value, sum = cal_value(
                            inp, max_flow, solc, alpha)
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
        
        #share connections
        for i in range(len(sol)):
            for j in range(len(sol)):
                if i != j:
                    solc = copy(best_sol)
                    total_conn = solc[i] + solc[j]
                    if max_rn_conn[i] + max_rn_conn[j] == 0: 
                        continue

                    oldi = solc[i]
                    solc[i] = math.ceil(total_conn * max_rn_conn[i]/(max_rn_conn[i] + max_rn_conn[j]))
                    solc[j] = total_conn - solc[i]

                    if solc[i] == oldi:
                        continue

                    if ifValid(inp, max_rn_conn, solc, best_value, alpha):
                        max_flow = BSR(inp, solc)
                        if max_flow == -1:
                            continue
                        value, sum = cal_value(
                            inp, max_flow, solc, alpha)
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

        if(value_k == best_value and sum_k == best_sum):
            break
        else:
            best_sol = sol_k
            best_value = value_k
            best_sum = sum_k

        print('Iteration: ', k+1)
        print('Best value: {}. Best sum: {}'.format(
            best_value, best_sum))
        print('Best solution: {}\n'.format(best_sol))
    print('-------------------------')
    return best_value


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--alpha', type=float, default=0.5,
                        help='Alpha coefficient')
    # parser.add_argument('--outdir', type=str, default='data/small_data/LS')
    parser.add_argument('--indir', type=str,default='small_data')
    return parser.parse_args()


if __name__ == '__main__':
    if "small_data_result.txt" in os.listdir("."):
        os.remove("small_data_result.txt")
    args_ = parse_arguments()
    f = open(os.path.join('data', args_.indir, 'LS{}'.format(str(int(args_.alpha*10)))), 'w+')
    # f = open(os.path.join('data', args_.indir, 'LS'), 'w+')
    file_list = os.listdir(os.path.join('data',args_.indir))
    for file_name in file_list:
        if file_name == 'BOUND' or 'LS' in file_name or file_name == '.DS_Store':
            continue
        print(file_name)
        inp = WusnInput.from_file(os.path.join("data",args_.indir,str(file_name)))
        f.write('{0} {1:.3f}\n'.format(file_name, inp.e_max))#LS(inp, args_.alpha)))
    
    f.close()