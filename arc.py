from place import Place
from transition import Transition

class Arc:
    def __init__(self, to, frm, weight=1):
        self.weight = weight
        self.to = self._validate(to, frm)
        self.frm = self._validate(frm,to)
        
    def _validate(self, to, frm):
        if type(to)==Place:
            if type(frm)==Place:
                raise TypeError
        elif type(to)==Transition:
            if type(frm)==Transition:
                raise TypeError
        to.inArcs.append(self)
        frm.outArcs.append(self)
        return to

class InhibitorArc(Arc):
    def __init__(self,to, frm):
        super().__init__(self, to, frm)
    
    def _validate(self, to ,frm):
        if type(frm)==Place:
            raise TypeError
        assert(type(frm)==Transition)
        to.inArcs.append(self)
        frm.outArcs.append(self)
