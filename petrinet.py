from transition import Transition
from transition import ImmediateTransition, TimedTransition
from clock import Clock
from arc import Arc, InhibitorArc
from place import Place
from timer_utils import timer_normal, timer_sinusoidal, timer_uniform
from itertools import count
import sys
import time

class PetriNet:
    def __init__(self):
        self.clk = Clock()
        self.tick = self.clk.tick()


        self.T5 = TimedTransition(self.clk, timer=timer_normal(mu=2, sigma=3), name="RepairTransition")

        self.P10 = Place(token_number=3, name="Depo")

        self.T6 = TimedTransition(self.clk,timer= timer_normal(mu = 5, sigma=5), name="FailTransition")
        self.P11 = Place(name="RepairState")

        self.A10 = Arc(self.P10,self.T5)
        self.A11 = Arc(self.T6,self.P10)
        self.A12 = Arc(self.P11,self.T6)
        self.A13 = Arc(self.T5, self.P11)

        self.T7 = ImmediateTransition(self.clk,name="DemandTransition")

        self.P1 = Place(token_number=3, name="Demand")
        self.
        # self.T1 = TimedTransition(self.clk,timer=timer_sinusoidal(), )

        self.transitions = [self.T5, self.T6]
    
    def run(self):
        for i in count():
            try:
                time.sleep(1)
                next(self.tick)
                for t in self.transitions:
                    t.compute()
                    print("{} timeInterval: {}".format(t.name,t.timeInterval))
                    print("{} tickMark: {}".format(t.name, t.tickMark))
                    print("{} timeElapsed: {}".format(t.name, t.clock.timeElapsed))
                print("P10: Token_number: {}".format(self.P10.token_number))
                print("P11: Token_number: {}".format(self.P11.token_number))
            except KeyboardInterrupt as e:
                sys.exit(1)
        # inPlaces = []
        
        # for transition in self.transitions:
        #     for arc in transition.inArcs:
        #         removedArcs = []
        #         if arc.frm in inPlaces:
        #             removedArcs.append(arc)
        #             inArcs.remove(arc)
        #         transition.compute()
        #         inArcs.extend(removedArcs)
def main():
    net = PetriNet()
    net.run()

if __name__=='__main__':
    main()
            
        
