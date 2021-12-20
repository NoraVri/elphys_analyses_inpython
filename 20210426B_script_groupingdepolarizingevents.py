# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210426B'
singleneuron_data = SingleNeuron(neuron_name)
singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True, postttl_t_inms=20)
# separately by conditions: low/high light intensity
singleneuron_data.plot_rawdatatraces_ttlaligned()  # only one light file for this neuron, intensity=20%