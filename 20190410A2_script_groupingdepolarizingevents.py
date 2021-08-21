# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190410A2'
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
nbins = 50
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# nice long recording of neuron doing mostly nothing except maintaining baselinev; then quite far into recordings
# fast-events get turned on (shortPulse and final gapFree file).

fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
probably_spikelets = (unlabeled_spontevents & (des_df.amplitude < 1.7) & (des_df.maxdvdt < 0.12))  # see plots and analyses section

# %%
# summary plots:
# histograms of events parameters
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')

# compound events
des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('compound events parameter distributions')

# spikelets
des_df[probably_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('probably-spikelets parameter distributions')

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots of the main events-groups (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# %%
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% plots for publication figures
# most fast-events occur during shortPulse_0001, so let's see those:
probably_neatevents = ((des_df.file_origin == 'shortPulse_0001.abf'))

singleneuron_data.plot_depolevents((fastevents & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                        'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                                 bins=nbins)
plt.suptitle('fast-events, neat ones only')
# neat compound fast-events:
# singleneuron_data.plot_depolevents((compound_events & probably_neatevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' neat compound events'
#                                    )
# des_df[(compound_events & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                                              'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                                  bins=nbins)
# plt.suptitle('compound events, neat ones only')

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# using the second segment of the final gapFree file to extract events

# block_no = 3
# segment_no = 1
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                             oscfilter_lpfreq=10,
#                                                                             min_depolspeed=0.2  # below that it seems rather random what things get picked up as events, it all mostly just looks like noise
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolspeed=0.2,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-triggered experiments done for this neuron

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
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )

# it seems pretty clear from the amplitude/rise-time scatter what should be fast-events: amp > 2 events all have
# rise-time < 1; at amps below that there's a cloud of events that should be spikelets and such, and the divide
# is really very clear. However, the amp/maxdvdt scatter suggests that there might be some fast-events with amp ~0.2mV
# (there's a few fast-events there with maxdvdt ~0.2, same as one of the groups of larger-amp fast-events).
# %%
# 3. Let's see events with amp>2mV:
events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 2))

singleneuron_data.plot_depolevents(events_underinvestigation,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# I think I'm gonna have to call all of these fast-events - the 'neat ones' don't get turned on until way late into
# the recording, so the handful that come before that I guess can be expected to have a slightly different shape due
# to differences in recording conditions. Labeling them:
singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
singleneuron_data.write_results()

### -- this concludes finding and labeling fast-events for this neuron. -- ###

# hmm... Looking more closely again one could argue that one of the two ~10mV amp events is in fact compound...