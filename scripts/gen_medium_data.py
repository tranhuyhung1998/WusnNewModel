import os, random, math, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from common.dems_input import *
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
        print("Generating small data for %s\n" % file_name)
        for r in range(len(radius)):
            inp.scale(101, 101, 5)
            new_file_name = file_name.split('.')[0]
            f = open("../small_data/" + new_file_name  + "_" + str(r) + ".in", "w")
            f.write(str(W) + " " + str(H) + "\n")
            f.write(str(depth) + " " + str(height) + "\n")
            f.write(str(num_of_relays) + " " + str(num_of_sensors) + "\n")
            f.write(str(radius[r]) + "\n")

            x_centa = 0
            y_centa = 0

            for i in range(num_of_relays):
                x = random.random() * W
                y = random.random() * H
                z = estimate(x, y, inp) + height
                x_centa += x
                y_centa += y
                f.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            for i in range(num_of_sensors):
                x = random.random() * W
                y = random.random() * H
                z = estimate(x, y, inp) - depth
                x_centa += x
                y_centa += y
                f.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            x_centa /= num_of_relays + num_of_sensors
            y_centa /= num_of_relays + num_of_sensors
            z_centa = estimate(x_centa, y_centa, inp)
            f.write(str(x_centa) + " " + str(y_centa) + " " + str(z_centa) + "\n")
            f.close()

