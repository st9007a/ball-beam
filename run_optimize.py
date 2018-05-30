#!/usr/bin/env python3
import time
import sys
from math import pi

from opt.bench import Bench
from opt.PSO import PSO_CW

from ballbeam import PID, BallBeam

if len(sys.argv) <= 1:
    print('Usage: python3 run_optimize.py [A] [R] [THETA]')
    print('')
    print('Example: python3 run_optimize.py 1 1 0.0564')
    exit()

A = int(sys.argv[1])
R = int(sys.argv[2])
THETA = float(sys.argv[3])

def expr(r, theta, a, kp, ki, kd):

    pid = PID(kp = kp, ki = ki, kd = kd)
    bb = BallBeam(r = r, theta = theta, a = a, b = 0.6)

    while True:
        pid.set_point = bb.yd()
        bb.feed(pid.output)
        pid.compute(bb.output)

        if abs(bb.output) > 4 or (bb.total_time) > 300:
            break

    return pid.objective_value / pid.total_time + max(300 - pid.total_time, 0)

def objective(vec):
    return expr(R, THETA, A, vec[0], vec[1], vec[2])

if __name__ == '__main__':

    optimizer = PSO_CW(c1 = 2, c2 = 2.1, num_particles = 100)
    bench_fn = Bench(dims = 3, func = objective, up = 1, low = 0, optima = 0)

    optimizer.optimize(iters = 10000, bench = bench_fn)
    print(optimizer.best_vec)
