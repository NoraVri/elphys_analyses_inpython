# %% putative axonal spine responses in IO neurons, as evoked by synaptic inputs in the Thy1-mouse IO.
# Focus of this investigation: fast, depolarizing events of highly consistent waveform
# (as reflected by near-identical rise-time and half-width), that fall into groups
# of different specific amplitudes.

# Running this script will output summary results over all neurons in the dataset;
# full analyses can be found in an individual script per neuron (for those that have obvious fast-events).

# For now, we are looking for neurons that obviously have these events (they come in multiple amplitudes, all >3mV),
# to then determine whether light-evoked responses in these neurons (also) contain this response.


# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

## getting lists of relevant subsets of neurons
# list of all neurons recorded on those experiment days:
allneurons_list = [
    '20190527A',
    '20190527B',
    '20190527C',
    '20190529A1',
    '20190529A2',
    '20190529B',
    '20190529C',
    '20190529D',
    '20190529E',
    '20200630A',
    '20200630B1',
    '20200630B2',
    '20200630C',
    '20200630D',
    '20200701A',
    '20200701B',
    '20200701C',
    '20200701D',
    '20200706A',
    '20200706B',
    '20200706C',
    '20200706D',
    '20200706E',
    '20200707A',
    '20200707C',
    '20200707E',
    '20200708A',
    '20200708B',
    '20200708C',
    '20200708D',
    '20200708E',
    '20200708F',
    '20200708G'
]
# !Note: not all neurons have had depolarizing events extracted with individually-set parameter settings;
# the batch-wise parameter settings were min_depolspeed=0.2, min_depolamp=2, ttleffect_windowinms=10.

# getting the subsets of neurons in the dataset with light-activations applied and with events > 3mV
lightactivatedneurons_list = []
largesponteventsneurons_list = []
largeevokedeventsneurons_list = []
for neuron in allneurons_list:
    neuron_data = SingleNeuron(neuron)
# skip neurons for which no depolarizing events were extracted
    if neuron_data.depolarizing_events.empty:
        continue
        # in all these things, we'll want to exclude any events that are spikeshoulderpeaks
    spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
        # and things that were recorded in vclamp mode
    vclampblocks = list(set(
        [blockname for blockname in neuron_data.depolarizing_events.file_origin if 'Vclamp' in blockname]))
    vclampevents = neuron_data.depolarizing_events.file_origin.isin(vclampblocks)
    excludedevents = vclampevents | spikeshoulderpeaks
    # check if neuron has events occurring in the ttl-applied window
    evokedevents = neuron_data.depolarizing_events.applied_ttlpulse & (~excludedevents)
    if sum(evokedevents) > 0:
        lightactivatedneurons_list.append(neuron)
    # check if neuron has large-amplitude (>3mV) events
    largeampevents = (neuron_data.depolarizing_events.amplitude > 3) & (~excludedevents)
    if sum(largeampevents) > 0:
    # check if neuron has spontaneously occurring large-amplitude events
        largespontevents = (~neuron_data.depolarizing_events.applied_ttlpulse) & largeampevents & (~excludedevents)
        if sum(largespontevents) > 0:
            largesponteventsneurons_list.append(neuron)
    # check if neuron has evoked large-amplitude events
        largeevokedevents = evokedevents & largeampevents & (~excludedevents)
        if sum(largeevokedevents) > 0:
            largeevokedeventsneurons_list.append(neuron)

largeampspontandevokedneurons_list = list(set(largeevokedeventsneurons_list) & set(largesponteventsneurons_list))

print('total number of patched neurons in the dataset: ' + str(len(allneurons_list)))
print('number of neurons with light-evoked depolarizations: ' + str(len(lightactivatedneurons_list)))
print('number of neurons with spont. depolarizations > 3mV: ' + str(len(largesponteventsneurons_list)))
print('number of neurons with light-evoked depolarizations > 3mV: ' + str(len(largeevokedeventsneurons_list)))
print('number of neurons with both spont. '
      'and light-evoked depolarizations > 3mV: ' + str(len(largeampspontandevokedneurons_list)))

# %%
for neuron in largeampspontandevokedneurons_list:
    print(neuron)
    neuron_data = SingleNeuron(neuron)
    spikeshoulderpeaks = (neuron_data.depolarizing_events.event_label == 'spikeshoulderpeak')
    largeampevents = (neuron_data.depolarizing_events.amplitude > 3) & (~spikeshoulderpeaks)
    evokedevents = neuron_data.depolarizing_events.applied_ttlpulse & largeampevents
    spontevents = (~neuron_data.depolarizing_events.applied_ttlpulse) & largeampevents
    neuron_data.plot_depoleventsgroups_overlayed(evokedevents, spontevents,
                                                 group_labels=['evoked events', 'spont. events'],
                                                 plt_title=neuron,
                                                 do_baselining=True
                                                 )





