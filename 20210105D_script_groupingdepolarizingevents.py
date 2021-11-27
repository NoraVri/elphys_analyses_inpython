# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210105D'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
# smallslowevents = unlabeled_spontevents  # unless seen otherwise

# %% plotting light-evoked activity
# just one block with light, and first 4 traces it's not actually on
singleneuron_data.plot_rawdatatraces_ttlaligned(skip_vtraces_idcs=[0, 1, 2, 3],
                                                colorby_measure='baselinev')

# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=10)
# singleneuron_data.write_results()

# %% plotting spont. depolarizing events
singleneuron_data.plot_depolevents(unlabeled_spontevents,
                                   colorby_measure='baselinev')

singleneuron_data.plot_depolevents((aps & spont_events),
                                   colorby_measure='baselinev')

