import os, sys
from ortools.graph import pywrapgraph
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from common.input import *

def generate_connect_matrix(inp: WusnInput, max_num, relays):
    R = inp.radius
    connect = {}
    for rn in relays:
        count = 0
        for sn in inp.sensors:
            if distance(sn, rn) <= 2*R:
                count += 1
                connect[(sn, rn)] = 1
        if count == 0:
            return False
    return connect

def max_flow(inp: WusnInput, max_num, rns):
    start_nodes = []
    end_nodes = []
    capacities = []
    source = inp.num_of_relays + inp.num_of_sensors + 1
    sink = inp.num_of_relays + inp.num_of_sensors + 2
    
    for i in rns:
        start_nodes.append(source)
        end_nodes.append(i)
        capacities.append(max_num[inp.relays[i]])

    for i in rns:
        for j in range(inp.num_of_sensors):
            if distance(inp.relays[i], inp.sensors[j]) <= 2*inp.radius:
                start_nodes.append(i)
                end_nodes.append(j+inp.num_of_relays) 
                capacities.append(1)

    for i in range(inp.num_of_sensors):
        start_nodes.append(i+inp.num_of_relays)   
        end_nodes.append(sink)
        capacities.append(1)
    
    for i in range(len(start_nodes)):
        print(start_nodes[i], end_nodes[i], capacities[i])

    mf = pywrapgraph.SimpleMaxFlow()

    for i in range(0, len(start_nodes)):
        mf.AddArcWithCapacity(start_nodes[i], end_nodes[i], capacities[i])

    if mf.Solve(source, sink) == mf.OPTIMAL:
        print('Max flow:', mf.OptimalFlow())
        print('')
        print('  Arc    Flow / Capacity')
        for i in range(mf.NumArcs()):
            if mf.Flow(i) != 0:
                print('%1s -> %1s   %3s  / %3s' % (
                    mf.Tail(i),
                    mf.Head(i),
                    mf.Flow(i),
                    mf.Capacity(i)))
        print('Source side min-cut:', mf.GetSourceSideMinCut())
        print('Sink side min-cut:', mf.GetSinkSideMinCut())
    else:
        print('There was an issue with the max flow input.')