from LSwMF import LS
import os, time
from common.input import WusnInput

if __name__ == '__main__':
    if "small_data_result.txt" in os.listdir("."):
        os.remove("small_data_result.txt")
    f = open("small_data_result_ls.txt", "w+")
    file_list = os.listdir("small_data")
    for file_name in file_list:
        # print(str(file_name))
        # f.write(file_name + "\n")
        inp = WusnInput.from_file("small_data/" + str(file_name))
        LS(inp)
        # print(inp.base_station)
        # start = time.time()
        # res = GA(inp)
        # end = time.time()
        # print(end-start)
        # f.write(str(res) + "\n")
        # f.write(str(end-start) + "s" + "\n")
        # print()
        # break
    f.close()