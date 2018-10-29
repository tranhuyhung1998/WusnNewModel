import pulp
from input import *

def model_lp(inp: WusnInput):
    loss = inp.relay_loss
    prob = pulp.LpProblem('RelaySelection')
    N, M, Y = inp.num_of_sensors, inp.num_of_relays, inp.Y

    