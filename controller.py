#!/usr/bin/env python3
import time

class PID():

    def __init__(self, kp, ki, kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

    def init(self):

        self.prev_ts = time.time()
        self.current_ts = self.prev_ts

        self.p = 0
        self.i = 0
        self.d = 0

        self.last_err = 0
        self.err = 0

    def compute(self, answer, feedback):

        self.err = answer - feedback
        self.current_ts = time.time()

        self.p = self.err
        self.i += (self.current_ts - self.prev_ts) * self.err
        self.d = self.err - self.last_err

        self.prev_ts = self.current_ts
        self.last_err = self.err

        return self.kp * self.p + self.ki * self.i + self.kd * self.d

def y(t):
    return 0 if t < 100 else 1

if __name__ == '__main__':

    controller = PID(kp = 0.8, ki = 3, kd = 0.001)
    controller.init()
    feedback = 0

    i = 1

    while True:
        feedback = controller.compute(y(i), feedback)
        print(controller.err, feedback)

        time.sleep(0.02)
        i += 1
