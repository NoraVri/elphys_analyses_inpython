# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210426C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not a good recording at all: cell is getting held with -1 - -2nA DC most of the time to keep a halfway
# decent baselineV; still, cell is doing spont.APs and fastevents and responding to light (looks like synapse and/or spikelets: rise-time 2-3ms and amp increasing with hyperpolarization)

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()


# %% summary plots - all events:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   plot_dvdt=True)

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
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
# There are two events of 35-40mV I thought would be spont.APs but didn't get labeled as such; indeed they may just be giant fastevents.
# Also in aps_oncurrentpulsechange there are 4 kinda small ones that didn't get labeled.
# No light-evoked APs recorded in this neuron.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# far from all light responses got picked up - unsurprising given that most have amp < 2mV.
# Did not see anyting labeled that should actually be spont.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# Looks like events mostly got picked up nicely - I do see quite a lot of events with amp 1 - 1.5mV (not labeled by
# the algorithm) but with the neuron being mostly dead it'd be practically impossible to tell whether those are
# spikelets or fastevents.
# Also one of those small APs evoked by +DC pulse got picked up along with spikeshoulderpeak; labeling these:
# ap_peak = (unlabeled_spont_events & (des_df.peakv_idx == 1374834))
# ap_spikeshoulderpeak = (unlabeled_spont_events & (des_df.peakv_idx == 1374994))
# singleneuron_data.depolarizing_events.loc[ap_peak, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.depolarizing_events.loc[ap_spikeshoulderpeak, 'event_label'] = 'spikeshoulderpeak'
# singleneuron_data.write_results()

# plotting all as-yet unlabeled events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )

# events_underinvestigation = (unlabeled_spont_events) # & (des_df.))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# cleanup:
# Looks like the two giant things are in fact APs (or at least AIS spikes) - one of them has a very clear pre-potential.
# spontaps = (unlabeled_spont_events & (des_df.amplitude > 30))
# # and there's a noise-thing with rise-time < 0.2ms:
# noiseevent = (unlabeled_spont_events & (des_df.rise_time_20_80 < 0.2))
# # and the one event with width > 4ms must be a compound one (its rise is the same as the other events)
# compound_event = (unlabeled_spont_events & (des_df.width_50 > 4))
# singleneuron_data.depolarizing_events.loc[spontaps, 'event_label'] = 'actionpotential'
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# the rest of the events are all fastevents: amps 2 - 15mV, rise-time < 1ms for all.
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not marking neatevents for this neuron: it's terribly leaky and unstable, not a good recording at all.