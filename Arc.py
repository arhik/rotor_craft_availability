class Arc:
    def __init__(self):
        self.weight = None
        self.to = None
        self.frm = None
        
    def _validate(self):
        if self.to is not None:
            if type(self.to) == type(Transition) 