#!/usr/bin/env python3
"""
Energetic Causal Set simulation main module
"""

import argparse
import os
import random

from lib import CausalSet, init, select, compose

def main(seed, nPast, nEvents, nonLocal, noWrap, xMin, xMax, plotDir, plotType, showPlot):
    """Main simulation routine"""

    # Create plot directory if it does not exist and the causal set will be plotted
    if seed != None and not os.path.exists(plotDir):
        os.makedirs(plotDir)

    # Initialise random number generator, None corresponds to using the current system time
    random.seed(args.seed)

    print('Starting simulation: nPast={}, nEvents={}, seed={}'.format(nPast, nEvents, seed))

    # Create causal set
    initMethod = init.poissonOnStrip(nPast, xMin, xMax)
    selectionMethod = select.maxPastSelection if nonLocal else select.minPastSelection
    compositionMethod = compose.futureIntersectionWithoutWrapAround(xMin, xMax) if noWrap else compose.futureIntersectionWithWrapAround(xMin, xMax)
    causalSet = CausalSet.init(initMethod, selectionMethod, compositionMethod)

    # Grow causal set nEvents times
    causalSet.growN(nEvents)

    # Set plotting filename, if the seed is set, for reproducibility
    fileName = None
    if seed != None:
        fileName = os.path.join(plotDir, 'plot_{}_{}_{}_{}_{}_{}_{}.{}'.format('nonlocal' if nonLocal else 'local', 'nowrap' if noWrap else 'wrap', xMin, xMax, nPast, nEvents, seed, plotType))

    title = 'Energetic causal set simulation with $nPast={}$ initial events and \n$nEvents={}$ generated events using the {} selection rule\n {} with $xMin={}$ and $xMax={}${}'.format(
        nPast, nEvents,
        'non-local' if nonLocal else 'local',
        'in extended space' if noWrap else 'on a strip with wrap-around',
        xMin, xMax,
        '' if seed == None else ' with seed {}'.format(seed)
        )

    # Plot the causal set
    causalSet.plot(title, fileName, showPlot)

    print('Completed simulation')
    return

def parseArgs():
    """Parse arguments"""

    # Determine simulation arguments
    parser = argparse.ArgumentParser(description='Energetic causal set simulation.')
    parser.add_argument('nPast', metavar='nPast', type=int, nargs='?', default=10,
                    help='Number of past events (at t=0)')
    parser.add_argument('nEvents', metavar='nEvents', type=int, nargs='?', default=1000,
                    help='Number of events to be generated')
    parser.add_argument('seed', metavar='seed', type=int, nargs='?', default=None,
                    help='Seed value for the random number generator')
    parser.add_argument('--nonlocal', dest='nonLocal', action='store_const', const=True, default=False,
                    help='Use non-local selection rule (maximally different pasts)')
    parser.add_argument('--nowrap', dest='noWrap', action='store_const', const=True, default=False,
                    help='Simulation in extended space (no wrap around)')
    parser.add_argument('--xmin', dest='xMin', type=float, nargs='?', default=0,
                    help='Simulation in extended space (no wrap around)')
    parser.add_argument('--xmax', dest='xMax', type=float, nargs='?', default=10,
                    help='Simulation in extended space (no wrap around)')
    parser.add_argument('--plotdir', dest='plotDir', type=str, nargs='?', default='./plots',
                    help='Plot output directory')
    parser.add_argument('--plottype', dest='plotType', type=str, nargs='?', default='pdf',
                    help='Plot output directory')
    parser.add_argument('--show', dest='show', action='store_const', const=True, default=False,
                    help='Show plot')
    args = parser.parse_args()

    # Always show plot, if the seed is None / random
    args.show = args.show or (args.seed == None)

    return args

if __name__ == '__main__':
    args = parseArgs()
    main(args.seed, args.nPast, args.nEvents, args.nonLocal, args.noWrap, args.xMin, args.xMax, args.plotDir, args.plotType, args.show)

