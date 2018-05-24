#!/usr/bin/env python3
import numpy as np
import random
import struct

from math import inf
from math import isnan

FLOAT_DIGIT = 32

# def bin_to_float(b):
#     """ Convert binary string to a float. """
#     bf = int_to_bytes(int(b, 2), 8)
#     return struct.unpack('>d', bf)[0]

# def int_to_bytes(n, minlen=0):
#     """ Int/long to byte string. """
#     nbits = n.bit_length() + (1 if n < 0 else 0)
#     nbytes = (nbits+3) // 8
#     b = bytearray()
#     for _ in range(nbytes):
#         b.append(n & 0xff)
#         n >>= 8
#     if minlen and len(b) < minlen:
#         b.extend([0] * (minlen-len(b)))
#     return bytearray(reversed(b))

# def float_to_bin(f):
#     """ Convert a float into a binary string. """
#     ba = struct.pack('>d', f)
#     ba = bytearray(ba)
#     s = ''.join('{:08b}'.format(b) for b in ba)
#     return s[:-1] + s[0]

def bin_to_float(b):
    if FLOAT_DIGIT == 32:
        return struct.unpack('f', struct.pack('I', int(b, 2)))[0]
    else:
        return struct.unpack('d', struct.pack('L', int(b, 2)))[0]

def float_to_bin(f):
    if FLOAT_DIGIT == 32:
        return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('f', f))
    else:
        return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('d', f))

def population_to_bin(pop):
    b = ''
    for p in pop:
        b = b + float_to_bin(p)
    return b

def bin_to_population(bin):
    p = []
    for i in range(int(len(bin) / FLOAT_DIGIT)):
        p.append(bin_to_float(bin[i * FLOAT_DIGIT:(i + 1) * FLOAT_DIGIT]))
    return p

class GA():

    def __init__(self, num_population, crossover_p = 0.8, mutation_p = 0.008):
        self.num_population = num_population
        self.crossover_p = crossover_p
        self.mutation_p = mutation_p

    def init(self, bench):
        self.history = []
        self.populations = []
        for _i in range(self.num_population):
            population = list(np.random.uniform(bench.low, bench.up, bench.dims))
            for idx, pop in enumerate(population):
                if isnan(pop):
                    population[idx] = bench.low
            self.populations.append(population)
        self.scores = [0] * self.num_population
        self.best_population = None
        self.best_score = -inf
        self.next_gen = []

    def reproduction(self, bench):
        scores = []
        for population in self.populations:
            scores.append(self.fitness_score(bench, population))
        p = [score / (sum(scores) + 1e-4) for score in scores]
        counts = [int(round(x * self.num_population)) for x in p]
        for idx, count in enumerate(counts):
            for _i in range(count):
                self.next_gen.append(self.populations[idx])
        if len(self.next_gen) < self.num_population:
            for _i in range(self.num_population - len(self.next_gen)):
                self.next_gen.append(self.populations[random.randint(0, self.num_population - 1)])
        elif len(self.next_gen) > self.num_population:
            self.next_gen = self.next_gen[:self.num_population]
        self.populations = self.next_gen

    def crossover(self, bench):
        l = random.sample(list(range(0, self.num_population)), self.num_population)
        have_mate = [False] * self.num_population
        mates = [-1] * self.num_population
        for idx in range(0, len(l), 2):
            mates[l[idx]] = l[idx + 1]
            mates[l[idx + 1]] = l[idx]

        sites = np.random.randint(bench.dims, size=self.num_population)
        for idx, mate in enumerate(mates):
            if have_mate[idx] == True:
                continue
            else:
                have_mate[idx] = have_mate[mate] = True
                if random.random() <= self.crossover_p:
                    a = list(population_to_bin(self.next_gen[idx]))
                    b = list(population_to_bin(self.next_gen[mate]))
                    sites = np.random.randint(bench.dims * FLOAT_DIGIT, size=bench.dims)
                    sites = sorted(sites)
                    for siteidx in range(0, len(sites), 2):
                        sperm = a[sites[siteidx]: sites[siteidx+1]]
                        a[sites[siteidx]: sites[siteidx+1]] = b[sites[siteidx]: sites[siteidx+1]]
                        b[sites[siteidx]: sites[siteidx+1]] = sperm
                    self.next_gen[idx] = bin_to_population(''.join(a))
                    self.next_gen[mate] = bin_to_population(''.join(b))
                    for genidx, num in enumerate(self.next_gen[idx]):
                        if num > bench.up:
                            self.next_gen[idx][genidx] = bench.up
                        elif num < bench.low:
                            self.next_gen[idx][genidx] = bench.low
                        elif isnan(num):
                            self.next_gen[idx][genidx] = bench.low
                    for genidx, num in enumerate(self.next_gen[mate]):
                        if num > bench.up:
                            self.next_gen[mate][genidx] = bench.up
                        elif num < bench.low:
                            self.next_gen[mate][genidx] = bench.low
                        elif isnan(num):
                            self.next_gen[mate][genidx] = bench.low

    def mutation(self, bench):
        site = np.random.randint(0, bench.dims * FLOAT_DIGIT)
        for idx, _population in enumerate(self.next_gen):
            if random.random() <= self.mutation_p:
                a = list(population_to_bin(self.next_gen[idx]))
                if a[site] == '0':
                    a[site] = '1'
                else:
                    a[site] = '0'
                population = bin_to_population(''.join(a))
                for i in range(len(population)):
                    if isnan(population[i]):
                        population[i] = bench.low
                self.next_gen[idx] = population

    def migrate(self, bench):
        self.populations = self.populations + self.next_gen
        self.next_gen = [self.best_population]

    def fitness_score(self, bench, vec):
        return 1 / (abs(bench.eval(list(vec)) - bench.optima) + 1e-4)

    def step(self, iters, bench):
        self.reproduction(bench)
        self.crossover(bench)
        self.mutation(bench)

        for idx, population in enumerate(self.populations):
            score = self.fitness_score(bench, population)
            self.scores[idx] = score
            if score > self.best_score:
                self.best_score = score
                self.best_population = population
                self.history.append({'iter': iters, 'vec': self.best_population, 'val': bench.eval(self.best_population)})

        self.migrate(bench)

    def optimize(self, iters, bench):
        self.init(bench)

        for i in range(iters):
            self.step(i, bench)

    def mean_fitness_last_iter(self, bench):
        total = 0

        for idx, vec in enumerate(self.populations):
            score = self.fitness_score(bench, list(vec))
            total += score

        return total / len(self.populations)
