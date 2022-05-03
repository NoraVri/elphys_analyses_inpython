# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200701B'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not the greatest recording, but has some spont.fastevents and nice light responses; no APs whatsoever.

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15
# re-running with min_depolamp = 1, because I see a recurring spont.event of ~1mV that stands out very clearly

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1, ttleffect_window=15)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# not a single AP of any kind recorded in this neuron (no DC pulses to see spiking applied).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Looks like all evoked responses got picked up as such very nicely; definitely nothing
# that is in fact spont. got labeled as evoked.
# (This neuron also has some blocks recorded in voltage clamp; nothing got picked up in those).

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# there's definitely spont. depolarizing events in this recording, but the largest one has amp barely over 2mV; I'll
# run the extraction again to catch also some smaller ones (I did also see a few with amp ~0.5mV, but at that amp
# they're very likely to be too noisy to tell whether they're spikelets or fastevents so I'll leave those be for now)
# Seems like all things that got picked up are indeed events, no noise-things seen.

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )

events_underinvestigation = (unlabeled_spont_events)
singleneuron_data.plot_depolevents(events_underinvestigation,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# not sure what to do with these: the measured parameters look mostly OK for fastevents, then again the amps are all
# <3mV and things are noisy enough that it's hard to say whether normalized decays are identical or not.
# In the evoked events the smallest thing is ~4mV.


#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# definitely not marking neat events for this neuron: has bad baselineV throughout, and I'm not even sure
# whether events are spikelets or fastevents.