# %% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantities as pq

from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_longpulsemeasures
from singleneuron_analyses_functions import apply_rawvtrace_manipulations
from singleneuron_analyses_functions import make_derivative_per_ms
# %% importing singleneuron data
# singleneuron_data = SingleNeuron('20190529B')
# singleneuron_data = SingleNeuron('20190529D')
singleneuron_data = SingleNeuron('20190812A')
# singleneuron_data = SingleNeuron('20200106C')
# singleneuron_data = SingleNeuron('20200310G')

# %%
allfiles_names = singleneuron_data.get_blocknames(printing='off')
longpulses_filesnames = [filename for filename in allfiles_names if 'IV' in filename]

# singleneuron_data.plot_blocks_byname('IV')
singleneuron_data.plot_blocks_byname(longpulses_filesnames[0])

block_idx = allfiles_names.index(longpulses_filesnames[0])
segment = singleneuron_data.blocks[block_idx].segments[0]
longpulses_resultsdict = get_longpulsemeasures(longpulses_filesnames[0],
                                               1, segment)
# %%
# manipulated_traces = apply_rawvtrace_manipulations(np.array(np.squeeze(segment.analogsignals[0])),
#                                                    singleneuron_data.rawdata_readingnotes[
#                                                        'getdepolarizingevents_settings']['oscfilter_lpfreq'],
#                                                    singleneuron_data.rawdata_readingnotes[
#                                                        'getdepolarizingevents_settings']['noisefilter_hpfreq'],
#                                                    float(segment.analogsignals[0].sampling_rate),
#                                                    segment.analogsignals[0].times,
#                                                    plot='on')
