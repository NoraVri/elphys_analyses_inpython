# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import singleneuron_plotting_functions as plots

interesting_neurons = ['20190527A', '20201125D', '20200708F',
                        '20210113C', '20210113G', '20210113H', '20210124A', '20210203B']

example_neurons = ['20190527A', '20210113C', '20201125D']
for neuron in example_neurons: #interesting_neurons:
    neuron_data = SingleNeuron(neuron)
    des_df = neuron_data.depolarizing_events
    neat_spont_aps = (des_df.event_label == 'actionpotential') & ~des_df.applied_ttlpulse & des_df.neat_event
    # show APs at full scale
    # axis, dvdt_axis, ddvdt_axis = \
    # neuron_data.plot_depolevents(neat_spont_aps,
    #                              prealignpoint_window_inms=3,
    #                              plotwindow_inms=8,
    #                              colorby_measure='baselinev',
    #                              plot_ddvdt=True,
    #                              # display_measures=True,
    #                              )
    # axis.set_ylim([-5, 100])
    # dvdt_axis.set_xlim([-5, 100])
    # dvdt_axis.set_ylim([-4.1, 15])
    # ddvdt_axis.set_xlim([-5, 100])
    # ddvdt_axis.set_ylim([-4, 4])

    # zoom-in on initial rising phase
    axis, dvdt_axis, ddvdt_axis = \
        neuron_data.plot_depolevents(neat_spont_aps,
                                     prealignpoint_window_inms=3,
                                     plotwindow_inms=2.5,
                                     colorby_measure='baselinev',
                                     plot_ddvdt=True,
                                     display_measures=True,
                                     )
    axis.set_xlim([0, 2.5])
    axis.set_ylim([-1, 15])
    dvdt_axis.set_xlim([-1, 15])
    dvdt_axis.set_ylim([-0.1, 2.5])
    ddvdt_axis.set_xlim([-1, 15])
    ddvdt_axis.set_ylim([-0.1, 0.8])


