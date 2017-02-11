class Place:
    def __init__(self, token_number=0, capacity=float('Inf'), clk = None, name=None):
        self.clk = clk # to be set
        if self.clk is not None:
            self.clk.clockListeners.append(self)
        self._token_number = token_number
        self.inArcs = []
        self.outArcs = []
        self.tokenObservers = []
        self.activityListeners = []
        self.intervalActivityListeners = []
        self.relativeActivityListeners = []
        self.name = name
        self.capacity = capacity
        self._active = 0
        self._activeSum = 0
        self._intervalActivity = []
        self._percentActive = float(0)
        self._percentIntervalActive = float(0)
        
        
    @property
    def active(self):
        return self._active
    
    @property
    def totalActivity(self):
        return self._activeSum
    
    @property
    def steadyStateActivity(self):
        return self._percentActive
    
    @property
    def intervalActivity(self):
        if len(self._intervalActivity)==24:
            self._percentIntervalActive = float(sum(self._intervalActivity))/24
            self._intervalActivity  = []
        return self._percentIntervalActive


    @property
    def token_number(self):
        return self._token_number
    
    def broadcast(self):
        self._active = 1 if self.token_number > 0 else 0
        self._intervalActivity.append(self.token_number)
        self._activeSum = self._activeSum + self.active
        self._percentActive  = self._activeSum/self.clk.timeElapsed
        if self.clk is not None:
            for tokenObserver in self.tokenObservers:
                tokenObserver.update(self.token_number)
            for activityListener in self.activityListeners:
                activityListener.update(self.steadyStateActivity)
            for relativeActiveListener in self.relativeActivityListeners:
                relativeActiveListener.relativeUpdate(0)
            for intervalActivityListener in self.intervalActivityListeners:
                intervalActivityListener.update(self.intervalActivity)
    
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
