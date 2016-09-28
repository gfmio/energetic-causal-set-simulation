"""
Initialisation method module
Contains all methods used to insert the initial events into the causal set
"""

import random

from .event import Event

def poissonOnStrip(n, xMin=0, xMax=10):
    """Init method for the causal set which places n events in a Poisson process on a strip between xMin and xMax at t=0."""
    def initRoutine(causalSet):
        for k in range(0,n):
            causalSet.events.append(Event(
                t=0,
                x=random.random() * (xMax - xMin) + xMin))
        return causalSet
    return initRoutine
