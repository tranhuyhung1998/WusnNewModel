import pulp
import glob
import numpy as np

from argparse import ArgumentParser
from pulp import LpVariable
from concurrent.futures import ProcessPoolExecutor

import common.input as cinp
import common.point as point

from common.input import WusnInput


def model_lp(inp: WusnInput, alpha=0.5):
    sensor_loss = inp.sensor_loss
    sensors, relays = list(inp.sensors), list(inp.relays)
    n, m = inp.num_of_sensors, inp.num_of_relays
    E_Rx, E_Da = cinp.E_Rx, cinp.E_Da
    e_mp = cinp.e_fs
    C = _get_conn_matrix(sensor_loss, sensors, relays)
    Et = _get_sn_loss_matrix(sensor_loss, sensors, relays)
    dB = _get_bs_distances(relays, inp.base_station)
    Emax = _get_emax(Et, dB, cinp.k_bit, E_Rx, E_Da, e_mp)

    prob = pulp.LpProblem('RelaySelection', pulp.LpMinimize)

    # Variables
    Z = [LpVariable('z_%d' % j, lowBound=0, upBound=1, cat=pulp.LpBinary) for j in range(m)]
    Z = np.asarray(Z, dtype=object)
    A = []
    for i in range(n):
        row = [LpVariable('a_%d_%d' % (i, j), lowBound=0, upBound=1, cat=pulp.LpBinary) for j in range(m)]
        A.append(row)
    A = np.asarray(A, dtype=object)
    Ex = LpVariable('Ex', lowBound=0)
    Er = [LpVariable('Er_%d' % j) for j in range(m)]
    Er = np.asarray(Er, dtype=object)

    # Constraints
    for j in range(m):
        asum = sum(A[:, j])
        prob += (Er[j] == (cinp.k_bit * (asum * (E_Rx + E_Da) + e_mp * (dB[j] ** 4))))
        prob += ((asum - Z[j] * n) <= 0)
        prob += (asum >= Z[j])
        prob += (Ex >= Er[j])
    for i in range(n):
        prob += (sum(A[i]) == 1)
    for i in range(n):
        for j in range(m):
            prob += (A[i, j] <= C[i, j])
            prob += (Ex >= A[i, j])

    Cx = alpha / m * sum(Z) + (1 - alpha) / Emax * Ex
    prob.setObjective(Cx)

    return prob


def _get_bs_distances(relays, base_station):
    ds = []
    for rn in relays:
        ds.append(point.distance(rn, base_station))
    return ds


def _get_emax(sn_loss_mat, bs_distance, l, E_Rx, E_Da, e_fs):
    n, m = sn_loss_mat.shape
    vals = list(sn_loss_mat.flatten())
    for d in bs_distance:
        vals.append(l * (n * (E_Rx + E_Da) + e_fs * (d ** 4)))

    return max(vals)


def _get_sn_loss_matrix(sensor_loss, sensors, relays):
    n, m = len(sensors), len(relays)
    mat = np.zeros(n, m, dtype=np.float)
    for i, sn in enumerate(sensors):
        for j, rn in enumerate(relays):
            if (sn, rn) in sensor_loss.keys():
                mat[i, j] = sensor_loss[(sn, rn)]
    return mat


def _get_conn_matrix(sensor_loss, sensors, relays,):
    n, m = len(sensors), len(relays)
    mat = np.zeros(n, m, dtype=np.int)
    for i, sn in enumerate(sensors):
        for j, rn in enumerate(relays):
            if (sn, rn) in sensor_loss.keys():
                mat[i, j] = 1
    return mat


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument(dest='input', nargs='+', help='Input files. Accept globs as input.')
    parser.add_argument('-p', '--procs', type=int, default=4, help='Number of processes to fork')

    return parser.parse_args()

