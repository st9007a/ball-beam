#!/usr/bin/env python3
import time
from math import pi

from opt.bench import Bench
from opt.PSO import StandardPSO

from ballbeam import PID, BallBeam

def expr(r, theta, a, kp, ki, kd):

    pid = PID(kp = kp, ki = ki, kd = kd)
    bb = BallBeam(r = r, theta = theta, a = a, b = 0.6)

    start_ts = time.time()
    curr_ts = start_ts

    while True:
        pid.set_point = bb.yd()
        bb.feed(pid.output)
        pid.compute(bb.output)

        curr_ts = time.time()

        if abs(bb.output) > 4 or (curr_ts - start_ts) > 15:
            break

        time.sleep(0.02)

    return abs(pid.i) + 1 / (curr_ts - start_ts)

def objective(vec):
    return expr(1, 0.0564, 1, vec[0], vec[1], vec[2])

if __name__ == '__main__':

    optimizer = StandardPSO(c1 = 0.5, c2 = 0.5, num_particles = 50)
    bench_fn = Bench(dims = 3, func = objective, up = 5, low = -5, optima = 0)

    optimizer.optimize(iters = 50, bench = bench_fn)
    print(optimizer.best_vec)
