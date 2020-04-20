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
# %% general raw-data plotting
def plot_block(block):
    """ takes a block and plots all analogsignals, one subplot per channel_index.
    """
    #getting the time axis all traces have in common
    time_axis = block.channel_indexes[0].analogsignals[0].times
    time_axis = time_axis.rescale('ms')
    #making one subplot per active recording channel
    nsubplots = len(block.channel_indexes)
    figure,axes = plt.subplots(nrows=nsubplots,ncols=1,sharex=True)
    for i in range(nsubplots):
        traces = np.transpose(np.squeeze(np.array(list(iter(
                                block.channel_indexes[i].analogsignals)))))
        traces_unit = block.channel_indexes[i].analogsignals[0].units
        axes[i].plot(time_axis,traces)
        axes[i].set_xlabel('time (ms)')
        axes[i].set_ylabel(str(traces_unit))


# %% depolarizing events
