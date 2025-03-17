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
from singleneuron_analyses_functions import get_aps_from_cellattachedrecording
from singleneuron_analyses_functions import apply_filters_to_vtrace

# %% importing some data
cell20250217A1 = SingleNeuron('20250217A1')
cell20250217B2 = SingleNeuron('20250217B2')
cell20250217C1 = SingleNeuron('20250217C1')

recording_segment = cell20250217A1.blocks[3].segments[0]
sampling_frequency = float(recording_segment.analogsignals[0].sampling_rate.rescale('Hz'))
recording_segment_datatrace = recording_segment.analogsignals[0].squeeze()

plt.plot(recording_segment_datatrace)

data_trace_lpfiltered, data_trace_hpfiltered = apply_filters_to_vtrace(recording_segment_datatrace,
                                                                       0.5,
                                                                       5000,
                                                                       sampling_frequency,
                                                                       plot='off')

eventdetect_trace = np.array(recording_segment_datatrace) - data_trace_lpfiltered - data_trace_hpfiltered

get_aps_from_cellattachedrecording('block', 0, recording_segment,
                                   plot='on')

# single_segment = recording_segment
# recording_primary = single_segment.analogsignals[0]
# recording_secondary = single_segment.analogsignals[1]
# time_axis = recording_primary.times
# sampling_frequency = float(recording_primary.sampling_rate.rescale('Hz'))  # cast to float gets rid of quantities
#
# primary_recording_unit = str(recording_primary.units)[-2:]
# data_trace = recording_primary.squeeze()

