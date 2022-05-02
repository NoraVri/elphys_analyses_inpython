# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190527C'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# neuron has good resting potential (-50 - -55mV) and responds to light with fast things of amp up to to 60mV
# - not sure if those are meant to be APs... Also notably, +DC current can drive this neuron way > 0mV
# without activating an AP. Spont. fastevents are very few but definitely there.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise

# %% summary plots - all events:
# histograms of events parameters
nbins = 100
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')

singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()

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
# None of the aps_oncurrentpulsechange are actually that: the current takes the measured membrane voltage
# up to ~+50mV without ever eliciting an AP. Events in this group that have amp > 10mV are currentpulsechanges,
# the other things are noiseevents (very small amp, but +peakV got them labeled as 'actionpotential').
# Labeling as such:
# currentpulsechanges = (aps_oncurrentpulsechange & (des_df.amplitude > 10))
# noiseevents = (aps_oncurrentpulsechange & (des_df.amplitude < 10))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Same story for things marked aps_spont: they are small-amp noise-things riding +DC pulses that take
# membrane voltage > 0mV without eliciting AP. Labeling them accordingly:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Nothing light-evoked got labeled as AP automatically (peakVs up to ~-10mV tops).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# response peaks all got picked up quite nicely, baseline-points a little less so; not surprising given that the light
# response usually starts as a rather broad, slow-rising potential. Definitely nothing that is in fact spontaneous
# got labeled as evoked.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# Definitely nothing that is in fact evoked got labeled as spont. Other than that, we do have some problems here with
# noise-things getting picked up as events: in the first recording file (gapFree_0000) noise-things riding on DC pulses
# get large enough amp to get picked up as events; same towards the end of recordings (light_0001) where neuron grows
# suddenly visibly noisier and leakier. Let's find these events by their location within the raw data and
# label them as noise:
# gf_block_noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx < 1000000))
# light_block_noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'light_0001.abf') & (des_df.segment_idx > 8))
# singleneuron_data.depolarizing_events.loc[(gf_block_noiseevents | light_block_noiseevents), 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# now let's see the remaining events:
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
#
# events_underinvestigation = (unlabeled_spont_events)
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# # the very first fastevent that this neuron displays in the recording has a noticably wider peak than all the others, but its rise-time (<1ms) and amp (just over 3.5mV) measurements fit right in with the fastevents group, so I will label it as such.
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# notes:
# Neuron's baselineV is ~-50 - -55mV throughout recording, but with noise in a range up to ~3mV which makes me think
# it's not very happy; plus the fact that I cannot evoke AP with somatic depolarization makes it very hard to judge
# the health of this neuron, making me loath to put it on the 'neat' pile. So, I will not label any neat events for
# this neuron.