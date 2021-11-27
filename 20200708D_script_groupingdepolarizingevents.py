# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200708D'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section3
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
# smallslowevents = unlabeled_spontevents  # unless seen otherwise

# %% plotting light-evoked activity
# two files at different light intensities
# 30%
singleneuron_data.plot_rawdatatraces_ttlaligned('0000', plt_title='light intensity = 30%',
                                                # color_lims=[-80, -45],
                                                colorby_measure='applied_current',
                                                color_lims=[-700, 0],
                                                prettl_t_inms=1,
                                                postttl_t_inms=20,
                                                plotlims=[-5, 102, -5.2, 15],
                                                # do_baselining=False, plotlims=[-80, 45, -5.2, 15],
                                                )
# 3% - except in sweep2 where 2%=no light on at all
singleneuron_data.plot_rawdatatraces_ttlaligned('01', skip_vtraces_idcs=[1], plt_title='light intensity = 3%',
                                                # color_lims=[-80, -45],
                                                colorby_measure='applied_current',
                                                color_lims=[-700, 0],
                                                prettl_t_inms=1,
                                                postttl_t_inms=20,
                                                plotlims=[-5, 102, -5.2, 15],
                                                # do_baselining=False, plotlims=[-80, 45, -5.2, 15],
                                                )

# %% plotting spont.APs and depolarizing events:
# they all got picked up nicely by the algorithm; the last one (occurring during light protocol) should be excluded
# though, as it occurs due to the neuron severely depolarizing and then dying.
# singleneuron_data.plot_depolevents((aps & spont_events & ~(des_df.file_origin == 'light_0001.abf')),
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=7,
#                                    plotwindow_inms=22)

# finding the right depolarizing events to go along with the APs:
# singleneuron_data.plot_depolevents(fastevents,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=7,
#                                    plotwindow_inms=22
#                                    )
# that's not so neat; let's try and take only fastevents immediately preceding or following APs
fastevents_idcs = []
for idx in des_df[(aps & (des_df.file_origin == 'gapFree_0000.abf'))].index:
    precedingevent = des_df.iloc[idx - 1]
    if precedingevent.event_label == 'fastevent':
        fastevents_idcs.append(idx - 1)
    followingevent = des_df.iloc[idx + 1]
    if followingevent.event_label == 'fastevent':
        fastevents_idcs.append(idx + 1)
fastevents_idcs = list(set(fastevents_idcs))
fastevents_forplotting = pd.Series(des_df.index.isin(fastevents_idcs))

singleneuron_data.plot_depolevents(fastevents_forplotting | (aps & spont_events & ~(des_df.file_origin == 'light_0001.abf')),
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=7,
                                   plotwindow_inms=22)


# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# evoked events are all rather large and fast, and all seem to have gotten picked up with nice baseline-points

# Seeing that spontaneous fast-events got picked up:
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spontevents, segments_overlayed=False)
# notes:
# Generally looking very nice; I did not see any events that should have gotten picked up but didn't.
# 1. There are two stretches of recording where noise-things got picked up: the second half of the final recording trace
# where the neuron dies, and another short stretch during spont.activity recording where the neuron seems to have a
# small stroke. Labeling these things as noiseevents:
# noiseevents_light = unlabeled_spontevents & (des_df.file_origin == 'light_0001.abf') & (des_df.segment_idx == 13)
# # gapFree between 450 and 455s (-28 for trace start t)
# sampling_freq = float(singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate)
# noiseevents_gapfree = unlabeled_spontevents & (des_df.file_origin == 'gapFree_0000.abf') \
#                       & (des_df.peakv_idx > (422 * sampling_freq)) & (des_df.peakv_idx < (427 * sampling_freq))
# noiseevents = (noiseevents_light | noiseevents_gapfree)
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# 2. In the now remaining events there is one left that is definitely not a fast-event; turns out it's a
# currentpulsechange that didn't get labeled as such. Re-labeling it now:
# currentpulsechange = (des_df.file_origin == 'gapFree_0000.abf') & (des_df.width_50.isna())
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# 3. The now remaining events all have parameters falling within what we think of as fast-events
# (rise-time up to 0.7ms, amps 2 - 14mV). However, not only is the amplitude grouping not very clear,
# the shape also looks to vary quite a lot, with some events having much rounder shapes than others.
# Hyperpolarizing seems to make events narrower, whereas at resting baselinev they grow steadily rounder/wider again.
# Still, I see no reason why these shouldn't all be fastevents. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[unlabeled_spontevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# nbins = 50
# events_underinvestigation = unlabeled_spontevents
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# des_df[events_underinvestigation].hist(column=['width_10', 'width_30', 'width_50', 'width_70'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation - widths')
# singleneuron_data.scatter_depolarizingevents_measures('width_70', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )


#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %%