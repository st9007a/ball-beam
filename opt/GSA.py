#!/usr/bin/env python3
import numpy as np

from random import uniform
from math import inf, log
from heapq import nlargest

class GSA():

    def __init__(self, num_agents, g, kbest, kbest_decay = 1e-3, g_decay = 1e-2, epsilon = 1e-4):
        self.g = g
        self.g_decay = g_decay
        self.kbest = kbest
        self.kbest_decay = kbest_decay
        self.epsilon = epsilon
        self.num_agents = num_agents

    def init(self, bench):
        self.history = []

        self.mass_score = [0] * self.num_agents
        self.mass = [0] * self.num_agents

        self.best_vec = None
        self.best_score = -inf

        mean = (bench.up + bench.low) / 2
        std = (bench.up - bench.low) / 6
        self.particles = np.random.normal(mean, std, [self.num_agents, bench.dims])

        # truncated
        np.clip(self.particles, bench.low, bench.up, out = self.particles)

        self.speed = np.random.normal(0, 1, [self.num_agents, bench.dims])

    def fitness_score(self, bench, vec):
        return 1 / (abs(bench.eval(list(vec)) - bench.optima) + self.epsilon)

    def compute_mass_score(self, iters, bench, vec):
        score = self.fitness_score(bench, vec)
        # score = -log(abs(bench.eval(list(vec)) - bench.optima) + 1e-4)

        if score > self.best_score:
            self.best_score = score
            self.best_vec = list(vec)
            self.history.append({'iter': iters, 'vec': self.best_vec, 'val': bench.eval(self.best_vec)})

        return score

    def mass_param(self):

        best = max(self.mass_score)
        worst = min(self.mass_score)

        mass = 0

        for f in self.mass_score:
            mass += (f - worst + self.epsilon) / (best - worst)

        return mass, best, worst

    def step(self, iters, bench):

        # Evaluate fitness score
        for idx, pos in enumerate(self.particles):
            self.mass_score[idx] = self.compute_mass_score(iters, bench, pos)

        # Update G, kbest, best, worst
        g = self.g * (1 - self.g_decay) ** iters
        kbest = int(self.kbest * (1 - self.kbest_decay) ** iters)
        mass_sum, best, worst = self.mass_param()

        # Update mass
        for i in range(self.num_agents):
            self.mass[i] = (self.mass_score[i] - worst + 1e-4) / (best - worst) / mass_sum

        # Calcuate a
        kbest_mass = nlargest(kbest, self.mass)

        for i in range(self.num_agents):
            f = np.zeros([bench.dims])
            ri = uniform(0, 1)

            for m in kbest_mass:
                j = self.mass.index(m)

                if i == j:
                    continue

                rj = uniform(0, 1)
                f += rj * g * self.mass[i] * self.mass[j] / np.linalg.norm(self.particles[j] - self.particles[i]) * (self.particles[j] - self.particles[i])

            a = f / self.mass[i]

            self.speed[i] = ri * self.speed[i] + a


        for i in range(self.num_agents):
            self.particles[i] += self.speed[i]

        np.clip(self.particles, bench.low, bench.up, out = self.particles)

    def optimize(self, iters, bench):

        self.init(bench)

        for i in range(iters):
            self.step(i, bench)

        # Evaluate fitness score
        for idx, pos in enumerate(self.particles):
            self.mass_score[idx] = self.compute_mass_score(iters, bench, pos)

    def mean_fitness_last_iter(self, bench):
        total = 0

        for idx, vec in enumerate(self.particles):
            score = self.fitness_score(bench, list(vec))
            total += score

        return total / len(self.particles)
