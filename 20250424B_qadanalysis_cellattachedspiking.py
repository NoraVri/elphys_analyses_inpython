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
neuron_name = '20250424B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# it's a nice enough signal, but spiking is very intermittent and cell stops doing it after ~2min.

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_0004
# t_start: 0; mean freq.=0.3205568530475798, CoV=0.44213803917291306 (recording file start)
# t_start: 25000; mean freq.=0.40222268254373666, CoV=0.5582001356964592 (where some of the fastest spiking observed)
# cell pretty much stops spiking after that.