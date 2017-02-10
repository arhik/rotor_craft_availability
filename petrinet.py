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

        # Buffer Section
        self.T5 = TimedTransition(self.clk, timer=timer_normal(mu=3, sigma=2), name="RepairTransition")
        self.P10 = Place(token_number=3, name="Depo")
        self.T6 = TimedTransition(self.clk,timer= timer_normal(mu =2, sigma=2), name="FailTransition")
        self.P11 = Place(name="RepairState")
        self.A10 = Arc(self.P10,self.T5)
        self.A11 = Arc(self.T6,self.P10)
        self.A12 = Arc(self.P11,self.T6)
        self.A13 = Arc(self.T5, self.P11)


        
        #InputDemand Section
        self.T0 = TimedTransition(self.clk, timer=timer_sinusoidal(amp=3,low=0,high=2), name="InputDemandTransition")
        self.P1 = Place(name="DemandPlace")
        self.A0 = Arc(self.P1,self.T0, name="InputDemandArc")

        
        #Request Section
        self.T8 = TimedTransition(self.clk, timer=timer_normal(mu=3,sigma=2), name="InputRequestTransition")
        self.P12 = Place(capacity=1,name="RequestPlace")
        self.A14 = Arc(self.P12, self.T8,name="InputTRequestPArc")

        # InputDemand and Request Reset Section
        self.T9 = ImmediateTransition(self.clk,name="InputRequestResetTransition")
        self.A15 = Arc(self.T9, self.P12, name="RequestPResetTArc")
        self.A18 = Arc(self.T9, self.P1, name="DemandPResetTArc")

        # Demand Reset Arc
        # self.T10 = ImmediateTransition(self.clk, name="DemandRequestResetTransition")
        # self.A16 = Arc(self.T10, self.P1, name="DemandPlaceResetArc")
        # self.A17 = Arc(self.T10, self.P12, name="RequestDemandPlaceResetArc")
        #subscribe Demand token_number with arcweight
        self.P1.token_observers.append(self.A18)

        # Main Logic Transitions and Arcs
        self.T7 = ImmediateTransition(self.clk,name="AvailabilityTransition")
        self.A7 = Arc(self.T7,self.P1,name="DemandPAvailabilityTArc")
        self.A8 = Arc(self.T7, self.P12, name="RequestPAvailabilityTArc")
        self.A9 = InhibitorArc(self.T7, self.P10, name="DepoPAvailabilityArc")

        # subscribe the A9 weight to P1.token_number
        self.P1.token_observers.append(self.A9)
        self.P1.token_observers.append(self.A7)
        
        # Availability Section
        self.P2 = Place(name="AvailabilityPlace")
        self.A6 = Arc(self.P2, self.T7, name='AvailabilityTAvailabilityPArc')
        
        # self.T4 = ImmediateTransition(self.clk, name="AvailabiltyPlaceResetTransition")
        # self.A5 = Arc(self.T8, self.P2, name='AvailabiltyPAvailabilityResetArc')

        self.transitions = [self.T0,self.T8,  self.T5, self.T6,self.T7, self.T9 ] #, self.T4
    
    def run(self):
        for i in count():
            try:
                time.sleep(3)
                next(self.tick)
                print("--"*25)
                print("--"*10+"BEFORE"+"--"*10)
                print("--"*25)

                print("{} Token_number: {}".format(self.P12.name, self.P12.token_number))
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
                print("{} Token_number: {}".format(self.P12.name, self.P12.token_number))
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
            
        
