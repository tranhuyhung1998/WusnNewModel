from GAwHeuristic.GA import *
from GAwHeuristic.heuristic import *
from common.input import *
from common.point import *
import time

if __name__ == "__main__":
    inp = WusnInput.from_file("data/small_data/uu-dem3_r30_1.in")
    # inp = WusnInput.from_file("data/small_data/" + str(uu-dem3_r30_1.in))
    # print(inp.BS)
    # print(inp)