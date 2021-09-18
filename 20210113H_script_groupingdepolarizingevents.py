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
# quite nice stable recording, with stretches of time where DC current is applied to change baselinev (not to keep it
# in good range). Fast-events may come in amplitude groups as small as ~1mV (few of those got labeled as fast-event by
# selecting by maxdvdt), though it's hard to say since they're so small.

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

# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=10,
#                                                      min_depolamp=0.2,
#                                                      min_depolspeed=0.15,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 200
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Definitely all evoked events got picked up as such, and mostly with pretty good parameters, too -
# the response to light is often rather beautiful, with clearly seperable spikelets and a fast-event riding on top
# (and despite all that the fast-event tends to get picked up with a nice baseline point).
# Experiment-day notes say that it didn't look like the fast-event was getting evoked at all, but looking at the full
# traces I'd say it's not just by accident that fast-events often coincide with light (though it should be noted that
# they occur regularly spontaneously, and that the light response often does not include a fast-event).

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# looks good - I'm not gonna say that no noise-things got picked up at all or that all spikelets got caught, but it's
# definitely close. My eye caught one clearly mislabeled AP (with spikeshoulderpeaks - it's a weird one because AP amp
# drops suddenly and dramatically), but aside from that it should really just be a matter of separating the fast-events
# from the small, slow ones.

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# 1. First, let's get rid of any mislabeled APs and spikeshoulderpeaks - looks like it's just the one AP.
# It couldn't be more clear which events are the mislabeled AP and spikeshoulderpeaks. Adding their labels:
# ap = (unlabeled_spont_events & (des_df.amplitude > 50))
# singleneuron_data.depolarizing_events.loc[ap, 'event_label'] = 'actionpotential'
# spikeshoulderpeak = (unlabeled_spont_events & (des_df.baselinev > -15))
# singleneuron_data.depolarizing_events.loc[spikeshoulderpeak, 'event_label'] = 'spikeshoulderpeak'
# singleneuron_data.write_results()

# 2. Now looking at the remaining events' parameter distributions, it seems like fast-events could be pretty easily
# picked out from among the rest by rise-time and maxdvdt. Let's see:
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.15) & (des_df.rise_time_20_80 < 1))
# 2a. there's two 'events' in there that are just the weird negative noise; luckily they also stand way out by amplitude.
# The rest all look like fast-events, even if the amplitude grouping isn't very clear, although it does look like there
# are a handful of compound events in there as well.
# Labeling the noiseevents:
# noiseevents = (events_underinvestigation & (des_df.amplitude < 0.5))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# 2b. now let's see if we can separate the compound events from the single ones. Having seen them all in detail plotted,
# I'm quite convinced that there's just three compound events, and they're not so simple to separate from the others by
# parameters... But here goes:
# compound_events = (events_underinvestigation & (des_df.amplitude > 10) & (des_df.baselinev < -56))
# compound_event = (events_underinvestigation & (des_df.amplitude > 7.85) & (des_df.amplitude < 7.95))
# compound_events = (compound_event | compound_events)
# and the remainder of these events are all fast-events. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# fastevents = (events_underinvestigation & ~compound_events)
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3a. In the now remaining events the main thing that stands out is a slew of events that have really large maxdvdt for
# their very small amplitude (<1mV). Indeed, they are fast negative noise events - one or two cases may have an actual
# event (probably spikelet) occurring just after, but I'd rather just label them as noise anyway. Labeling them:
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.08) & (des_df.amplitude < 1))
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# 3b. Now we still have some events with good amplitude, rise-time and maxdvdt values for being fast-events, but also
# a bunch of pretty small events that could still be fast-events and a few other outliers. It seems that events with
# maxdvdt >- 0.7 are generally fast-event-ish if their amplitude is large enough; events with amp < 0.3mV are all noise.
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt >= 0.09))
# First let's label things that are obviously noiseevents:
# noiseevents = (events_underinvestigation & (des_df.amplitude < 0.3))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# 3b. Now let's see the outliers - one is a large (6mV) compound event occurring at very depolarized potential,
# another is like a stroke of spikelets happening in quick succession, and one may not be a proper event at all...
# Labeling them:
# compound_event = (events_underinvestigation & (des_df.amplitude > 5.8))
# compound_event2 = (events_underinvestigation & (des_df.amplitude > 1.5) & (des_df.rise_time_20_80 > 1)
#                    & (des_df.file_origin == 'gapFree_0000.abf'))
# singleneuron_data.depolarizing_events.loc[(compound_event | compound_event2), 'event_label'] = 'compound_event'
# currentpulsechange = (events_underinvestigation & (des_df.amplitude > 1.5) & (des_df.rise_time_20_80 > 1)
#                       & (des_df.file_origin == 'light_0009.abf'))
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# 3c. In the now remaining events there's a big group with amp ~1mV that may very well represent fast-events, but it
# may just as well represent a group of spikelets. I've been looking closely at events trying to find a cutoff value by
# maxdvdt and/or amplitude, but there's no clear set of values that would convincingly separate one group of events from
# the rest. I am quite sure that by selecting events with maxdvdt >= 0.09 we get only fast-events, and that we may be
# missing a ton of smaller ones...
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
## Note: may want to revise by labeling more of the small events as fast-events.










