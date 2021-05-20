# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

neuron_name = '20210113G'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# This neuron definitely has fast-events, though only 8 of them altogether
# and amplitude groups are not very clear (normalized decay identicalness is very nice though).
# This neuron also has other_fastevents (3 events, 2 amplitudes) and other events that I have no idea what they are.

# summary plots:
des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
other_fastevents = des_df.event_label == 'other_fastevent'
other_events = des_df.event_label == 'other_event'
aps = des_df.event_label == 'actionpotential'
# fast-events, amp and rise-time as histograms and scatters
plt.figure(), des_df.loc[fastevents,'amplitude'].plot.hist(bins=5)
plt.title('all spont. events >2mV, amplitude')
plt.figure(), des_df.loc[fastevents,'rise_time_20_80'].plot.hist(bins=5)
plt.title('all spont. events >2mV, rise-time')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=fastevents,
                                                      )
# fast-events, baselined /baselined and normalized
singleneuron_data.plot_depolevents(fastevents,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   plt_title='fast-events')
singleneuron_data.plot_depolevents(fastevents,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='baselinev',
                                   plt_title='fast-events')

# other interesting events (if any)
singleneuron_data.plot_depoleventsgroups_overlayed(other_events, aps, other_fastevents, fastevents,
                                                   group_labels=['other events', 'aps',
                                                                 'other-fastevents','fastevents'],
                                                   do_baselining=True,
                                                   )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# in light-applied files, stimulus goes to as short as 1ms; the effect is rather immediate but can be longer
# (up to 20ms maybe), so setting ttleffect window at 15ms (that should pick up the peaks of all light responses)
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=15)


# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# sub-threshold depolarizations get picked up weirdly sometimes (weird baselinepoints because compound responses),
# but definitely everything that's evoked got labeled as such so I think it'll do.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_10_90 < 1))
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# LOADS of things got extracted, mostly tiny stuff (spikelets and noisy things).
# The neuron clearly has spont.events of amp > 5mV,
# and there are a few things that are definitely APs (got a shoulder and everything)
# that didn't get labeled a such and have to get picked out manually.
# Let's filter down to things with amp > 2mV, and see amplitude and rise-time for the rest to narrow down from there:
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))
plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
plt.title('all spont. events >2mV, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
plt.title('all spont. events >2mV, rise-time')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# Let's see the events with amp > 30mV first -
# Those are all small-amplitude APs (all very clearly have a shoulder).
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[
#     (possibly_spontfastevents & (des_df.amplitude > 30)), 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# singleneuron_data.plot_depolevents((possibly_spontfastevents & (des_df.amplitude > 30)),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms=100,
#                                    plt_title='possibly unlabeled APs'
#                                    )

# Let's see all the events we're left with at this point
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    do_baselining=True,
#                                    colorby_measure='baselinev')
# Getting close to fast-events only, but there are still a few weird things left.
# The things with amp up to ~5mV look like noisy things: - not quite:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(possibly_spontfastevents & (des_df.amplitude < 5.5)))
# I don't see any indication in the raw recording that these would be artefacts, except for way the rising phase looks.
# Labeling them as "other events":
# singleneuron_data.depolarizing_events.loc[
#     (possibly_spontfastevents & (des_df.amplitude < 5.5)), 'event_label'] = 'other_event'
# singleneuron_data.write_results()
# Now we just have to separate three different-looking events from the proper fast-events:
# !note: the three other-fastevents come in two different amplitudes (6 and 10mV) and have
# practically identical normalized decay (especially when accounting for change in baselineV).
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='baselinev')
# looks like it can be done by rise-time_10_90: - indeed:
# singleneuron_data.plot_depolevents((possibly_spontfastevents & (des_df.rise_time_10_90 > 1)),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms=100,
#                                    plt_title='possibly <<other>> fast-events'
#                                    )
# Labeling them as "other_fastevent":
# singleneuron_data.depolarizing_events.loc[
#     (possibly_spontfastevents & (des_df.rise_time_10_90 > 1)), 'event_label'] = 'other_fastevent'
# singleneuron_data.write_results()
# Now we're left with fast-events only. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[
#     (possibly_spontfastevents), 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Let's check that there isn't things in the events <2mV that are very clearly fast-events, too;
# plotting events of amp 1-2mV shows some that have very fast rise for their amplitude.
# Checking all events with rise-time < 1ms it's clear that most are just kinda noisy,
# but there are a few with amp ~1-2mV that might be real events.
# Let's see them plotted alongside fast-events and other-fastevents and determine if they're likely to belong to either:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude >= 1))
# otherfastevents = des_df.event_label == 'other_fastevent'
# fastevents = des_df.event_label == 'fastevent'
# singleneuron_data.plot_depoleventsgroups_overlayed(possibly_spontfastevents, fastevents, otherfastevents,
#                                                    group_labels=['possibly fast-events',
#                                                                  'definitely fast-events',
#                                                                  'other fast events'],
#                                                    do_baselining=True,
#                                                    do_normalizing=True)
# I don't think so: their rise is right between the regular and the other fast-events,
# and their decay is decidedly different. Most likely they are just regular spikelets.

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
# Looks like some of the 'spont' APs may actually be light-evoked: - nope:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(aps & spont_events))
# It all checks out, the weird up-slopes are on APs that occur late after the rebound potential from hyperpolarization.
# And there's one event that isn't an AP but looks much more like a huge (35mV) fast-event.
# It should separate from the APs by rise-time:
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=aps)
# Let's see the one that has rise_time_10_90 < 0.5ms:
# singleneuron_data.plot_depolevents((aps & (des_df.rise_time_10_90 < 0.5)),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
# Yup, that's the one... Let's see it alongside fast-events to compare:
# possibly_fastevent = aps & (des_df.rise_time_10_90 < 0.5)
# singleneuron_data.plot_depoleventsgroups_overlayed(possibly_fastevent, fastevents, otherfastevents,
#                                                    group_labels=['possibly fast-events',
#                                                                  'definitely fast-events',
#                                                                  'other fast events'],
#                                                    do_baselining=True,
#                                                    do_normalizing=True)
# Nope, it's got way too fast rise and decay to be a fast-event. Labeling it as "other event":
# singleneuron_data.depolarizing_events.loc[
#     (aps & (des_df.rise_time_10_90 < 0.5)), 'event_label'] = 'other_event'
# singleneuron_data.write_results()
