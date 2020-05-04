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


# plotting all traces of a block, in individual subplots per channel
def plot_block(block, events_to_mark='none'):
    """ takes a block and plots all analogsignals (voltage/current/aux (if applicable)),
    one subplot per channel_index.
    If a subthreshold events or action potentials DataFrame is passed through,
    baselinev and peakv points will be marked accordingly.
    """
    # getting the time axis all traces have in common
    time_axis = block.channel_indexes[0].analogsignals[0].times
    time_axis = time_axis.rescale('ms')
    # making one subplot per active recording channel
    nsubplots = len(block.channel_indexes)
    figure, axes = plt.subplots(nrows=nsubplots, ncols=1, sharex='all')
    # plotting all the traces of the block
    for i in range(nsubplots):
        traces = np.transpose(np.squeeze(np.array(list(iter(
                                block.channel_indexes[i].analogsignals)))))
        traces_unit = block.channel_indexes[i].analogsignals[0].units
        axes[i].plot(time_axis, traces)
        axes[i].set_xlabel('time (ms)')
        axes[i].set_ylabel(str(traces_unit))

    # marking event baselines and peaks, if applicable
    if isinstance(events_to_mark, pd.DataFrame):
        block_events = events_to_mark.loc[
                            events_to_mark['file_origin'] == block.file_origin]
        for idx, signal in enumerate(block.channel_indexes[0].analogsignals):
            vtrace = np.squeeze(np.array(signal))
            trace_events = block_events.loc[block_events['segment_idx'] == idx]
            axes[0].scatter(time_axis[list(trace_events['baselinev_idx'])],
                            vtrace[list(trace_events['baselinev_idx'])],
                            color='green')
            axes[0].scatter(time_axis[list(trace_events['peakv_idx'])],
                            vtrace[list(trace_events['peakv_idx'])],
                            color='red')




# %% depolarizing events and action potentials - line plots of raw data


# plotting an individual event, optionally with measures and/or baselined and/or normalized
def plot_single_event(vtrace, sampling_period_inms,
                      axis_object, plot_startidx, plotwindow_inms=40,
                      eventmeasures_series=pd.Series(),
                      get_measures_type='raw', display_measures=False,
                      do_baselining=False, do_normalizing=False,
                      linecolor='blue', label=None):
    """ This function takes as inputs:
    - a vtrace as np.array (raw voltage by default)
    - the corresponding sampling period in ms
    - the starting index of the trace-bit to plot, and the total length of the plotting window in ms
    - the axis object onto which the trace is to be plotted.
    optional arguments:
    - line color and label are passed through to plot
    - use_measurestype = 'raw' - by default, raw-trace event-measures are used for plotting/baselining/normalizing
    - eventmeasures_series - pandas Series object containing all measures taken for this event
    - do_baselining and do_normalizing - if True, uses baselinev and amplitude measures from the eventmeasures_series (which therefore has to be present)
    - display_measures - if True, event measures are displayed in the plot as well. Doesn't work if baselining and/or normalizing are applied.
    """
    # creating the event-trace and corresponding time axis
    event_trace = vtrace[plot_startidx:plot_startidx + int(plotwindow_inms / sampling_period_inms)]
    time_axis = np.linspace(start=0, stop=plotwindow_inms, num=len(event_trace))

    # optional:
    # baselining
    if do_baselining and not eventmeasures_series.empty and get_measures_type == 'raw':
        baseline_value = eventmeasures_series['baselinev']
        event_trace = event_trace - baseline_value
    elif do_baselining and not eventmeasures_series.empty:
        baseline_value = eventmeasures_series['edtrace_baselinev']
        event_trace = event_trace - baseline_value

    # normalizing
    if do_normalizing and not eventmeasures_series.empty and get_measures_type == 'raw':
        normalize_value = eventmeasures_series['amplitude']
        event_trace = event_trace / normalize_value
    elif do_normalizing and not eventmeasures_series.empty:
        normalize_value = eventmeasures_series['edtrace_amplitude']
        event_trace = event_trace / normalize_value

    # plotting the line
    axis_object.plot(time_axis, event_trace,
                     color=linecolor, label=label)
    axis_object.set_xlabel('time (ms)')

    # optional: adding scatterpoints and/or horizontal lines to demark measures where relevant:
    if display_measures and not eventmeasures_series.empty:
        measures_dict = make_eventmeasures_dict_forplotting(eventmeasures_series,
                                                            get_measures_type)
        for key, valsdict in measures_dict.items():
            point = valsdict['idx']
            if point - plot_startidx < len(event_trace):
                if len(valsdict) == 2:
                    axis_object.scatter(time_axis[point - plot_startidx], event_trace[point - plot_startidx],
                                        color=valsdict['color'],
                                        label=key)

                if len(valsdict) == 3:
                    axis_object.hlines(y=event_trace[point - plot_startidx],
                                       xmin=time_axis[point - plot_startidx],
                                       xmax=time_axis[point - plot_startidx] + valsdict['duration'],
                                       color=valsdict['color'],
                                       label=(key + ' = ' + str(valsdict['duration']) + 'ms'))
        axis_object.legend()


# plotting all events of a rawdata_block, overlayed, using measures information
def plot_singleblock_events(rawdata_block, block_eventsmeasures,
                            getdepolarizingevents_settings,
                            timealignto_measure='peakv_idx',
                            colorby_measure='', color_lims=[],
                            prealignpoint_window_inms=5, total_plotwindow_inms=50,
                            axis_object = None,
                            **kwargs):

    # do not proceed unless event-measures data is provided
    if block_eventsmeasures.empty:
        print('missing event-measures data')
        return

    # optional: setting the color mapping
    if colorby_measure and len(color_lims) == 2:
        colormap, cm_normalizer = get_colors_forlineplots(colorby_measure, color_lims)
    elif colorby_measure:
        colormap, cm_normalizer = get_colors_forlineplots(colorby_measure, block_eventsmeasures)
        print('colorbar automatically generated from single-block data')

    # optional: create figure axes to plot onto
    if not axis_object:
        figure, axis = plt.subplots(1, 1, squeeze=True)
        if colorby_measure:
            figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer,cmap=colormap),
                            label=colorby_measure)
    else:
        axis = axis_object

    # getting the individual segments from the block
    segments_for_plotting_idcs = list(set(block_eventsmeasures['segment_idx']))
    for segment_idx in segments_for_plotting_idcs:
        segment_eventsmeasures = block_eventsmeasures.loc[block_eventsmeasures['segment_idx'] == segment_idx]
        vtrace_asanalogsignal = rawdata_block.segments[segment_idx].analogsignals[0]
        sampling_frequency = float(vtrace_asanalogsignal.sampling_rate)
        sampling_period_inms = float(vtrace_asanalogsignal.sampling_period) * 1000
        vtrace = np.squeeze(np.array(vtrace_asanalogsignal))

        # optional: getting the event-detect trace instead of the raw vtrace
        if 'get_measures_type' in kwargs.keys() and not kwargs['get_measures_type'] == 'raw':
            vtrace, _, _ = snafs.apply_filters_torawdata(vtrace,
                                                         getdepolarizingevents_settings['oscfilter_lpfreq'],
                                                         getdepolarizingevents_settings['noisefilter_hpfreq'],
                                                         sampling_frequency,
                                                         plot='off')

        # plotting the events of the segment
        for event_idx, eventmeasures in segment_eventsmeasures.iterrows():
            plot_startidx = (eventmeasures[timealignto_measure]
                             - int(prealignpoint_window_inms / sampling_period_inms))
            if colorby_measure:
                linecolor = colormap(cm_normalizer(eventmeasures[colorby_measure]))
                plot_single_event(vtrace, sampling_period_inms, axis,
                                  plot_startidx, total_plotwindow_inms,
                                  eventmeasures_series=eventmeasures,
                                  linecolor=linecolor,
                                  **kwargs)
            else:
                plot_single_event(vtrace, sampling_period_inms, axis,
                                  plot_startidx, total_plotwindow_inms,
                                  eventmeasures_series=eventmeasures,
                                  **kwargs)
            # print('event no.' + str(event_idx) + ' plotted')

    if not axis_object:
        return figure, axis


# plotting all events of a single voltage trace individually, displaying measures
def plot_singlesegment_events_individually_withmeasures(get_subthreshold_events,
                                                        block, block_events,
                                                        trace_idx, reading_notes,
                                                        plotwindow_inms=40,
                                                        prebaselinewindow_inms = 5):
    """ This function does the grunt work for the SingleNeuron.plot_individualdepolevents_withmeasures method.
    """
    # extracting the relevant vtrace, event-measures etc. and (re)creating event-detect trace
    block_name = block.file_origin
    vtrace = block.segments[trace_idx].analogsignals[0]
    trace_events = block_events.loc[block_events['segment_idx'] == trace_idx]
    sampling_frequency = float(vtrace.sampling_rate)
    sampling_period_inms = float(vtrace.sampling_period) * 1000
    vtrace = np.squeeze(np.array(vtrace))

    if get_subthreshold_events:
        # unless action potentials are called for, both the raw and the event-detect traces are plotted
        edtrace, _, _ = snafs.apply_filters_torawdata(vtrace,
                                                      oscfilter_lpfreq = reading_notes['oscfilter_lpfreq'],
                                                      noisefilter_hpfreq = reading_notes['noisefilter_hpfreq'],
                                                      sampling_frequency = sampling_frequency,
                                                      plot = 'off')
        # looping over each event for this vtrace
        for event_idx, event_measures in trace_events.iterrows():
            plot_startidx = event_measures['baselinev_idx'] - int(prebaselinewindow_inms
                                                                  / sampling_period_inms)
            # creating a figure, number matching the idx of the event as listed in the dataframe
            figure, axes = plt.subplots(1, 2, sharex='all', num=event_idx)
            plt.suptitle(block_name + ' segment' + str(trace_idx))

            plot_single_event(vtrace, sampling_period_inms, axes[0],
                              plot_startidx, plotwindow_inms=plotwindow_inms,
                              linecolor='blue',
                              eventmeasures_series=event_measures,
                              get_measures_type='raw',
                              display_measures=True)
            axes[0].set_ylabel('voltage (mV)')
            axes[0].set_title('raw voltage')

            plot_single_event(edtrace, sampling_period_inms, axes[1],
                              plot_startidx, plotwindow_inms=plotwindow_inms,
                              linecolor='black',
                              eventmeasures_series=event_measures,
                              get_measures_type='edtrace',
                              display_measures=True)
            axes[1].set_title('event-detect trace')

    else: # plotting action potentials
        for event_idx, event_measures in trace_events.iterrows():
            plot_startidx = event_measures['baselinev_idx'] - int(prebaselinewindow_inms
                                                                  / sampling_period_inms)
            # creating a figure, number matching the idx of the event as listed in the dataframe
            figure, axis = plt.subplots(1, 1, squeeze=True, num=event_idx)
            plt.suptitle(block_name + ' segment' + str(trace_idx))

            plot_single_event(vtrace, sampling_period_inms, axis,
                              plot_startidx, plotwindow_inms=plotwindow_inms,
                              linecolor='blue',
                              eventmeasures_series=event_measures,
                              get_measures_type='raw',
                              display_measures=True)
            axis.set_ylabel('voltage (mV)')
            axis.set_title('raw voltage')


# helper functions:
# getting colormap information
def get_colors_forlineplots(colorby_measure,data):
    colormap = mpl.cm.viridis
    if isinstance(data, list) and len(data) == 2:
        cm_normalizer = mpl.colors.Normalize(vmin=data[0],vmax=data[1])
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
    Measures are added only if their value is not <= 0 or nan.
    If measuretype is not "raw", values gotten from the event-detect trace will be returned.
    """
    # all events have a baseline-point and a peak-point, and it's the same in the raw and event-detect traces.
    measuresdict = {
        'baseline_v': {'idx': eventmeasures_series['baselinev_idx'],
                       'color': 'green'
                       },

        'peak_v': {'idx': eventmeasures_series['peakv_idx'],
                   'color': 'red'}
    }

    # getting parameters as measured from the raw voltage trace
    if measuretype == 'raw':
        if float(eventmeasures_series['rise_time']) > 0:
            measuresdict['rise_time'] = {
                'idx': eventmeasures_series['rt_start_idx'],
                'duration': float(eventmeasures_series['rise_time']),
                'color': 'red'
            }

        if float(eventmeasures_series['half_width']) > 0:
            measuresdict['half_width'] = {
                'idx': eventmeasures_series['hw_start_idx'],
                'duration': float(eventmeasures_series['half_width']),
                'color': 'green'
            }

        # measures that are specific to subthreshold depolarizing events
        if 'width_at10%amp' in eventmeasures_series.keys():
            if float(eventmeasures_series['width_at10%amp']) > 0:
                measuresdict['width'] = {
                    'idx': eventmeasures_series['rt_start_idx'] - 1,
                    'duration': float(eventmeasures_series['width_at10%amp']),
                    'color': 'black'
                }

        # measures that are specific to action potentials
        if 'thresholdv' in eventmeasures_series.keys():
            if float(eventmeasures_series['thresholdv']) > 0:
                measuresdict['threshold_v'] = {
                    'idx': eventmeasures_series['threshold_idx'],
                    'color': 'blue'
                }

            if float(eventmeasures_series['threshold_width']) > 0:
                measuresdict['threshold_width'] = {
                    'idx': eventmeasures_series['threshold_idx'],
                    'duration': float(eventmeasures_series['threshold_width']),
                    'color': 'black'
                }

            if not np.isnan(eventmeasures_series['ahp_min_idx']):
                measuresdict['ahp_min'] = {
                    'idx': int(eventmeasures_series['ahp_min_idx']),
                    'color': 'red'
                }

            if not np.isnan(eventmeasures_series['ahp_end_idx']):
                measuresdict['ahp_end'] = {
                    'idx': int(eventmeasures_series['ahp_end_idx']),
                    'color': 'green'
                }

            if eventmeasures_series['n_spikeshoulderpeaks'] > 0:
                shoulderpeaks_idcs_asstr = eventmeasures_series['spikeshoulderpeaks_idcs']
                # unless shoulderpeaks_idcs is an empty list (in the form of a string),
                # unpack the string into a list of indices and add each to the measuresdict
                if not shoulderpeaks_idcs_asstr == '[]':
                    idcs_asstr = shoulderpeaks_idcs_asstr.replace('[','')
                    idcs_asstr = idcs_asstr.replace(']','')
                    idcs_asstr = idcs_asstr.replace(',','')
                    [*idcs_asstrs] = idcs_asstr.split(' ')
                    for i, idx in enumerate(idcs_asstrs):
                        measuresdict['spikeshoulderpeak'+str(i)] = {
                            'idx': int(idx),
                            'color': 'red'
                        }


    # getting parameters as measured from the event-detect trace
    else:
        if float(eventmeasures_series['edtrace_rise_time']) > 0:
            measuresdict['rise_time'] = {
                'idx': eventmeasures_series['edtrace_rt_start_idx'],
                'duration': float(eventmeasures_series['edtrace_rise_time']),
                'color': 'red'
            }

        if float(eventmeasures_series['edtrace_half_width']) > 0:
            measuresdict['half_width'] = {
                'idx': eventmeasures_series['edtrace_hw_start_idx'],
                'duration': float(eventmeasures_series['edtrace_half_width']),
                'color': 'green'
            }

        if float(eventmeasures_series['edtrace_width_at10%amp']) > 0:
            measuresdict['width'] = {
                'idx': eventmeasures_series['edtrace_rt_start_idx'] - 1,
                'duration': float(eventmeasures_series['edtrace_width_at10%amp']),
                'color': 'black'
            }

    return measuresdict
