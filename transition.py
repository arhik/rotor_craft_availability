
class Transition:
    def __init__(self, name=None):
        self.fire_bool = False
        self.inArcs = []
        self.outArcs = []
        self.name = name

    def computeFire(self):
        self.fire_bool = False
        if len(self.inArcs)==0:
            self.fire_bool = True
            return self.fire_bool
        if len(self.outArcs)==0:
            self.fire_bool = True
            return self.fire_bool
        # if type(self) not in [TimedTransition, ImmediateTransition]:
        #     raise TypeError

        for arc in self.inArcs:
            if arc.type=="InhibitorArc":
                self.fire_bool = self.fire_bool | bool(not (arc.frm.token_number <= arc.weight)) # double check equality
            self.fire_bool = self.fire_bool | arc.frm.token_number >= arc.weight
        return self.fire_bool

    def fire(self):
        for arc in self.inArcs:
            if arc.type=="InhibitorArc":
                continue
            # I think I should copy places
            if arc.frm.token_number > 0:
                arc.frm.token_number = arc.frm.token_number - arc.weight
        for arc in self.outArcs:
            arc.to.token_number = arc.to.token_number + arc.weight

    def compute(self):
        raise TypeError




class TimedTransition(Transition):
    def __init__(self,clock, timer=None, name=None):
        super().__init__(name)
        self.timer = timer
        self.clock = clock
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

    def compute(self):
        self.computeFire()
        if not self.fire_bool:
            self.timeMark = None
            self.timeInterval = None
        if  self.fire_bool:
            if self.tickMark ==None:
                self.tickMark = self.clock.timeElapsed
            if self.timeInterval == None:
                self.timeInterval = int 
            if (self.timeInterval == (self.clock.timeElapsed - self.tickMark)):
                self.fire()
                self.tickMark = None
                self.timeInterval = None


class ImmediateTransition(TimedTransition):
    def __init__(self, clock, timer=None,name=None):
        super().__init__(clock, timer, name)
        self.timer = None