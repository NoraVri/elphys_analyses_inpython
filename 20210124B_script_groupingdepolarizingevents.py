# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124B'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %%
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000',
                                                plt_title='low light intensity',
    # newplot_per_ttlduration=True,
    postttl_t_inms=20
                                                )

singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001',
                                                plt_title='low light intensity',
    # newplot_per_ttlduration=True,
    postttl_t_inms=20
                                                )
# %%
skip_vtraces = list(np.arange(18,33)) + list(np.arange(37, 40))
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0002',
                                                skip_vtraces_idcs=skip_vtraces,
                                                plt_title='100% light intensity',
    # newplot_per_ttlduration=True,
    postttl_t_inms=20
                                                )
