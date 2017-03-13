from place import Place
from transition import Transition

class Clock:
    def __init__(self, interval = 10):
        self._timeElapsed = 0
        self.clockListeners = []
        self.interval = interval
        self._intervalCount = 0

    @property
    def timeElapsed(self):
        return self._timeElapsed
    
    @timeElapsed.setter
    def timeElapsed(self, n):
        self._timeElapsed = self._timeElapsed + 1
        self.sync()
        if self.endOfInterval:
                self._intervalCount += 1
                print("Present Interval Count is {}".format(self._intervalCount))
        

    @property
    def endOfInterval(self):
        return bool(self.timeElapsed % self.interval == 0) if self.timeElapsed !=0 else False

    @property
    def currentInterval(self):
        _currentInterval = [i for i in range(self._intervalCount*self.interval+1, (self._intervalCount+1)*self.interval+1)] 
        return _currentInterval
    
    def reset(self):
        self._timeElapsed = 0
        self._intervalCount = 0
        for i in self.clockListeners:
            if isinstance(i, Place):
                i.reset()
            elif isinstance(i, Transition):
                i.reset()


    def sync(self):
        for i in self.clockListeners:
            if isinstance(i, Place):
                i.broadcast()

    def tick(self):
        while True:
            self.timeElapsed = self.timeElapsed + 1
            yield self.timeElapsed
            
            

