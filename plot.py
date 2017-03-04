
from itertools import count

import pyqtgraph as pg
import pyqtgraph.multiprocess as mp

pg.mkQApp()

class Window:
    def __init__(self): 
        self.proc = mp.QtProcess()
        self.rpg = self.proc._import('pyqtgraph')
        self.rpg.setConfigOption('background', 'w')
        self.rpg.setConfigOption('foreground', 'k')

class Curve:
    def __init__(self, clk, curve, proc):
        self.clk = clk
        self.curve = curve
        self.data_x = proc.transfer([])
        self.data_y = proc.transfer([])
        self._t = None
        self.type = "curve"

    @property
    def t(self):
        self._t = self.clk.timeElapsed
        return self._t
    
    def update(self,x):
        self.data_y.extend([x], _callSync='async')
        self.data_x.extend([self.t], _callSync='async',)
        self.curve.setData(y=self.data_y, _callSync='async')
        # self.curve.setPos(self.t,0)