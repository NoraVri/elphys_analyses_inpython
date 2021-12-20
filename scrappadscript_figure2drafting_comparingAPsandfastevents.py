# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_data_Thy1 = SingleNeuron('20200708D')  # example shown in Figure1
neuron_data_RBP = SingleNeuron('20201125D')  # example shown in Figure1
neuron_data_midbrain = SingleNeuron('20210124B')  # example shown in Figure1

# %%
# RBP: light-evoked vs. spontaneous APs
# let's see them as picked up by the getdepolarizingevents-algorithm:
des_df_rbp = neuron_data_RBP.depolarizing_events
aps_all = des_df_rbp.event_label == 'actionpotential'
aps_spont = (aps_all & ~(des_df_rbp.applied_ttlpulse))
aps_evoked = (aps_all & (des_df_rbp.applied_ttlpulse))
axis_spont, dvdt_axis_spont = neuron_data_RBP.plot_depolevents(aps_spont,
                                 colorby_measure='baselinev')
# save the figure, then re-set axes limits for inset:
axis_spont.set_xlim([0, 5])
axis_spont.set_ylim([0, 15])
dvdt_axis_spont.set_xlim([0, 15])  # should be the same as axis_spont ylims
dvdt_axis_spont.set_ylim([0, 1.5])

axis_evoked, dvdt_axis_evoked = neuron_data_RBP.plot_depolevents(aps_evoked,
                                 colorby_measure='baselinev')
# save the figure, then re-set axes limits for inset:
axis_evoked.set_xlim([0, 5])
axis_evoked.set_ylim([0, 15])
dvdt_axis_evoked.set_xlim([0, 15])  # should be the same as axis_spont ylims
dvdt_axis_evoked.set_ylim([0, 1.5])

# spont. fastevents:
events = (des_df_rbp.event_label.isna() & ~des_df_rbp.applied_ttlpulse)
neuron_data_RBP.plot_depolevents(events,
                                 colorby_measure='baselinev')

# %%
# midbrain input: light-evoked vs. spontaneous APs
des_df_midbrain = neuron_data_midbrain.depolarizing_events
aps_all = des_df_midbrain.event_label == 'actionpotential'
aps_spont = (aps_all & ~(des_df_midbrain.applied_ttlpulse))  # this neuron has only APs driven by big +DC
aps_evoked = (aps_all & (des_df_midbrain.applied_ttlpulse))
# axis_spont, dvdt_axis_spont = neuron_data_midbrain.plot_depolevents(aps_spont,
#                                  colorby_measure='baselinev')
# # save the figure, then re-set axes limits for inset:
# axis_spont.set_xlim([0, 5])
# axis_spont.set_ylim([0, 15])
# dvdt_axis_spont.set_xlim([0, 15])  # should be the same as axis_spont ylims
# dvdt_axis_spont.set_ylim([0, 1.5])

axis_evoked, dvdt_axis_evoked = neuron_data_midbrain.plot_depolevents(aps_evoked,
                                 colorby_measure='baselinev')
# save the figure, then re-set axes limits for inset:
# axis_evoked.set_xlim([0, 5])
# axis_evoked.set_ylim([0, 15])
# dvdt_axis_evoked.set_xlim([0, 15])  # should be the same as axis_spont ylims
# dvdt_axis_evoked.set_ylim([0, 1.5])
# %%
# light-evoked vs. spontaneous fast depolarizing events
fastdepolarizations_all = ((des_df_midbrain.maxdvdt > 0.1)
                           & (~aps_all)
                           & (~des_df_midbrain.event_label.str.contains('currentpulsechange', na=False)))
fastdepolarizations_spont = (fastdepolarizations_all & ~des_df_midbrain.applied_ttlpulse)
fastdepolarizations_evoked = (fastdepolarizations_all & des_df_midbrain.applied_ttlpulse)
axis_spont, dvdt_axis_spont = neuron_data_midbrain.plot_depolevents(fastdepolarizations_spont,
                                 colorby_measure='baselinev',
                                                                    plt_title='spont. events')
# # save the figure, then re-set axes limits for inset:
# axis_spont.set_xlim([0, 5])
# axis_spont.set_ylim([0, 15])
# dvdt_axis_spont.set_xlim([0, 15])  # should be the same as axis_spont ylims
# dvdt_axis_spont.set_ylim([0, 1.5])

axis_evoked, dvdt_axis_evoked = neuron_data_midbrain.plot_depolevents(fastdepolarizations_evoked,
                                 colorby_measure='baselinev',
                                                                      plt_title='evoked events')
# save the figure, then re-set axes limits for inset:
# axis_evoked.set_xlim([0, 5])
# axis_evoked.set_ylim([0, 15])
# dvdt_axis_evoked.set_xlim([0, 15])  # should be the same as axis_spont ylims
# dvdt_axis_evoked.set_ylim([0, 1.5])
