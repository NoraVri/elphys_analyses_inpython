# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron1_data = SingleNeuron('20220802A')
neuron2_data = SingleNeuron('20220802B')
neuron3_data = SingleNeuron('20220802C')

# %%
neuron1_blocks = neuron1_data.get_blocknames(printing='off')
neuron1_stimblocks = [block for block in neuron1_blocks if 'Stim' in block]
neuron1_data.plot_rawdatatraces_ttlaligned(*neuron1_stimblocks)

neuron2_blocks = neuron2_data.get_blocknames()
neuron2_stimblocks = [block for block in neuron2_blocks if 'Stim' in block]

neuron3_blocks = neuron3_data.get_blocknames()
neuron3_stimblocks = [block for block in neuron3_blocks if 'Stim' in block]



