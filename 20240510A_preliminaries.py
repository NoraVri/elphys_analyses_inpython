# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_plotting_functions import plot_ttlaligned
import singleneuron_analyses_functions as snafs
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %%
neuron_name = '20240510A'
#

singleneuron_data = SingleNeuron(neuron_name)

# %%
# singleneuron_data.plot_rawdatablocks()
# singleneuron_data.get_ttlonmeasures_fromrawdata()

# %%
# %% getting depolarizing events
# # let's see how my algorithm does with the settings identified for a previously analyzed SNr neuron:
#
# singleneuron_data.plot_eventdetecttraces_forsegment(34, 1,
#                                                     oscfilter_lpfreq=1,
#                                                     depol_to_peak_window=10)
# it's not perfect on picking up spontaneously occurring depolarizing events - they often come in quick succession in small bouts, which trips up the algorithm when it comes to picking up each consecutive one.
# Performance on the light-evoked events looks good though, although note that for spiking responses, the after-hyperpolarization-depolarization overshoot tends to get picked up as a subthreshold event as well.


# # Let's run it for all the data:
# singleneuron_data.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=1, depol_to_peak_window=10)
# singleneuron_data.write_results()

# %% removing references to data from one bad recording file
# the first optoStim file got recorded all weird, as pClamp does sometimes - removing all references to it from the extracted measures tables:
# des_df = singleneuron_data.depolarizing_events
# new_des_df = des_df[~(des_df.file_origin == 'optoStim_withSulpiride_0000.abf')]
#
# ttlon_df = singleneuron_data.ttlon_measures
# new_ttlon_df = ttlon_df[~(ttlon_df.file_origin == 'optoStim_withSulpiride_0000.abf')]
#
# singleneuron_data.depolarizing_events = new_des_df
# singleneuron_data.ttlon_measures = new_ttlon_df
#
# re-casting idx values to int datatype to prevent errors down the line:
# des_df = singleneuron_data.depolarizing_events
# dtypes_dict = {}
# for key in des_df.keys():  # converting columns containing idcs & missing values
#     if 'idx' in key:                         # to bypass their being cast to float
#         dtypes_dict[key] = 'Int64'
# new_des_df = des_df.astype(dtypes_dict)
# singleneuron_data.depolarizing_events = new_des_df
#
# ttlon_measures = singleneuron_data.ttlon_measures
# dtypes_dict = {}
# for key in ttlon_measures.keys():  # converting columns containing idcs & missing values
#     if 'idx' in key:                         # to bypass their being cast to float
#         dtypes_dict[key] = 'Int64'
# new_ttlon_measures = ttlon_measures.astype(dtypes_dict)
# singleneuron_data.ttlon_measures = new_ttlon_measures


# singleneuron_data.write_results()
# %% figuring out a figure of averaged traces
# First let's see what subthreshold responses may look like:
singleneuron_data.ttlon_measures.plot.scatter('baselinev', 'response_maxamp')
# There's a pretty clear split between subthreshold and AP responses, except at some more depolarized baselinev where
# measured response amplitudes get low; probably spontaneous APs are messing with the automatic measurement.

# let's see what's going on with responses occurring at high baselinev:
# highbaselinev_responses = singleneuron_data.ttlon_measures[(singleneuron_data.ttlon_measures.baselinev > -40)]
# plot_ttlaligned(singleneuron_data.blocks, highbaselinev_responses, prettl_t_inms=10, postttl_t_inms=150)
# these are all cases where an AP was happening just before/as the light pulse hits.

# OK. So we want to focus on subthreshold responses, which looks like should be all responses with amp < 25 mV occurring at baselinev < -50mV.
ttlonmeasures_df = singleneuron_data.ttlon_measures
subthresholdresponses_df = ttlonmeasures_df[(ttlonmeasures_df.response_maxamp < 25) & (ttlonmeasures_df.baselinev < -50)]
# splitting out by drug condition
nodrug_sr_df = subthresholdresponses_df[~subthresholdresponses_df.file_origin.str.contains('Sulpiride')]
yesdrug_sr_df = subthresholdresponses_df[subthresholdresponses_df.file_origin.str.contains('Sulpiride')]

# check and see all raw data, split out by drug condition
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

# %%
# check and see: holding current, baselinev and response amp, split out by drug condition
figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('baselinev', 'response_maxamp',
                          ax=axes)
yesdrug_sr_df.plot.scatter('baselinev', 'response_maxamp',
                           c='red',
                           ax=axes)
figure.legend(['no drug', 'drug',])

figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('applied_current', 'response_maxamp',
                          ax=axes)
yesdrug_sr_df.plot.scatter('applied_current', 'response_maxamp',
                           c='red',
                           ax=axes)
figure.legend(['no drug', 'drug',])

figure, axes = plt.subplots(1, 1, squeeze=True)
nodrug_sr_df.plot.scatter('applied_current', 'baselinev',
                          ax=axes)
yesdrug_sr_df.plot.scatter('applied_current', 'baselinev',
                           c='red',
                           ax=axes)
figure.legend(['no drug', 'drug',])
# my impression is that the baselinev may be trending downward just a little after sulpiride application;
# however, it is quite variable and with similar-looking spread in both the drug and non-drug conditions, so I think we're OK to compare responses taken at -500 and -300 pA DC holding levels (the two that agree between drug and non-drug conditions):

holding_levels = [-500, -300,]
# def split_dfs_by_appliedcurrent(df, appliedcurrent_levels_list):
#     hl_ranges = []
#     for hl in appliedcurrent_levels_list:
#         hl_range = [(hl - 5), (hl + 5)]
#         hl_ranges.append(hl_range)
#
#     clean_df = df[(df.applied_current_range < 1)]
#     split_dfs_list = []
#     for hl_range in hl_ranges:
#         hl_df = clean_df[(clean_df['applied_current'] > hl_range[0]) & (clean_df['applied_current'] < hl_range[1])]
#         split_dfs_list.append(hl_df)
#
#     return split_dfs_list
#
# beforedrug_dfs_by_level = split_dfs_by_appliedcurrent(nodrug_sr_df, holding_levels)
# withdrug_dfs_by_level = split_dfs_by_appliedcurrent(yesdrug_sr_df, holding_levels)

# for i, level in enumerate(holding_levels):
#     if (len(beforedrug_dfs_by_level[i]) > 0) and (len(withdrug_dfs_by_level[i]) > 0):
#         singleneuron_data.plot_averaged_traces(beforedrug=beforedrug_dfs_by_level[i],
#                                                withdrug=withdrug_dfs_by_level[i])
# even with this data looking much neater, simply averaging comes out looking not nice at all


# %% going at it by using the picked up depolarizing events
all_depolarizing_events = singleneuron_data.depolarizing_events
evoked_subthreshold_events = (all_depolarizing_events.applied_ttlpulse) & (all_depolarizing_events.amplitude < 30) & (all_depolarizing_events.baselinev < -50)
# splitting out by drug condition
beforedrug_ese = evoked_subthreshold_events & ~(all_depolarizing_events.file_origin.str.contains('Sulpiride'))
withdrug_ese = evoked_subthreshold_events & (all_depolarizing_events.file_origin.str.contains('Sulpiride'))

def make_levels_ranges(levels_list, range):
    ranges_list = []
    for level in levels_list:
        level_range = [level - (range/2), level + (range/2)]
        ranges_list.append(level_range)
    return ranges_list

holding_ranges = make_levels_ranges(holding_levels, 10)

for holding_current in holding_ranges:
    holdinglevel_eventstoplot = (all_depolarizing_events.applied_current > holding_current[0]) & (all_depolarizing_events.applied_current < holding_current[1])
    beforedrug_eventstoplot = beforedrug_ese & holdinglevel_eventstoplot
    withdrug_eventstoplot = withdrug_ese & holdinglevel_eventstoplot
    figure, axis = singleneuron_data.plot_depoleventsgroups_overlayed(beforedrug_eventstoplot, withdrug_eventstoplot, group_labels=['without', 'with'], prealignpoint_window_inms=10, plotwindow_inms=50)
    axis.set_ylim([-3, 30])
    figure, axis, _ = singleneuron_data.plot_depoleventsgroups_averages(beforedrug_eventstoplot, withdrug_eventstoplot, group_labels=['without', 'with'], plot_dvdt=False, prealignpoint_window_inms=10, plotwindow_inms=50, plt_title=('DC level = ' + str((holding_current[0] + 5))))
    axis.set_ylim([-3, 30])
    holdinglevel_average_nodrug, _, _ = snafs.get_events_average(singleneuron_data.blocks, singleneuron_data.depolarizing_events,
                                                                         singleneuron_data.rawdata_readingnotes[
                                                                             'getdepolarizingevents_settings'],
                                                                         singleneuron_data.recordingblocks_index,
                                                                         beforedrug_eventstoplot,)
    holdinglevel_average_yesdrug, _, _ = snafs.get_events_average(singleneuron_data.blocks,
                                                                 singleneuron_data.depolarizing_events,
                                                                 singleneuron_data.rawdata_readingnotes[
                                                                     'getdepolarizingevents_settings'],
                                                                 singleneuron_data.recordingblocks_index,
                                                                 withdrug_eventstoplot, )
    print('at holding level ' + str(holding_current) + 'pA DC, the average response amplitude was ' + str(np.max(holdinglevel_average_nodrug)) + 'mV without drug and ' + str(np.max(holdinglevel_average_yesdrug)) + 'mV with drug')



