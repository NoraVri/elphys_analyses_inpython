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
neuron_name = '20250505A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# looks like a decent enough recording, though signal amplitude not great to start and deteriorating - will have to pay close attention that detection threshold is set well.

# recording condition: baseline @ PT  (initial, and return)
# use file gapFree_0000
# t_end: 70000; mean freq.=17.132157327517564, CoV=0.1655035181240262 (last 30s of first recording file, tuning pulses (mostly) off; detection_threshold=0.3)
# use file gapFree_0001
# t_start: 11000; mean freq.=17.700153367806173, CoV=0.1400593780963499 (start of the file, after small voltage step applied)
# use file gapFree_0002
# t_start: 0; mean freq.=15.18439635305737, CoV=0.1384129587420536 (start of the file)

# use file gapFree_gabazineWashOut_0000
# t_end: 931900; mean freq.=, CoV= (last 30s; it's the best I've got before turning temp down)

# recording condition: gabazine applied @ PT
# use file gapFree_gabazineWashOn_0003 (gabazine plenty washed on already)
# t_start: 0; mean freq.=14.086892649492956, CoV=0.14177149819294363 (first 30s; detection threshold set to 40 (I think I saw one spike missed and one made up, so that feels kinda fair still))
# t_end: 100000; mean freq.=15.407133502811801, CoV=0.23424735378480102 (last 30s; detection threshold = 45 (feels like the magic number where as many spikes are missed as made up; still no more than ~3 here or there))
# use file gapFree_with_gabazine_0000
# t_start: 0; mean freq.=13.771878430342579, CoV=0.14786511104815922 (first 30s; detection threshold=45, extracted numbers vary very little for setting it 40-50)
# t_end: 338000; mean freq.=14.719219981927907, CoV=0.18348542325805675 (last 30s; detection threshold=45, changing it starts to make a rather significant difference)

# recording condition: baseline @ RT (where baseline means: washed of drugs)
# t_start: 0; mean freq.=14.274198965540403, CoV=0.14865824256979526 (first 30s, where still warm; detection threshold=50 looks like gets all spikes without noise)
# t_start: 900000; mean freq.=4.48137690305346, CoV=0.3987237832107891 (~15min. into cooldown, bath should be mostly RT by now; detection threshold=35 looks still mostly reliable, missing ~3spikes)
# t_end: 960000; mean freq.=4.716244919009524, CoV=0.4674304540866331 (next minute; data going on gets really bad, already here I'm barely trusting that these numbers are reasonably accurate. detection threshold=35)

