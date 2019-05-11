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
from copy import copy 

class State():
    def __init__(self, objective_value, cumulative_energy_consumption, solution):
        self.objective_value = objective_value
        self.cumulative_energy_consumption = cumulative_energy_consumption
        self.solution = solution
        
    def __lt__(self, other):
        return (self.objective_value, self.cumulative_energy_consumption) > (other.objective_value, other.cumulative_energy_consumption)

    def value(self):
        return (self.objective_value, self.cumulative_energy_consumption)

class FixedSizeOrderedStates():
    def __init__(self, size=5):
        self.size = size
        self.x = []
    
    def add(self, value):
        self.x.append(value)
        self.x = list(reversed(sorted(self.x)))[:self.size]

    def get(self, index):
        if index < self.size:
            return self.x[index]
        else:
            return None

    def worst_state(self):
        return (self.x[-1].objective_value, self.x[-1].cumulative_energy_consumption)
    
    def best_state(self):
        return (self.x[0].objective_value, self.x[0].cumulative_energy_consumption)

    def clear(self):
        self.x = []

class LocalSearch():
    def __init__(self, input_path, alpha=0.5, max_iteration = 1000, random_initial_state=0, candidate_size=5):
        self.inp = WusnInput.from_file(input_path)
        self.alpha = alpha
        self.max_iteration = max_iteration
        self.random_initial_state = random_initial_state
        self.candidate_size = candidate_size
        self.max_rn_conn = [self.inp.max_rn_conn[k] for k in self.inp.max_rn_conn]

        self.success = True
        self.best_value = None
        self.energy = None
        self.iter = None
        self.relays_used = None

    def initial_state(self):
        sol = []
        max_flow = None

        if self.random_initial_state == 0:
            sol = []
            max_flow = self.solve_max_flow(self.max_rn_conn, self.inp.radius)
            for i in range(max_flow.NumArcs()):
                if max_flow.Head(i) == self.inp.num_of_relays + self.inp.num_of_sensors + 1:
                    sol.append(max_flow.Flow(i))
        else:
            counter = 0

            while True:
                counter += 1
                if counter > 10000:
                    self.success = False
                    return None, None

                sol = copy(self.max_rn_conn)
                reduce_quantity = sum(sol) - self.inp.num_of_sensors

                while reduce_quantity != 0:
                    index = randint(0, self.inp.num_of_sensors - 1)
                    quant = randint(0, min(reduce_quantity, sol[index]))
                    sol[index] -= quant
                    reduce_quantity -= quant

                max_flow = self.BSR(sol)
                if max_flow == -1:
                    continue
                break

        return sol, max_flow

    def if_valid(self, sol, best_value):
        value = -float('inf')
        
        sensors_arr = [k for k in self.inp.sensors]
        relays_arr = [k for k in self.inp.relays]

        activated_relays = np.where(np.array(sol) > 0)[0]
        num_activated_relays = len(activated_relays)
        
        for i in range(len(activated_relays)):
            relay_idx = activated_relays[i]
            value = max([value, self.inp.static_relay_loss[relays_arr[relay_idx]] +
                        sol[relay_idx]*self.inp.dynamic_relay_loss[relays_arr[relay_idx]]])

        return all(sol[i] <= self.max_rn_conn[i] and sol[i] >= 0 for i in range(len(sol))) and num_activated_relays * self.alpha / self.inp.num_of_relays + value * (1 - self.alpha) / self.inp.e_max <= best_value

    def solve_max_flow(self, sol, dist):
        max_flow = pywrapgraph.SimpleMaxFlow()

        sensors_arr = [k for k in self.inp.sensors]
        relays_arr = [k for k in self.inp.relays]

        N, M = self.inp.num_of_sensors, self.inp.num_of_relays

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


    def BSR(self, sol):
        R, N = self.inp.radius, self.inp.num_of_sensors
        min_r, left, right = R, 0, R

        mid = (left+right)/2

        if(self.solve_max_flow(sol, R).OptimalFlow() < N):
            return -1

        while(right-left > 1e-6):
            if(self.solve_max_flow(sol, mid).OptimalFlow() < N):
                left = mid
            else:
                right = mid
                min_r = mid
            mid = (left + right)/2

        return self.solve_max_flow(sol, min_r)


    def cal_value(self, max_flow, sol):
        sensors_arr = [k for k in self.inp.sensors]
        relays_arr = [k for k in self.inp.relays]

        value = -float('inf')
        sum = 0

        activated_relays = np.where(np.array(sol) > 0)[0]
        num_activated_relays = len(activated_relays)

        for i in range(len(activated_relays)):
            relay_idx = activated_relays[i]
            value = max([value, self.inp.static_relay_loss[relays_arr[relay_idx]] +
                        sol[relay_idx]*self.inp.dynamic_relay_loss[relays_arr[relay_idx]]])
            sum += self.inp.static_relay_loss[relays_arr[relay_idx]] + \
                sol[relay_idx]*self.inp.dynamic_relay_loss[relays_arr[relay_idx]]

        for i in range(max_flow.NumArcs()):
            if max_flow.Tail(i) <= self.inp.num_of_sensors and max_flow.Tail(i) > 0 and max_flow.Flow(i) > 0:
                tail, head = max_flow.Tail(
                    i)-1, max_flow.Head(i)-1-self.inp.num_of_sensors
                value = max(value, self.inp.sensor_loss[(
                    sensors_arr[tail], relays_arr[head])])
                sum += self.inp.sensor_loss[(sensors_arr[tail], relays_arr[head])]

        return num_activated_relays * self.alpha / self.inp.num_of_relays + value * (1 - self.alpha) / self.inp.e_max, sum

    def cal_energy(self, max_flow, sol):
        sensors_arr = [k for k in self.inp.sensors]
        relays_arr = [k for k in self.inp.relays]

        value = -float('inf')
        sum = 0

        activated_relays = np.where(np.array(sol) > 0)[0]

        for i in range(len(activated_relays)):
            relay_idx = activated_relays[i]
            value = max([value, self.inp.static_relay_loss[relays_arr[relay_idx]] +
                        sol[relay_idx]*self.inp.dynamic_relay_loss[relays_arr[relay_idx]]])
            sum += self.inp.static_relay_loss[relays_arr[relay_idx]] + \
                sol[relay_idx]*self.inp.dynamic_relay_loss[relays_arr[relay_idx]]

        for i in range(max_flow.NumArcs()):
            if max_flow.Tail(i) <= self.inp.num_of_sensors and max_flow.Tail(i) > 0 and max_flow.Flow(i) > 0:
                tail, head = max_flow.Tail(
                    i)-1, max_flow.Head(i)-1-self.inp.num_of_sensors
                value = max(value, self.inp.sensor_loss[(
                    sensors_arr[tail], relays_arr[head])])
                sum += self.inp.sensor_loss[(sensors_arr[tail], relays_arr[head])]

        return value

    def isSolvable(self):
        N, M, R = self.inp.num_of_sensors, self.inp.num_of_relays, self.inp.radius

        sensors_arr = [k for k in self.inp.sensors]
        relays_arr = [k for k in self.inp.relays]

        for i in range(N):
            ok = False
            for j in range(M):
                if distance(sensors_arr[i], relays_arr[j]) <= 2*R:
                    ok = True
                    break
            if ok == False:
                return False
        return True


    def search(self):
        if self.isSolvable() == False:
            return False

        candidates = FixedSizeOrderedStates(size=self.candidate_size)
        
        sol, max_flow = self.initial_state()
        if self.success == False:
            return None

        best_value, best_sum = self.cal_value(max_flow, sol)
        best_sol = sol
        
        k = 0
        for k in range(self.max_iteration):
            candidates.add(State(best_value, best_sum, sol))
            #move
            for i in range(len(sol)):
                for j in range(len(sol)):
                    if i != j:
                        solc = copy(best_sol)

                        if self.max_rn_conn[i] <= solc[i] + solc[j]:
                            solc[i] = solc[i] + solc[j]
                            solc[j] = 0
                        else:
                            continue

                        if self.if_valid(solc, candidates.worst_state()[0]):
                            max_flow = self.BSR(solc)
                            if max_flow == -1:
                                continue                            
                            value, sum = self.cal_value(max_flow, solc)
                            if (value, sum) < candidates.worst_state():
                                candidates.add(State(value, sum, solc))

            #move 1 connection
            for i in range(len(sol)):
                for j in range(len(sol)):
                    if i != j:
                        solc = copy(best_sol)
                        solc[i], solc[j] = solc[i]+1, solc[j]-1

                        if self.if_valid(solc, candidates.worst_state()[0]):
                            max_flow = self.BSR(solc)
                            if max_flow == -1:
                                continue                            
                            value, sum = self.cal_value(max_flow, solc)

                            if (value, sum) < candidates.worst_state():
                                candidates.add(State(value, sum, solc))

            #swap connections
            for i in range(len(sol)):
                for j in range(len(sol)):
                    if i < j:
                        solc = copy(best_sol)
                        if solc[i] == solc[j]:
                            continue
                        solc[i], solc[j] = solc[j], solc[i]

                        if self.if_valid(solc, candidates.worst_state()[0]):
                            max_flow = self.BSR(solc)
                            if max_flow == -1:
                                continue                            
                            value, sum = self.cal_value(max_flow, solc)
                            
                            if (value, sum) < candidates.worst_state():
                                candidates.add(State(value, sum, solc))            

            #share connections
            for i in range(len(sol)):
                for j in range(len(sol)):
                    if i != j:
                        solc = copy(best_sol)
                        total_conn = solc[i] + solc[j]
                        if self.max_rn_conn[i] + self.max_rn_conn[j] == 0: 
                            continue

                        oldi = solc[i]
                        solc[i] = math.ceil(total_conn * self.max_rn_conn[i]/(self.max_rn_conn[i] + self.max_rn_conn[j]))
                        solc[j] = total_conn - solc[i]

                        if solc[i] == oldi:
                            continue

                        if self.if_valid(solc, candidates.worst_state()[0]):
                            max_flow = self.BSR(solc)
                            if max_flow == -1:
                                continue                            
                            if (value, sum) < candidates.worst_state():
                                candidates.add(State(value, sum, solc))

            if (candidates.best_state() == (best_value, best_sum)) == False:
                state = candidates.get(randint(0, len(candidates.x)-1))

                while (state.value() == (best_value,best_sum)):
                    state = candidates.get(randint(0, len(candidates.x)-1))

                best_sol = state.solution
                best_value = state.objective_value
                best_sum = state.cumulative_energy_consumption
            else:
                break
                
            candidates.clear()

        self.best_value = best_value
        self.relays_used = len(np.where(np.array(best_sol) > 0)[0])
        self.energy = self.cal_energy(self.BSR(best_sol), best_sol)
        self.iter = k + 1

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--alpha', type=float, default=0.5,
                        help='Alpha coefficient')
    # parser.add_argument('--outdir', type=str, default='data/small_data/LS')
    parser.add_argument('--indir', type=str, default='small_data')
    parser.add_argument('--init', type=int, default=0, help='random initialization flags')
    return parser.parse_args()


if __name__ == '__main__':
    if "small_data_result.txt" in os.listdir("."):
        os.remove("small_data_result.txt")
    args_ = parse_arguments()

    dirpath = ""
    if args_.init == 1:
        dirpath = os.path.join('data', args_.indir, 'random_init_results')
    else:
        dirpath = os.path.join('data', args_.indir, 'flow_init_results')

    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    for i in range(1,21):
        print("{} Times".format(i))
        outpath = os.path.join(dirpath, 'LS{}'.format(i))

        if os.path.exists(outpath):
            continue

        file_list = os.listdir(os.path.join('data', args_.indir))

        for file_name in file_list:
            if not file_name.endswith('.in'):
                continue

            outpath = os.path.join(dirpath, '{}_{}.out'.format(file_name.split('.')[0], i))
            if os.path.exists(outpath):
                continue
            print(file_name)
            ls = LocalSearch(os.path.join("data",args_.indir,str(file_name)), alpha = args_.alpha, random_initial_state = args_.init)

            ls.search()

            best_value, relays_used, energy, iter = ls.best_value, ls.relays_used, ls.energy, ls.iter

            with open(outpath, 'w+') as f:
                f.write('{} {} {} {} {} {}\n'.format(file_name, best_value, relays_used, energy, ls.inp.e_max, iter))