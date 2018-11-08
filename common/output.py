import json

from common.input import WusnInput
from common.point import SensorNode, RelayNode


class WusnOutput:
    def __init__(self, inp: WusnInput, mapping=None):
        if mapping is None:
            mapping = {}

        self.inp = inp
        self.mapping = mapping

    def assign(self, relay, sensor):
        if relay not in self.mapping.keys():
            self.mapping[relay] = set()
        self.mapping[relay].add(sensor)

    def to_dict(self):
        inp_dict = self.inp.to_dict()
        mapping = list(self.mapping.items())
        mapping = map(lambda x: (x[0].to_dict(), x[1].to_dict()), mapping)
        mapping = dict(mapping)

        d = {
            'input': inp_dict,
            'mapping': mapping
        }

        return d

    @classmethod
    def from_dict(cls, d):
        inp = WusnInput.from_dict(d['inp'])
        mapping = list(d['mapping'].items())
        mapping = map(lambda x: (SensorNode.from_dict(x[0]), RelayNode.from_dict(x[1])), mapping)
        mapping = dict(mapping)
        return cls(inp, mapping)

    def save(self, path):
        with open(path, 'wt') as f:
            json.dump(self.to_dict(), f)
