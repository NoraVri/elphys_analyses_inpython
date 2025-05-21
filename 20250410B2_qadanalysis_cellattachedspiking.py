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
neuron_name = '20250410B2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# looks very nice and usable all throughout, at least by eye

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_tempUp_0002 (detection threshold = 2; baseline lpfilter = 2.5)
# t_start: 55500; mean freq.=13.816925734024176, CoV=0.057134868665487996 (start of recording, tuning pulses first turned off)
# t_start: 95500; mean freq.=13.36193727946928, CoV=0.07061003451177778
# t_end: 132000; mean freq.=13.340905501359291, CoV=0.06961171321955513
# t_end: 182000; mean freq.=12.835417688684016, CoV=0.05439550936416525

# use file gapFree_tempUp_0004
# t_start: 0; mean freq.=12.755445464580921; CoV=0.05214223302447468
# t_end: 379000; mean freq.=13.267031761945793; CoV=0.06416050441250257

# recording condition: gabazine wash in
# t_start: 0; mean freq.=12.755445464580921, CoV=0.05214223302447468
# t_end: 379000; mean freq.=13.267031761945793; CoV=0.06416050441250257

# recording condition: gabazine applied
# use file gapFree_withGabazine_0000
# mean freq.=14.675815587033322, CoV=0.07285757123809047 (entire block; >5min. of recording)
# t_start: 0; mean freq.=12.711637017360273, CoV=0.057669122164863224
# t_start: 150000; mean freq.=15.361008862765486, CoV=0.04694002297188461
# t_end: 358000; mean freq.=14.99290694312779, CoV=0.04661816792965865

# recording condition: gabazine applied, quinpirole wash in (>5min. of recording)
# use file gapFree_withGabazine_quinpiroleWashIn_0000
# t_start: 0; mean freq.=15.075410628668125; CoV=0.04303568308336727
# t_end: 287000; mean freq.=15.02753090623058, CoV=0.04387244533261917

# recording condition: gabazine and quinpirole applied
# use file gapFree_withGabazine_with_quinpirole_0000
# t_start: 0; mean freq.=14.656004087546092, CoV=0.05025663222212914
# t_end: 200000; mean freq.=13.337835272694893; CoV=0.05716086298170085 (just previous to rather sudden change in signal amplitude)
# t_end: 323000; mean freq.=13.869462499559223, CoV=0.06369404758527544 (end of this recording block)

# recording condition: drugs washout
# use file gapFree_tempUp_drugsWashOut_0000 (~13min. of recording; may not be enough for wash to take full effect)
# t_start: 0; mean freq.=13.908205841446453; CoV=0.06318130035627681
# t_end: 820000; mean freq.=13.961805210949388; CoV=0.056092983741238306

# recording condition: drugs washout, cool down to RT
# use file gapFree_tempDown_drugsWashOut_0000 (almost 50 min. of recording)
# t_start: 0; mean freq.=13.87843629579842; CoV=0.0630024987668492
# t_start: 300000; mean freq.=10.348686694353043; CoV=0.05332359541663153
# t_start: 500000; mean freq.=10.896268532484497; CoV=0.059249826393850055
# t_start: 1000000; mean freq.=10.666343648057758; CoV=0.04990218889172881
# t_start: 1500000; mean freq.=10.777077829024979; CoV=0.0468633395814591
# t_end: 2961000; mean freq.=11.940198388408616; CoV=0.0580661350189674
