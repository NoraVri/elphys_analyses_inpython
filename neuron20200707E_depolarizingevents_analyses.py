# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

# getting neuron20190527A data (including APs and depolarizing events)
neuron_data = SingleNeuron('20200707E')

# general notes on single neuron data & analyses:
#
# %%
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
neuron_data.plot_blocks_byname('light', events_to_mark=largespontevents_df, segments_overlayed=False)
neuron_data.plot_blocks_byname('gapFree', events_to_mark=largespontevents_df)

# %%
# plot of spont. and evoked events overlayed, colored per group
neuron_data.plot_depoleventsgroups_overlayed(largeevokedevents, largespontevents,
                                             group_labels=['evoked events', 'spont. events'],
                                             plt_title=neuron_data.name,
                                             do_baselining=True,
                                             # do_normalizing=True
                                             )