#!/usr/bin/env python3

class Bench():

    def __init__(self, dims, func, up, low, optima):
        self.func = func
        self.dims = dims
        self.up = up
        self.low = low
        self.optima = optima

    def eval(self, vector):
        return self.func(vector)
