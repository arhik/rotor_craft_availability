
class Transition:
    def __init__(self,timer=None):
        self.fire = False
        self.fired = False
        self.inArcs = []
        self.outArcs = []
        self.timer = timer
        self.timeInterval = None
        self.timePassed = None

    def computeFire(self):
        self.Fire = False
        if len(self.inArcs)==0:
            if type(self) not in [TimeTransition, ImmediateTransition]:
                raise TypeError

        for arc in self.inArcs:
            if type(arc)==type(InhibitorArc):
                self.fire = self.fire | arc.frm.token_number <= arc.weight # double check equality
            self.fire = self.fire | arc.frm.token_number >= arc.weight
        return self.fire

    def fire(self):
        readyToFire = self.computeFire()
        if readyToFire:
            for arc in self.inArcs:
                # I think I should copy places
                arc.frm.token_number = arc.frm.token_number - arc.weight
            for arc in self.outArcs:
                arc.to.token_number = arc.to.token_number + arc.weight

    def compute(self):
        raise TypeError


class ImmediateTransition(Transition):
    def __init__(self, clock, timer=None):
        super().__init__(timer)
        self.clock = clock
        
    def compute(self):
        self.fire()


class TimedTransition(Transition):
    def __init__(self,clock, timer=None):
        super().__init__(timer)
        self.clock = clock
        self.tickmark = clock.timeElapsed
        self.timeInterval = 1 if type(timer) != Timer else next(timer)

    def compute(self):
        if  timeInterval == self.clock.timeElapsed - tickmark:
            self.fire()
            self.tickmark = self.clock.timeElapsed
            self.timeInterval = 1 if type(timer) != Timer else next(timer)
