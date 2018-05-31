#!/usr/bin/env python3
import os
import json
from ballbeam import PID, BallBeam


if __name__ == '__main__':

    if not os.path.isdir('visualize/log'):
        os.makedirs('visualize/log')

    with open('result.csv', 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        params = [float(token) for token in line.rstrip('\n').split(',')]
        print(params)

        controller = PID(kp = params[4], ki = params[5], kd = params[6], time_units = 0.02)
        environment = BallBeam(r = params[2], theta = params[3], a = params[0], b = params[1], time_units = 0.02)

        log = []

        while True:
            controller.set_point = environment.yd()

            environment.feed(controller.output)
            controller.compute(environment.output)

            log.append({'t': environment.total_time, 'r': environment.x1, 'theta': environment.x3})

            if abs(environment.x1) > 4 or environment.total_time > 300:
                break

        with open('visualize/log/a_%d_r_%d_theta_%.4f.json' % (int(params[0]), int(params[2]), params[3]), 'w') as j:
            json.dump(log, j, indent = 4)
