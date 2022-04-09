# %% imports
# openly available packages
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
# stuff I wrote
from singleneuron_class import SingleNeuron

# %% first exploration of data
# Three neurons clearly identified as TH+: 20220303B (WT) and 20200307B and C (mutant). Cell C was not actually
# a recording according to notes, so we'll start with the Bs.

thneuron_wt = SingleNeuron('20220303B')
# thneuron_wt.plot_rawdatablocks()
#
thneuron_mut = SingleNeuron('20220307B')
# thneuron_mut.plot_rawdatablocks()

# That looks promising - there seems to be an order of magnitude difference in Rin, and the shortPulse measurement
# is also in line with an increase in membrane resistance. Let's see if we can capture those things into pictures:
# %%
# plotting longPulses on the same axes for both neurons:

_, axes_mut = thneuron_mut.plot_rawdatablocks('longPulses_0005.abf')
axes_mut[0].set_xlim([800, 2500])
axes_mut[0].set_ylim([-105, 45])
axes_mut[1].set_ylim([-800, 300])
_, axes_wt = thneuron_wt.plot_rawdatablocks('longPulses_0.abf')
axes_wt[0].set_xlim([800, 2500])
axes_wt[0].set_ylim([-105, 45])
axes_wt[1].set_ylim([-800, 300])

# %%
# plotting baselined and averaged shortPulses
def get_baselined_averaged_snippet(block, start_t, trace_length_inms):
    voltage_traces = block.channel_indexes[0].analogsignals
    current_trace = np.squeeze(np.array(block.channel_indexes[1].analogsignals[0]))
    sampling_rate = int(voltage_traces[0].sampling_rate)
    time_axis = voltage_traces[0].times.rescale('ms')
    trace_length_insamples = int(sampling_rate / 1000 * trace_length_inms)
    start_idx = int(start_t / 1000 * sampling_rate)
    baselining_endidx = int(5 / 1000 * sampling_rate)
    snippets_array = np.zeros((trace_length_insamples, len(voltage_traces)))
    snippet_time_axis = time_axis[start_idx:(start_idx + trace_length_insamples)]
    snippet_current_trace = current_trace[start_idx:(start_idx + trace_length_insamples)]
    for i, trace in enumerate(voltage_traces):
        trace = np.squeeze(np.array(trace))
        snippet_trace = trace[start_idx:(start_idx + trace_length_insamples)]
        snippet_trace_baseline = np.mean(snippet_trace[0:baselining_endidx])
        snippet_trace_baselined = snippet_trace - snippet_trace_baseline
        snippets_array[:, i] = snippet_trace_baselined

    snippet_mean = np.nanmean(snippets_array, axis=1)
    snippet_std = np.nanstd(snippets_array, axis=1)

    figure, axes = plt.subplots(2, 1)
    axes[0].plot(snippet_time_axis, snippet_mean)
    axes[0].plot(snippet_time_axis, (snippet_mean - snippet_std), '--')
    axes[0].plot(snippet_time_axis, (snippet_mean + snippet_std), '--')

    axes[1].plot(snippet_time_axis, snippet_current_trace)
    figure.suptitle(block.file_origin)
    return figure, axes

shortPulses_block_wt = thneuron_wt.blocks[7]
wtfigure, wtaxes = get_baselined_averaged_snippet(shortPulses_block_wt, 1042, 40)
shortPulses_block_mut = thneuron_mut.blocks[20]
mutfigure, mutaxes = get_baselined_averaged_snippet(shortPulses_block_mut, 1042, 40)


