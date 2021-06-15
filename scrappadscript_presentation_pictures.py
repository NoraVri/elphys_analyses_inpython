# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %% picture: APs can be evoked from fast-events

# %% let's see 20200708F - if memory serves well, it had lots of fast-events and plenty of APs
# it's pretty cool - at practically the same baselinev (-48 - -50mV) it looks like a just slightly larger fast-event
# evoked APs. But not exactly the perfect example, I think.
# !notes say this neuron has lots of double-events, too, may be cool to look at those
neuron_name = '20200708F'
singleneuron_data = SingleNeuron(neuron_name)

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
selected_spontfastevents = (possibly_spontfastevents
                            & (des_df.amplitude > 5)
                            & (des_df.amplitude < 15)
                            & (des_df.rise_time_20_80 < 1)
                            & (des_df.baselinev < -48.2)
                            & (des_df.baselinev > -48.5)
                            )
# singleneuron_data.plot_depolevents(selected_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plot_dvdt=True,
#                                    )

selected_aps = (aps
                & (des_df.baselinev < -45) & (des_df.baselinev > -60)
                & (des_df.amplitude > 70) & (des_df.amplitude < 85))
# singleneuron_data.plot_depolevents(selected_aps,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plot_dvdt=True,
#                                    )

singleneuron_data.plot_depoleventsgroups_overlayed(selected_aps, selected_spontfastevents,
                                                   timealignto_measure='rt20_start_idx',
                                                   do_baselining=True,
                                                   # do_normalizing=True,
                                                   plotwindow_inms=15,
                                                   plot_dvdt=True,
                                                   )
singleneuron_data.plot_depolevents((selected_aps | selected_spontfastevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plot_dvdt=True,
                                   )

# %% let's see another neuron
singleneuron_data = SingleNeuron('20200630C')
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)

selected_spontfastevents = (possibly_spontfastevents
                            & (des_df.amplitude > 2)
                            # & (des_df.amplitude < 15)
                            # & (des_df.rise_time_20_80 < 1)
                            & (des_df.baselinev < -46)
                            & (des_df.baselinev > -55)
                            )
# singleneuron_data.plot_depolevents(selected_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plot_dvdt=True,
#                                    )

selected_aps = (aps
                & (des_df.baselinev < -46) & (des_df.baselinev > -55)
                & (des_df.amplitude > 80) #& (des_df.amplitude < 85)
                & (des_df.rise_time_10_90 < 2.5)
                )
# singleneuron_data.plot_depolevents(selected_aps,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plot_dvdt=True,
#                                    )

singleneuron_data.plot_depoleventsgroups_overlayed(selected_aps, selected_spontfastevents,
                                                   timealignto_measure='peakv_idx',
                                                   do_baselining=True,
                                                   # do_normalizing=True,
                                                   plotwindow_inms=12,
                                                   prealignpoint_window_inms=2.5,
                                                   plot_dvdt=True,
                                                   )
singleneuron_data.plot_depolevents((selected_aps | selected_spontfastevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=13,
                                   prealignpoint_window_inms=3,
                                   plot_dvdt=True,
                                   )



# %% picture: evoking depolarizing events by glutamate uncaging
# There's only one neuron really that has anything worth showing: 20200310G
# using plot1 from evokedsynapticexcitation_plotting
plot1(cell20200310G, 7, color_lims=[-47, -43], time_window=[0.02, 3])  # the light pulse is 200ms


# %% picture: evoking depolarizing events by glutamate puff
# looks like here, too, we've got just one neuron worth looking at: 20201116B
# using plot2 from evokedsynapticexcitation_plotting
plot2(cell20201116B, [1, 3], baseline_lims=[-56, -43], time_window=[0.02, 0.75])


# %% picture: evoking depolarizations using optogenetics

# finding the relevant neuron recordings
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')


# %% Thy1 - using picture made previously (for grant / SfN2019 poster)


# %% RBP
RBPmice_condition = experimentdays_metadata.genetics.isin(['RBP', 'RBP4-cre/Ai32'])
RBPevokedexcitations_experiments_dates = experimentdays_metadata[RBPmice_condition].date
RBPevokedexcitations_experimentdays_recordings = recordings_metadata[
    recordings_metadata.date.isin(RBPevokedexcitations_experiments_dates)]

relevantneuronrecordings_names = RBPevokedexcitations_experimentdays_recordings.name.dropna()
print(relevantneuronrecordings_names)

for neuron_name in relevantneuronrecordings_names:
    neuron_data = SingleNeuron(neuron_name)
    blockslist = neuron_data.get_blocknames(printing='off')
    for blockname in blockslist:
        if 'light' in blockname:
            plot2(neuron_data, blockname)

# 9 neurons with light-applied traces (3 different recording days)
# just one with basically no response (20200818B)
# 20201125 was the best day: C and D are both nice examples; B looks like it may be getting fast-events evoked (has them at rather high frequency to begin with)
# %%
neuron_data = SingleNeuron('20201125C')
plot2(neuron_data, [1, 2, 3, 4], baseline_lims=[-100, -35])

# %%
neuron_data = SingleNeuron('20201125D')
plot2(neuron_data, [3, 4, 5], baseline_lims=[-100, -35])
plot2(neuron_data, [6, 7])

# %% MDJ injection
injected_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',
                    'HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
injectedmice_condition = experimentdays_metadata.virusinjection_ID.isin(injected_mice)
MDJevokedexcitations_experiments_dates = experimentdays_metadata[injectedmice_condition].date
MDJevokedexcitations_experimentdays_recordings = recordings_metadata[
    recordings_metadata.date.isin(MDJevokedexcitations_experiments_dates)]

relevantneuronrecordings_names = MDJevokedexcitations_experimentdays_recordings.name.dropna()
print(relevantneuronrecordings_names)

for neuron_name in relevantneuronrecordings_names:
    neuron_data = SingleNeuron(neuron_name)
    blockslist = neuron_data.get_blocknames(printing='off')
    for blockname in blockslist:
        if 'light' in blockname:
            plot2(neuron_data, blockname)

# only ~5 neurons that did not clearly respond to the light, ever


# %% fast-event/APs as all-or-nothing evoked things
neuron_data = SingleNeuron('20210110E')
plot2(neuron_data, [ 3, 4], baseline_lims=[-60, -47])  # removed a bunch of traces from light 1 and 2 to get this

# let's see

# %% uncorrelated response amp to baselinev (to contrast with RBP synaptic response)
# neuron_data = SingleNeuron('20210113A')
# plot2(neuron_data, [ 3, 4], baseline_lims=[-100, -40])  # let's see these split out by baselinev:
baselinerange1 = [-90, -80.1]
baselinerange2 = [-80, -70.1]
baselinerange3 = [-70, -60.1]
baselinerange4 = [-60, -50.1]

plot2(neuron_data, [ 3, 4], baseline_lims=baselinerange1)
plot2(neuron_data, [ 3, 4], baseline_lims=baselinerange2)
plot2(neuron_data, [ 3, 4], baseline_lims=baselinerange3)
plot2(neuron_data, 3, baseline_lims=baselinerange4)



