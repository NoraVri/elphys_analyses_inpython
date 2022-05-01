# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190529D'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# only 9 spontaneous fast-events in 46min. of recording;
# they're not very large (~3.5 - 6mV) but they very clearly group into 3 amplitudes with all having pretty much exactly
# the same normalized decay shape.
# Light-evoked activity always seems to include also a broad, slow depolarization, possibly sometimes with small events
# riding on top, and quite often a full sodium AP without shoulder.

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'
spont_events = ~des_df.applied_ttlpulse

# summary plots:
des_df = singleneuron_data.depolarizing_events
fast_events = des_df.event_label == 'fastevent'
fast_events_df = des_df[fast_events]
fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=15)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
singleneuron_data.plot_depolevents((aps & spont_events), colorby_measure='baselinev', do_baselining=True)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.2 to find good parameter settings; playing with parameters was done elsewhere -
# using saved parameter settings to re-create depolarizing-events data table:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()


# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_spont  #aps_oncurrentpulsechange  #aps_evokedbylight
# blocknames = des_df[events].file_origin.unique()
# singleneuron_data.plot_rawdatablocks(*blocknames,
#                                      events_to_mark=events,
#                                      segments_overlayed=False)
# the one that got labeled as being on currentpulsechange isn't actually; the current changes ~50ms after AP peak.
# Re-labeling:
# singleneuron_data.depolarizing_events.loc[aps_oncurrentpulsechange, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# for the rest all looks good.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events

# 1. seeing that evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Looks like evoked responses were all picked up right; there's always an immediate response, often quite compound
# (which is why baselinepoints aren't always perfect) and often with an additional depolarization (usually a spikelet)
# getting picked up after the main peak. Also, a lot of the evoked APs have no shoulder at all (AIS spike alone?)

# 2. seeing that spontaneous fast-events got picked up
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# This neuron is getting TONS of spikelets all throughout recordings, and pretty big ones, too - up to 3mV or so.
# Definitely not all spikelets got picked up, but all fast-events that are easily picked out by eye (amp ~4mV or so)
# definitely did.
# There's a handful of events that could arguably be part of the light-evoked response as they are riding the evoked
# depolarization; they all look like spikelets (amp up to 2mV) and I don't think it should bother the analysis, so
# leaving as is.

# The amplitude histogram shows a pretty clean break and then groups of events >3mV.
# Let's see those larger events, and see amplitude and rise-time to narrow down from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 3))

# The scatter shows a group of points with similar rise-time, and then three further-spaced points with rise-time > 2.
# Let's see the events with rise-time > 2; by amp two of them look like spikelets, and one is 12mV that's puzzling
# singleneuron_data.plot_rawdatablocks(events_to_mark=(possibly_spontfastevents&(des_df.rise_time_10_90 > 2)))
# The big one is a slow-peaking rebound potential; labeling it as 'currentpulsechange':
# currentpulsechange_event = (possibly_spontfastevents & (des_df.rise_time_10_90 > 2) & (des_df.amplitude > 10))
# singleneuron_data.depolarizing_events.loc[currentpulsechange_event, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# The other two look like spikelets with a double rising phase; labeling them as 'other_event':
# other_events = possibly_spontfastevents & (des_df.rise_time_10_90 > 2)
# singleneuron_data.depolarizing_events.loc[other_events, 'event_label'] = 'other_event'
# singleneuron_data.write_results()
# We're now left with fast-events only; labeling them as such:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 3))
# singleneuron_data.depolarizing_events.loc[possibly_spontfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# From the summary plots so far we can see that the fast-events have rise_time_10_90 < 1.8, _20_80 < 1.
# Let's see if we can find events with those parameters among the ones with amp < 3mV:
# possibly_spontfastevents = (possibly_spontfastevents
#                             & (des_df.rise_time_10_90 < 2) & (des_df.rise_time_20_80 < 1.2))
# Thinning out the events by one rise-time or both gets rid of a few hundred events, but does not change how
# the distributions look in the histograms: amplitude is long-tailed with a peak at ~0.25mV and the single largest
# event being 2.75mV; rise-times look normally distributed. Still, the rise-time vs amp scatter shows a small group
# of events (about 7, amp <1mV) that stand out for having extremely short (<0.5ms) rise-time for their amplitude;
# let's see whether they might be fast-events:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_10_90 < 0.5)
#                             & (des_df.amplitude > 0.1))  # there's just so many events there, need to filter to see

# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (10-90%)')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms = 30,
#                                    )
# singleneuron_data.plot_depoleventsgroups_overlayed(possibly_spontfastevents, fast_events,
#                                                    group_labels=['small events', 'fast_events'],
#                                                    do_normalizing=True, do_baselining=True)
# My eye might say there's an event or two that rise faster than the others, but at this amp (<1mV) it's impossible
# to make the case that they aren't just spikelets (which they probably are).
# Abandoning the search for more fast-events at this point.
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(fast_events | aps),
#                                      segments_overlayed=False)
# I don't think this neuron should get neatevents labeled: even though its resting baselineV doesn't seem too bad
# (~-40mV w/o DC) it is getting held with -DC most of the time, and by AP amp recording conditions aren't all too
# stable. Anyway, it's a pretty boring neuron, firing just a handful of spont.fastevents in 45 minutes.
