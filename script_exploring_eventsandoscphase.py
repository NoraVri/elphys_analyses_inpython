# %% imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from singleneuron_class import SingleNeuron

# %% data: neurons that are oscillating and exhibit spontaneously occurring fast-events
# singleneuron_data = SingleNeuron('20200310G')
singleneuron_data = SingleNeuron('20190812A')
# singleneuron_data.plot_allrawdata()
# %% plotting 'gap-free' recordings traces along with plots of hilbert transform to see where phase estimation is good
allblocksnames_list = singleneuron_data.get_blocknames()
gapfreefiles_list = [name for name in allblocksnames_list if 'gapFree' in name]
# gapfreefiles_list = [name for name in allblocksnames_list if 'spontactivity' in name]
singleneuron_data.plot_blocks_byname(*gapfreefiles_list)
# %%
for file in gapfreefiles_list:
    file_idx = allblocksnames_list.index(file)
    singleneuron_data.plot_eventdetecttraces_forsegment(file_idx, 0)
# %%
# in gapFree_0001.abf starting at 555s in
# in gapFree_0002.abf starting at 340s in
sampling_rate = singleneuron_data.blocks[1].segments[0].analogsignals[0].sampling_rate
gf1_minidx = sampling_rate * 555
gf2_minidx = sampling_rate * 340

goodphase_blocks = ['gapFree_0001.abf', 'gapFree_0002.abf']
goodphase_events = (
        ((singleneuron_data.depolarizing_events.file_origin == goodphase_blocks[0])
         & (singleneuron_data.depolarizing_events.baselinev_idx > gf1_minidx))
        | ((singleneuron_data.depolarizing_events.file_origin == goodphase_blocks[1])
           & (singleneuron_data.depolarizing_events.baselinev_idx > gf2_minidx))
)
# %% finding fast-events criteria
singleneuron_data.scatter_depolarizingevents_measures('amplitude',
                                                      'rise_time',
                                                      cmeasure='approx_oscinstphase')

# %%
# definitelyfastevents = ((singleneuron_data.depolarizing_events.amplitude > 2)
#                         & (singleneuron_data.depolarizing_events.rise_time < 1.5))
definitelyfastevents = ((singleneuron_data.depolarizing_events.amplitude > 5)
                        & (goodphase_events))
possiblyfastevents = (((singleneuron_data.depolarizing_events.amplitude > 1)
                        & (singleneuron_data.depolarizing_events.amplitude < 5))
                      & (goodphase_events)
                      & (singleneuron_data.depolarizing_events.baselinev < -30))

# %% looking at things that are definitely fast-events
singleneuron_data.plot_depolevents_overlayed(definitelyfastevents,
                                             colorby_measure='baselinev',
                                             do_baselining=True)
singleneuron_data.plot_depolevents_overlayed(definitelyfastevents,
                                             colorby_measure='approx_oscinstphase',
                                             do_baselining=True,
                                             do_normalizing=True)
definitelyfastevents_df = singleneuron_data.depolarizing_events[definitelyfastevents]

definitelyfastevents_df.hist(column='approx_oscinstphase', bins=36, range=[-3.15, 3.15])
definitelyfastevents_df.hist(column='baselinev', bins=30)
definitelyfastevents_df.plot.scatter(x='amplitude',
                                     y='approx_oscinstphase',
                                     c='rise_time')

# %%
singleneuron_data.plot_depolevents_overlayed(possiblyfastevents,
                                             colorby_measure='baselinev',
                                             do_baselining=True)
singleneuron_data.plot_depolevents_overlayed(possiblyfastevents,
                                             colorby_measure='approx_oscinstphase',
                                             do_baselining=True,
                                             do_normalizing=True)
