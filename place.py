class Place:
    def __init__(self, token_number=0, capacity=float('Inf'), name=None):
        self.clk = None # to be set
        self._token_number = token_number
        self.inArcs = []
        self.outArcs = []
        self.token_observers = []
        self.activeListeners = []
        self.name = name
        self.capacity = capacity
        self._active = 0
        self._activeSum = 0
        self._percentActive = float(0)
        
        
    @property
    def active(self):
        self._active = 1 if self.token_number > 0 else 0
        self._activeSum = self._activeSum + self._active
        return self._active

    @property
    def percentage_active(self):
        pass

    @property
    def token_number(self):
        return self._token_number
    
    @token_number.setter 
    def token_number(self, updated_token_number):
        self._token_number = updated_token_number if updated_token_number <= self.capacity else self._token_number
        for token_observer in self.token_observers:
            token_observer.update(self.token_number)
    
    def _validateInArc(self):
        pass
    
    def _validateOutAtc(self):
        pass
