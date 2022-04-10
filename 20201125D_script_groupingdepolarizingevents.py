# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20201125D'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

# des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section3
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
# aps = des_df.event_label == 'actionpotential'
# spont_events = ~des_df.applied_ttlpulse  #
# unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
# unlabeled_spontevents = (spont_events & unlabeled_events)
# smallslowevents = unlabeled_spontevents  # unless seen otherwise

# %% plotting light-evoked activity
# light intensity is identical for all traces, except light_0003 trace1 where light wasn't on
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True,)
# there are different TTL durations, however, only with the longest one does the recording also cover the
# full dynamic range of the neuron.
# Using light 01 only for the plot - plenty of traces there: (light2 has more with APs, but I don't think we need it)
skip_vtraces = list(np.arange(1,len(singleneuron_data.blocks[3].segments),2))
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001',
                                                skip_vtraces_idcs=skip_vtraces,
                                                colorby_measure='applied_current',
                                                color_lims=[-700, 100],
                                                prettl_t_inms=1,
                                                postttl_t_inms=20,
                                                # plotlims=[-5, 102, -5.2, 15],
                                                # do_baselining=False, plotlims=[-95, 45, -5.2, 15],
                                                )
# %%
singleneuron_data.plot_rawdatatraces_ttlaligned('light',
                                                newplot_per_ttlduration=True,
                                                postttl_t_inms=20)



# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=20)
# singleneuron_data.write_results()
# %% seeing spont.APs
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #

singleneuron_data.plot_depolevents((aps & spont_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' spont aps'
                                   )
