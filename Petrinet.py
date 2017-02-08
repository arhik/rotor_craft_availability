from Place import Place
from Transition import TimedTransition, ImmediateTransition
from Clock import Clock

class PetriNet:
    def __init__(self):
            self.transitions = None
            self.places = places # copy places somehow
    
    def run(self):
