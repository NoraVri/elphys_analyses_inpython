# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

from detecta import detect_peaks
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_analyses_functions import make_cellattachedspikepeaks_dictionary

# %% importing some data
cell20250217A1 = SingleNeuron('20250217A1')
cell20250217A1_spikes_df = cell20250217A1.get_spikes_fromcellattachedrecording(plot='on')

# %%

cell20250217B2 = SingleNeuron('20250217B2')
cell20250217C1 = SingleNeuron('20250217C1')
cell230608A = SingleNeuron('230608A')
# getting spikes
cell20250217B2_spikes_df = cell20250217B2.get_spikes_fromcellattachedrecording()
cell20250217C1_spikes_df = cell20250217C1.get_spikes_fromcellattachedrecording()
cell230608A_spikes_df = cell230608A.get_spikes_fromcellattachedrecording()





# %%





recording_segment = cell20250217A1.blocks[3].segments[0]
# sampling_frequency = float(recording_segment.analogsignals[0].sampling_rate.rescale('Hz'))
# recording_segment_datatrace = recording_segment.analogsignals[0].squeeze()
#
# plt.plot(recording_segment_datatrace)
#
# data_trace_lpfiltered, data_trace_hpfiltered = apply_filters_to_vtrace(recording_segment_datatrace,
#                                                                        0.5,
#                                                                        5000,
#                                                                        sampling_frequency,
#                                                                        plot='off')
#
# eventdetect_trace = np.array(recording_segment_datatrace) - data_trace_lpfiltered - data_trace_hpfiltered

spikes_dict, data_trace_pastthreshold_idcs = get_spikes_from_cellattachedrecording(recording_segment, 'file', 0,
                                   plot='off')

# single_segment = recording_segment
# recording_primary = single_segment.analogsignals[0]
# recording_secondary = single_segment.analogsignals[1]
# time_axis = recording_primary.times
# sampling_frequency = float(recording_primary.sampling_rate.rescale('Hz'))  # cast to float gets rid of quantities
#
# primary_recording_unit = str(recording_primary.units)[-2:]
# data_trace = recording_primary.squeeze()
# empty_dict = make_cellattachedspikepeaks_dictionary()
# for block in cell20250217B2.blocks:
#     for i, segment in enumerate(block.segments):
#         dict = get_spikes_from_cellattachedrecording(segment, block.file_origin, i,
#                                                      plot='off')
#         for key in empty_dict:
#             empty_dict[key] += list(dict[key])
