# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210113H'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# quite nice stable recording, with stretches of time where DC current is applied to change baselinev (not to keep it in good range).

# %% extracting depolarizing events
# notes:
# this neuron's got loads of events, but response to light is clearly not more than syanpse/spikelet
# using gapFree_0002 for setting extraction parameters

# block_no = 2
# segment_no = 0
# time_slice = [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                                                     min_depolamp=0.2, # anything below that is not clearly recognizable as anything
#                                                                     min_depolspeed=0.15,
#                                                                     oscfilter_lpfreq=10,
# )

singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=10,
                                                     min_depolamp=0.2,
                                                     min_depolspeed=0.15,
                                                     oscfilter_lpfreq=10)
singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 200
# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


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

















# %% analyses done on events>2mV (so extracted) only
# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Definitely all evoked events got picked up as such, and mostly with pretty good parameters, too -
# the response to light is often rather beautiful, with clearly seperable spikelets and a fast-event riding on top
# (and despite all that the fast-event tends to get picked up with a nice baseline point).
# Experiment-day notes say that it didn't look like the fast-event was getting evoked at all, but looking at the full
# traces I'd say it's not just by accident that fast-events often coincide with light (though it should be noted that
# they occur regularly spontaneously, and that the light response often does not include a fast-event).

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# Looks good - definitely all events that are easy to see by eye got picked up, and while there's clearly also a lot of
# events in the range <2mV these generally look clearly like spikelets; fast-events seem to have amps between 3 - 10mV.
# I saw one AP+spikeshoulderpeak that didn't get properly labeled, but aside from those there shouldn't be much to filter.

# Let's see the events, and their amplitude and rise-time to narrow down from there:
# It couldn't be more clear which events are the mislabeled AP and spikeshoulderpeak. Adding their labels:
# ap = (possibly_spontfastevents & (des_df.amplitude > 50))
# singleneuron_data.depolarizing_events.loc[ap, 'event_label'] = 'actionpotential'
# spikeshoulderpeak = (possibly_spontfastevents & (des_df.baselinev > -15))
# singleneuron_data.depolarizing_events.loc[spikeshoulderpeak, 'event_label'] = 'spikeshoulderpeak'
# singleneuron_data.write_results()

# Now let's see all remaining events:
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   )
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
nbins = 40
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude', 'maxdvdt'], bins=nbins)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# By eye one stands out not only for having the highest baselinev, but also because it looks to have a rounder,
# wider shape - but by the parameter distributions it doesn't look out of tune with fast-events.

# # Let's see how things play out when colored by time in the recording:
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='peakv_idx',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='peakv_idx',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='peakv_idx',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='peakv_idx',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
#
# # %%
# baselinerange = ((des_df.baselinev > -55) & (des_df.baselinev < -45))
# singleneuron_data.plot_depolevents((possibly_spontfastevents & baselinerange),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    )
#
#
# # %%
# wider_events = (possibly_spontfastevents & (des_df.maxdvdt < 0.3) & (des_df.amplitude > 4))
# # singleneuron_data.plot_rawdatablocks(events_to_mark=wider_events)
# singleneuron_data.plot_depolevents((wider_events & baselinerange),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    )
# # OK. Definitely none of the wider events occur early on in the recording, but there's still a quite long period of time
#
# # %%
# probably_fastevents = (possibly_spontfastevents & ~wider_events & baselinerange)
# probably_fastevents_df = des_df[probably_fastevents]
# probably_fastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude', 'maxdvdt'], bins=nbins)









# Let's see if the dvdt-plot will make things clearer:
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=1,
#                                    plotwindow_inms=8,
#                                    plot_dvdt=True,
#                                    )
# Indeed, and it looks like the events may be separable by max.dvdt.
# Let's see:
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       spont_events=possibly_spontfastevents
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='width_50',
#                                                       spont_events=possibly_spontfastevents
#                                                       )
# From the scatters it looks like the boundary should be around dvdt=0.04 in the dvdt of the normalized waveform.
# Here's the thing though: the different shapes of the two types of events are very clear from plotting
# dV/dt vs V for the normalized voltage, but maxdvdt does not actually separate between the two groups.
# probably_fastevents = (possibly_spontfastevents & (des_df.maxdvdt > 0.4))
# probably_otherfastevents = (possibly_spontfastevents & ~(des_df.maxdvdt > 0.4))
# plotting the events, in two separate plots
# singleneuron_data.plot_depolevents(probably_fastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=1,
#                                    plotwindow_inms=8,
#                                    plot_dvdt=True,
#                                    plt_title='probably all classic fast-events'
#                                    )
# singleneuron_data.plot_depolevents(probably_otherfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=1,
#                                    plotwindow_inms=8,
#                                    plot_dvdt=True,
#                                    plt_title='probably all other events'
#                                    )
# histograms
# plt.figure(), plt.suptitle('amplitude (mV)')
# des_df.loc[probably_fastevents, 'amplitude'].hist()
# des_df.loc[probably_otherfastevents, 'amplitude'].hist()
# plt.figure(), plt.suptitle('rise-time (10-90%)')
# des_df.loc[probably_fastevents, 'rise_time_10_90'].hist()
# des_df.loc[probably_otherfastevents, 'rise_time_10_90'].hist()
# plt.figure(), plt.suptitle('width (50% amp)')
# des_df.loc[probably_fastevents, 'width_50'].hist()
# des_df.loc[probably_otherfastevents, 'width_50'].hist()
# plt.figure(), plt.suptitle('max dvdt')
# des_df.loc[probably_fastevents, 'maxdvdt'].hist()
# des_df.loc[probably_otherfastevents, 'maxdvdt'].hist()
# Still not quite sure what to make of this.

# Let's see the 'slower fast-events' in the raw data:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(probably_otherfastevents & (des_df.amplitude >4)), segments_overlayed=False)
# Well, it's far from perfect as there's events marked all over, but it does seem like by far the majority are
# in the last two recording files (shortPulse_0001 and gapFree_0002).