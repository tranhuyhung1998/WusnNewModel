from GAwHeuristic.GA import *
from GAwHeuristic.heuristic import *
from common.input import *
from common.point import *
import time

if __name__ == "__main__":
    inp = WusnInput.from_file("data/small_data/uu-dem10_r50_1.in")
    print(inp.e_max)
    print(inp.BS)
    indi = random_init_individual(inp.num_of_relays)
    # print(out.loss())

    # res = GA(inp)

    # inp = res[0]
    # out = res[1]



    # print(inp)
    # print(len(out.used_relays))
    # print(len(out.mapping))
    # print(out.mapping)
    # print(out.used_relays)

    for a in out.mapping:
        print(out.inp.relays.index(out.mapping[a]))
    
    # print(out.inp.e_max, out.max_consumption())
    
    # inp = WusnInput.from_file("data/small_data/" + str(uu-dem3_r30_1.in))
    # print(inp.BS)
    # print(inp)