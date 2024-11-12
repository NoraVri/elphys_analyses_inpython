# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
from singleneuron_plotting_functions import plot_ttlaligned
import os

path = "C:\\Users\\wgo5481\\OneDrive - Northwestern University\\Documents\\pCLAMP - copy\\Data_recordedByDeNard"
neuron_recordings = os.listdir(path)

for neuron in neuron_recordings:
    neuron_data = SingleNeuron(neuron)
    neuron_data.plot_ttlaligned()

