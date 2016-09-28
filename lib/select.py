"""
Selection method module
Contains all methods used to select event pairs for growing a causal set
"""

import sys

from .event import Event

def greater(a,b):
    return a > b

def less(a,b):
    return a < b

def pastSelectionMethod(relation):
    def selectionMethod(causalSet):
        """Generic selection method, which depending on the relation (< or >) used will select the maximally similar or dissimilar events."""
        # Reduce memory burden
        # Events whose child events exist and have computed their own past and pastSet values may remove their pastSet, since it is never needed again.
        # Since this is the biggest contribution to memory growth (up to 10s of GB), this clean-up reduces the memory burden significantly and allows the algorithm to
        # run on normal computers consuming 10s to 100s of MB depending on the number of events to be generated).
        cleanUpEvents = list(filter(lambda event: event.futureLeftMovingEvent != None and event.futureRightMovingEvent != None and event.futureLeftMovingEvent._past != None and event.futureRightMovingEvent._past != None, causalSet.events))
        for event in cleanUpEvents:
            event._pastSet = None

        # Filter events without left and right moving events respectively
        openLeftMovingEvents = list(filter(lambda event: event.futureLeftMovingEvent == None, causalSet.events))
        openRightMovingEvents = list(filter(lambda event: event.futureRightMovingEvent == None, causalSet.events))

        selectedLeftMovingEvent = None
        selectedRightMovingEvent = None

        # Iterate through all event pairs
        dij_value = None
        for eLeftMoving in openLeftMovingEvents:
            for eRightMoving in openRightMovingEvents:
                # Ignore if the events are the same, because otherwise the same events would always interact with itself
                if eLeftMoving == eRightMoving:
                    continue
                # Compute the dij value
                dij = abs(eRightMoving.past()**2 - eLeftMoving.past()**2)
                # If the dij value is extremal (based on relation), choose this event
                if dij != None and (dij_value == None or relation(dij, dij_value)):
                    dij_value = dij
                    selectedLeftMovingEvent = eLeftMoving
                    selectedRightMovingEvent = eRightMoving
        # After all events have been compared, an extremal pair should have been selected for growing the causal set
        if selectedLeftMovingEvent == None or selectedRightMovingEvent == None:
            print("Error: No event pair found. Abort.")
            sys.exit(1)
        
        return selectedLeftMovingEvent, selectedRightMovingEvent
    return selectionMethod

def minPastSelection(causalSet):
    """Maximally similar (local) past selection method"""
    return pastSelectionMethod(less)(causalSet)

def maxPastSelection(causalSet):
    """Maximally different (non-local) past selection method"""
    return pastSelectionMethod(greater)(causalSet)
