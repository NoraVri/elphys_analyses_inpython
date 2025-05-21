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
neuron_name = '20250410B1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# nice long recording (1.5hr), though with some problems: VC data clipped at 200pA, and there may be multiple bouts
# where neuron isn't spiking at all for minutes on end (though it seems to revive at least once).

## raw data cleanups
# # removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_tempUp_0002 (detection threshold = 2)
# t_start: 97000; mean freq.=15.515851805183907, CoV=0.04468598935119824 (just after tuning pulses turned off)
# t_end: 180000; mean freq.=14.953371297909033, CoV=0.04592149960728254 (end of this block)

# use file gapFree_tempUp_0004
# t_start: 0; mean freq.=15.423535308998796, CoV=0.04503843433226727
# t_end: 379000; mean freq.=15.758406858595105, CoV=0.05790106929920752

# recording condition: gabazine wash in
# use file gapFree_GabazineWashIn_0000
# t_start: 0; mean freq.=15.144239648358143, CoV=0.053794835312377436 (no gabazine effect yet)
# t_end: 91000; mean freq.=17.577050544083505, CoV=0.06586854768420272 (gabazine may just about be taking effect)

# recording condition: gabazine applied
# use file gapFree_withGabazine_0000
# mean freq.=19.39524558382173, CoV=0.07036907145625469 (entire block; >5min. of recording)
# t_start: 0; mean freq.=17.846270481698348, CoV=0.04642592815856638
# t_start: 150000; mean freq.=20.359165140287363, CoV=0.04398544433394519
# t_end: 358000; mean freq.=21.16884160883191, CoV=0.047855168076744566

# recording condition: gabazine applied, quinpirole washin (>5min. of recording; drug should be in effect by the end)
# use file gapFree_withGabazine_quinpiroleWashIn_0000
# t_start: 0; mean freq.=21.741642951302403, CoV=0.04823544637438149 (detection threshold = 150)
# t_end: 288000; mean freq.=26.14365974461456, CoV=0.299859344400282 (just before neuron seems to abruptly stop spiking; detection threshold = 200)

# recording condition: gabazine and quinpirole applied
# I'm gonna say this block is no good; yes, it looks like cell goes back to spiking about halfway through but the pattern looks very ugly (both in amplitudes and over time) - not hallmarks of a healthy cell.
neuron_data.rawdata_remove_nonrecordingblock('gapFree_tempUp_withGabazine_with_quinpirole_0000.abf')
neuron_data.rawdata_remove_nonrecordingblock('gapFree_tempUp_drugsWashOut_0000.abf')
neuron_data.rawdata_remove_nonrecordingblock('gapFree_tempDown_drugsWashOut_0000.abf')
neuron_data.write_results()