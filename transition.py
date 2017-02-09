
class Transition:
    def __init__(self,timer=None, name=None):
        self.fire_bool = False
        self.inArcs = []
        self.outArcs = []
        self.timer = timer
        self.timeInterval = None
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
        readyToFire = self.computeFire()
        if readyToFire:
            for arc in self.inArcs:
                if arc.type=="InhibitorArc":
                    continue
                # I think I should copy places
                arc.frm.token_number = arc.frm.token_number - arc.weight
            for arc in self.outArcs:
                print("Hello")
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
        self.timer = timer
        self.clock = clock
        self.tickmark = clock.timeElapsed
        self.timeInterval = 1 if self.timer==None else next(self.timer)

    def compute(self):
        if  (self.timeInterval == (self.clock.timeElapsed - self.tickmark)):
            self.fire()
            self.tickmark = self.clock.timeElapsed
            self.timeInterval = 1 if self.timer==None else next(self.timer)
