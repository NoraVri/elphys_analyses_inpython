from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
from scrappadscript_evokedsynapticexcitation_plotting import plot2

neuron_data_MDJevoked = SingleNeuron('20210113G')
neuron_data_RBPevoked = SingleNeuron('20201125D')
neuron_data_Thy1evoked = SingleNeuron('20190527A')
# %%
plot2(neuron_data_RBPevoked, [3, 4,], baseline_lims=[-80, -45], skip_n_vtraces=3)

plot2(neuron_data_MDJevoked, [8], baseline_lims=[-80, -45])


# %%




