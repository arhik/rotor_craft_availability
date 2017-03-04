class Publisher:
    def __init__(self):
        self.subscribers = []
    
    def add_subscriber(self):
        self.subscribers.append(subscriber)

    def publish(self):
        for i in self.subscribers:
            i.update()


class Subscriber:
    def __init__(self):
        pass
    
    def update(self):
        pass