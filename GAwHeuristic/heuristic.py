import os, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from input import *

def get_relay_list(individual):
    relay_list = []
    ll = len(individual)
    for i in range(ll):
        if individual[i] == 1:
            relay_list.append(i)
    return relay_list

def generate_connect_matrix(inp: WusnInput, individual):
    "Check if there is a sensor can't connect to any relay and whether sensor can connect to relay or not at the same time"
    connect = {}
    for sn in inp.sensors:
        count = 0
        for i in range (0, len(individual)):
            if individual[i] == 1:
                if distance(sn, inp.relays[i]) <= 2*R:
                    connect[(sn, inp.relays[i])] = 1
                    count += 1
        if count == 0:
            return False
    return connect

def heuristic(inp: WusnInput, individual):
    connect = generate_connect_matrix(inp, individual)
    if connect == False:
        return None, 9999, 9999
    relay_list = get_relay_list(individual)
    num_sensors_to_relay = [0] * len(individual)
    basic_relays_loss = inp.relay_loss
    sensor_loss = inp.sensor_loss
    selected_relay_list = []

    num_sensors = inp.num_of_sensors
    config = [0]*num_sensors
    value = -float("inf")

    config = [0]*inp.num_of_sensors
    for i in range(inp.num_of_sensors):
        min_max = float("inf")
        selected_id = 0
        for rn_id in relay_list:
            if (inp.sensors[i], inp.relays[rn_id]) in connect:
                loss1 = sensor_loss[(inp.sensors[i], inp.relays[rn_id])]
                loss2 = (num_sensors_to_relay[rn_id] + 1) * basic_relays_loss[inp.relays[rn_id]]
                local_max = max(loss1, loss2)
                if local_max < min_max:
                    min_max = local_max
                    selected_id = rn_id
        config[i] = selected_id
        num_sensors_to_relay[selected_id] += 1
        if selected_id not in selected_relay_list:
            selected_relay_list.append(selected_id)
        if min_max > value:
            value = min_max
    return config, value, len(selected_relay_list)