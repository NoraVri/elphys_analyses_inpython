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

from detecta import detect_peaks

# %% importing some data
cell20250217A1 = SingleNeuron('20250217A1')
cell20250217B2 = SingleNeuron('20250217B2')
cell20250217C1 = SingleNeuron('20250217C1')

recording_segment = cell20250217A1.blocks[3].segments[0].analogsignals[0].squeeze()






