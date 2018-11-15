from GAwHeuristic.GA import *
from GAwHeuristic.heuristic import *
from common.input import *
from common.point import *
import time

if __name__ == "__main__":
    # inp = WusnInput.from_file("small_data/dem3.in")
    # start = time.time()
    # indi = random_init_individual(inp.num_of_relays)
    # GA(inp)
    # a, b, c = heuristic(inp, indi)
    # print(a, b, c)
    # end = time.time()
    # print(end-start)

    f = open("small_data_result.txt", "w")
    file_list = os.listdir("small_data")
    for file_name in file_list:
        print(str(file_name))
        f.write(file_name + "\n")
        inp = WusnInput.from_file("small_data/" + str(file_name))
        start = time.time()
        res = GA(inp)
        end = time.time()
        print(end-start)
        f.write(str(res) + "\n")
        f.write(str(end-start) + "s" + "\n")
        print()
    f.close()

    # f = open("medium_data_result.txt", "w+")
    # file_list = os.listdir("medium_data")
    # for file_name in file_list:
    #     print(str(file_name))
    #     f.write(file_name + "\n")
    #     inp = WusnInput.from_file("medium_data/" + str(file_name))
    #     start = time.time()
    #     res = GA(inp)
    #     end = time.time()
    #     print(end-start)
    #     f.write(str(res) + "\n")
    #     f.write(str(end-start) + "s" + "\n")
    #     print()
    # f.close()