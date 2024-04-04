# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %% in this script:
# generating a data gallery of SNr neurons recorded so far towards supplement grant proposal.
# workflow for each neuron:
# 1. import data and apply clean-ups if necessary (removing parts of recording where neuron is getting broken into or no longer healthy/alive)
# 2. plot some traces showing representative behavior


# %%
neuron_name = '20240327D'
singleneuron_data = SingleNeuron(neuron_name)
# no drugs applied
# spont.activity, longPulses and optoStim
# naked eye sees no light response
# neuron is pretty steady about maintaining baselineV ~-50mV; otherwise not very alive though (no spont. spikes)

# plotting long pulses:
singleneuron_data.plot_rawdatablocks('longPulses', time_axis_unit='s')

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned(plotdvdt=False)


# %%
neuron_name = '20240327C'
singleneuron_data = SingleNeuron(neuron_name)
# sulpiride applied for about half of recordings
# spont.activity, longPulses and optoStim
# neuron has steady baselineV ~-55mV at first, depolarized more with drug application
# my naked eye sees lots of variance in response amp, but no relationship between baselineV and response amp (i.e., driving force of response does not seem to increase with hyperpolarization)
# smallest optoStim response ~7mV depolarization, largest ~25mV; may be on average a little smaller with drug

# plotting long pulses - without drug applied:
singleneuron_data.plot_rawdatablocks('longPulses_0', time_axis_unit='s')
# plotting long pulses - with drug applied:
singleneuron_data.plot_rawdatablocks('longPulses_with', time_axis_unit='s')


# plotting opto response - without drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_0', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100)
# better view on subthreshold responses:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_0', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                color_lims=[-100, -80])

# plotting opto response - with drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_with', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                plt_title='with drug')
# better view on subthreshold responses:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_with', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                color_lims=[-100, -80],
                                                plt_title='with drug')


# %%
# neuron_name = '20240327B'
# singleneuron_data = SingleNeuron(neuron_name)
# not actually a good recording - looks like half-broken-in at first, then dying/dead

# %%
neuron_name = '20240327A'
singleneuron_data = SingleNeuron(neuron_name)
# sulpiride applied and washed out again
# spont.activity, longPulses and optoStim
# neuron looks a little unsteady at first, then settles in to baselineV ~-65mV and stays steady throughout recordings
# spont.activity looks distinctly different to me between drug and no drug conditions - with drug there seem to be more and larger EPSPs.
# response to opto stim. may have gotten up to 50% larger after drug application, or not changed at all - gonna have to do statistics on that

# plotting long pulses - without drug applied:
singleneuron_data.plot_rawdatablocks('longPulses_0', time_axis_unit='s')
# plotting long pulses - with drug applied:
singleneuron_data.plot_rawdatablocks('longPulses_withSulpiride_0', time_axis_unit='s')
# plotting long pulses - with drug washout:
singleneuron_data.plot_rawdatablocks('longPulses_withSulpirideWashout', time_axis_unit='s')


# plotting opto response - without drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_0', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                plt_title='without drug')

# plotting opto response - with drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_withSulpiride_', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                plt_title='with drug')

# plotting opto response - with drug washout:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_withSulpirideWashout', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                plt_title='drug washout')

# plotting again, focus on subthreshold responses
# plotting opto response - without drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_0', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100, color_lims=[-100, -70],
                                                plt_title='without drug')
# plotting opto response - with drug applied:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_withSulpiride_', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,color_lims=[-100, -70],
                                                plt_title='with drug')
# plotting opto response - with drug washout:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_withSulpirideWashout', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,color_lims=[-100, -70],
                                                plt_title='drug washout')


# %%
neuron_name = '20240311F'
singleneuron_data = SingleNeuron(neuron_name)
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# pretty stable recording in terms of baselineV, but AP peakV decreasing steadily and geting wobbly later on (probably some electrode drift effect)
# naked eye says there isn't really a response to light

# plotting long pulses:
singleneuron_data.plot_rawdatablocks('longPulses', time_axis_unit='s')

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 100, postttl_t_inms=500,
                                                color_lims=[-85, -40]
                                                )


# %%
# neuron_name = '20240311E'
# singleneuron_data = SingleNeuron(neuron_name)
# no real data here, just a failed seal formation and break-in to a mostly dead neuron

# %%
neuron_name = '20240311D'
singleneuron_data = SingleNeuron(neuron_name)
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# pretty stable in terms of baselineV, ~-60mV throughout
# no spontaneous spiking (or any spiking at all)
# does not appear to be responding to the light at all

# plotting long pulses:
singleneuron_data.plot_rawdatablocks('longPulses', time_axis_unit='s')

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 100, postttl_t_inms=500,
                                                newplot_per_ttlduration=True,
                                                color_lims=[-110, -30]
                                                )


# %%
neuron_name = '20240311C'
singleneuron_data = SingleNeuron(neuron_name)
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# seems pretty stable in terms of baselineV - AHP trough going down to -55mV early on, decreasing to -53mV later on in recordings
# spiking spontaneously throughout recordings, AHP peakV +20mV at first going down to just under 0mV towards the end of recordings
# pretty pronounced depolarizing response to light (non-responsive trials are due to light faltering)

# plotting long pulses:
singleneuron_data.plot_rawdatablocks('longPulses', time_axis_unit='s')

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 100, postttl_t_inms=500,
                                                # color_lims=[-85, -40]
                                                )


# %%
neuron_name = '20240311B'
singleneuron_data = SingleNeuron(neuron_name)
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# pretty steady at first, but markedly deteriorating in terms of baselineV and AP peakV later on
# spiking spontaneously throughout recordings nonetheless
# no response to light

# plotting long pulses:
singleneuron_data.plot_rawdatablocks('longPulses', time_axis_unit='s')

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 100, postttl_t_inms=500,
                                                # color_lims=[-85, -40]
                                                )


# %%
neuron_name = '20240311A'
singleneuron_data = SingleNeuron(neuron_name)


singleneuron_data.plot_rawdatablocks()
singleneuron_data.get_blocknames()
# %%
neuron_name = '20240306E'
singleneuron_data = SingleNeuron(neuron_name)


# %%
neuron_name = '20240306D'
singleneuron_data = SingleNeuron(neuron_name)


# %%
neuron_name = '20240306C'
singleneuron_data = SingleNeuron(neuron_name)


# %%
neuron_name = '20240306B'
singleneuron_data = SingleNeuron(neuron_name)


# %%
neuron_name = '20240306A'
singleneuron_data = SingleNeuron(neuron_name)



# %%
neuron_name = '20240304B'
singleneuron_data = SingleNeuron(neuron_name)


# %%
neuron_name = '20240304A'
singleneuron_data = SingleNeuron(neuron_name)






# %%
singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)