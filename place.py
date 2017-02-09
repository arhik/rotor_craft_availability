class Place:
    def __init__(self, token_number=0, capacity=float('Inf'), name=None):
        self._token_number = token_number
        self.inArcs = []
        self.outArcs = []
        self.token_observers = []
        self.name = name
        self.capacity = capacity

    @property
    def token_number(self):
        return self._token_number
    
    @token_number.setter 
    def token_number(self, updated_token_number):
        self._token_number = updated_token_number
        for token_observer in self.token_observers:
            token_observer.update(self.token_number)
    
    def _validateInArc(self):
        pass
    
    def _validateOutAtc(self):
        pass
