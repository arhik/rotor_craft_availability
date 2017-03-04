from transition import Transition
from transition import ImmediateTransition, TimedTransition, RequestTransition
from clock import Clock
from arc import Arc, InhibitorArc
from place import Place
from timer_utils import timer_normal, timer_sinusoidal, timer_uniform, timer_constant, timer_poisson
from itertools import count
import sys
import time

from plot import Window, Curve


class PetriNet:
    DEBUG = False
    def __init__(self):
        self.clk = Clock()
        self.tick = self.clk.tick()
        self.init_net()
        #self.init_plot()
    
    def init_net(self):
        #self.T0 = TimedTransition(self.clk, timer=timer_sinusoidal(clk = self.clk, amp=3,low=0,high=0, freq=540), name="InputDemandTransition")
        self.T0 = RequestTransition(self.clk,name="InputTransition")
        self.P0 = Place(name="Request", clk = self.clk)
        self.A0 = Arc(self.P0, self.T0)

        self.T1 = ImmediateTransition(self.clk, name="AvailabilityTransition")
        self.P1 = Place(name="Depot", clk = self.clk)
        self.A1 = Arc(self.T1, self.P0)
        self.A2 = Arc(self.T1, self.P1)

        self.P2 = Place(name="Mission", clk= self.clk)
        self.A3 = Arc(self.P2, self.T1)

        self.T2 = TimedTransition(self.clk, timer=timer_normal(mu=3,sigma=2), name="MissionCompletionTransition")
        #self.T2 = ImmediateTransition(self.clk, name="AvailabilityTransition")
        self.A4 = Arc(self.T2, self.P2)

        self.P3 = Place(name="Maintainance", clk= self.clk)
        self.A5 = Arc(self.P3, self.T2)

        self.T3 = TimedTransition(self.clk, timer=timer_normal(mu=1,sigma=2), name="MaintainanceTransition")
        #self.T3 = ImmediateTransition(self.clk, name="AvailabilityTransition")
        self.A6 = Arc(self.T3, self.P3)
        
        self.A7 = Arc(self.P1, self.T3)
        
        self.T4 = ImmediateTransition(self.clk, name="UnAvailabilityTransition")
        self.A8 = Arc(self.T4, self.P0)
        
        self.P4 = Place(name="Avail", clk=self.clk)
        self.A9 = Arc(self.P4, self.T1)
        self.T5 = ImmediateTransition(self.clk, name="AvailTransition")
        
        self.A10 = Arc(self.T5, self.P4)
        self.P0.relativeActivityListeners.append(self.P4)
        
        
        
        #self.transitions = [self.T4,self.T0, self.T1,self.T2,self.T3,self.T5]
        self.transitions = [self.T4,self.T0, self.T1,self.T2,self.T3,self.T5]

    def init_plot(self):
        self.window = Window()
        self.win = self.window.rpg.GraphicsWindow()
        
        

        self.P0_tokens = self.win.addPlot()
        self.P0_tokens.setLabel('top', 'Request Place', 'Number of tokens')
        self.P0_plot_curve = self.P0_tokens.plot(pen='k')
        self.P0.tokenObservers.append(Curve(self.clk, self.P0_plot_curve, self.window.proc))


        self.P0_intervalActivity_handle = self.win.addPlot()
        self.P0_intervalActivity_handle.setLabel('top', "Request Inteval Activity", "Request Activity")
        P0_intervalActivity_curve = self.P0_intervalActivity_handle.plot(pen="k")
        self.P0.intervalActivityListeners.append(Curve(self.clk, P0_intervalActivity_curve, self.window.proc))
        
        self.win.nextRow()
        self.P2_intervalActivity_handle = self.win.addPlot()
        self.P2_intervalActivity_handle.setLabel('top', "On Mission Activity", "On Mission Activity")
        P2_intervalActivity_curve = self.P2_intervalActivity_handle.plot(pen="k")
        self.P2.tokenObservers.append(Curve(self.clk, P2_intervalActivity_curve, self.window.proc))
        
        self.P4_intervalActivity_handle = self.win.addPlot()
        self.P4_intervalActivity_handle.setLabel('top', "Avail Activity", "Avail Activity")
        P4_intervalActivity_curve = self.P4_intervalActivity_handle.plot(pen="k")
        self.P4.intervalActivityListeners.append(Curve(self.clk, P4_intervalActivity_curve, self.window.proc))

        self.win.nextRow()
        self.P3_intervalActivity_handle = self.win.addPlot()
        self.P3_intervalActivity_handle.setLabel('top', "Maintenance Activity", "Maintenance Activity")
        P3_intervalActivity_curve = self.P3_intervalActivity_handle.plot(pen="k")
        self.P3.tokenObservers.append(Curve(self.clk, P3_intervalActivity_curve, self.window.proc))
                
        self.P1_intervalActivity_handle = self.win.addPlot()
        self.P1_intervalActivity_handle.setLabel('top', "Depot Activity", "Depot Activity")
        P1_intervalActivity_curve = self.P1_intervalActivity_handle.plot(pen="k")
        self.P1.tokenObservers.append(Curve(self.clk, P1_intervalActivity_curve, self.window.proc))
        

        """
        self.P1_tokens = self.win.addPlot()
        self.P1_tokens.setLabel('top', 'Depot Place', 'Number of tokens')
        self.P1_plot_curve = self.P1_tokens.plot(pen='k')
        self.P1.tokenObservers.append(Curve(self.clk, self.P1_plot_curve, self.window.proc))
        
        self.P2_tokens = self.win.addPlot()
        self.P2_tokens.setLabel('top', 'On Mission Place', 'Number of tokens')
        self.P2_plot_curve = self.P2_tokens.plot(pen='k')
        self.P2.tokenObservers.append(Curve(self.clk, self.P2_plot_curve, self.window.proc))
        
        self.P3_tokens = self.win.addPlot()
        self.P3_tokens.setLabel('top', 'Maintainance Place', 'Number of tokens')
        self.P3_plot_curve = self.P3_tokens.plot(pen='k')
        self.P3.tokenObservers.append(Curve(self.clk, self.P3_plot_curve, self.window.proc))
        """
        """
        self.win.nextRow()
        
        self.T0_firing = self.win.addPlot()
        self.T0_firing.setLabel('top', 'Job Arrival', 'Requests')
        self.T0_plot_curve = self.T0_firing.plot(pen='k')
        self.T0.
        """
    def run(self):
        
        #Init depot size
        
        
        #P4_relative = []
        
        
        total_time = 2400
        avg = 100
        P0_tokens = [0 for i in range(total_time)]
        P4_tokens = [0 for i in range(total_time)]
        for x in range(avg):
            self.P1.token_number = 10
        
            
            for time in range(total_time):
                next(self.tick)
                
                P0_tokens[time] += (self.P0.intervalActivity)
                P4_tokens[time] += (self.P4.relativeActivity)
                
                
                """
                cycle_pos = t%240
                if len(P0_tokens) <= cycle_pos:
                    P0_tokens.append(self.P0.token_number)
                    P4_tokens.append(self.P4.token_number)
                    P4_relative.append(self.P4.relativeActivity)
                else:
                    P0_tokens[cycle_pos] += self.P0.token_number
                    P4_tokens[cycle_pos] += self.P4.token_number
                    P4_relative[cycle_pos] += self.P4.relativeActivity
                """
                if self.DEBUG:
                    print("{} : {}".format(self.P0.name, self.P0.token_number))
                    print("{} : {}".format(self.P1.name, self.P1.token_number))
                    print("{} : {}".format(self.P2.name, self.P2.token_number))
                    print("{} : {}".format(self.P3.name, self.P3.token_number))
                    
                activeTransitions = []
                inactiveTransitions = []
                    
                for t in self.transitions:
                    if t.computeFire() == True:
                        activeTransitions.append(t)
                    else:
                        inactiveTransitions.append(t)
                
                for t in activeTransitions:
                    t.compute()
                    if self.DEBUG:
                        print("{} timeInterval: {}".format(t.name,t.timeInterval))
                        print("{} tickMark: {}".format(t.name, t.tickMark))
                        print("{} timeElapsed: {}".format(t.name, t.clock.timeElapsed))
                
            #self.P0.reset()
            self.clk.reset()
        P0_avg_tokens = [item/avg for item in P0_tokens]
        #print(P0_avg_tokens)
        P4_avg_tokens = [item/avg for item in P4_tokens]
        #print(P4_avg_tokens)
        
        with open('interval_act.csv','w') as f:
            for i, sum_tok in enumerate(P0_avg_tokens):
                f.write("{},{},{}\n".format(i,sum_tok,P4_avg_tokens[i]))

def main():
    net = PetriNet()
    net.run()

if __name__=='__main__':
    main()