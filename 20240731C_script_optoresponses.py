# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import os
import re
import json

neuron_name = '20240731C'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')

# Very nice sealing and break-in (@t=77.373s in gapFree_0000) while neuron spiking with freq just below 40Hz.
# AP peakV ~+20mV, AHPmin ~-47mV initially, keeps at ~-70mV w/ -100pA DC;
# After optoStim experiments, holding increased to -150pA to keep ~-70mV but AP parameters barely seem to have changed
# Active properties do seem to have deteriorated after longPulse experiments, will have to pay attention to that in analyses.

# %%
