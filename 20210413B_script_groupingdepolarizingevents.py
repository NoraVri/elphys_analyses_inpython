# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210413B'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True, postttl_t_inms=20)
# separately by conditions: low/high light intensity
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000',
                                                color_lims=[-75, -35],
                                                plt_title='high light intensity')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001',
                                                color_lims=[-75, -35],
                                                plt_title='low light intensity')

# %% plotting spontaneous events
des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)

singleneuron_data.plot_depolevents((unlabeled_spontevents),
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

singleneuron_data.plot_depolevents((aps & spont_events),
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# exttracting with standard parameters, min_depolamp 1mV (from seeing the raw data there's a spikelet of ~1mV, and nothing smaller)
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# all evoked things got extracted quite nicely, and with good baseline-points, too

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# Definitely all fast-events that my eye picked up got picked up by the algorithm, too; also some
# spikelets (~1mV) got picked up and in very short stretches of recording also some noise-things.
