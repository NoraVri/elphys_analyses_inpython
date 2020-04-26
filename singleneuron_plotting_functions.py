# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:30:10 2020

@author: neert
"""
# %% imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import singleneuron_analyses_functions as snafs
# %% general raw-data plotting
def plot_block(block):
    """ takes a block and plots all analogsignals (voltage/current/aux (if applicable)),
    one subplot per channel_index.
    """
    #getting the time axis all traces have in common
    time_axis = block.channel_indexes[0].analogsignals[0].times
    time_axis = time_axis.rescale('ms')
    #making one subplot per active recording channel
    nsubplots = len(block.channel_indexes)
    figure,axes = plt.subplots(nrows=nsubplots,ncols=1,sharex='all')
    for i in range(nsubplots):
        traces = np.transpose(np.squeeze(np.array(list(iter(
                                block.channel_indexes[i].analogsignals)))))
        traces_unit = block.channel_indexes[i].analogsignals[0].units
        axes[i].plot(time_axis,traces)
        axes[i].set_xlabel('time (ms)')
        axes[i].set_ylabel(str(traces_unit))



# %% depolarizing events




def plot_singlesegment_individualdepolevents_withmeasures(block, block_events,
                                                          trace_idx, reading_notes,
                                                          plotwindow_inms=40,
                                                          baselinewindow_inms = 5):
    """ This function does the grunt work for the SingleNeuron.plot_individualdepolevents_withmeasures method.
    """
    # extracting the relevant vtrace, event-measures etc. and (re)creating event-detect trace
    block_name = block.file_origin
    vtrace = block.segments[trace_idx].analogsignals[0]
    trace_events = block_events.loc[block_events['segment_idx'] == trace_idx]
    sampling_frequency = float(vtrace.sampling_rate)
    sampling_period_inms = float(vtrace.sampling_period) * 1000
    vtrace = np.squeeze(np.array(vtrace))
    edtrace, _, _ = snafs.apply_filters_torawdata(vtrace,
                                                  oscfilter_lpfreq = reading_notes['oscfilter_lpfreq'],
                                                  noisefilter_hpfreq = reading_notes['noisefilter_hpfreq'],
                                                  sampling_frequency = sampling_frequency,
                                                  plot = 'off')
    # plotting each event for this vtrace
    for event_idx, event_measures in trace_events.iterrows():
        plot_startidx = event_measures['baselinev_idx'] - int(baselinewindow_inms /
                                                              sampling_period_inms)

        figure, axes = plt.subplots(1, 2, sharex='all', num=event_idx) #event_idx is the idx of the entry of this event in the depolarizingevents_dataframe
        plt.suptitle(block_name + ' segment' + str(trace_idx))

        plot_single_event(vtrace, sampling_period_inms, axes[0],
                                plot_startidx, plotwindow_inms=plotwindow_inms,
                                linecolor='blue',
                                eventmeasures_series=event_measures,
                                eventmeasures_type='raw')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title('raw voltage')

        plot_single_event(edtrace, sampling_period_inms, axes[1],
                                plot_startidx, plotwindow_inms=plotwindow_inms,
                                linecolor='black',
                                eventmeasures_series=event_measures,
                                eventmeasures_type='edtrace')
        axes[1].set_title('event-detect trace')



def plot_single_event(vtrace, sampling_period_inms, ax,
                      plot_startidx, plotwindow_inms = 40,
                      linecolor = 'blue',
                      label = None,
                      eventmeasures_series = pd.Series(), eventmeasures_type = 'raw',
                      do_baselining = False, do_normalizing = False):
    """ This function takes a full vtrace and its sampling_period,
    a figure-axis object and information related to how to display the plot
    (the color and label to be associated with the plotted line, and the
    startidx and length (in ms) of the window to be plotted).
    It uses the axis-object to plot the snippet of vtrace demarked by the window
    on a time axis from 0 to window_end (in ms).
    If given a pd.Series containing depolarizing-event measures, it will also display those.
    Baselining and normalizing should only be used on raw data (it standard reads rawdata value for baselinev),
    and normalizing will only happen on baselined traces.
    """
    # creating the time axis
    time_axis = np.arange(0, plotwindow_inms, sampling_period_inms)
    if plot_startidx + int(plotwindow_inms / sampling_period_inms) > len(vtrace):
        time_axis = time_axis[0:len(vtrace) - plot_startidx]

    # getting the event from vtrace
    event_trace = vtrace[plot_startidx:plot_startidx + int(plotwindow_inms / sampling_period_inms)]

    # optional: baselining
    if do_baselining and not eventmeasures_series.empty:
        baseline_value = eventmeasures_series['baselinev']
        event_trace = event_trace - baseline_value
        # normalizing as well
        if do_normalizing:
            normalize_value = eventmeasures_series['amplitude']
            event_trace = event_trace / normalize_value

    # plotting the line
    ax.plot(time_axis,
            event_trace,
            color = linecolor,
            label = label)
    ax.set_xlabel('time (ms)')

    # optional: adding scatterpoints and/or horizontal lines to demark measures where relevant:
    if not eventmeasures_series.empty and not do_baselining: # don't want to add measures if traces are baselined
        measures_dict = make_measuresdict_for_subthresholdevent(eventmeasures_series,
                                                                eventmeasures_type)
        for key, valsdict in measures_dict.items():
            point = valsdict['idx']

            if len(valsdict) == 2:
                ax.scatter(time_axis[point - plot_startidx],
                           vtrace[point],
                           color = valsdict['color'],
                           label = key)

            if len(valsdict) == 3:
                ax.hlines(y = vtrace[point],
                          xmin = time_axis[point - plot_startidx],
                          xmax = time_axis[point - plot_startidx] + \
                                            valsdict['duration'],
                          color = valsdict['color'],
                          label = key + ' = ' + str(valsdict['duration']) + 'ms')
        ax.legend()



def make_measuresdict_for_subthresholdevent(eventmeasures_series,
                                            measuretype = 'raw'):
    """ This function takes a pd.Series object containing the measures for a single event,
    and returns them in a dictionary along with line/point color information for use in
    the plot_single_event function.
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

    if measuretype == 'raw': #other measures are added in only if their value is not <0 or nan
        if float(eventmeasures_series['rise-time']) > 0:
            measuresdict['rise-time'] = {
                'idx' : eventmeasures_series['rt_start_idx'],
                'duration' : float(eventmeasures_series['rise-time']),
                'color' : 'red'
            }

        if float(eventmeasures_series['half-width']) > 0:
            measuresdict['half-width'] = {
                'idx' : eventmeasures_series['hw_start_idx'],
                'duration' : float(eventmeasures_series['half-width']),
                'color' : 'green'
            }

        if float(eventmeasures_series['width_at10%amp']) > 0:
            measuresdict['width'] = {
                'idx' : eventmeasures_series['rt_start_idx'] - 1,
                'duration' : float(eventmeasures_series['width_at10%amp']),
                'color' : 'black'
            }

    else:
        if float(eventmeasures_series['edtrace_rise-time']) > 0:
            measuresdict['rise-time'] = {
                'idx' : eventmeasures_series['edtrace_rt_start_idx'],
                'duration' : float(eventmeasures_series['edtrace_rise-time']),
                'color' : 'red'
            }

        if float(eventmeasures_series['edtrace_half-width']) > 0:
            measuresdict['half-width'] = {
                'idx' : eventmeasures_series['edtrace_hw_start_idx'],
                'duration' : float(eventmeasures_series['edtrace_half-width']),
                'color' : 'green'
            }

        if float(eventmeasures_series['edtrace_width_at10%amp']) > 0:
            measuresdict['width'] = {
                'idx' : eventmeasures_series['edtrace_rt_start_idx'] - 1,
                'duration' : float(eventmeasures_series['edtrace_width_at10%amp']),
                'color' : 'black'
            }
    return measuresdict