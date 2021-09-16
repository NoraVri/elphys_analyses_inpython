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


# summary plots - all events:


# summary plots - 'neat' events:

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
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
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
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
# from these plots it seems highly likely that any event with amp>4mV is a fast-event (or a compound one) by rise-time;
# also by maxdvdt there seems to be a grouping, which should help to determine if the events with amp 2-4mV are also fast-events.
# Notably, there looks to be two groups of fast-events - probably something happened in the recording to make it so. Should check.

# 1. First, let's see events with amp>4mV:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 4))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# indeed, those look mostly like fast-events, but it's not exactly neat - I think there's a few compound ones in there,
# especially in the largest events/those occurring at more depolarized baselinev. Let's see:
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'width_50',
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=events_underinvestigation,
#                                                       )
# well, if there are compound events it's not clear from these distributions... Except for the single largest event
# (which stands out by amplitude and rise-time) which is clearly compound (as seen by dVdt/V-plot shape) I do not see
# any reason why these couldn't all be simple fast-events. Labeling them as such:
# compound_event = (events_underinvestigation & (des_df.amplitude > 14))
# fast_events = (events_underinvestigation & ~(des_df.amplitude > 14))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2. Now let's see events that are <4mV but may still be fast-events:











