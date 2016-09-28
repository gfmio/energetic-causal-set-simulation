Energetic Causal Set Simulation
===============================

This simulation was created as part of my MSc research project on causal sets at Imperial College London in 2016. The simulation reproduces the results reported in "The universe as a process of unique events" (Marina Cortês & Lee Smolin, 2014, [arXiv:gr-qc/1307.6167v3](http://arxiv.org/pdf/1307.6167.pdf)).

The model tries to explain the emergence of space-time from discrete space-time events that are causally connected. The model differentiates from other causal set models by postulating that time and energy-momentum are fundamental and attached to the events and links in the causal set.

# The simulation

The simulation is in 1+1 dimensional Minkowski space. Initally, `nPast` events get randomly placed at x positions in an interval from 0 to 10 at t=0. Then based on a selection rule, two events get selected, from whom a future event is calculated using a composition rule.

The simulation can be run as follows:

`./simulation.py [nPast=10] [nEvents=1000] [seed=None] [--nonlocal] [--nowrap] [--xmin xMin] [--xmax xMax] [--plotdir plotDir] [--plotdir plotDir] [--plottype (png|pdf)] [--show]`

The first two positional arguments determine the number of inital and generated events. The third positional argument is a seed value used to initiate the pseudo random number generator. Since the same seed produces the same set of random numbers, this allows for simulations to be reproducable, if the same options are supplied. If no seed value is supplied, the seed will be the current system time upon execution.

If the `--nonlocal` option is supplied, a non-local selection rule based on maximally different pasts of the events is used, otherwise a local selection rule based on minimally different pasts of the events is used. If the `--nowrap` option is supplied, the composition rule will create events in extended space, otherwise, the points at the end of the strip, where the events were generated, are identified, corresponding to the strip being "wrapped around" to form a cylinder. The `--xMin` and `--xMax` parameters can be used to supply a custom position for the strip (default are xMin=0, xMax=10). The `--plotdir` option allows to specify an arbitrary directory for the plots, default is `./plots` and the `--plottype` option allows to output the plot in various formats, as supported by matplotlib, e.g. png or pdf.

Since only a supplied seed value will result in reproducable plots, the plots are only saved into the `plotDir`, if such a value is supplied. The filename is constructed from the parameters of the simulation to allow a quick identification of plots and simulation parameters. The `--show` option allows the plot to be displayed interactively once the simulation has completed. By default, simulations with a supplied seed value will not be shown, but only saved to file, while a simulation without a seed value will always be shown.

License: MIT
