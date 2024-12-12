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

neuron_name = '240626Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# BAD TELEGRAPHS: both primary and secondary are recorded as having units of pA.
# Cell held with ~-1nA to keep -70mV (-1400pA), but holding quite variable especially during the first recording block
# (the only one without drug). Holding current then stabilizes and decreases somewhat; clearly getting quite a lot of
# spontaneously occurring activity at this point, too.