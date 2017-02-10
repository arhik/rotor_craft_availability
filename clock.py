class Clock:
    def __init__(self):
        self.timeElapsed = 0
        self.clockListeners = []

    def reset(self):
        self.timeElapsed = 0
        for i in clockListeners:
            if isinstance(i, Place):
                i.token_number = 0


    def update(self):
        for i in self.clockListeners:
            i.broadcast()
    
    def tick(self):
        while True:
            self.timeElapsed = self.timeElapsed + 1
            yield self.timeElapsed
            self.update()
