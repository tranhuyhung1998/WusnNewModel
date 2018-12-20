from common.point import *
import os, pickle, math, sys
import json
from pprint import pformat
# lib_path = os.path.abspath(os.path.join('..'))
# sys.path.append(lib_path)

# Unit: J
e_tx = 50*1e-9
e_rx = 50*1e-9
e_fs = 10*1e-12
e_da = 5*1e-12
e_mp = 0.0013*1e-12

# Num of bits
k_bit = 4000


class WusnInput:
    def __init__(self, _W, _H, _depth, _height, _num_of_relays, _num_of_sensors, _radius, _relays, _sensors, _BS):
        self.W = _W
        self.H = _H
        self.depth = _depth
        self.height = _height
        self.relays = _relays
        self.sensors = _sensors
        self.num_of_relays = _num_of_relays
        self.num_of_sensors = _num_of_sensors
        self.radius = _radius
        self.BS = _BS
        self.static_relay_loss = None
        self.dynamic_relay_loss = None
        self.sensor_loss = None
        # self.get_loss()
        self.calculate_loss()

    @classmethod
    def from_file(cls, path):
        f = open(path)
        d = json.load(f)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        W = d['W']
        H = d['H']
        depth = d['depth']
        height = d['height']
        num_of_relays = d['num_of_relays']
        num_of_sensors = d['num_of_sensors']
        radius = d['radius']
        relays = []
        sensors = []
        BS = Point.from_dict(d['center'])
        for i in range(num_of_sensors):
            sensors.append(SensorNode.from_dict(d['sensors'][i]))
        for i in range(num_of_relays):
            relays.append(RelayNode.from_dict(d['relays'][i]))
        # for _ in d['sensors']:
        #     sensors.append(Point.from_dict(_))
        # for _ in d['relays']:
        #     relays.append(Point.from_dict(_))
        return cls(W, H, depth, height, num_of_relays, num_of_sensors, radius, relays, sensors, BS)

    def to_dict(self):
        d = {}
        d['W'] = self.W
        d['H'] = self.H
        d['depth'] = self.depth
        d['height'] = self.height
        d['num_of_relays'] = self.num_of_relays
        d['num_of_sensors'] = self.num_of_sensors
        d['relays'] = self.relays
        d['sensors'] = self.sensors
        d['center'] = self.BS
        return d

    def to_file(self, file_path):
        d = self.to_dict()
        with open(file_path, "wt") as f:
            f.write(pformat(d))

    def get_loss(self):
        loss_file_name = str(hash(self)) + ".loss"
        list_loss_file = os.listdir("../cache")
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
        static_relay_loss = {}
        dynamic_relay_loss = {}
        R = self.radius
        BS = self.BS
        # print(BS.x)
        for sn in self.sensors:
            for rn in self.relays:
                if distance(sn, rn) <= 2*R:
                    sensor_loss[(sn, rn)] = k_bit * (e_tx + e_fs * math.pow(distance(sn, rn), 2))
        
        for rn in self.relays:
            dynamic_relay_loss[rn] = k_bit * (e_rx + e_da)
            static_relay_loss[rn] = k_bit * e_mp * math.pow(distance(rn, BS), 4)
        
        self.static_relay_loss = static_relay_loss
        self.dynamic_relay_loss = dynamic_relay_loss
        self.sensor_loss = sensor_loss

    def __hash__(self):
        return hash((self.W, self.H, self.depth, self.height, self.num_of_relays, self.num_of_sensors, self.radius,
                    tuple(self.relays), tuple(self.sensors)))


if __name__ == "__main__":
    inp = WusnInput.from_file('./small_data/dem1_0.in')
    print(inp.relays[0])

