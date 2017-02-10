from place import Place
from transition import Transition

class Arc:
    def __init__(self, to, frm, weight=1, name=None):
        self.weight = weight
        self._validate(to, frm)
        self._validate(frm,to)
        self.to = to
        self.frm = frm
        self.to.inArcs.append(self)
        self.frm.outArcs.append(self)
        self.type = "Arc"
        self.name = name
        
    def update(self, value):
        if value<=0:
            value = 1
        self.weight = value

    @staticmethod
    def _validate(to, frm):
        if type(to)==Place:
            if type(frm)==Place:
                raise TypeError
        elif type(to)==Transition:
            if type(frm)==Transition:
                raise TypeError


class InhibitorArc(Arc):
    def __init__(self,to, frm, weight=1, name=None):
        self.weight = weight
        self._validate(to,frm)
        self.to = to
        self.frm = frm
        self.to.inArcs.append(self)
        self.frm.outArcs.append(self)
        self.type = "InhibitorArc"
        self.name = name
    @staticmethod
    def _validate(to ,frm):
        if type(to)==Place:
            raise TypeError
        assert(type(frm)==Place)
