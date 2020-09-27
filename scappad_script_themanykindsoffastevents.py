# show me that Yaara does not have them
# show that you have them more often than in one recording
# show they are statistically significantly different from the normal ones
# If you have recordings with TTX, glut blockers, low temperature, anything
# - check if you see any of the weird ones there

# I will start from the recordings where I already have depolarizing events extracted,
# and then move to analyzing more data with synaptic blockers applied and data recorded at RT

# %% imports
import os
import pandas as pd
import matplotlib.pyplot as plt

from singleneuron_class import SingleNeuron

path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"


# %% 0. getting the list of relevant singleneuron-names
resultsfolder_path = path + "\\myResults_synapticexcitations"
resultsfiles_list = os.listdir(resultsfolder_path)
depoleventsfiles_list = [file for file in resultsfiles_list if 'depolarizing_events' in file]
neuronnames_list = [filename.split('_')[0] for filename in depoleventsfiles_list]


# %% 1. prevalence of 'regular' fast-events and the other kind of fast-events

# For starters, I looked at spont. events >3mV all plotted twice: baselined and baselined+normalized,
# to submit them to the YY-test of having the fast-events we're looking for
# and seeing whether there are (also) other kinds of fast depolarizing events (see code&notes at the bottom).

# SUMMARY: out of the 32 recordings looked at,
# 13 have fast-events (only):
# 20190527B (probably - amplitude-grouping not very clear but normalized decays look pretty much exactly the same)
# 20190527C (though should check that it's indeed oscillating: some of the decays are distorted)
# 20190529C (classic example, even if two out of three amplitude groups have only one instance in them)
# 20190529D (and other relatively fast events of ~4mV that look like spikelets)
# 20200630A (probably, just one event with amp >3mV)
# 20200630C (though check out only a single amplitude-group having an AHP, regardless of same baselinev)
# 20200630D (though not entirely exemplary for decay shape being exactly identical)
# 20200701A (though only two amplitude groups and just one instance in one of those groups)
# 20200701C (probably, just one event with amp >3mV)
# 20200706B (only two events with amp. no more than 1mV apart, but normalized decay entirely identical)
# 20200707A (probably, just one event with amp >3mV)
# 20200708B (classic example, even if relatively few events recorded altogether)
# 20200708E (probably - either just one amplitude-group or three very close-by groups)

# and another 7 have fast-events and other events with similar parameters:
# 20190527A (although generally rather ambiguous because of numerous compound events)
# 20190529A1 (however, the other events in this case are HUGE, and clearly separable from fast-events by amplitude)
# 20190529A2 (probably - it kind of looks like some events with rounder shapes are the reason amp-grouping is unclear)
# 20200706E (relatively few events in many amplitude groups, and some rounder events in a much smaller amp. range)
# 20200708A (though the round-events in this case don't quite look like the ones I've been noticing regularly)
# 20200708D (perhaps THE example: fast-events and rounder-events in the same amplitude range)
# 20200708F (although generally rather ambiguous because of numerous compound events)

# %% taking a closer look at 'representative examples'
# %% 20190527B
neuron_data = SingleNeuron('20190527B')
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
lightevoked_events = (neuron_data.depolarizing_events.applied_ttlpulse)

fast_events = ~(spikeshoulderpeaks | actionpotentials | lightevoked_events)
neuron_data.plot_rawdatablocks(events_to_mark=fast_events)
neuron_data.plot_depolevents(fast_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(fast_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
neuron_data.scatter_depolarizingevents_measures(xmeasure='amplitude',
                                                ymeasure='rise_time',
                                                cmeasure='half_width',
                                                fast_events=fast_events,
                                                # other_events=other_events
                                                )
fast_events_df = neuron_data.depolarizing_events[fast_events]
fast_events_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=20)
# I see no evidence for anything being not normally distributed here

# %% 20190529C
neuron_data = SingleNeuron('20190529C')
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
lightevoked_events = (neuron_data.depolarizing_events.applied_ttlpulse)

fast_events = (neuron_data.depolarizing_events.amplitude > 1) \
                 & (neuron_data.depolarizing_events.half_width < 10) \
                 & (neuron_data.depolarizing_events.baselinev < -45) \
                 & ~spikeshoulderpeaks \
                 & ~actionpotentials \
                 & ~lightevoked_events

other_events = ~(spikeshoulderpeaks | actionpotentials | lightevoked_events | fast_events)
# neuron_data.plot_rawdatablocks(events_to_mark=fast_events)
neuron_data.plot_depolevents(fast_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(fast_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
neuron_data.scatter_depolarizingevents_measures(xmeasure='amplitude',
                                                ymeasure='rise_time',
                                                cmeasure='half_width',
                                                fast_events=fast_events,
                                                other_events=other_events
                                                )
fast_events_df = neuron_data.depolarizing_events[fast_events]
fast_events_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=20)

# %% 20200708B
neuron_data = SingleNeuron('20200708B')
# in this neuron, any event with rise-time < 1ms (that isn't an AP or spikeshoulderpeak) looks like a fast-event;
# and as it turns out, all events with rise-time > 1ms are light-evoked
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
lightevoked_events = (neuron_data.depolarizing_events.applied_ttlpulse)
fast_events = neuron_data.depolarizing_events.rise_time < 1 \
                     & ~spikeshoulderpeaks \
                     & ~actionpotentials
other_events = ~(spikeshoulderpeaks | actionpotentials | lightevoked_events | fast_events)

# neuron_data.plot_rawdatablocks(events_to_mark=fast_events)
# neuron_data.plot_rawdatablocks(events_to_mark=other_events)
neuron_data.plot_depolevents(fast_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(fast_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
# possibly, the events with smaller amp (< 2.5mV) have a bit faster decay; should run event-extraction again with parameter settings better tuned to this neuron's data to find out more
neuron_data.scatter_depolarizingevents_measures(xmeasure='amplitude',
                                                ymeasure='rise_time',
                                                cmeasure='half_width',
                                                fast_events=fast_events,
                                                lightevoked_events=lightevoked_events,
                                                other_events=other_events)

fast_events_df = neuron_data.depolarizing_events[fast_events]
fast_events_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=20)
plt.suptitle('fast-events parameters histograms')
# rise-time and half-width look pretty much normally distributed, amplitudes fall into 4 or 5 different groups


# %% examples where 'identicalness' of the events is not so clear to me
# %% 20190529A1
neuron_data = SingleNeuron('20190529A1')
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
lightevoked_events = (neuron_data.depolarizing_events.applied_ttlpulse)

fast_events = (neuron_data.depolarizing_events.amplitude > 4) \
                 & (neuron_data.depolarizing_events.half_width < 15) \
                 & (neuron_data.depolarizing_events.baselinev > -80) \
                 & ~spikeshoulderpeaks \
                 & ~actionpotentials \
                 & ~lightevoked_events

other_events = ~(spikeshoulderpeaks | actionpotentials | lightevoked_events | fast_events)

neuron_data.plot_rawdatablocks(events_to_mark=fast_events)
neuron_data.plot_depolevents(fast_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(fast_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
neuron_data.scatter_depolarizingevents_measures(xmeasure='amplitude',
                                                ymeasure='rise_time',
                                                cmeasure='half_width',
                                                fast_events=fast_events,
                                                other_events=other_events
                                                )
fast_events_df = neuron_data.depolarizing_events[fast_events]
fast_events_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=20)

other_events_df = neuron_data.depolarizing_events[other_events]
other_events_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=20)

# %% 20200708D
neuron_data = SingleNeuron('20200708D')
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak') \
                     & (neuron_data.depolarizing_events.baselinev > -30)
actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
lightevoked_events = (neuron_data.depolarizing_events.applied_ttlpulse)
slowrisetime_events = neuron_data.depolarizing_events.rise_time > 1.5
othernogoodevents = (neuron_data.depolarizing_events.file_origin == 'light_0001.abf') \
                    & (neuron_data.depolarizing_events.segment_idx == 13)

definitely_not_fastevents = (spikeshoulderpeaks | actionpotentials | lightevoked_events
                             | slowrisetime_events | othernogoodevents)
possiblyfastevents = ~definitely_not_fastevents

neuron_data.plot_rawdatablocks(events_to_mark=possiblyfastevents)

neuron_data.plot_depolevents(possiblyfastevents, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(possiblyfastevents, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')

possiblyfastevents_df = neuron_data.depolarizing_events[possiblyfastevents]
possiblyfastevents_df.hist(column=['rise_time', 'rise_time_20_80', 'half_width', 'amplitude'], bins=40)
plt.suptitle('fast-events parameters histograms')
# %%
# let's see if we can get a clearer selection of fast-events only
halfwidth_cutoffvalue = 3.2
smallhalfwidth_events = possiblyfastevents & (neuron_data.depolarizing_events.half_width < halfwidth_cutoffvalue)
neuron_data.plot_depolevents(smallhalfwidth_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(smallhalfwidth_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
largehalfwidth_events = possiblyfastevents & (neuron_data.depolarizing_events.half_width > halfwidth_cutoffvalue)
neuron_data.plot_depolevents(largehalfwidth_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(largehalfwidth_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
# %%
risetime_cutoffvalue = 0.85
smallrisetime_events = possiblyfastevents & (neuron_data.depolarizing_events.rise_time < risetime_cutoffvalue)
neuron_data.plot_depolevents(smallrisetime_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(smallrisetime_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')
largerisetime_events = possiblyfastevents & (neuron_data.depolarizing_events.rise_time > risetime_cutoffvalue)
neuron_data.plot_depolevents(largerisetime_events, do_baselining=True, colorby_measure='baselinev')
neuron_data.plot_depolevents(largerisetime_events, do_baselining=True, do_normalizing=True, colorby_measure='baselinev')


# %% plotting spont. depolarizations baselined and baselined+normalized
# for neuron_name in neuronnames_list:
#     neuron_data = SingleNeuron(neuron_name)
#     spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
#     actionpotentials = (neuron_data.depolarizing_events.event_label == 'actionpotential')
#     probablynogoodevents = (neuron_data.depolarizing_events.baselinev > -30) \
#                            | (neuron_data.depolarizing_events.baselinev < -90)
#     smallevents = (neuron_data.depolarizing_events.amplitude < 3)
#     evokedevents = neuron_data.depolarizing_events.applied_ttlpulse
#     excludedevents = spikeshoulderpeaks | actionpotentials | probablynogoodevents | smallevents | evokedevents
#     relevantevents = neuron_data.depolarizing_events[~excludedevents]
#     neuron_data.plot_depolevents(~excludedevents,
#                                  colorby_measure='baselinev',
#                                  do_baselining=True,
#                                  plotwindow_inms=25)
#     neuron_data.plot_depolevents(~excludedevents,
#                                  colorby_measure='baselinev',
#                                  do_baselining=True,
#                                  do_normalizing=True,
#                                  plotwindow_inms=25)
#     plt.figure()
#     relevantevents.baselinev.plot.hist(bins=40)
#     plt.title(neuron_name+' histogram of putative fast-events baselinev')

## notes on each neuron recording
# 20190527A: hundreds of events, at a wide range of baselinev (~-70 - -40).
# Definitely passes the YY-test for fast-events, but also has the other kind of fast-events and
# a number of events that are clearly 'compound' (two events arriving in close succession).
# Should definitely look at events-groups split by baselinev, as it seems like the other kind of fast-event
# appears almost exclusively at baselinev ~-55mV

# 20190527B: just a handful of events.
# Has events that look like fast-events by their amplitude and rise-time;
# however, the amplitudes (range: 5.5 - 7mV) do not form clear groups.
# Should check if amplitude-grouping of fast-events is more clear if also smaller events are included.

# 20190527C: just a handful of events.
# The events look like classic fast-events by their amplitude, rise-time and grouping and probably pass the YY-test,
# even though it looks like an oscillation or something is distorting the decay of some of them.
# Should check if that's indeed what's up.

# 20190529A1: ~100 events, at a wide range of baselinev (~-90 - -35).
# Definitely has two kinds of events, but in this case clearly separable by amplitude;
# events with amp. up to ~10mV mostly look like classic fast-events (grouping and all), and then there's
# events with amp. ~15 - 30mV that look more like calcium spikes or something (fast rise-time but far more rounded).

# 20190529A2: dozens of events, over ~15mV range of baselinev (~-55 - -40).
# Most of the events look like classic fast-events except in that amplitude-grouping is not very clear;
# and then there's some that look more rounded to my eye which in this case seem to preferentially appear at
# baselinev ~-45mV and may just be the reason why amplitude-grouping isn't clear.

# 20190529B: no actual fast-events.

# 20190529C: about a dozen events, baselinev range ~-50 - -40mV.
# Would all pass the YY-test for being classic fast-events: most of them 7-8mV and then one each of 4 and 12mV,
# and normalized decay slowing down just a bit for more hyperpolarized Vrest.

# 20190529D: just a handful of events.
# Definitely passes the YY-test for fast-events: three amplitude groups and identical normalized decay.
# And then there's two slower things (spikelets?) that have amp > 3mV.

# 20190529E: doesn't seem to have any events in the parameter range that we're looking for

# 20200630A: has just a single event that could be a fast-event, should check if maybe there are also some with amp<3mV.

# 20200630B1: doesn't seem to have any events with parameters in the range we're looking for

# 20200630B2: doesn't seem to have any events with parameters in the range we're looking for

# 20200630C: about a dozen events, that all would probably pass the YY-test for being fast-events:
# 5 or 6 different amplitude groups (range: ~3 - 10mV) and highly similar normalized decay all around.
# something's weird though, with only one amplitude-group seeming to have an AHP (and other events
# at the same baselinev not exhibiting any AHP).

# 20200630D: a handful of events, most of them ~8mV and then one example at 4 more different amplitudes (up to 12mV).
# Most of them would probably pass the YY-test for the most part, although decays don't all look all that identical

# 20200701A: a handful of events, most of them ~14mV and one of 4mV. Identical waveforms, definitely passes the YY-test.

# 20200701B: doesn't seem to have any events with parameters in the range we're looking for

# 20200701C: just a single event (amp ~4mV) with the right parameters, can check smaller events to see if there are more

# 20200701D: doesn't seem to have any events with parameters in the range we're looking for

# 20200706A: doesn't seem to have any events with parameters in the range we're looking for

# 20200706B: has just two events (~5 - 6mV) with amp <1mV apart; normalized decay identical

# 20200706D: doesn't seem to have any events with parameters in the range we're looking for

# 20200706E: a few dozen events in as many as 6 amplitude groups (range ~4 - 18mV) with identical decays,
# and then some events that are definitely much more rounded (amp 10 - 13 mV)

# 20200707A: just a single event (amp ~4mV) with the right parameters, looks scarily similar to 20200701C...

# 20200707C: doesn't seem to have any events with parameters in the range we're looking for

# 20200707E: no real events, or even if they are then they're too noisy to say anything useful about them

# 20200708A: only 5 events altogether, baselinev range ~-44 - -38mV.
# Two things look like fast-events: amp 7 and 8 mV, identical decay waveform; they both have a 'foot' though,
# as though they're each riding on top of a spikelet.
# And then there's three more events, one with the same amp and two with even larger amp (13 - 14 mV)
# that definitely look much more rounded, and more similar to each other than to the fast-events,
# but not quite like the other events that I mean

# 20200708B: about a dozen events, some 5 different amplitudes (3 - 12mV), identical decays - definitely fast-events.

# 20200708C: doesn't seem to have any events with parameters in the range we're looking for

# 20200708D: many dozens of events, baselinev range ~-70 - -40.
# perhaps THE example that I'm looking for:
# some of the events are definitely fast-events, amplitudes in 5 or so groups 4-14mV.
# And some of the events are definitely round fast-events, less clear amplitude groups but same range as fast-events.

# 20200708E: Just three events, all pretty much identical (both in waveform and amp).

# 20200708F: many dozens of events, baselinev range ~-60 - -30mV and amp range 4 - 40mV (no they're not full APs).
# Many of the events are compound (two things happening in quick succession), and then there's definitely
# some that are classic fast-events and some that are round-events.

# 20200708G: doesn't seem to have any events with parameters in the range we're looking for


