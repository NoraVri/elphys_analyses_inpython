# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200706E'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise
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
# no DC-evoked APs recorded (no pulses applied); spont.APs all got picked up nicely including one that is waaay
# degenerate (lacking Na-peak completely, just a wide calcium potential). In the light-evoked APs one such degenerate
# AP did get picked up, another did not (different baselineV gives one a peakV > 0mV and the other not).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# looks like light-responses all got picked up quite nicely, though baseline-points not always so great.
# Definitely nothing that is in fact spont. got picked up as evoked.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# looks like events got picked up quite nicely even among the ~20mV oscillations (though oscillations may be
# distorting baseline-points somewhat). Definitely nothing that is in fact evoked got labeled as spont.
# I saw one 'event' at the beginning of recording that is just a noise-thing, let's find and label that by its
# location within the raw data:
# noiseevent = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0000.abf') & (des_df.baselinev < -85))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# now let's see all remaining events.
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
# OK then... Lots of things going on there: distortion of the waveform by oscillations, double events,
# and deterioration.
# # %%
# des_df = singleneuron_data.depolarizing_events
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# Let's start by seeing only events picked up from the first recording file:
# events_underinvestigation = (unlabeled_spont_events
#                              & (des_df.file_origin == 'gapFree_0000.abf'))
# looks like events with amp<4mV are spikelets, not fastevents
# events_underinvestigation = (events_underinvestigation
#                              & (des_df.amplitude > 4))
# The two events occurring here at high baselinev are very early on in the recording, and by rise-time and amplitude
# events_underinvestigation = (events_underinvestigation
#                              & (des_df.baselinev > -42))
# # these should be fastevents (even if they are kind of broad compared to the others). Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Next, the three events with amp 14 - 14.5mV all look like doubles:
# events_underinvestigation = (events_underinvestigation & (des_df.amplitude > 14) & (des_df.amplitude < 14.5))
# indeed: it's not so clear from the events themselves, but from the dV/dt plot there's no doubt that these are doubles.
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# And the single largest remaining event also looks like a double. Labeling it as such:
# events_underinvestigation = (events_underinvestigation & (des_df.amplitude > 17))
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Now let's go back to seeing also events from the other recording files:
# events_underinvestigation = (unlabeled_spont_events
#                              & (des_df.amplitude > 4))
# among these, the second largest one is compound, the rest looks like proper single fastevents.
# Labeling the compound one:
# events_underinvestigation = (events_underinvestigation & (des_df.amplitude > 16.15) & (des_df.amplitude < 16.25))
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# The remaining events are definitely all fastevents. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Finally, let's let's see also smaller events in the other files:
# events_underinvestigation = (unlabeled_spont_events
#                              & ~(des_df.file_origin == 'gapFree_0000.abf'))
# those are definitely fastevents, too, even if amp only ~3mV: rise-time < 0.65ms so they fit the bill. Labeling them:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
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
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not sure if it's worth marking neat events: osc amp is continuously decreasing making me doubt the stability of the
# recording;  plus the huge oscillations (20mV amp) early on really distort the fastevents (also baseline-point is often shifted).