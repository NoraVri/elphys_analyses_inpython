# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190812A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


# summary plots:

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# interesting neuron, with wacky oscillations and loads of spont.fast-events; not oscillating for a few minutes when
# first broken into, but also I saw only 1 fast-event there.
# Once blockers get applied, first fast-events go away, then osc amp increases from ~2 to ~8mV for a few minutes and goes back down again.

# I'll use blocks 1 (no blockers, yes oscillations) and 3 (with blockers) to tune get_depolarizingevents parameters.
# I don't see any real reason to change any of the detection values - this is a very lively neuron, all those tiny
# things that get picked up may very well indeed be spikelets.

# block_no = 1
# segment_no = 0
# time_slice = [300, 400]
# #
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolamp=0.1,
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.1)
# singleneuron_data.write_results()


# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-evoked experiments recorded for this neuron (though it does have glu-blockers applied).

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# plotting events parameters:
possibly_spontfastevents_df = des_df[unlabeled_spont_events]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )






















# %% plots: seeing that depolarizing events got extracted nicely - done on amp>3mV events (so extracted) only
# des_df = singleneuron_data.depolarizing_events
#
# # 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# # notes:
#
#
# # 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# # singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# # notes:
#
#
# # Let's see some events, and their amplitude and rise-time to narrow down from there:
# probably_neatevents = (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx > 12000000)
# possibly_spontfastevents = (possibly_spontfastevents & probably_neatevents)
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# nbins = 50
# possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
#
# # probably_neatevents = (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx > 12000000)
# # possibly_spontfastevents = (possibly_spontfastevents & probably_neatevents)
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
#
# # Let's check that there isn't things in the previously filtered events that are very clearly fast-events, too;
#
#
# # %%
# lowdvdt_events = (des_df.maxdvdt < 0.4) & possibly_spontfastevents
# highdvdt_events = (des_df.maxdvdt > 0.4) & possibly_spontfastevents
#
# singleneuron_data.plot_depolevents(lowdvdt_events,
# colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# singleneuron_data.plot_depolevents(highdvdt_events,
# colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
#
# singleneuron_data.plot_rawdatablocks('shortPulse', events_to_mark=lowdvdt_events,
#                                      time_axis_unit='s', segments_overlayed=False)
#
#
#
# # 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
# aps = des_df.event_label == 'actionpotential'
# # singleneuron_data.plot_depolevents((aps & spont_events),
# #                                    do_baselining=True,
# #                                    colorby_measure='baselinev',
# #                                    prealignpoint_window_inms=30,
# #                                    plotwindow_inms = 100,
# #                                    plt_title='spontaneous APs')
# # singleneuron_data.plot_depolevents((aps & ~spont_events),
# #                                    do_baselining=True,
# #                                    colorby_measure='baselinev',
# #                                    prealignpoint_window_inms=30,
# #                                    plotwindow_inms = 100,
# #                                    plt_title='light-evoked APs')
#
#
#
#
#
#
#
# # %% labeling of selected events: compound conditions
# fastevents_largerthan_params = {
#                                 'amplitude': 0.5,
#                                 # 'baselinev':-80,
#                                 }
# fastevents_smallerthan_params = {
#                                  'rise_time_20_80': 0.7,
#                                  }
# fastevents_candidates = unlabeled_events
# for key, value in fastevents_largerthan_params.items():
#     fastevents_candidates = fastevents_candidates & (des_df[key] > value)
# for key, value in fastevents_smallerthan_params.items():
#     fastevents_candidates = fastevents_candidates & (des_df[key] < value)
#
# singleneuron_data.plot_depolevents(fastevents_candidates,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    prealignpoint_window_inms=10,
#                                    plotwindow_inms=30,
#                                    plt_title='presumably all fast-events')
#
# # %% labeling fast-events as such, and saving the data table
# singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events
