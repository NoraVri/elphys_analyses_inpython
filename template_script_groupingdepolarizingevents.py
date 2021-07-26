# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = ''
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
nbins = 50
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


# %%
# summary plots:
aps = des_df.event_label == 'actionpotential'
comound_events = des_df.event_label == 'compound_event'
fastevents = des_df.event_label == 'fastevent'
possibly_unlabeledspontfastevents = ((~des_df.applied_ttlpulse)
                                     & des_df.event_label.isna()
                                     & (des_df.amplitude > 3)
                                     )
#
singleneuron_data.plot_depoleventsgroups_overlayed(aps, fastevents, comound_events, possibly_unlabeledspontfastevents,
                                                   group_labels=['APs', 'fastevents', 'compound events', 'possibly fast-events'],
                                                   do_baselining=True,
                                                   # do_normalizing=True,
                                                   plot_dvdt=True,
                                                   )
#
# singleneuron_data.plot_depolevents(possibly_unlabeledspontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )

# fastevents_df = des_df[fastevents]
# fastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=15)
# singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=15)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)

# %% plots for publication figures


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:


# block_no = 0
# segment_no = 0
# time_slice = [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# check that AHP width window wide enough
# )

singleneuron_data.get_depolarizingevents_fromrawdata()
singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# plotting events parameters:
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )

# plotting events:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df))
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )


# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
aps = des_df.event_label == 'actionpotential'
# singleneuron_data.plot_depolevents((aps & spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
# singleneuron_data.plot_depolevents((aps & ~spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='light-evoked APs')






