from transition import Transition
from transition import ImmediateTransition, TimedTransition
from clock import Clock
from arc import Arc, InhibitorArc
from place import Place
from timer_utils import timer_normal, timer_sinusoidal, timer_uniform, timer_constant
from itertools import count
import sys
import time

from plot import Window, Curve

# class Env:
#     def __init__(self,)
class PetriNet:
    def __init__(self):
        self.clk = Clock()
        self.tick = self.clk.tick()
        
        # Buffer Section
        self.T5 = TimedTransition(self.clk, timer=timer_normal(mu=3, sigma=2), name="RepairTransition")
        self.P10 = Place(token_number=3, clk = self.clk, name="Depo" )
        self.T6 = TimedTransition(self.clk, timer= timer_normal(mu =2, sigma=2), name="FailTransition")
        self.P11 = Place(clk = self.clk, name="RepairState")
        self.A10 = Arc(self.P10,self.T5)
        self.A11 = Arc(self.T6,self.P10)
        self.A12 = Arc(self.P11,self.T6)
        self.A13 = Arc(self.T5, self.P11)

        #InputDemand Section
        self.T0 = TimedTransition(self.clk, timer=timer_sinusoidal(clk = self.clk, amp=5,low=0,high=0), name="InputDemandTransition")
        self.P1 = Place(name="DemandPlace", clk = self.clk)
        self.A0 = Arc(self.P1,self.T0, name="InputDemandArc")

        #Request Section
        self.T8 = TimedTransition(self.clk, timer=timer_normal(mu=3,sigma=2), name="InputRequestTransition")
        self.P12 = Place(capacity=1,name="RequestPlace", clk = self.clk)
        self.A14 = Arc(self.P12, self.T8,name="InputTRequestPArc")
        # self.T10 = TimedTransition(self.clk, timer= timer_constant(),name="NextStepReset")
        # self.A19 = Arc(self.T10,self.P12, name="NextStepResetArc")

        # InputDemand and Request Reset Section
        self.T9 = ImmediateTransition(self.clk,name="InputRequestResetTransition")
        self.A15 = Arc(self.T9, self.P12, name="RequestPResetTArc")
        self.A18 = Arc(self.T9, self.P1, name="DemandPResetTArc")

        # Demand Reset Arc
        # self.T10 = ImmediateTransition(self.clk, name="DemandRequestResetTransition")
        # self.A16 = Arc(self.T10, self.P1, name="DemandPlaceResetArc")
        # self.A17 = Arc(self.T10, self.P12, name="RequestDemandPlaceResetArc")
        #subscribe Demand token_number with arcweight
        self.P1.tokenObservers.append(self.A18)
        
        # Main Logic Transitions and Arcs
        self.T7 = ImmediateTransition(self.clk,name="AvailabilityTransition")
        # self.A7 = Arc(self.T7,self.P1,name="DemandPAvailabilityTArc")
        self.A8 = Arc(self.T7, self.P12, name="RequestPAvailabilityTArc")
        self.A9 = InhibitorArc(self.T7, self.P10, name="DepoPAvailabilityArc")

        # subscribe the A9 weight to P1.token_number
        self.P1.tokenObservers.append(self.A9)
        # self.P1.tokenObservers.append(self.A7)
        
        # Availability Section
        self.P2 = Place(name="AvailabilityPlace",clk=self.clk)
        self.A6 = Arc(self.P2, self.T7, name='AvailabilityTAvailabilityPArc')
        
        self.T4 = ImmediateTransition(self.clk,name="AvailabiltyPlaceResetTransition")
        self.A5 = Arc(self.T4, self.P2, name='AvailabiltyPAvailabilityResetArc')

        self.transitions = [self.T0,self.T8,  self.T5, self.T6,self.T7, self.T9, self.T4]

        #setting up plots
        self.window = Window()
        
        # win = self.window.rpg.addPlot()
        self.win = self.window.rpg.GraphicsWindow()

        self.P1_handle = self.win.addPlot()
        self.P1_handle.setLabel("top", "Demand Place", "token_number")
        self.P12_handle = self.win.addPlot()
        self.P12_handle.setLabel('top', "Request Place", "token_number")


        self.P12_activity_handle = self.win.addPlot()
        self.P12_activity_handle.setLabel('top', "RequestPlaceActivity", "Percentage active")

        self.P1_intervalActivity_handle = self.win.addPlot()
        self.P1_intervalActivity_handle.setLabel('top', "Demand Inteval Activity", "Demand Activity")
        

        P1_plot_curve = self.P1_handle.plot(pen='k')
        P1_intervalActivity_curve = self.P1_intervalActivity_handle.plot(pen="k")

        P12_plot_curve = self.P12_handle.plot(pen='k')
        P12_activity_curve = self.P12_activity_handle.plot(pen='k')
        
        
        self.win.nextRow()

        self.P10_handle = self.win.addPlot()
        self.P10_handle.setLabel('top', "Depo Place", "token_number")
        self.P2_handle = self.win.addPlot()
        self.P2_handle.setLabel('top', "Available Place", "token_number")
        self.P2_activity_handle = self.win.addPlot()
        self.P2_activity_handle.setLabel('top', "Available Place Activiy", "Percentage Active")

        self.P2_intervalActivity_handle = self.win.addPlot()
        self.P2_intervalActivity_handle.setLabel('top', "Demand Inteval Activity", "OnDemand Availability Activity")

        P2_intervalActivity_curve = self.P2_intervalActivity_handle.plot(pen="k")

        P2_plot_curve = self.P2_handle.plot(pen='k')
        P2_activity_curve = self.P2_activity_handle.plot(pen='k')

        P10_plot_curve = self.P10_handle.plot(pen='k')

        self.P1.tokenObservers.append(Curve(self.clk, P1_plot_curve, self.window.proc))
        self.P10.tokenObservers.append(Curve(self.clk, P10_plot_curve, self.window.proc))
        self.P12.tokenObservers.append(Curve(self.clk, P12_plot_curve, self.window.proc))
        self.P2.tokenObservers.append(Curve(self.clk, P2_plot_curve, self.window.proc))
        self.P12.activityListeners.append(Curve(self.clk, P12_activity_curve, self.window.proc))
        self.P2.activityListeners.append(Curve(self.clk, P2_activity_curve, self.window.proc))
        self.P1.intervalActivityListeners.append(Curve(self.clk, P1_intervalActivity_curve, self.window.proc))
        self.P2.intervalActivityListeners.append(Curve(self.clk, P2_intervalActivity_curve, self.window.proc))
        
    def run(self):
        for i in count():
            try:
                time.sleep(.1)
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
                activeTransitions = []
                inActiveTransitions = []
                for t in self.transitions:
                    if t.computeFire() == True:
                        activeTransitions.append(t)
                    else:
                        inActiveTransitions.append(t)
                for t in activeTransitions:
                    t.compute()
                    if isinstance(t,Transition):
                        print("{} timeInterval: {}".format(t.name,t.timeInterval))
                        print("{} tickMark: {}".format(t.name, t.tickMark))
                        print("{} timeElapsed: {}".format(t.name, t.clock.timeElapsed))
                for t in inActiveTransitions:
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
def main():
    net = PetriNet()
    net.run()

if __name__=='__main__':
    main()
            
        
