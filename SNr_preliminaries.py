# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %% in this script:
# generating a data gallery of SNr neurons recorded so far towards supplement grant proposal.
# workflow for each neuron:
# 1. import data, look at it all and apply clean-ups if necessary (removing parts of recording where neuron is getting broken into or no longer healthy/alive)
# 2. plot some traces showing representative behavior (specifically subthreshold responses to optoStim)
# 3. get and save the auto-generated ttlon_measures table for nice recordings with light responses


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
# sulpiride applied for about half of recordings
# spont.activity, longPulses and optoStim
# neuron has steady baselineV ~-55mV at first, depolarized more with drug application
# my naked eye sees lots of variance in response amp, but no relationship between baselineV and response amp (i.e., driving force of response does not seem to increase with hyperpolarization)
# smallest optoStim response ~7mV depolarization, largest ~25mV; may be on average a little smaller with drug
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

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
# making some better comparison plots
nodrugfigure, ndaxes = singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_0', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                color_lims=[-95, -50],
                                                maxamp_for_plotting=50,
                                                )
yesdrugfigure, daxes = singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim_with', plotdvdt=False,
                                                prettl_t_inms = 10, postttl_t_inms=100,
                                                color_lims=[-95, -50],
                                                maxamp_for_plotting=50,
                                                plt_title='with drug',
                                                )


# %%
# neuron_name = '20240327B'
# singleneuron_data = SingleNeuron(neuron_name)
# not actually a good recording - looks like half-broken-in at first, then dying/dead


# %%
neuron_name = '20240327A'
# sulpiride applied and washed out again
# spont.activity, longPulses and optoStim
# neuron looks a little unsteady at first, then settles in to baselineV ~-65mV and stays steady throughout recordings
# spont.activity looks distinctly different to me between drug and no drug conditions - with drug there seem to be more and larger EPSPs.
# response to opto stim. may have gotten up to 50% larger after drug application, or not changed at all - gonna have to do statistics on that
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

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
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# seems pretty stable in terms of baselineV - AHP trough going down to -55mV early on, decreasing to -53mV later on in recordings
# spiking spontaneously throughout recordings, AHP peakV +20mV at first going down to just under 0mV towards the end of recordings
# pretty pronounced depolarizing response to light (non-responsive trials are due to light faltering)
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

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
# no drug applied
# spont.activity (also some cell-attached) and optoStim  - cell-attached APs look weird, occasionally there's a giant one with huge AHP
# not the happiest neuron - was spiking like mad during seal formation, but once broken in cell needs -DC to keep baselineV <-30mV
# strong response to light whenever it's on, response amplitude relative to baselineV looks in line with classic synapse
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 25, postttl_t_inms=100,
                                                newplot_per_ttlduration=True,
                                                color_lims=[-90, -50]
                                                )


# %%
# neuron_name = '20240306E'
# singleneuron_data = SingleNeuron(neuron_name)
# no real data in there, just a break-in to a dead cell


# %%
neuron_name = '20240306D'
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# excellent recording: spiking spontaneously throughout with APs going between ~-60 and +20mV with little variation
# super strong response to light, eliciting APs even when cell is hyperpolarized to -90mV
# response amplitude relative to baselineV looks in line with classic synaptic response
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 25, postttl_t_inms=100,
                                                newplot_per_ttlduration=True,
                                                color_lims=[-90, -55]
                                                )


# %%
neuron_name = '20240306C'
# no drug applied
# spont.activity and optoStim
# not a good recording, looks like it never quite broke in properly: APs are very degenerate and apparent resistance at the pipette tips looks to have stayed ~1/2GOhm
# does clearly respond to optoStim though
singleneuron_data = SingleNeuron(neuron_name)

# plotting opto response:
singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 25, postttl_t_inms=100,
                                                )


# %%
neuron_name = '20240306B'
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# quite nice recording on the whole, although neuron is spiking spontaneously at first and then suddenly decides to stop doing that
# clear depolarizing response to optoStim, although it's not very big
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 25, postttl_t_inms=100,
                                                )


# %%
neuron_name = '20240306A'
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim
# not exactly an excellent recording - neuron needs holding with -0.5 - -1.5nA DC to keep a functional baselineV; does a bunch of spont. spiking nonetheless though
# clear spiking response to optoStim - still evoking AP when holding baselineV at -95mV
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

singleneuron_data.plot_rawdatatraces_ttlaligned('optoStim', plotdvdt=False,
                                                prettl_t_inms = 25, postttl_t_inms=100,
                                                color_lims = [-95, -50]
                                                )


# %%
neuron_name = '20240304B'
# no drug applied
# cell-attached recording; spont.activity and optoStim
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatatraces_ttlaligned('Stim', plotdvdt=False,
                                                newplot_per_block=True,
                                                prettl_t_inms = 50, postttl_t_inms=100,
                                                )

# %%
neuron_name = '20240304A'
# no drug applied
# spont.activity, longPulses, shortPulses and optoStim (also paired pulses - none with subthreshold responses recorded though)
# very long recording: ~7.5hrs, with AP peakV deteriorating from ~+20 to ~+5mV (and no other clear signs of recording deterioration)
# my naked eye sees clear variations in spike rate occurring spontaneously when looking at minutes-long timeranges
# nothing too useful in optoStim data - almost all supra threshold responses
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.write_results()

# notes on light stimulation: intensity set to 50% throughout
# three kinds of optoStim files for this neuron:
# optoStim_0 - 'regular' single-pulse stim, illumination field size varying, duration varying - cell mostly fires off a bunch of APs in response to stim., needs hyperpolarizing to -90mV to get subthreshold response
# optoStim_twoPulses - paired pulses, 10 sweeps/block with increasing interval between pulses - unfortunately nothing very useful there, did not get subthreshold response
# optoStim_STN - tried moving so that illumination would hit STN directly, but that's where cell started dying.

# also, the very first block with optoStim has some kind of very weird noise in it that seems to break my plotting code.
# getting subsets of blocks to plot:
blocknames_list = singleneuron_data.get_blocknames(printing='off')
optoblocks_list = [block for block in blocknames_list if 'Stim' in block]
optoStim_list = [block for block in optoblocks_list if 'Stim_00' in block][1:]
optoStim_STN_list = [block for block in optoblocks_list if 'STN' in block]
optoStim_paired_list = [block for block in optoblocks_list if 'twoPulses' in block]

singleneuron_data.plot_rawdatatraces_ttlaligned(*optoStim_list, plotdvdt=False,
                                                newplot_per_block=True,
                                                prettl_t_inms = 50, postttl_t_inms=100,
                                                )
# clear excitatory response to light

singleneuron_data.plot_rawdatatraces_ttlaligned(*optoStim_paired_list, plotdvdt=False,
                                                newplot_per_ttlduration=True,
                                                prettl_t_inms = 50, postttl_t_inms=100,
                                                )
# not great plots, not even sure how my code is handling two pulses atm...

singleneuron_data.plot_rawdatatraces_ttlaligned(*optoStim_STN_list, plotdvdt=False,
                                                # newplot_per_ttlduration=True,
                                                prettl_t_inms = 50, postttl_t_inms=100,
                                                )
# nothing really interesting to be seen in there, cell is deteriorating rapidly at this point

