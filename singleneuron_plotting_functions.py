# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:30:10 2020

@author: neert
"""
# %% imports


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# imports of functions that I wrote
import singleneuron_analyses_functions as snafs


# %% general raw-data plotting


# plotting all traces of a block, in individual subplots per channel, optionally with events marked
def plot_block(block, depolarizingevents_df,
               events_to_mark=None, time_axis_unit='ms', segments_overlayed=True):
    """ Takes a block and plots all analogsignals (voltage/current/aux (if applicable)),
    one subplot per channel_index.
    Optional arguments:
    - events_to_mark: should be a pd boolean series for indexing into subthreshold_events DataFrame; baselinev and peakv points will be marked accordingly.
    - time_axis_unit: 'ms' by default, can be changed to 's' (or any other time unit understood by quantities).
    - segments_overlayed: True by default, so that consecutive segments of the same block are
        plotted overlayed. If False, consecutive segments are plotted consecutively in the same plot.
    Note: if events_to_mark are passed through, segments_overlayed is set to False and time_axis_unit to ms.
    """
    # making one subplot per active recording channel
    nsubplots = len(block.channel_indexes)
    figure, axes = plt.subplots(nrows=nsubplots, ncols=1, sharex='all')
    # marking event baselines and peaks, if applicable
    if (events_to_mark is not None) and (not events_to_mark.empty): #insert here: if events_to_mark='by_label'
        blockevents_to_mark = (events_to_mark & (depolarizingevents_df.file_origin == block.file_origin))
        block_events_df = depolarizingevents_df[blockevents_to_mark]
        for idx, signal in enumerate(block.channel_indexes[0].analogsignals):
            time_axis = signal.times.rescale('ms')
            vtrace = np.squeeze(np.array(signal))
            trace_events = block_events_df.loc[block_events_df['segment_idx'] == idx]
            axes[0].scatter(time_axis[list(trace_events['baselinev_idx'])],
                            vtrace[list(trace_events['baselinev_idx'])],
                            color='green')
            axes[0].scatter(time_axis[list(trace_events['peakv_idx'])],
                            vtrace[list(trace_events['peakv_idx'])],
                            color='red')
        # setting plot settings so that points will be in the right place
        time_axis_unit = 'ms'
        segments_overlayed = False

    # plotting all the traces of the block
    for i in range(nsubplots):
        analogsignals = block.channel_indexes[i].analogsignals
        trace_unit = analogsignals[0].units
        for analogsignal in analogsignals:
            if segments_overlayed:
                time_axis = analogsignals[0].times
            else:
                time_axis = analogsignal.times
            time_axis = time_axis.rescale(time_axis_unit)
            trace_forplotting = np.squeeze(np.array(analogsignal))
            axes[i].plot(time_axis, trace_forplotting)
        axes[i].set_xlabel('time  in ' + time_axis_unit)
        axes[i].set_ylabel(str(trace_unit))
    return figure, axes

# plotting traces aligned to TTL, in neat windows (including options for setting scales to be identical across neurons)
def plot_ttlaligned(blockslist, ttlmeasures_df,
                    prettl_t_inms=2, postttl_t_inms=20,
                    do_baselining=True, plotdvdt=True,
                    colorby_measure='baselinev',
                    color_lims=None, plotlims=None,
                    skip_vtraces_block=None,
                    skip_vtraces_idcs=None,
                    maxamp_for_plotting=None,
                    noisefilter_hpfreq=3000,):
    """
    This function takes a list of blocks, and plots vtraces aligned to ttl-onset (for those blocks that have ttl).
    Time axis is re-aligned so that ttl onset = 0ms.
    Skip_vtraces can be an int; if it is, every non-multiple vtrace will be omitted from the plot.
    !Note: all blocks passed to this function should have 3 channels: voltage, current and TTL.
    """
    # getting figure and axes to plot on
    if plotdvdt:
        figure, axes = plt.subplots(1, 2)
    else:
        figure, axes = plt.subplots(1, 1, squeeze=False)
        axes = axes.squeeze(axis=1)
    vaxis_label = 'voltage (mV)'
    if do_baselining:
        vaxis_label = vaxis_label + ' (baselined)'
    # getting only the relevant ttl measures
    blocknames_list = [block.file_origin for block in blockslist]
    blocks_ttlmeasures_df = ttlmeasures_df[(ttlmeasures_df.file_origin.isin(blocknames_list)
                                            & (~ttlmeasures_df.baselinev.isna()))]  # by skipping traces where no baselinev value was calculated, we skip vclamp-recordings and traces where ttl wasn't actually on (even though 3rd channel was recorded)
    if maxamp_for_plotting is not None:
        blocks_ttlmeasures_df = blocks_ttlmeasures_df[(blocks_ttlmeasures_df['response_maxamp'] < maxamp_for_plotting)]
    if color_lims is not None and colorby_measure is not None:
        blocks_ttlmeasures_df = blocks_ttlmeasures_df[(blocks_ttlmeasures_df[colorby_measure] >= color_lims[0])
                                                    & (blocks_ttlmeasures_df[colorby_measure] <= color_lims[1])]
    if skip_vtraces_block is None and isinstance(skip_vtraces_idcs, list):
        blocks_ttlmeasures_df = blocks_ttlmeasures_df[~blocks_ttlmeasures_df.segment_idx.isin(skip_vtraces_idcs)]
    if skip_vtraces_block is not None and isinstance(skip_vtraces_idcs, list):
        blocks_ttlmeasures_df = blocks_ttlmeasures_df[~(blocks_ttlmeasures_df.file_origin.isin(skip_vtraces_block)
                                                        & blocks_ttlmeasures_df.segment_idx.isin(skip_vtraces_idcs))]
    # getting colors for line plots
    if isinstance(color_lims, list) and (len(color_lims) == 2):
        colormap, cm_normalizer = get_colors_forlineplots(colorby_measure=None, data=color_lims)
    else:
        colormap, cm_normalizer = get_colors_forlineplots(colorby_measure=colorby_measure,
                                                          data=blocks_ttlmeasures_df)

    for block in blockslist:
        block_ttlmeasures_df = blocks_ttlmeasures_df[(blocks_ttlmeasures_df.file_origin == block.file_origin)]
        if block_ttlmeasures_df.empty:
            continue
        else:
            for _, ttlmeasures_series in block_ttlmeasures_df.iterrows():
                # getting a de-noised vtrace for plotting:
                vtrace = block.channel_indexes[0].analogsignals[ttlmeasures_series['segment_idx']]
                sampling_frequency = float(vtrace.sampling_rate.rescale('Hz'))
                time_axis = vtrace.times
                vtrace = np.squeeze(np.array(vtrace))
                _, voltage_noisetrace = snafs.apply_filters_to_vtrace(vtrace, 5, noisefilter_hpfreq, float(sampling_frequency))
                vtrace = vtrace - voltage_noisetrace
                # getting ttl on and off time
                ttlfirston_idx = ttlmeasures_series['ttlon_idx']
                ttllaston_idx = ttlmeasures_series['ttloff_idx']
                time_axis = time_axis.rescale('ms')
                ttlfirston_time = time_axis[ttlfirston_idx]
                ttllaston_time = time_axis[ttllaston_idx]
                # plotting vlines for ttl on and off (re-aligned so that ttlon = 0ms)
                ttllaston_time = ttllaston_time - ttlfirston_time
                axes[0].axvline(0, linewidth=2, color='b')  # ttl on
                axes[0].axvline(ttllaston_time, linewidth=2, color='k')
                # grabbing the snippet for plotting, with time axis re-aligned to ttlon = 0
                onems_insamples = int(sampling_frequency / 1000)
                time_axis = time_axis - ttlfirston_time
                plotwindow_startidx = ttlfirston_idx - int(onems_insamples * prettl_t_inms)
                plotwindow_endidx = ttlfirston_idx + int(onems_insamples * postttl_t_inms)
                vtrace = vtrace[plotwindow_startidx:plotwindow_endidx]
                if do_baselining:  # make baselinev = 0 for plotted line, if requested
                    vtrace = vtrace - ttlmeasures_series['baselinev']
                axes[0].plot(time_axis[plotwindow_startidx:plotwindow_endidx],
                             vtrace,
                             color=colormap(cm_normalizer(ttlmeasures_series[colorby_measure])))
                if plotdvdt:  # make dvdt vs V plot, if requested
                    vtrace_diff = np.diff(vtrace)
                    axes[1].plot(vtrace[:-1:], vtrace_diff,
                                 color=colormap(cm_normalizer(ttlmeasures_series[colorby_measure])))
                    axes[1].set_xlabel(vaxis_label)
                    axes[1].set_ylabel('dV/dt, mV/ms')
    # adding axes labels
    axes[0].set_xlabel('time (ms)')
    axes[0].set_ylabel(vaxis_label)

    # setting axes lims
    axes[0].set_xlim((-1*prettl_t_inms, postttl_t_inms))
    if plotlims is not None:
        if plotdvdt and (len(plotlims) == 4):
            axes[0].set_ylim(plotlims[0], plotlims[1])
            axes[1].set_xlim(plotlims[0], plotlims[1])
            axes[1].set_ylim(plotlims[2], plotlims[3])
        if not plotdvdt and (len(plotlims) == 2):
            axes[0].set_ylim(plotlims[0], plotlims[1])
    figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap))
    return figure, axes


# %% depolarizing events and action potentials - line plots of raw data


# plotting an individual event, optionally with measures and/or baselined and/or normalized
def plot_single_event(vtrace, sampling_period_inms, axis_object, plot_startidx,
                      plotwindow_inms=40,
                      eventmeasures_series=pd.Series(),
                      get_measures_type='raw', display_measures=False,
                      do_baselining=True, do_normalizing=False,
                      linecolor='blue', label=None,
                      dvdtaxis_object=None,
                      ddvdtaxis_object=None):
    """ This function takes as inputs:
    required arguments:
    - a vtrace as np.array. By default it should be the raw vtrace, but if event-detect measures
        are to be displayed then the event-detect trace should be passed through.
    - sampling period in ms
    - the axis object onto which the trace is to be plotted
    - the starting index of the trace-bit to plot
    - the total length of the plotting window in ms (default = 40)
    optional arguments:
    - eventmeasures_series - pandas Series object containing all measures taken for this event
    - get_measures_type = 'raw' - by default, raw-trace event-measures are used for
        plotting/baselining/normalizing, but if the default is changed event-detect-trace measures are used instead.
    - display_measures - if True and an eventmeasures_series is passed through as well,
        event measures are displayed in the plot as well.
    - do_baselining and do_normalizing - if True and an eventmeasures_series is passed through as well,
        uses baselinev and amplitude (raw or event-detect, depending on get_measures_type) values
        to do baselining and/or normalizing, respectively.
    - line color and line label are passed through to mpl.plot.
    """
    # creating the event-trace and corresponding time axis
    event_trace = vtrace[plot_startidx:plot_startidx + int(plotwindow_inms / sampling_period_inms)]
    if plot_startidx + int(plotwindow_inms / sampling_period_inms) > len(vtrace):
        newplotwindow_inms = (len(vtrace) - plot_startidx) * sampling_period_inms
        time_axis = np.linspace(start=0, stop=newplotwindow_inms, num=len(event_trace))
    else:
        time_axis = np.linspace(start=0, stop=plotwindow_inms, num=len(event_trace))

    # optional: baselining and/or normalizing
    if do_baselining and not eventmeasures_series.empty and get_measures_type == 'raw':
        baseline_value = eventmeasures_series['baselinev']
        event_trace = event_trace - baseline_value
    elif do_baselining and not eventmeasures_series.empty:
        baseline_value = eventmeasures_series['ed_baselinev']
        event_trace = event_trace - baseline_value

    if do_normalizing and not eventmeasures_series.empty and get_measures_type == 'raw':
        normalize_value = eventmeasures_series['amplitude']
        event_trace = event_trace / normalize_value
    elif do_normalizing and not eventmeasures_series.empty:
        normalize_value = eventmeasures_series['ed_amplitude']
        event_trace = event_trace / normalize_value

    # plotting the line
    axis_object.plot(time_axis, event_trace,
                     color=linecolor, label=label)
    axis_object.set_xlabel('time (ms)')

    # optional: plotting dV/dt vs V onto a second axis object
    if dvdtaxis_object is not None:
        diff_event_trace = np.diff(event_trace)
        dvdtaxis_object.plot(event_trace[:-1:], diff_event_trace,
                             color=linecolor, label=label)
        dvdtaxis_object.set_ylabel('dV/dt')
        dvdtaxis_object.set_xlabel('V')
        # optional: plotting ddV/dt vs V onto another axis object
        if ddvdtaxis_object is not None:
            ddiff_event_trace = np.diff(diff_event_trace)
            ddvdtaxis_object.plot(event_trace[:-2:], ddiff_event_trace,
                                  color=linecolor, label=label)
            ddvdtaxis_object.set_ylabel('ddV/dt')
            ddvdtaxis_object.set_xlabel('V')

    # optional: adding scatterpoints and/or horizontal lines to mark measures where relevant:
    if display_measures and not eventmeasures_series.empty:
        measures_dict = make_eventmeasures_dict_forplotting(eventmeasures_series,
                                                            get_measures_type)
        for key, valsdict in measures_dict.items():
            point = valsdict['idx'] - plot_startidx
            if point < len(event_trace):
                if len(valsdict) == 2:
                    axis_object.scatter(time_axis[point], event_trace[point],
                                        color=valsdict['color'],
                                        label=key)
                    if dvdtaxis_object is not None and (point < len(diff_event_trace)):
                        dvdtaxis_object.scatter(event_trace[point], diff_event_trace[point],
                                                color=valsdict['color'],
                                                label=key)
                    if ddvdtaxis_object is not None and (point < len(ddiff_event_trace)):
                        ddvdtaxis_object.scatter(event_trace[point], ddiff_event_trace[point],
                                                 color=valsdict['color'],
                                                 label=key)
                if len(valsdict) == 3:
                    axis_object.hlines(y=event_trace[point],
                                       xmin=time_axis[point],
                                       xmax=time_axis[point] + valsdict['duration'],
                                       color=valsdict['color'],
                                       label=(key + ' = ' + str(valsdict['duration']) + 'ms'))
        if ddvdtaxis_object is not None:
            ddvdtaxis_object.legend(loc='lower right')
        elif dvdtaxis_object is not None:
            dvdtaxis_object.legend(loc='lower right')
        else:
            axis_object.legend(loc='lower right')


# plotting all/selected events of a rawdata_block, overlayed or individually (through plot_single_event)
def plot_singleblock_events(rawdata_block, block_eventsmeasures, getdepolarizingevents_settings,
                            timealignto_measure='peakv_idx',
                            colorby_measure='', color_lims=None, colormap='viridis',
                            prealignpoint_window_inms=5,
                            axis_object=None, newplot_per_event=False,
                            plot_dvdt=False, dvdt_axis_object=None,
                            plot_ddvdt=False, ddvdt_axis_object=None,
                            **kwargs):
    """ This function as inputs:
    Required arguments:
    - a raw-data block
    - the corresponding event-measures dataframe
    - the parameter settings dictionary used for finding depolarizing events
    Optional arguments:
    - timealignto_measure = 'peakv_idx' - by default, traces are aligned to event peaks; any
        time-based event-measures are acceptable.
    - colorby_measure = '' - by default, all lines are plotted in blue; if the name of one of the
        event-measures columns is passed, lines will be color-coded by this measure.
    - color_lims = None - by default, color-scale limits are inferred from extrema in the data; if
        a two-element list is passed ([a b] where a < b) these will be set as the colorbar limits.
    - prealignpoint_window_inms = 5 - startpoint of the displayed trace, in ms before the alignment-point.
    - axis_object = None - by default, a new plot is created for each event;
        if an axis object is passed, traces are plotted onto it and no new figure is created (unless newplot_per_event).
    - newplot_per_event = False - by default, traces are overlayed onto a provided axis_object; if set to True,
        each event will be plotted individually (as well).
    Other kwargs (passed through to plot_single_event):
    - plotwindow_inms = 40 - the total width of the plotted window
    - get_measures_type - unless 'raw', the event-detect traces will be displayed instead of raw V.
    - display_measures - if True, event measures are displayed in the plot as well, for each event in the plot(s).
    - do_baselining, do_normalizing - if True, uses baselinev and amplitude (raw or event-detect,
        depending on get_measures_type) values to do baselining and/or normalizing, respectively.
    - linecolor - can be passed through as a color string; will be overriden if colorby_measure is passed.
    - label - string passed through to mpl.plot.
    """
    # do not proceed unless event-measures data is provided
    if block_eventsmeasures.empty:
        print('no event-measures data for block ' + rawdata_block.file_origin)
        return

    # optional: setting the color mapping
    if colorby_measure and (color_lims is not None) and (len(color_lims) == 2):
        color_map, cm_normalizer = get_colors_forlineplots(colorby_measure, color_lims, colormap=colormap)
    elif colorby_measure:
        color_map, cm_normalizer = get_colors_forlineplots(colorby_measure, block_eventsmeasures, colormap=colormap)
        # print('colorbar automatically generated from single-block data')
    else:
        color_map = []
        cm_normalizer = []
    #
    axis = axis_object
    dvdt_axis = dvdt_axis_object
    ddvdt_axis = ddvdt_axis_object

    # getting the individual segments from the block
    segments_for_plotting_idcs = list(set(block_eventsmeasures['segment_idx']))
    for segment_idx in segments_for_plotting_idcs:
        segment_eventsmeasures = block_eventsmeasures.loc[block_eventsmeasures['segment_idx'] == segment_idx]
        vtrace_asanalogsignal = rawdata_block.segments[segment_idx].analogsignals[0]
        sampling_frequency = float(vtrace_asanalogsignal.sampling_rate)
        sampling_period_inms = float(vtrace_asanalogsignal.sampling_period) * 1000
        vtrace = np.squeeze(np.array(vtrace_asanalogsignal))
        # subtracting high-frequency noise from the raw voltage (as done for calculating depolevents measures)
        oscillationstrace, noisetrace = snafs.apply_filters_to_vtrace(
                                             vtrace,
                                             getdepolarizingevents_settings['oscfilter_lpfreq'],
                                             getdepolarizingevents_settings['noisefilter_hpfreq'],
                                             sampling_frequency,
                                             plot='off')

            # optional: getting the event-detect trace instead of the raw vtrace
        if 'get_measures_type' in kwargs.keys() and not kwargs['get_measures_type'] == 'raw':
            vtrace = vtrace - oscillationstrace - noisetrace
        else:
            vtrace = vtrace - noisetrace
        # plotting the events of the segment
        for _, eventmeasures in segment_eventsmeasures.iterrows():
            plot_startidx = (eventmeasures[timealignto_measure]
                             - int(prealignpoint_window_inms / sampling_period_inms))
            # setting up axes to plot on, if relevant
            if newplot_per_event and plot_dvdt and plot_ddvdt:
                figure, axes = plt.subplots(1, 3, squeeze=True)
                axis = axes[0]
                dvdt_axis = axes[1]
                ddvdt_axis = axes[2]
            elif newplot_per_event and plot_dvdt:
                figure, axes = plt.subplots(1, 2, squeeze=True)
                axis = axes[0]
                dvdt_axis = axes[1]
            elif newplot_per_event or (axis is None):
                figure, axis = plt.subplots(1, 1, squeeze=True)
                dvdt_axis = None
            # plotting
            if colorby_measure:
                linecolor = color_map(cm_normalizer(eventmeasures[colorby_measure]))
                plot_single_event(vtrace, sampling_period_inms, axis,
                                  plot_startidx,
                                  eventmeasures_series=eventmeasures,
                                  linecolor=linecolor,
                                  dvdtaxis_object=dvdt_axis,
                                  ddvdtaxis_object=ddvdt_axis,
                                  **kwargs)
            else:
                plot_single_event(vtrace, sampling_period_inms, axis,
                                  plot_startidx,
                                  eventmeasures_series=eventmeasures,
                                  dvdtaxis_object=dvdt_axis,
                                  ddvdtaxis_object=ddvdt_axis,
                                  **kwargs)




# %% helper functions:
# getting colormap information
def get_colors_forlineplots(colorby_measure, data, colormap='viridis'):
    if colormap == 'viridis':
        colormap = mpl.cm.viridis  # cividis
    else:
        colormap = mpl.cm.cividis
    if isinstance(data, list) and len(data) == 2:
        cm_normalizer = mpl.colors.Normalize(vmin=data[0],
                                             vmax=data[1])
    elif isinstance(data, pd.DataFrame):
        cm_normalizer = mpl.colors.Normalize(vmin=min(data[colorby_measure]),
                                             vmax=max(data[colorby_measure]))
    else:
        print('line coloring could not be resolved.')
        return
    return colormap, cm_normalizer


# getting dictionaries with the relevant information for marking event measures
def make_eventmeasures_dict_forplotting(eventmeasures_series, measuretype='raw'):
    """ This function takes a pd.Series object containing the measures for a single event,
    and returns them in a dictionary along with line/point color information for use in
    displaying event-measures through the plot_single_event function.
    Measures taken from APs or subthreshold depolarizations are returned, based on the content of eventmeasures_series.
    Measures are added only if their value is not nan, and time-based measures only if they are > 0.
    If measuretype is not "raw", values gotten from the event-detect trace will be returned.
    """
    # all events have a baseline-point and a peak-point, and it's the same in the raw and event-detect traces.
    measuresdict = {
        'baseline_v': {'idx': eventmeasures_series['baselinev_idx'],
                       'color': 'green'},

        'peak_v': {'idx': eventmeasures_series['peakv_idx'],
                   'color': 'red'},
    }

    # getting parameters as measured from the raw voltage trace
    if measuretype == 'raw':
        # rise measures
        if not pd.isna(eventmeasures_series['maxdvdt_idx']):
            measuresdict['max_dvdt'] = {
                'idx': eventmeasures_series['maxdvdt_idx'],
                'color': 'slategrey'
            }
        if not pd.isna(eventmeasures_series['threshold_idx']):
            measuresdict['threshold'] = {
                'idx': eventmeasures_series['threshold_idx'],
                'color': 'black'
            }
        if not pd.isna(eventmeasures_series['dvdt10_idx']):
            measuresdict['dvdt=10_threshold'] = {
                'idx': eventmeasures_series['dvdt10_idx'],
                'color': 'lightgrey'
            }
        if 'ap_prepotential_amp' in eventmeasures_series.keys() \
                and not pd.isna(eventmeasures_series['ap_prepotential_amp']):
            measuresdict['ap_prepotential_amp'] = {
                'idx': int(eventmeasures_series['ap_prepotential_idx']),
                'color': 'red'
            }

        if eventmeasures_series['rise_time_10_90'] > 0:
            measuresdict['rise_time_10_90'] = {
                'idx': eventmeasures_series['rt10_start_idx'],
                'duration': eventmeasures_series['rise_time_10_90'],
                'color': 'firebrick'
            }
        if eventmeasures_series['rise_time_20_80'] > 0:
            measuresdict['rise_time_20_80'] = {
                'idx': eventmeasures_series['rt20_start_idx'],
                'duration': eventmeasures_series['rise_time_20_80'],
                'color': 'tomato'
            }
        if eventmeasures_series['rise_time_maxdvdt_peak'] > 0:
            measuresdict['rise_time_maxdvdt_peak'] = {
                'idx': eventmeasures_series['maxdvdt_idx'],
                'duration': eventmeasures_series['rise_time_maxdvdt_peak'],
                'color': 'red'
            }

        # width measures
        if eventmeasures_series['width_baseline'] > 0:
            measuresdict['width_baseline'] = {
                'idx': eventmeasures_series['baselinev_idx'],
                'duration': eventmeasures_series['width_baseline'],
                'color': 'darkolivegreen'
            }
        if eventmeasures_series['width_10'] > 0:
            measuresdict['width_10pct_amp'] = {
                'idx': eventmeasures_series['width_10_start_idx'],
                'duration': eventmeasures_series['width_10'],
                'color': 'palegreen'
            }
        if eventmeasures_series['width_30'] > 0:
            measuresdict['width_30pct_amp'] = {
                'idx': eventmeasures_series['width_30_start_idx'],
                'duration': eventmeasures_series['width_30'],
                'color': 'greenyellow'
            }
        if eventmeasures_series['width_50'] > 0:
            measuresdict['width_50pct_amp'] = {
                'idx': eventmeasures_series['width_50_start_idx'],
                'duration': eventmeasures_series['width_50'],
                'color': 'green'
            }
        if eventmeasures_series['width_70'] > 0:
            measuresdict['width_70pctamp'] = {
                'idx': eventmeasures_series['width_70_start_idx'],
                'duration': eventmeasures_series['width_70'],
                'color': 'yellowgreen'
            }

        # ahp measures
        if not pd.isna(eventmeasures_series['ahp_min_idx']):
            measuresdict['ahp_min'] = {
                'idx': eventmeasures_series['ahp_min_idx'],
                'color': 'darkviolet'
            }
        if not pd.isna(eventmeasures_series['ahp_end_idx']):
            measuresdict['ahp_width'] = {
                'idx': eventmeasures_series['ahp_end_idx'],
                'duration': (-1 * eventmeasures_series['ahp_width']),
                'color': 'purple'
            }

        # spikeshoulderpeaks
        if eventmeasures_series['n_spikeshoulderpeaks'] > 0:
            shoulderpeaks_idcs_asstr = eventmeasures_series['spikeshoulderpeaks_idcs']
            # unless shoulderpeaks_idcs is an empty list (in the form of a string),
            # unpack the string into a list of indices and add each to the measuresdict
            if not shoulderpeaks_idcs_asstr == '[]':
                idcs_asstr = shoulderpeaks_idcs_asstr.replace('[', '')
                idcs_asstr = idcs_asstr.replace(']', '')
                idcs_asstr = idcs_asstr.replace(',', '')
                [*idcs_asstrs] = idcs_asstr.split(' ')
                for i, idx in enumerate(idcs_asstrs):
                    measuresdict['spikeshoulderpeak'+str(i)] = {
                        'idx': int(idx),
                        'color': 'orange'
                    }

    else:  # getting measures for the event-detect trace
        # rise measures
        if not pd.isna(eventmeasures_series['ed_maxdvdt_idx']):
            measuresdict['max_dvdt'] = {
                'idx': eventmeasures_series['ed_maxdvdt_idx'],
                'color': 'slategrey'
            }
        if eventmeasures_series['ed_rise_time_20_80'] > 0:
            measuresdict['rise_time_20_80'] = {
                'idx': eventmeasures_series['ed_rt20_start_idx'],
                'duration': eventmeasures_series['ed_rise_time_20_80'],
                'color': 'tomato'
            }
        # width measures
        if eventmeasures_series['ed_half_width'] > 0:
            measuresdict['width_50pct_amp'] = {
                'idx': eventmeasures_series['ed_hw_start_idx'],
                'duration': eventmeasures_series['ed_half_width'],
                'color': 'green'
            }
        if eventmeasures_series['ed_baseline_width'] > 0:
            measuresdict['width_baseline'] = {
                'idx': eventmeasures_series['baselinev_idx'],
                'duration': eventmeasures_series['ed_baseline_width'],
                'color': 'darkolivegreen'
            }
        # ahp measures
        if not pd.isna(eventmeasures_series['ed_ahp_min_idx']):
            measuresdict['ahp_min'] = {
                'idx': eventmeasures_series['ed_ahp_min_idx'],
                'color': 'darkviolet'
            }
        if not pd.isna(eventmeasures_series['ed_ahp_end_idx']):
            measuresdict['ahp_width'] = {
                'idx': eventmeasures_series['ed_ahp_end_idx'],
                'duration': (-1 * eventmeasures_series['ed_ahp_width']),
                'color': 'purple'
            }

    return measuresdict
