class Place:
    def __init__(self, token_number=0, capacity=float('Inf'), clk = None, name=None):
        self.clk = clk # to be set
        if self.clk is not None:
            self.clk.clockListeners.append(self)
        self._token_number = token_number
        self.inArcs = []
        self.outArcs = []
        self.tokenObservers = []
        self.activationListeners = []
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
    
    def broadcast(self):
        if self.clk is not None:
            for tokenObserver in self.tokenObservers:
                tokenObserver.update(self.token_number)

    
    @token_number.setter 
    def token_number(self, updated_token_number):
        self._token_number = updated_token_number if updated_token_number <= self.capacity else self._token_number
        if self.clk is None:
            for tokenObserver in self.tokenObservers:
                tokenObserver.update(self.token_number)
    
    def _validateInArc(self):
        pass
    
    def _validateOutAtc(self):
        pass
