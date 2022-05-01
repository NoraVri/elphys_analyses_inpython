# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124B'
singleneuron_data = SingleNeuron(neuron_name)
singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# mostly boring neuron with very few spont.fastevents (and no other interesting spont.activity), but holding very nice
# and steady for almost the entire length of recordings, and regularly responding to light with something fast.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise
# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True)

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# pretty boring neuron for the most part, has some spikelets and just one spont. fast-event as far as my eye
# could see (~5mV). Not an overly noisy recording for the most part, but picking up events <1mV amp seems silly
# (things that clearly look like spikelets are larger than that). Other than that, default parameters will do.

# block_no = 0
# segment_no = 0
# time_slice = [4, 154]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# # this neuron doesn't have any spont.APs, only ones driven by huge +DC (no discernible AHP)
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
# singleneuron_data.write_results()

# following extraction, I was clearly wrong about this neuron having just one fast-event: there's clearly
# at least a handful of them, mostly 5-6mV and one example of 3mV, all occurring at resting baselinev.

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
# all looks OK - no spont.APs, and exactly one light-evoked one. In the final recording file (gapFree_0004),
# full APs are no longer evoked by current pulses (at the start of recording they are), but I don't see a point in
# labeling things as AP when they're this degenerate (peakV reaching only ~-20mV).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# not all evoked events got picked up as such, but definitely no spont.events got labeled as evoked so that's OK.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# all evoked events that didn't get picked up as such got labeled spont. instead - their peak comes just a little bit
# too long after the baseline-point that the algorithm finds, and with the stimulus being very short and my having
# forgotten to add a ttl-window value they didn't get labeled as evoked. Doing so now: (no spont.events in the block at all)
# also_evoked_events = (des_df.file_origin == 'light_0000.abf') & ~(des_df.applied_ttlpulse)
# singleneuron_data.depolarizing_events.loc[also_evoked_events, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()
# Other than that things look OK; I saw a single noise-thing that got picked up as event, let's remove it by its
# location in the raw data:
# noiseevent = unlabeled_spont_events & (des_df.file_origin == 'light_0001.abf') & (des_df.segment_idx == 22)
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Finding and labeling fast-events (and other types of events encountered along the way):
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
# From seeing the raw data, I expect just three spikelets - everything else has amp large enough to be fastevent.
# Indeed, the parameter distributions seem to agree: things with amp<2mV also have very small maxdVdt and relatively
# long rise-time. So let's see all the larger events:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 2))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# Indeed, those are all clearly fastevents, with identical normalized decay shape. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# Neuron gets visibly leakier towards the end of the last light-applied block, but up to and including then it's making
# fastevents with exactly identical normalized decay shapes... I'll label all blocks except the very last one as 'neat':
# neat_events = ~(des_df.file_origin == 'gapFree_0004.abf')
# # adding the neatevents-series to the depolarizing_events-df:
# neat_events.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neat_events)
# singleneuron_data.write_results()

