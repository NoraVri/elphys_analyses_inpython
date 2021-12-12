# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210411F'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True)

# separately by conditions: small/large illumination field size, and intensity
# small spot low intensity: files 2, 4, 6
singleneuron_data.plot_rawdatatraces_ttlaligned('2', '4', '6',
                                                plt_title='small field, low intensity',
                                                postttl_t_inms=20)
# large spot low intensity: files 1, 3, 7
singleneuron_data.plot_rawdatatraces_ttlaligned('1', '3', '7',
                                                plt_title='large field, low intensity',
                                                postttl_t_inms=20)
# large spot high intensity: files 0, 5, 8
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000', '5', '8',
                                                plt_title='large field, high intensity',
                                                postttl_t_inms=20)

# %% extracting depolarizing events


