# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

# quick-and-dirty analysis steps:
# import data, cleanup where necessary (i.e., remove channels not belonging to neuron and/or any any sections recorded in the wrong mode)
# identify unique recording conditions (temperature, drug) and collect all files per condition
# per condition, pick a 30s trace to get numbers from and (manually) place these in excel table

## importing the data
neuron_name = '20250505B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# nothing really to clean up, though there are intermittent periods where neuron is being recorded with tuning pulses on;
# signal very nice, despite (or maybe because of) very loose seal
# Also notably, this neuron is spiking highly intermittently at first: just a handful of spikes in the first minute of recording;
# spiking seems to pick up in bouts, but neuron still pauses for a second or more at the time when first gabazine washin already started.
# From looking at data by eye, spiking freq. inside bouts can be as fast as 80Hz (spiking that fast never seems to be sustained for long though)
# From notes: slices placed into bath @RT, then heater turned on; already found cell in the few min. it takes for bath to warm

## ran gui.py to extract spike peaks

## recording condition: baseline @PT (initial, as well as returns back to this condition)
# use file gapFree_0001
# t_start: 160000; mean freq.=1.795157562475222, CoV=1.949749433203128 (where signal first reliably reaches nA amplitude, and neuron first starts to do some high-frequency bursts)
# t_start: 425000; mean freq.=12.01197066876387, CoV=2.376173965638409 (where neuron seems to really kick into high gear, ending on a high-frequency burst)
# t_end: 640000; mean freq.=1.6299948692206916, CoV=0.8561046852670817 (end of this recording file)
# use file gapFree_gabazineWashIn_0000 - first 2 min. of recording should be still w/o gabazine
# t_start: 0; mean freq.=1.930190216533935, CoV=0.7588739226970019
# t_start: 60000; mean freq.=2.6209070463440107, CoV=1.481101126890021

# use file gapFree_gabazineWashOff_0000 - last 30s should be without gabazine already
# t_end: 1201000; mean freq.=17.66524363315194, CoV=0.21619817209703662
# use file gapFree_gabazineWashed_0000 (5 minutes of recording following 20 minutes of washoff (separate file))
# t_start: 0; mean freq.=13.52371684088659, CoV=0.2676907119532665
# t_end: 318000; mean freq.=17.554968156493842, CoV=0.21747947124248584
# use file gapFree_gabazineWashOffAgain_0000, end of recording file (~20min. after starting wash)
# t_end: 1174000; mean freq.=18.28606641928005, CoV=0.2067006470557995
# use file gapFree_gabazineWashedAgain_tempDown, start of recording file (where still PT, before proper cool down)
# t_start: 0; mean freq.=20.119680294597647, CoV=0.22009316754052807

# use file gapFree_gabazineWashedAgain_tempUpAgain_0000 - end of recording file, where bath should be PT again
# t_start: 353000; mean freq.=13.099727116937673, CoV=0.31478949015932917  (detection threshold set to 200 to avoid problems with tuning pulses)

## recording condition: gabazine applied @PT
# use file gapFree_gabazineWashIn_0000 - last 30s should definitely be with gabazine already
# t_end: 312000; mean freq.=4.605524936716353, CoV=0.47290607000222995
# use file gapFree_gabazineApplied_0000 - note: ~720s into this file, neuron takes a 6s pause in firing, with strong irregularities in firing pattern surrounding this event (not captured in the numbers below)
# t_start: 0; mean freq.=5.296924897414523, CoV=0.34232965043961805 (first 30s)
# t_end: 974000; mean freq.=10.933318531302083, CoV=0.3775481975078477 (last 30s)
# use file gapFree_gabazineWashOff_0000 - first 30s should be still with gabazine
# t_start: 0; mean freq.=13.978823426626297, CoV=0.24146670372733203
# use file gapFree_gabazineAppliedAgain_0000
# t_start: 0; mean freq.=13.2719561221087, CoV=0.33385336468144494 (first 30s)
# t_end: 546000; mean freq.=21.286316011426308, CoV=0.2296332002399605 (last 30s)

## recording condition: baseline @ RT (baseline here is: drugs washed off)
# use file: gapFree_gabazineWashedAgain_tempDown_0000
# t_end: 861000; mean freq.=5.390981802893486, CoV=0.30574799540554126 (last 30s)
# t_end: 801000; mean freq.=5.40850359631473, CoV=0.376436687942869 (a minute earlier)
# t_end: 741000; mean freq.=5.446298644382227, CoV=0.3197122209970797 (a minute earlier)
