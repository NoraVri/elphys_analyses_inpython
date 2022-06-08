# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import singleneuron_analyses_functions as snafs

neuron_name = '20160712B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# very nice recording of oscillating neuron with steady baselineV; has fastevents and spont.APs initially but they disappear.
# Has a beautiful reconstructred morph.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# neuron kicks into very steeply wacky oscillations towards the very end (after ~1hr of recording) some of which are
# probably gonna get picked up as 'events' by the algorithm. Other than that though the oscs are very steady in
# freq (~8mV), a little less so in amp, though it's generally between 3 - 8 mV. AHPs are 100-120ms max.

# block_no = 0
# segment_no = 0
# time_slice = [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# # check that AHP width window wide enough
# )
# extraction with default settings looks quite good; we don't need all the very small events, so I'll just skip those for now.

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1.5)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# for each category of APs, see that they are indeed that:
events = aps_oncurrentpulsechange  #aps_spont
blocknames = des_df[events].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=events,
                                         segments_overlayed=False)
# the 4 APs recorded for this neuron all got labeled properly.
# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# extraction looks really quite good - not all events got picked up (on purpuse, by limiting amplitude to >1.5mV) and
# indeed it looks like the group of smallest-amp events are all spikelets, not fastevents.
# In IV files, the only 'events' that got picked up are all Ca in response to release from hyperpolarization - I'll
# start by labeling these as currentpulsechanges:
# currentpulsechanges = (unlabeled_spont_events & (des_df.file_origin.str.contains('IV')))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()

# Now let's see the remaining events:
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
# It's very clear that only events > 4mV could be fastevents; and then there's a single large and fast-rising event
# that occurs at the most depolarized baselineV that looks like a Ca-spike to me (definitely has a VERY different shape
# from the fastevents).
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 4) & (des_df.baselinev < -42))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# In the remaining events it's very clear that a few of them are compound: they have wider peaks,
# and the dV/dt plot shows an extra bump. Labeling events accordingly:
# compound_events = events_underinvestigation & (des_df.width_70 > 1.6)
# fastevents = events_underinvestigation & (des_df.width_70 < 1.6)
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through sub-threshold events and labeling fastevents -- ####

# %% getting fastevents traces packaged for sending
fastevents_df = des_df[fastevents]
blocknameslist = singleneuron_data.get_blocknames(printing='off')

tracesnippet_length_inms = 30
sampling_frequency = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_rate)
sampling_period_inms = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_period) * 1000
tracesnippet_length_insamples = int(tracesnippet_length_inms / sampling_period_inms)
prepeakwindow_inms = 5

eventstraces_array = np.zeros((tracesnippet_length_insamples, len(fastevents_df)))
running_index = 0
for _, event in fastevents_df.iterrows():
    block_idx = blocknameslist.index(event.file_origin)
    segment_idx = event.segment_idx
    vtrace_full = np.squeeze(np.array(singleneuron_data.blocks[block_idx].segments[segment_idx].analogsignals[0]))
    _, noisetrace = snafs.apply_filters_to_vtrace(
    vtrace_full,
    singleneuron_data.rawdata_readingnotes['getdepolarizingevents_settings']['oscfilter_lpfreq'],
    singleneuron_data.rawdata_readingnotes['getdepolarizingevents_settings']['noisefilter_hpfreq'],
    sampling_frequency,
    plot='off')
    vtrace_denoised = vtrace_full - noisetrace
    event_startidx = (event.peakv_idx - (int(prepeakwindow_inms / sampling_period_inms)))
    event_trace = vtrace_denoised[event_startidx:event_startidx + tracesnippet_length_insamples]
    eventstraces_array[:, running_index] = event_trace
    running_index += 1

import os
os.chdir(path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy")
np.savetxt('cell20160712B_fastevents.txt', eventstraces_array, delimiter=',')
