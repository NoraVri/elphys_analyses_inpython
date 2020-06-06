# %% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantities as pq

from singleneuron_class import SingleNeuron

# %% importing singleneuron data
# singleneuron_data = SingleNeuron('20190529B')
# singleneuron_data = SingleNeuron('20190529D')
singleneuron_data = SingleNeuron('20190812A')
# singleneuron_data = SingleNeuron('20200106C')
# singleneuron_data = SingleNeuron('20200310G')

# %%
allfiles_names = singleneuron_data.get_blocknames(printing='off')
longpulses_filesnames = [filename for filename in allfiles_names if 'IV' in filename]
