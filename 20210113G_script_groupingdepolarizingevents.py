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
# light-evoked response is always big and fast and always has AP at resting baselineV.
# %%
# summary plots:
des_df = singleneuron_data.depolarizing_events
spont_events = ~des_df.applied_ttlpulse
fastevents = des_df.event_label == 'fastevent'
aps = des_df.event_label == 'actionpotential'
spont_aps = (aps & spont_events)
# fast-events, amp and rise-time as histograms and scatters
plt.figure(), des_df.loc[fastevents,'amplitude'].plot.hist(bins=15)
plt.title('fast-events, amplitude')
plt.figure(), des_df.loc[fastevents,'rise_time_20_80'].plot.hist(bins=5)
plt.title('fast-events, rise-time')
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
singleneuron_data.plot_depoleventsgroups_overlayed(spont_aps, fastevents,
                                                   group_labels=['spont. aps', 'fastevents'],
                                                   do_baselining=True,
                                                   )

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000', '0001', '0002',
    newplot_per_ttlduration=True,
                                                # skip_vtraces_idcs=skip_vtraces,
                                                colorby_measure='applied_current',
                                                color_lims=[-700, 100],
                                                prettl_t_inms=1,
                                                postttl_t_inms=20,
                                                # plotlims=[-5, 102, -5.2, 15],
                                                do_baselining=False, plotlims=[-95, 45, -5.2, 15],
                                                )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# in light-applied files, stimulus goes to as short as 1ms; the effect is rather immediate but can be longer
# (up to 20ms maybe), so setting ttleffect window at 15ms (that should pick up the peaks of all light responses)
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=15)

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_evokedbylight #aps_spont  #aps_oncurrentpulsechange
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# in the aps_oncurrentpulsechange three got mistakenly labeled as AP when they're in fact just release from -DC;
# relabeling accordingly:
# currentpulsechanges = (aps_oncurrentpulsechange & (des_df.baselinev < -70))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# in the aps_spont there are 4 that are in fact on a currentpulse: re-labeling accordingly:
# aps_oncurrentpulse = (aps_spont & (des_df.file_origin == 'gapFree_0000.abf'))
# onemore_ap_oncurrentpulse = (aps_spont & (des_df.file_origin == 'gapFree_0005.abf') & (des_df.applied_current > 100))
# aps_oncurrentpulses = (aps_oncurrentpulse | onemore_ap_oncurrentpulse)
# singleneuron_data.depolarizing_events.loc[aps_oncurrentpulses, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events

# 1. seeing that evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# sub-threshold depolarizations get picked up weirdly sometimes (weird baselinepoints because compound responses),
# but definitely everything that's evoked got labeled as such so I think it'll do.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_10_90 < 1))
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# LOADS of things got extracted, mostly tiny stuff (spikelets and noisy things).
# The neuron clearly has spont.events of amp > 5mV,
# and there are a few things that are definitely APs (got a shoulder and everything)
# that didn't get labeled a such and have to get picked out manually.
# Let's filter down to things with amp > 2mV, and see amplitude and rise-time for the rest to narrow down from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))
# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('all spont. events >2mV, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('all spont. events >2mV, rise-time')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
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
# I don't see any indication in the raw recording that these would be artefacts, except for the way the rising phase looks.
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
# aps = des_df.event_label == 'actionpotential'
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

# Revisiting other_events and other_fastevents:
# events = other_fastevents #other_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# Looks to me that the other_events are indeed artefacts, probably from touching the rig during recording.
# Labeling them as noiseevents instead:
# singleneuron_data.depolarizing_events.loc[other_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Looks like the other_fastevents had already gotten relabeled as fastevents; their shape is affected by recording
# quality drift but they're definitely that.
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# Looking at the raw data carefully I see the recording deteriorating only during the last two blocks (light #3 and gapFree#5);
# the rest of recording all looks really neat, with steady baselineV and AP amp (even if there isn't much actually happening).
# Labeling 'neat' events accordingly:
# neat_events = ~((des_df.file_origin == 'light_0003.abf') | (des_df.file_origin == 'gapFree_0005.abf'))
# adding the neatevents-series to the depolarizing_events-df:
# neat_events.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neat_events)
# singleneuron_data.write_results()
