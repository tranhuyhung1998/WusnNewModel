from GAwHeuristic.GA import *
from GAwHeuristic.heuristic import *
from common.input import *
from common.point import *
import time

if __name__ == "__main__":
    inp = WusnInput.from_file("data/small_data/uu-dem3_r30_1.in")
    indi = random_init_individual(inp.num_of_relays)
    out = heuristic(inp, indi)

    res = GA(inp)

    print(out)
    print(out.loss())
    print(len(out.used_relays))
    # inp = WusnInput.from_file("data/small_data/" + str(uu-dem3_r30_1.in))
    # print(inp.BS)
    # print(inp)