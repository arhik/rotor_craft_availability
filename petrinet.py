from Place import Place
from Transition import TimedTransition, ImmediateTransition
from Clock import Clock

class PetriNet:
    def __init__(self):
        # declare Places
        P1 = Place()
        P2 = Place()
        P3 = Place()

        # declare transitions
        T1 = Transition()

        # declare arcs
        
        # Append places to the transitions using arc
        T1.inPlaces.append(a1)

        self.transitions = [T1,T2]
    
    def run(self):
        for transition in self.transitions:
            
        
