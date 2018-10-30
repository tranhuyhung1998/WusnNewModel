import pulp
import glob
import numpy as np

from argparse import ArgumentParser
from pulp import LpVariable
from concurrent.futures import ProcessPoolExecutor

import common.input as cinp

from common.input import WusnInput


def model_lp(inp: WusnInput):
    loss = inp.relay_loss
    n, m = inp.num_of_sensors, inp.num_of_relays
    E_Rx, E_Da = cinp.E_Rx, cinp.E_Da

    prob = pulp.LpProblem('RelaySelection', pulp.LpMinimize)


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument(dest='input', nargs='+', help='Input files. Accept globs as input.')
    parser.add_argument('-p', '--procs', type=int, default=4, help='Number of processes to fork')

    return parser.parse_args()

