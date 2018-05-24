#!/usr/bin/env python3
import json
import time
from math import sin, cos, pi

class PID():

    def __init__(self, kp, ki, kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.sample_time = 0.01
        self.curr_ts = time.time()
        self.prev_ts = self.curr_ts

        self.init()

    def init(self):

        self.set_point = 0.0

        self.p = 0.0
        self.i = 0.0
        self.d = 0.0

        self.last_err = 0
        self.err = 0

        self.windup_guard = 20.0
        self.output = 0.0

    def compute(self, feedback):

        self.err = self.set_point - feedback
        self.curr_ts = time.time()

        delta_time = self.curr_ts - self.prev_ts
        delta_err = self.err - self.last_err


        if delta_time >= self.sample_time:
            self.p = self.err
            self.i += delta_time * self.err

            if self.i > self.windup_guard:
                self.i = self.windup_guard
            elif self.i < -self.windup_guard:
                self.i = -self.windup_guard

            self.d = delta_err / delta_time

        self.prev_ts = self.curr_ts
        self.last_err = self.err

        self.output = self.kp * self.p + self.ki * self.i + self.kd * self.d
        if self.output > 20 * pi / 180:
            self.output = 20 * pi / 180
        elif self.output < -20 * pi / 180:
            self.output = -20 * pi / 180

class BallBeam():

    def __init__(self, r, theta, a, b):

        self.a = a
        self.B = b

        self.x1 = r
        self.x2 = 0.0
        self.x3 = theta
        self.x4 = 0.0

        self.init()

    def init(self):

        self.G = 9.81

        self.curr_ts = time.time()
        self.start_ts = self.curr_ts
        self.prev_ts = self.curr_ts

    def feed(self, u):

        self.curr_ts = time.time()
        delta_time = self.curr_ts - self.prev_ts

        x1_dot = self.x2
        x2_dot = self.B * (self.x1 * self.x4 * self.x4 - self.G * sin(self.x3))
        x3_dot = self.x4
        x4_dot = u

        self.x1 += x1_dot * delta_time
        self.x2 += x2_dot * delta_time
        self.x3 += x3_dot * delta_time
        self.x4 += x4_dot * delta_time

        self.prev_ts = self.curr_ts
        self.output = self.x1

    def yd(self):
        return self.a * cos(pi * (time.time() - self.start_ts) / 5)


if __name__ == '__main__':

    pid = PID(kp = 0.6, ki = 0.07, kd = 0.004)
    bb = BallBeam(r = 1, theta = 0.0564, a = 1, b = 0.6)

    log = []

    start_ts = time.time()

    while True:
        pid.set_point = bb.yd()
        bb.feed(pid.output)
        pid.compute(bb.output)

        time.sleep(0.02)

        print(bb.x1, bb.x3 * 180 / pi, pid.set_point, pid.output * 180 / pi, pid.i)
        log.append({'t': time.time() - start_ts, 'r': bb.x1, 'theta': bb.x3})

        if abs(bb.output) > 4:
            break

    # with open('log.json', 'w') as j:
    #     json.dump(log, j, indent = 4)
