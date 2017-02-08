from random import Random
import math
def timer_uniform(low=0, high=10):
    r = Random()
    while True:
        yield r.randint(low, high)


def timer_normal(mu=10, sigma=5):
    r = Random()
    while True:
        yield floor(r.normalvariate(mu, sigma))

def timer_sinusoidal(amp = 10, low = 0, high = 10):
    init  = 0
    r = Random()
    while True:
        init = init + 1
        yield amp + math.floor(amp*math.sin(init)) + r.randint(low,high)
