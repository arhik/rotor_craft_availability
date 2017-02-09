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
        

        self.demand_arc = Arc(self.T7,self.P1,weight=3,name="demand_arc")
        self.inhibitor_arc = InhibitorArc(self.T7, self.P10, weight=3, name="depo_inspection_arc")

        self.P2 = Place(name="Availability state")
        self.result_arc = Arc(self.P2, self.T7, name='result_arc')

        self.T8 = ImmediateTransition(self.clk, name="ResetTransition")
        self.resetArc = Arc(self.T8, self.P2, name='resetArc')
        # self.
        # self.T1 = TimedTransition(self.clk,timer=timer_sinusoidal(), )
        self.transitions = [self.T8, self.T5, self.T6,self.T7 ]
    
    def run(self):
        for i in count():
            try:
                time.sleep(3)
                next(self.tick)
                print("--"*25)
                print("--"*10+"BEFORE"+"--"*10)
                print("--"*25)
                print("{} Token_number: {}".format(self.P10.name, self.P10.token_number))
                print("{} Token_number: {}".format(self.P11.name, self.P11.token_number))
                print("{} Token_number: {}".format(self.P1.name, self.P1.token_number))
                print("{} Token_number: {}".format(self.P2.name, self.P2.token_number))

                print("--TRANSITIONS--")
                for t in self.transitions:
                    t.compute()
                    if isinstance(t,Transition):
                        print("{} timeInterval: {}".format(t.name,t.timeInterval))
                        print("{} tickMark: {}".format(t.name, t.tickMark))
                        print("{} timeElapsed: {}".format(t.name, t.clock.timeElapsed))
                print("--"*25)
                print("--"*10+"AFTER"+"--"*10)
                print("--"*25)
                print("{} Token_number: {}".format(self.P10.name, self.P10.token_number))
                print("{} Token_number: {}".format(self.P11.name, self.P11.token_number))
                print("{} Token_number: {}".format(self.P1.name, self.P1.token_number))
                print("{} Token_number: {}".format(self.P2.name, self.P2.token_number))

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
            
        
