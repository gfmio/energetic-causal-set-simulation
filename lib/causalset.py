"""
Causal set class module
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc

from .event import Event

class CausalSet(object):
    def __init__(self, selectionMethod, compositionMethod):
        """Init method for a CausalSet. The causal set is defined by its selection method and the composition method for growing new events."""
        self.events = []
        self.selectionMethod = selectionMethod
        self.compositionMethod = compositionMethod

    @staticmethod
    def init(initMethod, selectionMethod, compositionMethod):
        """
        Initialise a new causal set with random events provided by initMethod
        initMethod should accept a causal set and return an initialised causal set
        """
        causalSet = initMethod(CausalSet(selectionMethod, compositionMethod))
        return causalSet

    def grow(self):
        """Grow the causal set by selecting a pair of elements using selectionMethod
        and add a new event using compositionMethod"""

        leftMovingEvent, rightMovingEvent = self.selectionMethod(self)
        newEvent = self.compositionMethod(leftMovingEvent, rightMovingEvent)
        self.events.append(newEvent)
        return

    def growN(self, N):
        """Grow the causal set N times"""
        for n in range(0,N):
            self.grow()
            print(str(n+1) + ' of ' + str(N) + ' generated')
        return

    def plot(self, title, fileName, showPlot):
        """Plot the causal set"""
        fig = plt.figure(figsize=(7, 10))

        plt.rc('text', usetex=False)
        plt.rcParams['ps.usedistiller'] = 'xpdf'
        plt.rc('font', family='Linux Libertine O')

        T = list(map(lambda event: event.t, self.events))
        X = list(map(lambda event: event.x, self.events))
        plt.scatter(X,T, marker=",", s=2, edgecolors='none')

        plt.grid(True)
        plt.autoscale(enable=True, axis='both', tight=True)

        plt.axes().set_xlabel('Position $x$')
        plt.axes().set_ylabel('Time $t$')
        plt.axes().set_title(title, fontsize=12,  y=1.02)

        if fileName != None:
            plt.savefig(fileName, dpi=600)
            print('Plot saved to ' + fileName)
        if showPlot:
            plt.show()
