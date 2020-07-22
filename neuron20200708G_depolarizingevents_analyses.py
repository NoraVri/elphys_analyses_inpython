# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

# getting neuron20190527A data (including APs and depolarizing events)
neuron_data = SingleNeuron('20200708G')

# general notes on single neuron data & analyses:
# this neuron recording isn't all that great - Vrest is rather depolarized and it has barely anything going on
# spontaneously. Still, there's a handful of events (both spont. and evoked) that might correspond to fast-events
# (amp. 3 - 6 mV) although their rise-time is rather slow, both rise and decay look damn near identical on all of them

# selecting relevant events
spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
vclampblocks = list(set(
    [blockname for blockname in neuron_data.depolarizing_events.file_origin if 'Vclamp' in blockname]))
vclampevents = neuron_data.depolarizing_events.file_origin.isin(vclampblocks)
excludedevents = vclampevents | spikeshoulderpeaks
largeampevents = (neuron_data.depolarizing_events.amplitude > 3) & (~excludedevents)
largeevokedevents = neuron_data.depolarizing_events.applied_ttlpulse & largeampevents
largespontevents = (~neuron_data.depolarizing_events.applied_ttlpulse) & largeampevents

largespontevents_df = neuron_data.depolarizing_events[largespontevents]
largeevokedevents_df = neuron_data.depolarizing_events[largeevokedevents]
# %% plots of events - raw data
# plot of spont. and evoked events overlayed, colored per group
neuron_data.plot_depoleventsgroups_overlayed(largeevokedevents, largespontevents,
                                             group_labels=['evoked events', 'spont. events'],
                                             plt_title=neuron_data.name,
                                             do_baselining=True,
                                             do_normalizing=True
                                             )

# spont. events only, colored by baselinev
neuron_data.plot_depolevents_overlayed(largespontevents,
                                       colorby_measure='baselinev',
                                       do_baselining=True,
                                       do_normalizing=True,
                                       plt_title=(neuron_data.name + ' spont. events'))
# evoked events only, colored by baselinev
neuron_data.plot_depolevents_overlayed(largeevokedevents,
                                       colorby_measure='baselinev',
                                       do_baselining=True,
                                       do_normalizing=True,
                                       plt_title=(neuron_data.name + ' evoked events'))

# something is off - I did not see any spont. events in the raw data really, especially not
# in traces with hyperpolarized V.
neuron_data.plot_blocks_byname('light', events_to_mark=largespontevents_df, segments_overlayed=False)
# Indeed, all events >3mV are in fact evoked events...

# %% overview-plots of depolarizing events parameters
# histograms:
# amplitude
largeampevents_df = neuron_data.depolarizing_events[largeampevents]
maxeventamp = largeampevents_df.amplitude.max() + 1
binwidth = 0.1
plot1, axes = plt.subplots(1, 1, sharex='row', sharey='row')
largeampevents_df.hist('amplitude', ax=axes[0], bins=np.arange(0, maxeventamp, binwidth))
axes[0].set_title('spont. events')
plot1.suptitle(neuron_data.name + ' evoked events (>3mV) amplitudes histogram')
