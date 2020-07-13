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
print('total number of neurons patched: ' + str(len(allneurons_list)))
# the list of neurons in the dataset with light-evoked synaptic activations
lightactivated_list = [
    '20190527A',
    '20190527C',
    '20190529A1',
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
    '20200701D',
    '20200706B',
    '20200706D',
    '20200706E',
    '20200707E',
    '20200708B',
    '20200708C',
    '20200708D',
    '20200708F',
    '20200708G'
]
print('number of neurons with light-evoked synaptic excitations in the dataset: ' + str(len(lightactivated_list)))
# %% for neurons on the lightactivated-list,
#   1.] see if they have events of amp > 3 mV;
#   2.] if so, see if they could correspond to the fast-events we're looking for
#   2a] they come in multiple amplitude, but with the same waveform
#   2b] there are no amplitude-groups, but the rise-time parameters of the event fit the description
#   2c] there are light-evoked events that fit the description

#   0.] if they don't have APs and fast-events extracted already, run get_depolarizingevents
#   with standard settings since we're (for now) only looking for neurons with very obvious fast-events
# for neuron in allneurons_list:
#     neuron_data = SingleNeuron(neuron)
#     if 'getdepolarizingevents_settings' in neuron_data.rawdata_readingnotes.keys():
#         continue
#     else:
#         neuron_data.get_depolarizingevents_fromrawdata(min_depolspeed=0.2,
#                                                        min_depolamp=2,
#                                                        ttleffect_windowinms=10)
#         neuron_data.write_results()

# 1.] for neurons that have events of amp > 2mV, plot those
