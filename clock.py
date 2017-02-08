class Clock:
    def __init__(self):
        self.timeElapsed = 0
    def reset(self):
        self.timeElapsed = 0
    def tick(self):
        while True:
            self.timeElapsed = self.timeElapsed + 1
            yield self.timeElapsed
