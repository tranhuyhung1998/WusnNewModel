import os, random, math, sys, json
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from common.dems_input import *
from common.input import *
from common.point import *
from pprint import pformat
from scipy import interpolate

# Config
W = 500.000
H = 500.000
depth = 1
height = 10
num_of_sensors = 100
num_of_relays = 100
radius = [25, 30, 35, 40, 45, 50]

# Calculate height by interpolation
def estimate(x, y, inp: DemsInput):
    id1 = math.floor(x/inp.cellsize)
    id2 = math.floor(y/inp.cellsize)
    xx = [id1 * inp.cellsize, (id1+1) * inp.cellsize]
    yy = [id2 * inp.cellsize, (id2+1) * inp.cellsize]
    z = [[inp.height[id1][id2], inp.height[id1][id2+1]], [inp.height[id1+1][id2], inp.height[id1+1][id2+1]]]
    plane = interpolate.interp2d(xx, yy, z)
    return plane(x, y)[0]

if __name__ == "__main__":
    dems = os.listdir("../dems_data")
    dems = list(filter(lambda x: x.endswith(".asc"), dems))
    
    for file_name in dems:
        inp = DemsInput.from_file("../dems_data/" + str(file_name))
        print("Generating medium data for %s\n" % file_name)
        inp.scale(101, 101, 5)
        for r in range(len(radius)):
            new_file_name = file_name.split('.')[0] + "_" + str(r)
            data_dictionary = {}
            data_dictionary['W'] = W
            data_dictionary['H'] = H
            data_dictionary['depth'] = depth
            data_dictionary['height'] = height
            data_dictionary['num_of_relays'] = num_of_relays
            data_dictionary['num_of_sensors'] = num_of_sensors
            data_dictionary['radius'] = radius[r]
            data_dictionary['relays'] = []
            data_dictionary['sensors'] = []
            x_centa = 0
            y_centa = 0
            for i in range(num_of_relays):
                x = random.random() * W
                y = random.random() * H
                z = estimate(x, y, inp) + height
                new_relay = RelayNode(x, y, z)
                x_centa += x
                y_centa += y
                data_dictionary['relays'].append(new_relay.to_dict())
            for i in range(num_of_sensors):
                x = random.random() * W
                y = random.random() * H
                z = estimate(x, y, inp) - depth
                new_sensor = SensorNode(x, y, z)
                x_centa += x
                y_centa += y
                data_dictionary['sensors'].append(new_sensor.to_dict())
            x_centa /= num_of_relays + num_of_sensors
            y_centa /= num_of_relays + num_of_sensors
            z_centa = estimate(x_centa, y_centa, inp)
            data_dictionary['center'] = Point(x_centa, y_centa, z_centa).to_dict()
            # inpp = WusnInput(W, H, depth, height, num_of_relays, num_of_sensors, data_dictionary['relays'], data_dictionary['sensors'], data_dictionary['center'])
            
            with open("../medium_data/" + new_file_name + ".in", "wt") as f:
                f.write(json.dumps(data_dictionary, indent=2))