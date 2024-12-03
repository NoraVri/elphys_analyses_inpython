# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

neuron_name = '240626X'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# BAD TELEGRAPHS: both primary and secondary are recorded as having units of pA.
# Otherwise, looks like a pretty nice recording: cell held with ~-200pA to keep -70mV (-1400pA); there are some
# spontaneous depolarizations going on but they're relatively small.
# Does look like optostim response amplitude is highly variable.