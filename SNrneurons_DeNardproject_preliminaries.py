## imports
# openly available packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# stuff I wrote
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import apply_filters_to_vtrace
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording

# %% first exploration of data

# first, let's see that I can open recording files sent to me by DeNard:
example_data = SingleNeuron('20230720C',
                            path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')
# single_segment = example_data.blocks[0].segments[0]
# segment_spikes = get_spikes_from_cellattachedrecording('block', 0, single_segment, plot='on')

# %%
example_data2 = SingleNeuron('230511A',
                             path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')

# %%
example_bad_data = SingleNeuron('230202_bad traces',
                             path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')
# block = example_bad_data.blocks[0]
# segments_idcs = [0, 50, 88, 99]
block = example_bad_data.blocks[1]
# segments_idcs = [0, 7, 13, 18]
# for i in segments_idcs:
#         get_aps_from_cellattachedrecording(block.file_origin, i,
#                                            block.segments[i], plot='on')
peaks_idcs = get_spikes_from_cellattachedrecording(block.file_origin, 7,
                                           block.segments[7], plot='on')
# %%
# and let's see some of the data I recorded in I-clamp and V-clamp:
nv_example_data = SingleNeuron('230608A',
                               path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')

nv_example_data2 = SingleNeuron('230727A',
                               path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')

segment = nv_example_data.blocks[3].segments[0]
peaks_idcs = get_spikes_from_cellattachedrecording('file', 0,
                                                   segment, plot='on')

segment2 = nv_example_data.blocks[1].segments[0]
peaks_idcs2 = get_spikes_from_cellattachedrecording('file', 0,
                                                   segment2, plot='on')

# %% let's see what applying filters does to cc and vc recordings:
for block in example_data.blocks:
    vc_segment = block.segments[0].analogsignals[0]
    time_axis = vc_segment.times
    sampling_frequency = float(vc_segment.sampling_rate.rescale('Hz'))
    vc_segment = np.array(np.squeeze(vc_segment))

    lpfiltered, hpfiltered = apply_filters_to_vtrace(vc_segment, 2, 5000, sampling_frequency)
    figure, axes = plt.subplots(6,1, sharex='all')
    axes[0].plot(time_axis, vc_segment)
    axes[0].set_title('raw recording')
    axes[1].plot(time_axis, lpfiltered, label='lp-filtered trace')
    axes[1].set_title('lp-filtered')
    axes[2].plot(time_axis, hpfiltered, label='hp-filtered')
    axes[2].set_title('hp-filtered')
    axes[3].plot(time_axis, (vc_segment - hpfiltered), label='raw - hp_filtered')
    axes[3].set_title('raw - hp-filtered')
    axes[4].plot(time_axis, (vc_segment - lpfiltered), label='raw - lp_filtered')
    axes[4].set_title('raw - lp-filtered')
    axes[5].plot(time_axis, (vc_segment - lpfiltered - hpfiltered))
    axes[5].set_title('raw - lp-filtered - hp-filtered')
# figure.legend()

# cc_segment = np.squeeze(nv_example_data2.blocks[0].segments[0].analogsignals[0])
# cc_lpfiltered, cc_hpfiltered = apply_filters_to_vtrace(cc_segment, plot='on')


# %%
neuron_data = SingleNeuron('20221229E')
des_df = neuron_data.depolarizing_events

intervals_df = neuron_data.get_events_intervals_inms(event_labels=['actionpotential', 'fastevent'])

