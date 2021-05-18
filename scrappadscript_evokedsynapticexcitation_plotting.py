from singleneuron_class import SingleNeuron
from singleneuron_plotting_functions import get_colors_forlineplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# plotting all traces of a block (except those with an evoked AP), baselined to V just before TTL on
def plot1(singleneuron, block_id, color_lims=[-100, -20], time_window=[0.0022, 0.03]):
    figure, axis = plt.subplots(1, 1)
    colormap, cm_normalizer = get_colors_forlineplots(colorby_measure=None, data=color_lims)

    if isinstance(block_id, int):
        blockslist = [block_id] #singleneuron.blocks[block_id]
    elif isinstance(block_id, str):
        allblocks_names = singleneuron.get_blocknames(printing='off')
        blockslist = [allblocks_names.index(block_id)]
    elif isinstance(block_id, list) and isinstance(block_id[0], int):
        blockslist = block_id
    else:
        print('could not resolve block id(s)')
        return

    for blockidx in blockslist:
        block = singleneuron.blocks[blockidx]
        vtraces = block.channel_indexes[0].analogsignals
        ttltrace = block.channel_indexes[2].analogsignals[0]
        ttlon_boolean = np.squeeze(ttltrace > 1)
        ttlfirston_idx = np.where(ttlon_boolean == True)[0][0]
        time_axis = vtraces[0].times
        time_axis = time_axis.rescale('ms')
        ttlfirston_time = time_axis[ttlfirston_idx]
        time_axis = time_axis - ttlfirston_time
        for vtrace in vtraces:
            vtrace = np.squeeze(np.array(vtrace))
            # skip traces where an AP is evoked
            if np.amax(vtrace[ttlfirston_idx:ttlfirston_idx + 1000]) > -10:
                continue
            # baselining value: meanv in the ms before ttl on
            baselinev = np.mean(vtrace[ttlfirston_idx - 20:ttlfirston_idx])
            vtrace = vtrace[(ttlfirston_idx - int(20000 * time_window[0])):(ttlfirston_idx + int(20000 * time_window[1]))]  # grabbing a snippet around ttlon
            vtrace_forplotting = vtrace - baselinev
            axis.plot(time_axis[(ttlfirston_idx - int(20000 * time_window[0])):(ttlfirston_idx + int(20000 * time_window[1]))],
                      vtrace_forplotting, color=colormap(cm_normalizer(baselinev)))
            axis.axvline(0)
        axis.set_xlabel('time (ms)')
        axis.set_ylabel('voltage (baselined)')
    axis.set_title(singleneuron.name + 'file(s) ' + str(block_id))
    figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap))

# plotting all traces of a block (with baseline falling within a certain range) twice: 1.raw baselined, 2.dV/dt vs V
def plot2(singleneuron, block_id, baseline_lims=[-100, -20], time_window=[0.002, 0.03]):
    figure, axes = plt.subplots(1, 2)
    colormap, cm_normalizer = get_colors_forlineplots(colorby_measure=None, data=baseline_lims)

    if isinstance(block_id, int):
        blockslist = [block_id] # singleneuron.blocks[block_id]
    elif isinstance(block_id, str):
        allblocks_names = singleneuron.get_blocknames(printing='off')
        blockslist = [allblocks_names.index(block_id)]
    elif isinstance(block_id, list) and isinstance(block_id[0], int):
        blockslist = block_id
    else:
        print('could not resolve block id(s)')
        return

    for blockidx in blockslist:
        block = singleneuron.blocks[blockidx]
        vtraces = block.channel_indexes[0].analogsignals
        ttltrace = block.channel_indexes[2].analogsignals[0]
        ttlon_boolean = np.squeeze(ttltrace > 1)
        ttlfirston_idx = np.where(ttlon_boolean == True)[0][0]
        time_axis = vtraces[0].times
        time_axis = time_axis.rescale('ms')
        ttlfirston_time = time_axis[ttlfirston_idx]
        time_axis = time_axis - ttlfirston_time
        for vtrace in vtraces:
            vtrace = np.squeeze(np.array(vtrace))
            # baselining value: meanv in the ms before ttl on
            baselinev = np.mean(vtrace[ttlfirston_idx - 20:ttlfirston_idx])
            # skip trace if baseline value outside of range
            if ~(baseline_lims[0] < baselinev < baseline_lims[1]):
                continue
            vtrace = vtrace[(ttlfirston_idx - int(20000 * time_window[0])):(ttlfirston_idx + int(20000 * time_window[1]))]  # grabbing a snippet around ttlon
            vtrace_baselined = vtrace - baselinev
            vtrace_diff = np.diff(vtrace)

            axes[0].plot(time_axis[(ttlfirston_idx - int(20000 * time_window[0])):(ttlfirston_idx + int(20000 * time_window[1]))],
                      vtrace_baselined, color=colormap(cm_normalizer(baselinev)))
            axes[0].axvline(0)

            axes[1].plot(vtrace_baselined[:-1:], vtrace_diff, color=colormap(cm_normalizer(baselinev)))

        axes[0].set_xlabel('time (ms)')
        axes[0].set_ylabel('voltage (baselined), mV')
        axes[1].set_xlabel('voltage (baselined), mV')
        axes[1].set_ylabel('dV/dt, mV/ms')
    axes[0].set_title(singleneuron.name + 'file(s) ' + str(block_id))
    figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap))




# %%
neuron_data = SingleNeuron('20210426B')
plot2(neuron_data, 1, baseline_lims=[-52, -30])

des_df = neuron_data.depolarizing_events
decentamp_events = des_df.amplitude > 2
unlabeled_events = des_df.event_label.isna() & decentamp_events
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
evoked_events = unlabeled_events & des_df.applied_ttlpulse

neuron_data.plot_depolevents(spont_unlabeled_events,
                             do_baselining=True,
                             # do_normalizing=True,
                             # colorby_measure='amplitude',
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=5,
                             plotwindow_inms=30,
                             )

neuron_data.plot_depolevents(evoked_events,
                             do_baselining=True,
                             # do_normalizing=True,
                             # colorby_measure='amplitude',
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=5,
                             plotwindow_inms=30,
                             )

decentv_spont_events = spont_unlabeled_events & (des_df.baselinev < -45)
neuron_data.plot_depoleventsgroups_overlayed(decentv_spont_events, evoked_events,
                                             group_labels=['spont', 'evoked'],
                                             # timealignto_measure='rt10_start_idx',
                                             do_baselining=True,
                                             do_normalizing=True
                                             )

# %%
neuron_data = SingleNeuron('20210426C')
plot2(neuron_data, [1, 2, 3], baseline_lims=[-52, -20])

des_df = neuron_data.depolarizing_events
decentamp_events = des_df.amplitude > 2
unlabeled_events = des_df.event_label.isna() & decentamp_events
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
# evoked_events = unlabeled_events & des_df.applied_ttlpulse

neuron_data.plot_depolevents(spont_unlabeled_events,
                             do_baselining=True,
                             # do_normalizing=True,
                             # colorby_measure='amplitude',
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=5,
                             plotwindow_inms=30,
                             )

# %%
neuron_data = SingleNeuron('20210426D')
plot2(neuron_data, 3, baseline_lims=[-70, -40])
plot2(neuron_data, [4, 5], baseline_lims=[-70, -40])
plot2(neuron_data, [6, 7], baseline_lims=[-60, -30])

des_df = neuron_data.depolarizing_events
decentamp_events = des_df.amplitude > 2
unlabeled_events = des_df.event_label.isna() & decentamp_events
fast_unlabeled_events = unlabeled_events & (des_df.rise_time_20_80 < 0.8)

spont_events = fast_unlabeled_events & ~des_df.applied_ttlpulse
evoked_events = unlabeled_events & des_df.applied_ttlpulse

neuron_data.plot_depolevents(spont_events,
                             do_baselining=True,
                             # do_normalizing=True,
                             # colorby_measure='amplitude',
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=5,
                             plotwindow_inms=30,
                             )

neuron_data.plot_depolevents(evoked_events,
                             do_baselining=True,
                             # do_normalizing=True,
                             # colorby_measure='amplitude',
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=5,
                             plotwindow_inms=30,
                             )

evoked_fastevents = evoked_events & (des_df.amplitude > 4)
neuron_data.plot_depoleventsgroups_overlayed(spont_events, evoked_fastevents,
                                             group_labels=['spont', 'evoked'],
                                             # timealignto_measure='rt10_start_idx',
                                             do_baselining=True,
                                             # do_normalizing=True
                                             )

# %%
neuron_data = SingleNeuron('20210411F')
plot2(neuron_data, 1, baseline_lims=[-40, -20])
plot2(neuron_data, 2, baseline_lims=[-40, -20])

# %%

# %%
neuron_data = SingleNeuron('20210123D')
neuron_data.plot_rawdatablocks('gapFree')
neuron_data.plot_rawdatablocks('light')
neuron_data.get_blocknames()

lims = [-75, -38]
plot2(neuron_data, [2, 3, 4, 5, 6], baseline_lims=lims, color_lims=lims, time_window=[0.01, 0.04])


# %% the effect of changing baseline voltage (at the same light duration)
# %%
cell1 = SingleNeuron('20201125B')
# cell1.plot_rawdatablocks('light')
# cell1.get_blocknames()
# light 0-2 duration=1ms; light3 duration=3ms; light4 duration=6ms; different baselinevs in all
color_lims = [-100, -35]
plot1(cell1, [4, 5], color_lims=color_lims)
plot1(cell1, 6, color_lims=color_lims)
plot1(cell1, 7, color_lims=color_lims)

# %%
cell2 = SingleNeuron('20201125C')
# cell2.plot_rawdatablocks('light')
# cell2.get_blocknames()
# light 0-3 duration=1ms; light4 duration=3ms (and cell dying)
# in light0 has one trace that looks different from all the others (as though a fast-event just happens to arrive at the same time as the light)
color_lims = [-80, -40]
# plot1(cell2, 1, color_lims=color_lims)
plot1(cell2, [1, 2, 3, 4], color_lims=color_lims)
plot1(cell2, 5, color_lims=color_lims)

# %%
cell3 = SingleNeuron('20201125D')  # 'best representative example' so far
# cell3.plot_rawdatablocks('light')
# cell3.get_blocknames()
# light 0-2 duration=1ms; light3 duration=0.5ms; light4 duration=0.2ms; light5 duration=0.05ms; light6 duration=0.01?ms
# light duration going down to the barely perceptible (and it actually seems to be making a difference)
color_lims = [-100, -40]
plot1(cell3, [3, 4, 5], color_lims=color_lims)
plot1(cell3, 6, color_lims=color_lims)
plot1(cell3, 7, color_lims=color_lims)
plot1(cell3, 8, color_lims=color_lims)
plot1(cell3, 9, color_lims=color_lims)
# %%
cell4 = SingleNeuron('20201125E')
# cell4.plot_rawdatablocks('light')
# cell4.get_blocknames()
# just one block and cell dies in the middle; illumination time = 1ms
color_lims = [-55, -25]
plot1(cell4, 1, color_lims=color_lims)
# %%
cell5 = SingleNeuron('20201125F')
# cell5.plot_rawdatablocks('light')
# cell5.get_blocknames()
# same exact story as E
color_lims = [-100, -40]
plot1(cell5, 2, color_lims=color_lims)


# %%
thy1cell1 = SingleNeuron('20200630B2')
# thy1cell1.plot_rawdatablocks('light')
# thy1cell1.get_blocknames()

color_lims = [-60, -35]
plot1(thy1cell1, [2, 3, 4, 5, 6, 7], color_lims=color_lims)

# %%
neuron_data = SingleNeuron('20210113G')
# neuron_data.plot_rawdatablocks()
lims = [-70, -50]
plot2(neuron_data, 8, baseline_lims=lims, color_lims=lims, time_window=[0.002, 0.02])

# %% the effect of changing light duration (at the same baseline voltage)



