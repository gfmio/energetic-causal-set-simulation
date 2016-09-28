"""
Event class module
"""

class Event(object):
    def __init__(self, t=None, x=None):
        """Init method for an event, which is defined by its position (t,x). It has its parent elements and its child events as referenced values."""
        super(Event, self).__init__()
        self.t = t
        self.x = x

        self.pastLeftMovingEvent = None
        self.pastRightMovingEvent = None

        self.futureLeftMovingEvent = None
        self.futureRightMovingEvent = None

        self._past = None
        self._pastSet = None

    def past(self):
        """Compute the past value of the event."""
        # The past value is stored, once it has been computed, to speed up the algorithm
        if self._past != None:
            return self._past

        # The past value is computed from the positions of all elements in the past set of the event
        pastSet = self.pastSet()
        _past = 0
        for event in pastSet:
            _past += -1 * event.t**2 + event.x**2
        _past /= len(pastSet)
        self._past = _past

        return self._past

    def pastSet(self):
        """Compute the past set of the event. Events in the past of both parent events do not count twice (it is a set, not a list).
        The past set is saved to speed up the computation of child event past sets and values."""
        if self._pastSet != None:
            return self._pastSet

        pastSet = set()
        pastSet.add(self)

        if self.pastLeftMovingEvent != None:
            pastSet |= self.pastLeftMovingEvent.pastSet()
        if self.pastRightMovingEvent != None:
            pastSet |= self.pastRightMovingEvent.pastSet()
        self._pastSet = pastSet

        return self._pastSet
