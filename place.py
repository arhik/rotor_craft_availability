class Place:
    def __init__(self, token_number=0, capacity=float('Inf'), clk = None, name=None, offset=0):
        self.clk = clk # to be set
        if self.clk is not None:
            self.clk.clockListeners.insert(0, self)
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
        self._percentActivity = float(0)
        self._relativeActivity = 0
        self._relativeOffsetActivity = []
        self._relativeOffsetIntervalActivity = {}
        self._history = {}
        self._offset = offset
        self._intervalActivity = []
    
    @property
    def deltaT(self):
        return self.clk.interval

    @property
    def isActive(self):
        return bool(self._active)

    @property
    def activity(self):
        return self._active
    
    @property
    def offset(self):
        return self._offset

    @property
    def history(self):
        return self._history
    
    @property
    def totalActivity(self):
        return self._activeSum
    
    @property
    def percentActivity(self):
        try:
            self._percentActivity = self.totalActivity/self.clk.timeElapsed
        except ZeroDivisionError:
            self._percentActivity = 0.
        return self._percentActivity
    
    @property
    def totalIntervalActivity(self):
        return sum(self._intervalActivity)
    
    @property
    def intervalActivity(self):
        # print("currentInterval:{}".format(self.clk.currentInterval))
        # print("IntervalActivity:{}".format(self._intervalActivity))
        self._intervalActivity = [self.history[i] for i in self.clk.currentInterval[:min(len(self.history), self.clk.interval)]]
        return self._intervalActivity

    @property
    def percentIntervalActivity(self):
        return float(self.totalIntervalActivity)/len(self.intervalActivity)

    @property
    def token_number(self):
        return self._token_number

    @property
    def relativeActivity(self):
        return self._relativeActivity

    def relativeActivityUpdate(self, remotehistory):
        if self.clk.endOfInterval:
            try:
                tmp = []
                # print(remotehistory)
                for i in self.clk.currentInterval:
                    try:
                        tmp.append(remotehistory[i-self.offset])
                    except KeyError as e:
                        tmp.append(0)
                self._relativeOffsetActivity = [i*j for i,j in zip(self.intervalActivity, tmp[:len(self.intervalActivity)])]
                print("remotehistory: {}\n selfhistory: {}\n output: {}\n".format(tmp, self.intervalActivity, self._relativeOffsetActivity))
                self._relativeActivity = (float(sum(self._relativeOffsetActivity))/sum(tmp)) if sum(self._relativeOffsetActivity) > 0 else 1.0
            except ZeroDivisionError as z:
                self._relativeActivity = 0.
            except KeyError as k:
                self._relativeActivity = 0.


    def reset(self):
        self._token_number = 0
        self._active = 0
        self._activeSum = 0
        self._percentIntervalActive = float(0)
        self._relativeActivity = False
        self._previous_active = False
        self._history = {}
        self._intervalActivity = []
        
    
    def broadcast(self):
        self._active = 1 if self.token_number > 0 else 0
        self._history.update({self.clk.timeElapsed: self._active})
        self._activeSum = self._activeSum + self._active
        if self.clk is not None:
            for tokenObserver in self.tokenObservers:
                tokenObserver.update(self.token_number)
            for activityListener in self.activityListeners:
                activityListener.update(self.percentActivity)
            for relativeActiveListener in self.relativeActivityListeners:
                if isinstance(relativeActiveListener, Place):
                    relativeActiveListener.relativeActivityUpdate(self.history)
                elif relativeActiveListener.type == "curve":
                    relativeActiveListener.update(self.relativeActivity)
            for intervalActivityListener in self.intervalActivityListeners:
                if self.clk.endOfInterval:
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
