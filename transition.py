import random, math
import numpy as np

class Transition:
    def __init__(self, name=None):
        self.fireBool = False
        self.inArcs = []
        self.outArcs = []
        self.name = name

    def computeFire(self):
        # self.fireBool = False
        # if len(self.inArcs)==0:
        #     self.fireBool = True
        #     return self.fireBool
        # if len(self.outArcs)==0:
        #     self.fireBool = True
        #     return self.fireBool

        # if type(self) not in [TimedTransition, ImmediateTransition]:
        #     raise TypeError
        self.fireBool = True
        for arc in self.inArcs:
            if arc.type=="InhibitorArc":
                self.fireBool = self.fireBool and bool(arc.frm.token_number >= arc.weight) # double check equality
            else:
                self.fireBool = self.fireBool and bool(arc.frm.token_number >= arc.weight)
        return self.fireBool

    def fire(self):
        for arc in self.inArcs:
            if arc.type=="InhibitorArc":
                continue
            # I think I should copy places in general before update atleast in cases of conflict
            # Case of reset kind of transitions should be designed
            if arc.frm.token_number > 0:
                arc.frm.token_number = arc.frm.token_number - arc.weight
        for arc in self.outArcs:
            arc.to.token_number = arc.to.token_number + arc.weight

    def compute(self):
        raise TypeError

    def reset(self):
        raise TypeError

           

class TimedTransition(Transition):
    def __init__(self,clock, timer=None, name=None):
        super().__init__(name)
        self.timer = timer
        self.clock = clock
        self.clock.clockListeners.append(self)
        self.tickMark = None
        self._timeInterval = None
    
    @property
    def timeInterval(self):
        return self._timeInterval
    
    @timeInterval.setter
    def timeInterval(self, x):
        if x is None:
            self._timeInterval = None
        else:
            self._timeInterval = 0 if self.timer==None else next(self.timer)
        
    def reset(self):
        self.tickMark = None
        self.timeInterval = None

    def compute(self):
        # self.computeFire()
        if not self.fireBool:
            self.tickMark = None
            self.timeInterval = None
        if  self.fireBool:
            if self.tickMark == None:
                self.tickMark = self.clock.timeElapsed
            if self.timeInterval == None:
                self.timeInterval = 0 
            if (self.timeInterval == (self.clock.timeElapsed - self.tickMark)):
                self.fire()
                self.tickMark = None
                self.timeInterval = None


class ImmediateTransition(TimedTransition):
    def __init__(self, clock, timer=None,name=None):
        super().__init__(clock, timer, name)
        self.timer = None
        
        
class RequestTransition(TimedTransition):
    def __init__(self, clock, timer=None,name=None):
        super().__init__(clock, timer, name)
        self.timer = None
        self.clock = clock
    
    
    def fireProb(self,freq=240):
        t = self.clock.timeElapsed*(2*math.pi/freq)
        #value  = (1 + math.sin(t))/2
        value = (0.4 + 0.8*(1 + math.sin(t)))/2
        return np.random.choice(2,1,p=[1.0-value,value])[0]
        
    
    def compute(self):
        # self.computeFire()
        if self.fireProb(240):
            self.fire()
            self.tickMark = None
            self.timeInterval = None