# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210411A'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# neuron very steady in terms of keeping baselineV and doing wacky oscillations; not seeing much of anything else though
# (also no response to light). Notes say had to break in with buzz because kiss wouldn't work.


# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned(prettl_t_inms=300, postttl_t_inms=500)

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
# # none of the aps_oncurrentpulsechange are actually that: V gets driven well >0mV and there are some ap-like things
# # riding the depolarizations occasionally, but no real APs. Labeling them all as currentpulsechange:
# singleneuron_data.depolarizing_events.loc[aps_oncurrentpulsechange, 'event_label'] = 'currentpulsechange'
# # also spont.APs aren't actually that, but noise-things riding the +DC pulses. Re-labeling them, too:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# no light-evoked APs in this neuron.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no events labeled; not surprising given that there is no response to light.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# lots of cleanup to do here - mostly currentpulsechanges that didn't get labeled right, occasionally
# osc peaks that got picked up as events.
# In gapFree_0001, towards the end of the trace currentpulsechanges didn't get labeled right:
# currentpulse_events = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0001.abf')
#                        & (des_df.peakv_idx > (20000 * 50)))
# # in gapFree_0007 it's all just noise-things and osc peaks (they get real steep when neuron is far hyperpolarized)
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0007.abf'))
# # in gapFree_0008 there's another currentpulse-change that didn't get labeled right
# currentpulse_event2 = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0008.abf'))
# # in file gapFree_0009 some more currentpulsechanges in the first bit of the recording
# currentpulse_events3 = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0009.abf')
#                         & (des_df.peakv_idx < (20000 * 60)))
# # and in file gapFree_0000 it's all currentpulsechanges except for two events towards the middle of the recording
# # (one of which has a bad baselineV point)
# currentpulse_events4 = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0000.abf')
#                         & ~((des_df.peakv_idx > (20000*145)) & (des_df.peakv_idx < (20000*165))))
# all_currentpulse_events = (currentpulse_events | currentpulse_event2 | currentpulse_events3 | currentpulse_events4)
# singleneuron_data.depolarizing_events.loc[all_currentpulse_events, 'event_label'] = 'currentpulsechange'
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Now let's see what we're left with:
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
# events_underinvestigation = (unlabeled_spont_events) # & (des_df.))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# Well I'm not too sure what to do with those - they practically all look different, but they're all large amp with pretty fast rise-time.
# events = unlabeled_spont_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

# Final judgement: out of the remaining 7 events, I think two are likely to be fastevents: rise-time is very fast (0.2ms),
# amplitudes are different (4 and 8mV) yet waveforms look practically identical. The other events look to me more like
# Ca-spikes arising somewhere far away in the dendrites.
# Labeling fastevents:
# fastevents = (unlabeled_spont_events & (des_df.rise_time_20_80 <= 0.5))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not marking neatevents for this neuron: baselineV may be good and stable, but there are no APs anywhere (can't be
# evoked using DC either) so no way to judge recording quality on this point.