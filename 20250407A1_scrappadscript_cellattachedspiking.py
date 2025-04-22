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

neuron_name = '20250407A1'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_spikes_fromcellattachedrecording()


