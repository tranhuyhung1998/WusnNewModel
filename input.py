from point import *
import os, pickle, gen_small_data, math

# Unit: J
E_Tx = 50*1e-9
E_Rx = 50*1e-9
e_fs = 10*1e-12

# Num of bits
k_bit = 4000

# Radius
R = 100
class WusnInput:
    def __init__(self, _W, _H, _depth, _height, _num_of_relays, _num_of_sensors, _relays, _sensors, _Y, _base_station):
        self.W = _W
        self.H = _H
        self.depth = _depth
        self.height = _height
        self.relays = _relays
        self.sensors = _sensors
        self.num_of_relays = _num_of_relays
        self.num_of_sensors = _num_of_sensors
        self.Y = _Y
        self.base_station = _base_station
        self.relay_loss = None
        self.sensor_loss = None
        self.get_loss()

    @classmethod
    def from_file(cls, path):
        f = open(path)
        line1 = f.readline().split(' ')
        W = float(line1[0])
        H = float(line1[1])
        line2 = f.readline().split(' ')
        depth = float(line2[0])
        height = float(line2[1])
        line3 = f.readline().split(' ')
        num_of_relays = int(line3[0])
        num_of_sensors = int(line3[1])
        Y = int(line3[2])
        relays = []
        sensors = []
        for i in range(num_of_relays):
            line = f.readline()[:-2].split(' ')
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])
            relays.append(RelayNode(x, y, z))
        for i in range(num_of_sensors):
            line = f.readline()[:-2].split(' ')
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])
            sensors.append(SensorNode(x, y, z))
        BS_info = f.readline()[:-2].split(' ')
        x_centa = float(BS_info[0])
        y_centa = float(BS_info[1])
        z_centa = float(BS_info[2])
        BS = Point(x_centa, y_centa, z_centa)
        return WusnInput(W, H, depth, height, num_of_relays, num_of_sensors, relays, sensors, Y, BS)

    def get_loss(self):
        loss_file_name = str(hash(self)) + ".loss"
        list_loss_file = os.listdir("cache")
        if loss_file_name in list_loss_file:
            print("Loading cache from %s" % loss_file_name)
            f = open("cache/" + loss_file_name, "rb")
            data = pickle.load(f)
            self.relay_loss = data[0]
            self.sensor_loss = data[1]
        else:
            print("Cache not found, calculating loss")
            self.calculate_loss()

    def create_cache(self):
        loss_file_name = str(hash(self)) + ".loss"
        list_loss_file = os.listdir("cache")
        if loss_file_name in list_loss_file:
            print("Cache exist")
        else:
            print("Creating cache")
            f = open("cache/" + loss_file_name, "wb")
            self.calculate_loss()
            data = [self.relay_loss, self.sensor_loss]
            pickle.dump(data, f)
            f.close()

    def calculate_loss(self):
        sensor_loss = {}
        relays_loss = {}
        BS = self.base_station
        for sn in self.sensors:
            for rn in self.relays:
                if (distance(sn, rn) <= 2*R):
                    sensor_loss[(sn, rn)] = k_bit*(E_Tx + e_fs*math.pow(distance(sn, rn), 2))
        
        for rn in self.relays:
            relays_loss[rn] = k_bit*(E_Rx + e_fs*math.pow(distance(rn, BS), 2))
        
        self.relay_loss = relays_loss
        self.sensor_loss = sensor_loss

    def __hash__(self):
        return hash((self.W, self.H, self.depth, self.height, self.num_of_relays, self.num_of_sensors, 
                    self.Y, tuple(self.relays), tuple(self.sensors)))


if __name__ == "__main__":
    inp = WusnInput.from_file("small_data/dem1.in")

