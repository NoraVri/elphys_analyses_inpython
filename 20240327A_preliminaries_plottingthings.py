# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_plotting_functions import plot_ttlaligned
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %%
neuron_name = '20240327A'
# sulpiride applied and washed out again
# spont.activity, longPulses and optoStim
# neuron looks a little unsteady at first, then settles in to baselineV ~-65mV and stays steady throughout recordings
# spont.activity looks distinctly different to me between drug and no drug conditions - with drug there seem to be more and larger EPSPs.
# response to opto stim. may have gotten up to 50% larger after drug application, or not changed at all - gonna have to do statistics on that
singleneuron_data = SingleNeuron(neuron_name)


# %% figuring out a figure of averaged traces
# First let's see what subthreshold responses may look like:
singleneuron_data.ttlon_measures.plot.scatter('baselinev', 'response_maxamp')
# there's a clear split: anything with response_maxamp < 30mV are subthreshold responses; 50mV or more are APs (I checked).


subthreshold_responses_df = singleneuron_data.ttlon_measures[(singleneuron_data.ttlon_measures.response_maxamp < 30)]
# subthreshold_responses_df = subthreshold_responses_df[(subthreshold_responses_df.response_maxamp_postttl_t_inms < 8)]

nodrug_sr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('Stim_00')]
yesdrug_sr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('withSulpiride_00')]
washoutdrug_sr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('SulpirideWashout')]


figure1, axes1 = plot_ttlaligned(singleneuron_data.blocks, nodrug_sr_df,
                                 do_baselining=False,
                                 plotdvdt=False, prettl_t_inms=10, postttl_t_inms=150)
figure1.suptitle('no drug')
axes1[0].set_ylim([-100, -40])

figure2, axes2 = plot_ttlaligned(singleneuron_data.blocks, yesdrug_sr_df,
                                 do_baselining=False,
                                 plotdvdt=False, prettl_t_inms=10, postttl_t_inms=150)
figure2.suptitle('with drug')
axes2[0].set_ylim([-100, -40])

figure3, axes3 = plot_ttlaligned(singleneuron_data.blocks, washoutdrug_sr_df,
                                 do_baselining=False,
                                 plotdvdt=False, prettl_t_inms=10, postttl_t_inms=150)
figure3.suptitle('with drug washout')
axes3[0].set_ylim([-100, -40])

figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('baselinev', 'response_maxamp',
                          ax=axes)
yesdrug_sr_df.plot.scatter('baselinev', 'response_maxamp',
                           c='red',
                           ax=axes)
washoutdrug_sr_df.plot.scatter('baselinev', 'response_maxamp',
                               c='grey',
                               ax=axes)
figure.legend(['no drug', 'drug', 'washout'])

figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('applied_current', 'response_maxamp',
                          ax=axes)
yesdrug_sr_df.plot.scatter('applied_current', 'response_maxamp',
                           c='red',
                           ax=axes)
washoutdrug_sr_df.plot.scatter('applied_current', 'response_maxamp',
                               c='grey',
                               ax=axes)
figure.legend(['no drug', 'drug', 'washout'])

figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('applied_current', 'baselinev',
                          ax=axes)
yesdrug_sr_df.plot.scatter('applied_current', 'baselinev',
                           c='red',
                           ax=axes)
washoutdrug_sr_df.plot.scatter('applied_current', 'baselinev',
                               c='grey',
                               ax=axes)
figure.legend(['no drug', 'drug', 'washout'])
# %% plotting traces averaged by recording condition, subthreshold responses only
subthreshold_responses_df = singleneuron_data.ttlon_measures[(singleneuron_data.ttlon_measures.response_maxamp < 30)]
# subthreshold_responses_df = subthreshold_responses_df[(subthreshold_responses_df.response_maxamp_postttl_t_inms < 8)]
beforedrug_sthr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('Stim_00')]
withdrug_sthr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('withSulpiride_00')]
washdrug_sthr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('SulpirideWashout')]

# recordings were performed with varying levels of holding current; split out traces by -DC level:
holding_levels = [-400, -300, -200, -100, 0, 100]

def split_dfs_by_appliedcurrent(df, appliedcurrent_levels_list):
    hl_ranges = []
    for hl in appliedcurrent_levels_list:
        hl_range = [(hl - 5), (hl + 5)]
        hl_ranges.append(hl_range)

    clean_df = df[(df.applied_current_range < 1)]
    split_dfs_list = []
    for hl_range in hl_ranges:
        hl_df = clean_df[(clean_df['applied_current'] > hl_range[0]) & (clean_df['applied_current'] < hl_range[1])]
        split_dfs_list.append(hl_df)

    return split_dfs_list

beforedrug_dfs_by_level = split_dfs_by_appliedcurrent(beforedrug_sthr_df, holding_levels)
withdrug_dfs_by_level = split_dfs_by_appliedcurrent(withdrug_sthr_df, holding_levels)

for i, level in enumerate(holding_levels):
    if (len(beforedrug_dfs_by_level[i]) > 0) and (len(withdrug_dfs_by_level[i]) > 0):
        singleneuron_data.plot_averaged_traces(beforedrug=beforedrug_dfs_by_level[i],
                                               withdrug=withdrug_dfs_by_level[i])

#
# # singleneuron_data.plot_averaged_traces(
# #                                        nodrug_n400=beforedrug_dfs_by_level[0],
# #                                        # nodrug_n300=beforedrug_dfs_by_level[1],
# #                                        # nodrug_n200=beforedrug_dfs_by_level[2],
# #                                        # nodrug_n100=beforedrug_dfs_by_level[3],
# #                                        nodrug_0=beforedrug_dfs_by_level[4],
# #                                        # nodrug_100=beforedrug_dfs_by_level[5],
# # )

# %% going at it another way: by using the picked up depolarizing events

all_depolarizing_events = singleneuron_data.depolarizing_events
evoked_subthreshold_events = (all_depolarizing_events.applied_ttlpulse) & (all_depolarizing_events.amplitude < 30) & (all_depolarizing_events.amplitude > 3)
# widdling taking off some events that are likely to be compound (greater width than expected for single depolarizing event):
evoked_subthreshold_events = evoked_subthreshold_events & (all_depolarizing_events.width_30 <= 12)
# splitting out by drug condition
beforedrug_ese = evoked_subthreshold_events & (all_depolarizing_events.file_origin.str.contains('Stim_00'))
withdrug_ese = evoked_subthreshold_events & (all_depolarizing_events.file_origin.str.contains('withSulpiride_00'))

# singleneuron_data.plot_depoleventsgroups_overlayed(beforedrug_ese, withdrug_ese, group_labels=['without', 'with'])

def make_levels_ranges(levels_list, range):
    ranges_list = []
    for level in levels_list:
        level_range = [level - (range/2), level + (range/2)]
        ranges_list.append(level_range)
    return ranges_list

holding_levels = [-200, -100, 0, 100]  # [-400, -300, -200, -100, 0, 100]
holding_ranges = make_levels_ranges(holding_levels, 10)

for holding_current in holding_ranges:
    holdinglevel_eventstoplot = (all_depolarizing_events.applied_current > holding_current[0]) & (all_depolarizing_events.applied_current < holding_current[1])
    beforedrug_eventstoplot = beforedrug_ese & holdinglevel_eventstoplot
    withdrug_eventstoplot = withdrug_ese & holdinglevel_eventstoplot
    figure, axis = singleneuron_data.plot_depoleventsgroups_overlayed(beforedrug_eventstoplot, withdrug_eventstoplot, group_labels=['without', 'with'], prealignpoint_window_inms=10, plotwindow_inms=50)
    axis.set_ylim([-3, 30])
    figure, axis, _ = singleneuron_data.plot_depoleventsgroups_averages(beforedrug_eventstoplot, withdrug_eventstoplot, group_labels=['without', 'with'], plot_dvdt=False, prealignpoint_window_inms=10, plotwindow_inms=50, plt_title=('DC level = ' + str((holding_current[0] + 5))))
    axis.set_ylim([-3, 30])

