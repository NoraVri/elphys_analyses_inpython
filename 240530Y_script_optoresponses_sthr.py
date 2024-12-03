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

neuron_name = '240530Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a pretty neat recording at first sight: held with ~-200pA to keep -70mV.
# However, recording also looks unstable: capacitance artefacts changing gradually during the first recording block,
# then stabilizing for a bit before changing again suddenly during second recording block; then APcurrents start to
# appear as rebound-responses to voltage step. Clamp clearly bad at this point, reflected in voltage measurement.








