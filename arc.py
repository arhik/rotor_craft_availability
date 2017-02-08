from place import Place
from transition import Transition

class Arc:
    def __init__(self, to, frm):
        self.weight = None
        self.to = self._validate(to, frm)
        self.frm = self._validate(frm,to)
        
    def _validate(self, to, frm):
        if type(to)==type(Place):
            assert(type(frm)==type(Transition))
        else type(to)==type(Transition):
            assert(type(frm)==type(Place))
        to.inArcs.append(self)
        frm.outArcs.append(self)
        return to