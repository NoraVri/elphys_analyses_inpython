# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

# getting  data (including APs and depolarizing events)
neuron_data = SingleNeuron('20200708B')

# general notes on single neuron data & analyses:
# This neuron has two APs and a handful of fast-events of different amplitudes spontaneously,
# and nothing else going on at all really.
# Evoked events have very different rise but practically the same decay as spont. fast-events,
# and seem to come in similar amplitude groups as spont. events.
# TODO: get also smaller events for this neuron
# there is another fast-event of ~1.5 mV, but since the neuron is not doing anything else it's VERY clear,
# and an event of this size is also often evoked.
# This neuron was not held at different resting Vs; it's holding pretty steadily throughout (-50 < Vrest < -40 mV)
# until it quickly dies.

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
# %% plot of raw data traces with events marked
neuron_data.plot_blocks_byname('light', events_to_mark=largeevokedevents_df, segments_overlayed=False)
neuron_data.plot_blocks_byname('gapFree', events_to_mark=largespontevents_df)

# %%
# plot of spont. and evoked events overlayed, colored per group
neuron_data.plot_depoleventsgroups_overlayed(largeevokedevents, largespontevents,
                                             group_labels=['evoked events', 'spont. events'],
                                             plt_title=neuron_data.name,
                                             do_baselining=True,
                                             do_normalizing=True
                                             )

# figure1, axes = plt.subplots(1, 2, sharey='row', sharex='row')
neuron_data.plot_depolevents_overlayed(largespontevents,
                                       colorby_measure='baselinev',
                                       do_baselining=True,
                                       # axis_object=axes[0]
                                       )
neuron_data.plot_depolevents_overlayed(largeevokedevents,
                                       colorby_measure='baselinev',
                                       do_baselining=True,
                                       # axis_object=axes[1]
                                       )


# %% overview-plots of spontaneous depolarizing events parameters
# %% histograms:
# amplitude
maxeventamp = max(largespontevents_df.amplitude.max(), largeevokedevents_df.amplitude.max()) + 1
binwidth = 0.2
plot1, axes = plt.subplots(1, 2, sharex='row', sharey='row')
largespontevents_df.hist('amplitude', ax=axes[0], bins=np.arange(0, maxeventamp, binwidth))
axes[0].set_title('spont. events')
largeevokedevents_df.hist('amplitude', ax=axes[1], bins=np.arange(0, maxeventamp, binwidth))
axes[1].set_title('evoked events')
plot1.suptitle(neuron_data.name + ' event amplitudes')


