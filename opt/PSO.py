#!/usr/bin/env python3
import numpy as np

from random import uniform
from math import inf

class StandardPSO():

    def __init__(self, num_particles, c1, c2):

        self.num_particles = num_particles
        self.c1 = c1
        self.c2 = c2

    @property
    def best_vec(self):
        return self.gbest_vec

    def init(self, bench):
        self.history = []

        mean = (bench.up + bench.low) / 2
        std = (bench.up - bench.low) / 6
        self.particles = np.random.normal(mean, std, [self.num_particles, bench.dims])

        # truncated
        np.clip(self.particles, bench.low, bench.up, out = self.particles)

        self.speed = np.random.normal(0, 1, [self.num_particles, bench.dims])

        self.pbest_val = np.zeros([self.num_particles])
        self.pbest_val.fill(-inf)

        self.pbest_vec = [None] * self.num_particles

        self.gbest_val = -inf
        self.gbest_vec = None


    def compute(self, iters, bench):
        for idx, vec in enumerate(self.particles):
            score = self.fitness_score(bench, list(vec))

            if score > self.pbest_val[idx]:
                self.pbest_val[idx] = score
                self.pbest_vec[idx] = list(vec)

            if score > self.gbest_val:
                self.gbest_val = score
                self.gbest_vec = list(vec)
                self.history.append({'iter': iters, 'vec': self.gbest_vec, 'val': bench.eval(self.gbest_vec)})

    def compute_speed(self, speed, idx, iters, r1, r2):
        return speed + self.c1 * r1 * (self.pbest_vec[idx] - self.particles[idx]) + self.c2 * r2 * (self.gbest_vec - self.particles[idx])

    def fitness_score(self, bench, vec):
        return 1 / ((bench.eval(vec) - bench.optima) ** 2 + 1e-4)

    def step(self, iters, bench):

        self.compute(iters, bench)

        for idx, speed in enumerate(self.speed):
            r1 = uniform(0, 1)
            r2 = uniform(0, 1)
            self.speed[idx] = self.compute_speed(speed, idx, iters, r1, r2)

        for idx in range(self.num_particles):
            self.particles[idx] += self.speed[idx]

        np.clip(self.particles, bench.low, bench.up, out = self.particles)

    def optimize(self, iters, bench):

        self.init(bench)

        for i in range(iters):
            self.step(i, bench) 
            print('step %05d: %s' % (i, self.best_vec))

        self.compute(iters, bench)

    def mean_fitness_last_iter(self, bench):
        total = 0

        for idx, vec in enumerate(self.particles):
            score = self.fitness_score(bench, list(vec))
            total += score

        return total / len(self.particles)
