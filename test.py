#!/usr/python/env python3
from transition import Transition
from transition import ImmediateTransition, TimedTransition
from clock import Clock
from arc import Arc, InhibitorArc
from place import Place
from timer_utils import timer_normal
from itertools import count
import sys
import time

clk = Clock()

P1 = Place(token_number=1)
P2 = Place(token_number=1)

T1 = ImmediateTransition(clk, timer_normal())

print(T1.inArcs)
print(T1.outArcs)

A1 = Arc(P1,T1)

print(A1)

print(A1.to)
print(A1.frm)
print(T1.inArcs)
print(T1.outArcs)

A2 = Arc(T1, P2)

print(A2)

print(T1.inArcs)
print(T1.outArcs)



T1.compute()

print(P1.token_number)
print(P2.token_number)

# -----------------------------
print("_____________________")

P3 = Place(token_number=4)
P4 = Place(token_number=6)

P5 = Place(token_number=0)

T2  = ImmediateTransition(clk)

A3 = Arc(T2, P3, weight = 2)
A4 = Arc(T2, P4, weight = 4)

A5 = Arc(P5, T2, weight = 3)


print("T2.inArcs: {}".format(T2.inArcs))

print("T2.outArcs: {}".format(T2.outArcs))

T2.compute()

print("P3.token_number: {}".format(P3.token_number))

print("P4.token_number: {}".format(P4.token_number))

print("P5.token_number: {}".format(P5.token_number))

print("-"*25)
print("Testing Inhibitor arc")
print("-"*25)

P6 = Place(token_number=14)
P7 = Place(token_number=9)

P8 = Place(token_number=0)

T3 = ImmediateTransition(clk)

A6 = Arc(T3, P6, weight=1)
A7 = InhibitorArc(T3, P7)


print("-"*30)
print("Token observers Test")
print("-"*30)

P6.token_observers.append(A7)


A8 = Arc(P8, T3)

T3.compute()

print("P6.token_number: {}".format(P6.token_number))

print("P7.token_number: {}".format(P7.token_number))

print("P8.token_number: {}".format(P8.token_number))

P6.token_number = 10

P6.token_number = 11

print("A7.weight: {}".format(A7.weight))
T3.compute()

print("P6.token_number: {}".format(P6.token_number))

print("P7.token_number: {}".format(P7.token_number))

print("P8.token_number: {}".format(P8.token_number))



T4 = TimedTransition(clk, timer=timer_normal())
P9 = Place(name="Requests")
A9 = Arc(P9, T4)



print(T4.timeInterval)
tick = clk.tick()
print("T4 outArcs: {}".format(T4.outArcs))
# for i in count(start=0, step=1):
#     try:
#         next(tick)
#         T4.compute()
        
#         print("T4 tickMark: {}".format(T4.tickmark))
#         print("T4 timeElapsed: {}".format(T4.clock.timeElapsed))
#         print("P9: Token_number: {}".format(P9.token_number))
#         print(P9.name)
#     except KeyboardInterrupt as e:
#         sys.exit(1)

# T5 = TimedTransition(clk, timer=timer_normal(mu=2, sigma=3))

# P10 = Place(token_number=3, name="Depo")

# T6 = TimedTransition(clk,timer= timer_normal(mu = 5, sigma=5))
# P11 = Place(name="RepairState")

# A10 = Arc(P10,T5)
# A11 = Arc(T6,P10)
# A12 = Arc(P11,T6)
# A13 = Arc(T5, P11)

# transitions = [T5, T6]
# for i in count():
#     try:
#         time.sleep(1)
#         next(tick)
#         for t in transitions:
#             t.compute()
#             print("T5 timeInterval: {}".format(T5.timeInterval))
#             print("T6 timeInterval: {}".format(T6.timeInterval))
#             print("T5 tickMark: {}".format(T5.tickMark))
#             print("T5 timeElapsed: {}".format(T5.clock.timeElapsed))
#             print("T6 tickMark: {}".format(T6.tickMark))
#             print("T6 timeElapsed: {}".format(T6.clock.timeElapsed))
#             print("P10: Token_number: {}".format(P10.token_number))
#             print("P11: Token_number: {}".format(P11.token_number))
#     except KeyboardInterrupt as e:
#         sys.exit(1)

P12 = Place(token_number=1)
P13 = Place(token_number=1)

T12 = ImmediateTransition(clk,name="ResetTransition")

A12 = Arc(T12, P12, name="ResetArc")
A13 = InhibitorArc(T12, P13, name="Inhibitor")

P14 = Place()
A14 = Arc(P14,T12, name="result")

print("--------------")
print(P12.token_number)
print(P13.token_number)
print(P14.token_number)
next(tick)
T12.compute()
print("--------------")
print(P12.token_number)
print(P13.token_number)
print(P14.token_number)
next(tick)
T12.compute()
print("--------------")
print(P12.token_number)
print(P13.token_number)
print(P14.token_number)






