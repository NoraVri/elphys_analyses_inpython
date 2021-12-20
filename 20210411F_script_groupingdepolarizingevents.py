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

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# exttracting with standard parameters, min_depolamp 1mV (from seeing the raw data there's a spikelet of ~1mV, and nothing smaller)
singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:

