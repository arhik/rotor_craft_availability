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
        self._relativeActivity = False
        self._previous_active = False
        
    @property
    def active(self):
        return self._active
    
    @property
    def totalActivity(self):
        return self._activeSum
    
    @property
    def steadyStateActivity(self):
        try:
            self._percentActive = self._activeSum/self.clk.timeElapsed
        except ZeroDivisionError:
            self._percentActive = 0.
        return self._percentActive
    
    @property
    def intervalActivity(self):
        if len(self._intervalActivity)==10:
            self._percentIntervalActive = float(sum(self._intervalActivity))
            self._intervalActivity  = []
        return self._percentIntervalActive


    @property
    def token_number(self):
        return self._token_number

    @property
    def relativeActivity(self):
        return self._relativeActivity

    def relativeActivityUpdate(self, remoteActivity):
        try:
            self._relativeActivity = float(self.totalActivity)/remoteActivity
        except ZeroDivisionError:
            self._relativeActivity = 0.
    
    def reset(self):
        self._token_number = 0
        self._active = 0
        self._activeSum = 0
        self._intervalActivity = []
        self._percentIntervalActive = float(0)
        self._relativeActivity = False
        self._previous_active = False
        
    
    def broadcast(self):
        self._previous_active = self._active
        self._active = 1 if self.token_number > 0 else 0
        self._intervalActivity.append(self.token_number)
        self._activeSum = self._activeSum + self.active
        if self.clk is not None:
            for tokenObserver in self.tokenObservers:
                tokenObserver.update(self.token_number)
            for activityListener in self.activityListeners:
                activityListener.update(self.steadyStateActivity)
            for relativeActiveListener in self.relativeActivityListeners:
                if isinstance(relativeActiveListener, Place):
                    relativeActiveListener.relativeActivityUpdate(self.totalActivity)
                elif relativeActiveListener.type == "curve":
                    relativeActiveListener.update(self.relativeActivity)
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
