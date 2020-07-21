# %% putative axonal spine responses in IO neurons, as evoked by synaptic inputs in the Thy1-mouse IO.
# Focus of this investigation: fast, depolarizing events of highly consistent waveform
# (as reflected by near-identical rise-time and half-width), that fall into groups
# of different specific amplitudes.

# Running this script will output summary results over all neurons in the dataset;
# full analyses can be found in an individual script per neuron (for those that have obvious fast-events).

# For now, we are looking for neurons that obviously have these events (they come in multiple amplitudes, all >3mV),
# to then determine whether light-evoked responses in these neurons (also) contain this response.


# %% initializing
## imports
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
largeampspontandevokedneurons_list.sort()

print('total number of patched neurons in the dataset: ' + str(len(allneurons_list)))
print('number of neurons with light-evoked depolarizations: ' + str(len(lightactivatedneurons_list)))
print('number of neurons with spont. depolarizations > 3mV: ' + str(len(largesponteventsneurons_list)))
print('number of neurons with light-evoked depolarizations > 3mV: ' + str(len(largeevokedeventsneurons_list)))
print('number of neurons with both spont. '
      'and light-evoked depolarizations > 3mV: ' + str(len(largeampspontandevokedneurons_list)))

# %% plotting spont. and evoked events overlayed, one plot per neuron
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

# first-impression notes on plots of spont. and evoked events > 3mV
#190527A: looks like it has fast-events spontaneously as well as evoked things that may be very similar;
# however, both spont. and evoked also include lots of other things, and it'll probably be hard to tease them all apart.
#190527C: among the spont. events only one looks like it would be a fast-event like the ones we're looking for,
# but in the evoked events there's a couple HUGE ones (25, 30 and 40 mV amps) that look like they may actually fit
#190529A1: looks like it probably has spont. fast-events of a few different amplitudes (up to 10mV),
# and like these may be among the evoked responses as well (though riding another, slower-rise response).
# But this neuron also has other spontaneous events with pretty fast rise time that are huge (15 - 30 mV)
# and definitely not fast-events.
#190529B: none of the large-amplitude spont. events are actually fast-events, they're all noise.
# The evoked responses look like they may very well include fast-events, but they're all compound
# (either multiple fast-events and/or also other things).
#190529D: looks like it has spont.events of a few different amplitudes (4, 5, and 6mV, as well as one of 15 mV);
# possibly they are also there in the evoked responses, but these are always much larger amplitude (6 - 30 mV)
#190529E: the single spont.event looks quite fast but it's also definitely a doublet;
# evoked responses are in the range of 3 - 5 mV and also look like they're often doublets
#200630A: there are some pretty fast things both in the spont. and evoked events,
# but it's not clear that any of these would be the fast-events we're looking for.
#200630B2: this may just be the golden example neuron: both spont. and evoked events seem to come in
# similar amplitude-groups, and I see a few examples where rise and decay look damn-well identical for spont. and evoked
# (though this is also aided by the fact that spont. events often seem to ride a slower depolarization).
#200630C: clearly has spont. fast-events (5 different amplitude groups, 2 - 10 mV);
# evoked responses look like they might have fast-events in them but it'll be hard to tease them apart from other things.
#200630D: seems to have fast-events (at least 3 different amplitudes, 5 - 10 mV)
# as well as a more-rounded, relatively fast-event in at least 2 different amplitudes (9 - 12 mV) and
# evoked responses that are all larger than that (12 - 40 mV) and could very well contain both of these responses
# and much more.
#200701A: looks like it has a spont.event of 14 mV (though a single 4mV event might be another example),
# and some of the evoked events look like they might have the same decay but their rise is very different for sure
#200706B: spont. events look more like APs without the Na-spike; honestly, so do most of the evoked responses
# although those do seem to come in different amplitude groups (5 - 25 mV, but the larges ones look compound).
#200706D: spont. 'events' aren't actually events, just Vrest depolarizing step-wise;
# evoked events all look the same (amp 3.5 mV) but too slow (rise-time ~3 ms)
#200706E: looks like it has fast-events spontaneously (multiple amplitude groups ranging 3 - 17 mV,
# though some are doublets) but these are never among the evoked events.
# Also has some sort of weird inverse-U-shaped response, spont. and once evoked, possibly in different amplitudes.
#200707E: spont. events look like they may come in amplitude groups (2 - 8 mV, though also many doublets);
# same for evoked responses
#200708B: has spont. events in multiple amplitude-groups (3 - 12 mV), as well as some evoked things that may have
# very similar decay (though their rise always much slower).
#200708C: single spont. 'event' is in fact an AP; single evoked event is nothing interesting.
#200708D: has lots of spont. fast-rise events (3 - 14 mV), looks like there's fast-events in multiple amplitude groups
# but also another, more rounded event with different decay. Evoked responses can get even larger (up to 20 mV)
# and may have similar decay as spont. fast-events, but always have different rise.
#200708F: this neuron's data should definitely get thoroughly analyzed: it's the one that had NMDA-blocker applied,
# and it has SO many fast and large events recorded (both spont. and evoked) I don't even know what to write here.
#200708G: events look somewhat slow and rather small for fast events (rise-time ~2ms, amp 3 - 6 mV) yet they look very
# consistent in decay, may come in amplitude groups and evoked events look exactly the same.

# candidate neurons that obviously have fast-events (and not too much of other large-amp fast things mucking them up),
# and are likely to have fast-events included in their response to excitation:
# 20190529D, 20200630B2, 20200630C, 20200707E, 20200708B, 20200708G

# other neurons that very possibly have fast-events but also other large-amp fast things,
# and are likely to have fast-events included in their response to excitation:
# 20190527A, 20190529A1, 20200630A, 20200630D, 20200707E, 20200708D, 20200708F 