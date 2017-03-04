from random import Random
import math
from clock import Clock

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

def timer_sinusoidal(clk = None, amp = 10, low = 0, high = 10, freq=120):
    if clk == None:
        t = 0
    r = Random()
    while True:
        if clk == None:
            t = t + 1
        else:
            t = clk.timeElapsed*(math.pi/freq)
        value  = amp*(1 + math.floor(math.sin(t))) + r.randint(low,high)
        yield int(value) if value >= 1 else 1

def timer_constant(const=1):
    while True:
        yield const

def timer_poisson(lmb=3):
    r = Random()
    while True:
        value = math.floor(math.log(r.uniform(0.0,1.0))/lmb)
        yield value if value >=1 else 1
