class Transition:
    def __init__(self,timer=None):
        self.fire = False
        self.fired = False
        self.inPlaces = []
        self.outPlaces = []
        self.timer = timer if type(timer)==Timer else None
        self.timeInterval = None
        self.timePassed = None

    def computeFire(self):
        self.Fire = False
        if len(self.inPlaces)==0:
            if type(self) not in [type(TimeTransition), type(ImmediateTransition)]:
                raise TypeError

        for place in self.inPlaces:
            self.fire = self.fire | place.token_number >= place.outWeight
        return self.fire

    def fire(self):
        readyToFire = self.computeFire()
        if readyToFire:
            for place in self.inPlaces:
                # I think I should copy places
                place.token_number = place.token_number - place.outWeight
            for place in self.outPlaces:
                place.token_number = place.token_number + place.outWeight

    def compute(self):
        raise TypeError


class ImmediateTransition(Transition):
    def __init__(self, clock, timer=None):
        super().__init__(self,timer)
        self.clock = clock
        
    def compute(self):
        self.fire()

class TimedTransition(Transition):
    def __init__(self,clock, timer=None):
        super().__init__(self, timer)
        self.clock = clock
        self.tickmark = clock.timeElapsed
        self.timeInterval = 1 if type(timer) != Timer else timer.next()

    def compute(self):
        if  timeInterval == self.clock.timeElapsed - tickmark:
            self.fire()
            self.tickmark = clock.timeElapsed
            self.timeInterval = 1 if type(timer) != Timer else timer.next()
        
        

    


