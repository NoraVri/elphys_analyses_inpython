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

# %% extracting depolarizing events
# notes:
# this neuron's got loads of events, but response to light is clearly not more than syanpse/spikelet
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=10, min_depolamp=2)
# singleneuron_data.write_results()


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
                                   )
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
nbins = 20
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# By eye one stands out not only for having the highest baselinev, but also because it looks to have a rounder,
# wider shape - but by the parameter distributions it doesn't look out of tune with fast-events
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   timealignto_measure='rt20_start_idx',
                                   prealignpoint_window_inms=2,
                                   plotwindow_inms=10,
                                   plot_dvdt=True,
                                   )