"""
Composition method module
Contains all methods used to compute new events from a given event pair
"""

from random import choice

from .event import Event

def wrappedX(x, xMin, xMax):
    """Computes the x position with wrap around between xMin and xMax"""
    newX = (x - xMin) % (xMax - xMin) + xMin
    if newX > xMax or newX < xMin:
        print("Error: new event out of bounds.")
        sys.exit(1)
    return newX

def extendedX(x, xMin, xMax):
    """Leaves the x coordinate as it is for extended space simulations"""
    return x

def futureIntersectionWithWrapAround(xMin, xMax):
    """Event computation with wrap around between xMax and xMin"""
    return futureIntersection(wrappedX, xMin, xMax)

def futureIntersectionWithoutWrapAround(xMin, xMax):
    """Event computation without wrap around. The xMin and xMax values themselves are not important, 
    only their difference, since events at to the left or right with a certain distance (xMax - xMin) are identified."""
    return futureIntersection(extendedX, xMin, xMax)

def futureIntersection(computeX, xMin, xMax):
    """The generic routine to compute new events from two existing events in the future. Depending on the parameters, the wrap can be enabled and customised."""
    def computeIntersection(leftMovingEvent, rightMovingEvent):
        newEvent = Event()

        newEvent.pastLeftMovingEvent = leftMovingEvent
        newEvent.pastRightMovingEvent = rightMovingEvent
        leftMovingEvent.futureLeftMovingEvent = newEvent        
        rightMovingEvent.futureRightMovingEvent = newEvent

        n = 0
        width = xMax - xMin
        while newEvent.t == None and newEvent.x == None:
            # We don't know with or without wrap around whether the new event is constructed from the left or the right 
            # moving event being moved to the left or right from the strip, so we consider all possibilities. 
            t = [
                0.5 * (leftMovingEvent.t + rightMovingEvent.t + (leftMovingEvent.x + n * width) - rightMovingEvent.x),
                0.5 * (leftMovingEvent.t + rightMovingEvent.t + (leftMovingEvent.x - n * width) - rightMovingEvent.x),
                0.5 * (leftMovingEvent.t + rightMovingEvent.t + leftMovingEvent.x - (rightMovingEvent.x + n * width)),
                0.5 * (leftMovingEvent.t + rightMovingEvent.t + leftMovingEvent.x - (rightMovingEvent.x - n * width))
            ]
            x = [
                0.5 * (leftMovingEvent.t - rightMovingEvent.t + (leftMovingEvent.x + n * width) + rightMovingEvent.x),
                0.5 * (leftMovingEvent.t - rightMovingEvent.t + (leftMovingEvent.x - n * width) + rightMovingEvent.x),
                0.5 * (leftMovingEvent.t - rightMovingEvent.t + leftMovingEvent.x + (rightMovingEvent.x + n * width)),
                0.5 * (leftMovingEvent.t - rightMovingEvent.t + leftMovingEvent.x + (rightMovingEvent.x - n * width))
            ]

            # Valid ts are those in the future of the parent events
            valid_ts = [ value for value in t if (value > leftMovingEvent.t and value > rightMovingEvent.t) ]
            if len(valid_ts) > 0:
                # The event to be generated will be the one with the smallest timelike distance to the parent events
                # If there are multiple such events, one is chosen at random (to prevent preference for one direction)
                indices = [i for i, t in enumerate(t) if t == min(valid_ts)]
                i = choice(indices)
                newEvent.t = t[i]
                # The x coordinate is computed based on whether the wrap around is active or not
                newEvent.x = computeX(x[i], xMin, xMax)
                
            # Increase n until there are valid future events
            n = n + 1
        return newEvent
    return computeIntersection
