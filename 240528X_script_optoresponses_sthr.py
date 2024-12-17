# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

neuron_name = '240528X'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Bad telegraphs: ch2 has pA units instead of mV.
# Looks like a pretty nice recording otherwise: cell held with ~-180pA and not showing much of any spontaneous activity.
# Capacitance does seem to change quite a bit over the course of recordings, and quite suddenly between files 0001 and 2


