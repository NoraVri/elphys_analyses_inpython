# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:30:10 2020

@author: neert
"""
# %% imports
from neo import io
#from neo.core import Block, Segment, ChannelIndex
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# %% general raw-data plotting
def plot_block(block):
    """ takes a block and plots all analogsignals, one subplot per channel_index.
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

def plot_single_event(vtrace, sampling_period_inms, ax,
                      plot_startidx, plotwindow_inms = 40,
                      linecolor = 'blue',
                      label = None,
                      measures_dict = None):

    time_axis = np.arange(0, plotwindow_inms, sampling_period_inms)

    ax.plot(time_axis,
            vtrace[plot_startidx:plot_startidx + int(plotwindow_inms / sampling_period_inms)],
            color = linecolor,
            label = label)
    ax.set_xlabel('time (ms)')

    if measures_dict:

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



def make_measuresdict_for_subthresholdevent(event_measuresrow,
                                            measuretype = 'raw'):

    measuresdict = {
        'baseline_v': {'idx': event_measuresrow['baselinev_idx'],
                       'color': 'green'
                       },
        'peak_v': {'idx': event_measuresrow['peakv_idx'],
                   'color': 'red'}
    }


    if measuretype == 'raw':

        if float(event_measuresrow['rise-time']) > 0:
            measuresdict['rise-time'] = {
                'idx' : event_measuresrow['rt_start_idx'],
                'duration' : float(event_measuresrow['rise-time']),
                'color' : 'red'}

        if float(event_measuresrow['half-width']) > 0:
            measuresdict['half-width'] = {
                'idx' : event_measuresrow['hw_start_idx'],
                'duration' : float(event_measuresrow['half-width']),
                'color' : 'green'
            }

        if float(event_measuresrow['width_at10%amp']) > 0:
            measuresdict['width'] = {
                'idx' : event_measuresrow['rt_start_idx'] + 2,
                'duration' : float(event_measuresrow['width_at10%amp']),
                'color' : 'black'
            }

    else:

        if float(event_measuresrow['edtrace_rise-time']) > 0:
            measuresdict['rise-time'] = {
                'idx' : event_measuresrow['edtrace_rt_start_idx'],
                'duration' : float(event_measuresrow['edtrace_rise-time']),
                'color' : 'red'}

        if float(event_measuresrow['edtrace_half-width']) > 0:
            measuresdict['half-width'] = {
                'idx' : event_measuresrow['edtrace_hw_start_idx'],
                'duration' : float(event_measuresrow['edtrace_half-width']),
                'color' : 'green'
            }

        if float(event_measuresrow['edtrace_width_at10%amp']) > 0:
            measuresdict['width'] = {
                'idx' : event_measuresrow['edtrace_rt_start_idx'] + 2,
                'duration' : float(event_measuresrow['edtrace_width_at10%amp']),
                'color' : 'black'
            }

    return measuresdict