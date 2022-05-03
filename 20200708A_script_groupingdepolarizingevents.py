# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200708A'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# just a single trace of spontaneous activity containing oscs, a handful fastevents and a couple APs.

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15

singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# for each category of APs, see that they are indeed that:
events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
blocknames = des_df[events].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=events,
                                         segments_overlayed=False)
# both spont.APs got nicely picked up; no other kinds of APs recorded in this neuron
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no light-evoked activity recorded in this neuron

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# just 6 events picked up altogether; the smallest one might be a spikelet and some may be compound

# Let's see the events:
# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# Indeed, the smallest one is clearly a spikelet; the two occurring at the most hyperpolarized V have compound rise;
# and the rest has the rise dynamics of fastevents (their decay looks very strange though...)
# Labeling events accordingly:
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev < -42))
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 3))
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not marking neatevents for this neuron: resting baselineV >-40mV throughout, and recording conditions clearly
# changing in the barely 7 minutes that it lasts