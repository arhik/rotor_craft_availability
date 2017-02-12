from place import Place
from transition import Transition
class Clock:
    def __init__(self):
        self.timeElapsed = 0
        self.clockListeners = []

    def reset(self):
        self.timeElapsed = 0
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
            self.sync()
            
