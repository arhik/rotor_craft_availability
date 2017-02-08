from place import Place
from transition import Transition

class Arc:
    def __init__(self, to, frm, weight=1):
        self.weight = weight
        self._validate(to, frm)
        self._validate(frm,to)
        self.to = to
        self.frm = frm
        self.to.inArcs.append(self)
        self.frm.outArcs.append(self)
        self.type = "Arc"
        
    def _validate(self, to, frm):
        if type(to)==Place:
            if type(frm)==Place:
                raise TypeError
        elif type(to)==Transition:
            if type(frm)==Transition:
                raise TypeError


class InhibitorArc(Arc):
    def __init__(self,to, frm):
        super().__init__(self, to, frm)
        self.type = "InhibitorArc"
    
    def _validate(self, to ,frm):
        if type(frm)==Place:
            raise TypeError
        assert(type(frm)==Transition)
