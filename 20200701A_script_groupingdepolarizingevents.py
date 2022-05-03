# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200701A'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# pretty nice recording, even though it deteriorates some before light applications; has some spont.APs and fastevents.
# %% plotting light-evoked activity
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
# spont. and light-evoked APs all got picked up nicely; no DC-evoked APs recorded in this neuron.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# all light-evoked responses got picked up, looks like even baseline-points came out pretty good.
# Definitely nothing that is in fact spont. got labeled as evoked.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# everything that looks like an event to me by eye indeed got picked up, and definitely
# nothing that is in fact evoked got labeled as spont. Looks like practically all picked up events should be fastevents.

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
# indeed, those are all fastevents. The smallest one (amp just over 2 mV) seems to have a slightly faster decay than
# all the others, but I think that is because of changing recording conditions - AP amp suddenly loses 20mV after the
# first ~12minutes of recording (depolarization clearly visible in the raw data).
# Labeling them all as fastevents:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# This starts out as a very neat recording, and then cell gets visibly more leaky (depolarizing,
# 20mV decrease in AP amp) at pretty much exactly 800s. So I will label the first 800s of recording as 'neat':

# block_name = 'gapFree_0000.abf'
# window_start_t = 0
# window_end_t = 800
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# if block_name in singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'].keys():
#     trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'][block_name]['t_start']
# else: trace_start_t = 0
# neatrecording_start_idx = (window_start_t - trace_start_t) * float(sampling_frequency)
# neatrecording_end_idx = (window_end_t - trace_start_t) * float(sampling_frequency)
# neat_events = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx >= neatrecording_start_idx)
#                        & (des_df.peakv_idx < neatrecording_end_idx)
#                        )
# adding the neatevents-series to the depolarizing_events-df:
# neat_events.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neat_events)
# singleneuron_data.write_results()
