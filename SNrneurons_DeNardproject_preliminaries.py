## imports
# openly available packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# stuff I wrote
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import apply_filters_to_vtrace
from singleneuron_analyses_functions import get_aps_from_cellattachedrecording

# %% first exploration of data

# first, let's see that I can open recording files sent to me by DeNard:
example_data = SingleNeuron('20230720C',
                            path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')
single_segment = example_data.blocks[0].segments[0]
get_aps_from_cellattachedrecording(0, 0, single_segment, plot='on')


example_data2 = SingleNeuron('230511A',
                             path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')


# and let's see some of the data I recorded in I-clamp and V-clamp:
nv_example_data = SingleNeuron('230608A',
                               path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')

nv_example_data2 = SingleNeuron('230727A',
                               path='D:\\Beaste_IIa_Documents_backup\\Surmeier lab - stuffs and things\\DVS_project_data')


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


