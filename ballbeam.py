#!/usr/bin/env python3
import os
import json
import time
from math import sin, cos, pi

class PID():

    def __init__(self, kp, ki, kd, time_units = 0.02):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.time_units = time_units

        self.init()

    def init(self):

        self.set_point = 0.0
        self.total_time = 0.0

        self.p = 0.0
        self.i = 0.0
        self.d = 0.0

        self.last_err = 0
        self.err = 0

        self.windup_guard = 20.0
        self.output = 0.0

        self.objective_value = 0

    def compute(self, feedback):

        self.err = self.set_point - feedback
        self.total_time += self.time_units

        self.objective_value += abs(self.err)

        delta_err = self.err - self.last_err

        self.p = self.err
        self.i += self.time_units * self.err

        if self.i > self.windup_guard:
            self.i = self.windup_guard
        elif self.i < -self.windup_guard:
            self.i = -self.windup_guard

        self.d = delta_err / self.time_units

        self.last_err = self.err

        self.output = self.kp * self.p + self.ki * self.i + self.kd * self.d
        if self.output > 20 * pi / 180:
            self.output = 20 * pi / 180
        elif self.output < -20 * pi / 180:
            self.output = -20 * pi / 180

class BallBeam():

    def __init__(self, r, theta, a, b, time_units = 0.02):

        self.a = a
        self.B = b

        self.x1 = r
        self.x2 = 0.0
        self.x3 = theta
        self.x4 = 0.0
        self.time_units = time_units

        self.init()

    def init(self):

        self.G = 9.81
        self.total_time = 0.0

    def feed(self, u):

        self.total_time += self.time_units

        x1_dot = self.x2
        x2_dot = self.B * (self.x1 * self.x4 * self.x4 - self.G * sin(self.x3))
        x3_dot = self.x4
        x4_dot = u

        self.x1 += x1_dot * self.time_units
        self.x2 += x2_dot * self.time_units
        self.x3 += x3_dot * self.time_units
        self.x4 += x4_dot * self.time_units

        self.output = self.x1

    def yd(self):
        return self.a * cos(pi * self.total_time / 5)


if __name__ == '__main__':

    pid = PID(kp = 0.04493496178999861, ki = 0.13718478597047323, kd = 0.6137969905270756, time_units = 0.02)
    bb = BallBeam(r = 3, theta = 0.1698, a = 2, b = 0.6, time_units = 0.02)

    log = []

    if not os.path.isdir('log'):
        os.makedirs('log')

    while True:
        pid.set_point = bb.yd()
        bb.feed(pid.output)
        pid.compute(bb.output)

        log.append({'t': bb.total_time, 'r': bb.x1, 'theta': bb.x3})

        if abs(bb.output) > 4:
            break

    with open('visualize/log/log_a2_cond3.json', 'w') as j:
        json.dump(log, j, indent = 4)
