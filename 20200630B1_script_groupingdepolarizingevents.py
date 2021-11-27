# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200630B1'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# doesn't seem to have any spont. fast-events, although in the evoked response there occasionally seems to be one

# %% plotting light-evoked activity

singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True)

# %% extracting depolarizing events
# notes:
# using default parameter settings
singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=10)
singleneuron_data.write_results()

# %%
des_df = singleneuron_data.depolarizing_events
singleneuron_data.plot_depolevents((des_df.amplitude > 2),
                                   colorby_measure='baselinev',
                                   )