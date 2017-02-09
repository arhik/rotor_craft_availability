from random import Random
import math
def timer_uniform(low=0, high=10):
    r = Random()
    while True:
        value = r.randint(low, high)
        yield value if value >=1 else 1


def timer_normal(mu=10, sigma=2):
    r = Random()
    while True:
        value = math.floor(r.normalvariate(mu, sigma))
        yield value if value >=1 else 1

def timer_sinusoidal(amp = 10, low = 0, high = 10):
    init  = 0
    r = Random()
    while True:
        init = init + 1
        value  = amp + math.floor(amp*math.sin(init)) + r.randint(low,high)
        yield value if value >= 1 else 1
