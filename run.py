#!/usr/bin/env python3
import time
from math import pi

from opt.bench import Bench
from opt.PSO import PSO_CW

from ballbeam import PID, BallBeam

def expr(r, theta, a, kp, ki, kd):

    pid = PID(kp = kp, ki = ki, kd = kd)
    bb = BallBeam(r = r, theta = theta, a = a, b = 0.6)

    while True:
        pid.set_point = bb.yd()
        bb.feed(pid.output)
        pid.compute(bb.output)

        if abs(bb.output) > 4 or (bb.total_time) > 30:
            break

    return pid.objective_value / pid.total_time

def objective(vec):
    return expr(2, 0.1129, 1, vec[0], vec[1], vec[2])

if __name__ == '__main__':

    optimizer = PSO_CW(c1 = 2, c2 = 2.1, num_particles = 100)
    bench_fn = Bench(dims = 3, func = objective, up = 10, low = 0, optima = 0)

    optimizer.optimize(iters = 10000, bench = bench_fn)
    # optimizer.optimize(iters = 1000000, bench = bench_fn, set_vec = [0.764178799, 0.277689114, 0.0])
    print(optimizer.best_vec)
