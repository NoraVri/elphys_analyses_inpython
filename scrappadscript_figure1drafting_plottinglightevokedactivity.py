# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_data_Thy1 = SingleNeuron('20200708D')
neuron_data_RBP = SingleNeuron('20201125D')
neuron_data_midbrain = SingleNeuron('20210124B')

# %% Thy1 activations: 2 plots, high and low light intensity
# two files at different light intensities
# 30%
neuron_data_Thy1.plot_rawdatatraces_ttlaligned('0000',
                                               plotdvdt=False,
                                               do_baselining=False,
                                               colorby_measure='applied_current',
                                               color_lims=[-1000, 300],
                                               prettl_t_inms=0.5,
                                               postttl_t_inms=20,
                                               plotlims=[-100, 45],
                                              )
# inset:
neuron_data_Thy1.plot_rawdatatraces_ttlaligned('0000',
                                               plotdvdt=False,
                                               # do_baselining=False,
                                               colorby_measure='applied_current',
                                               color_lims=[-1000, 300],
                                               prettl_t_inms=0,
                                               postttl_t_inms=7,
                                               plotlims=[-0.5, 18],
                                              )
# 3% - except in sweep2 where 2%=no light on at all
neuron_data_Thy1.plot_rawdatatraces_ttlaligned('01',
                                               skip_vtraces_idcs=[1],
                                               plotdvdt=False,
                                               do_baselining=False,
                                               colorby_measure='applied_current',
                                               color_lims=[-1000, 300],
                                               prettl_t_inms=0.5,
                                               postttl_t_inms=20,
                                               plotlims=[-100, 45],
                                               )
# inset:
neuron_data_Thy1.plot_rawdatatraces_ttlaligned('01',
                                               skip_vtraces_idcs=[1],
                                               plotdvdt=False,
                                               # do_baselining=False,
                                               colorby_measure='applied_current',
                                               color_lims=[-1000, 300],
                                               prettl_t_inms=0,
                                               postttl_t_inms=7,
                                               plotlims=[-0.5, 18],
                                               )
# RBP activations
# Using light 01 and 2: light2 has more with APs (more +DC)
# skip_vtraces = list(np.arange(1,len(neuron_data_RBP.blocks[3].segments)/2)) \
#                + list(np.arange(len(neuron_data_RBP.blocks[3].segments)/2, len(neuron_data_RBP.blocks[3].segments), 2))
full_set = set(np.arange(0, len(neuron_data_RBP.blocks[3].segments)))
keep_set = {0, 1, 3, 4, 26, 27, 65, 66, 72, 73}
skip_vtraces = list((full_set - keep_set))
neuron_data_RBP.plot_rawdatatraces_ttlaligned('light_0001', 'light_0002',
                                              # skip_vtraces_block=['light_0001'],
                                              skip_vtraces_idcs=skip_vtraces,
                                              plotdvdt=False,
                                              do_baselining=False,
                                              colorby_measure='applied_current',
                                              color_lims=[-1000, 300],
                                              prettl_t_inms=0.5,
                                              postttl_t_inms=20,
                                              plotlims=[-100, 45],
                                              )
# inset:
neuron_data_RBP.plot_rawdatatraces_ttlaligned('light_0001', 'light_0002',
                                              # skip_vtraces_block=['light_0001'],
                                              skip_vtraces_idcs=skip_vtraces,
                                              plotdvdt=False,
                                              # do_baselining=False,
                                              colorby_measure='applied_current',
                                              color_lims=[-1000, 300],
                                              prettl_t_inms=1,
                                              postttl_t_inms=7,
                                               plotlims=[-0.5, 18],
                                              )
# midbrain activations
skip_vtraces = list(np.arange(1, 18, 2)) \
               + list(np.arange(18, 33)) \
               + list(np.arange(34, 37)) \
               + list(np.arange(38, 40))
neuron_data_midbrain.plot_rawdatatraces_ttlaligned('light_0002',
                                                   skip_vtraces_idcs=skip_vtraces,
                                                   plotdvdt=False,
                                                   do_baselining=False,
                                                   colorby_measure='applied_current',
                                                   color_lims=[-1000, 300],
                                                   prettl_t_inms=0.5,
                                                   postttl_t_inms=20,
                                                   plotlims=[-100, 45],
                                                )
# inset:
neuron_data_midbrain.plot_rawdatatraces_ttlaligned('light_0002',
                                                   skip_vtraces_idcs=skip_vtraces,
                                                   plotdvdt=False,
                                                   # do_baselining=False,
                                                   colorby_measure='applied_current',
                                                   color_lims=[-1000, 300],
                                                   prettl_t_inms=1,
                                                   postttl_t_inms=7,
                                                   plotlims=[-0.5, 18],
                                                )

