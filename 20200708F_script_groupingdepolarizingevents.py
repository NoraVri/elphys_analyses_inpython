# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200708F'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# a super relevant recording: Thy1-evoked excitations, also with application of AP5
# there's about 15 min. of recording without blocker, and then almost an hour with;
# early on, the neuron is mostly just going in and out of oscillating (small and large amp), but
# later on it starts doing spikes and fast-events vigorously.
# !Note: it's the cell that just won't die, but that doesn't mean its unaffected by drift - there are periods where
# it's definitely not all that healthy, and bridge issues etc. may be playing up.

# summary plots:
# des_df = singleneuron_data.depolarizing_events
# aps = des_df.event_label == 'actionpotential'
# fast_events = des_df.event_label == 'fastevent'
# fast_events_df = des_df[fast_events]
# fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
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
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# This looks alright - the upstrokes of the evoked events are usually quite compound and baselinepoints aren't
# always perfect, but there definitely shouldn't be any contamination of spont.events with evoked ones so I'm happy.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# %%
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# Looking quite alright from the perspective of events getting picked up: definitely everything that's 2mV or larger
# got listed. My eyes did pick out some double-events though, where not the first but only the second peak got labeled
# (and the baseline-point can be off). This'll be interesting to tease apart...

# Let's see amplitude and rise-time distributions to narrow down from there:
# The amplitude histogram shows groups of events 5mV or larger; smaller events are just too numerous to say anything.
# But also in events with amp>5mV there seems to be significant variance in rise-time.
# Let's see only events >5mV to start with:
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 5))
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=60)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   )
# OK then, lots of things going on there... I'm sure some of them are classic fast-events, others are double-events,
# and then there's events with fast rise but different decay than the fast-events (and those come as doubles, too).


# Let's see their widths also, maybe it'll be easier to select them based on that:
possibly_spontfastevents_df.hist(column=['width_30', 'width_50', 'width_70'], bins=60)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# There's a clear break in the width_50 histogram at 7ms, and just a handful events wider than that - let's see them:
# probably_notfastevents = (possibly_spontfastevents & (des_df.width_50 > 7))
# These are not fast-events: though their shape is similar, their normalized waveforms are not identical to each other.
# The events wider than 7ms all have rise-time > 1.2, which makes me think that the real fast-events may all be faster.
# Let's see:
probably_notfastevents = (possibly_spontfastevents
                          & ((des_df.width_50 > 7) | (des_df.rise_time_10_90 > 1.2))
                          )
possibly_spontfastevents = (possibly_spontfastevents
                          & ~((des_df.width_50 > 7) | (des_df.rise_time_10_90 > 1.2))
                          )
singleneuron_data.plot_depolevents(probably_notfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   )
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   )
# OK, now it's starting to get clearer what are fast-events. The problem is that some of them have a break
# in the upslope, which gives them longer rise-time and width; and then the rounder events are just quite variable
# in all of amp, rise and width so that the distributions bleed into each other really badly.

# First let's filter out some of the things that are happening at depolarized baselinev
# depolarized_events = (possibly_spontfastevents & (des_df.baselinev > -35))
# singleneuron_data.depolarizing_events.loc[depolarized_events, 'event_label'] = 'other_event'
# singleneuron_data.write_results()

# Let's check that there isn't things in the previously filtered events that are very clearly fast-events, too;








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




# %%
# ongoing analysis notes:
# well... That pretty much does not at all look like what we expect from a neuron that has only axonal fast-events.
# will definitely have to do some noise-cleanup to get a clearer view on parameter distributions of fast(er) events.
# Interestingly, there are some light-evoked responses that are right around the amplitude criterion for APs,
# yet don't seem to have a shoulder at all.
# The more I'm analyzing this data, the more it feels like this neuron's dendrites are slowly giving out
# over the course of recordings, while the axon keeps doing its thing somehow...


# Let's see if cleaning up a bit will help:
# there are rather many 'events' in the stretches of recording where this neuron is behaving rather noisily,
# but they occur at depolarized baselinev and tend to be rather small (naked eye says fast-events are 2mV amp
# and up, while noise-events are ~1mV)
# noiseevents_candidates = possibly_spontfastevents & (des_df.baselinev > -30) # & (des_df.amplitude < 1.8)  # picked the amp.criterion based on seeing events that rise above the noise
# singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
#                                                       cmeasure='baselinev',
#                                                       noiseevents_candidates=noiseevents_candidates)
# singleneuron_data.plot_depolevents(noiseevents_candidates,
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# These do not look like noise at all, more like AIS spikes - leaving them be for now