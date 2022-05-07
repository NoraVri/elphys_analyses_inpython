# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20201125F'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# this neuron has some strange events - perhaps AIS getting activated alone? However, it doesn't ever actually fire a full AP...
# Not a great recording, has some 50Hz and other problems.

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()
# !!notes say first few segments of light file are with continuous illumination (light accidentally turned on while changing protocols)



# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# things that got labeled as aps_oncurrentpulsechange aren't in fact APs, just places where V gets driven >> 0mV
# (with just 250pA +DC). Labeling them as such:
# singleneuron_data.depolarizing_events.loc[aps_oncurrentpulsechange, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# The events that got labeled as spont.APs are indeed that, though they seem to be lacking the fast Na-peak and
# because of that have gotten bad baseline-points. Also, not all events that could be classified as such got labeled
# automatically (I think - we'll have to see in the rest of picked up events).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# far from all light responses got picked up, and those that did have bad baselineV points. I did not see anyting labeled that shouldn't be.

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# well that's not great - as few events as there are altogether, in each file there are things to fix.
# In gapFree_0000, the peaks that got picked up with baselineV > -20mV are APs just like the ones that got labeled
# as such automatically; I'll apply that label to these as well:
# aps = (unlabeled_spont_events & (des_df.baselinev > -25))
# singleneuron_data.depolarizing_events.loc[aps, 'event_label'] = 'actionpotential'
# and the thing that has negative amplitude is a badly picked up currentpulsechange:
# currentpulsechange = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0000.abf') & (des_df.amplitude < 0))
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# In gapFree_0001 the event with low baselinev is a currentpulsechange:
# currentpulsechange = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0001.abf') & (des_df.baselinev < -60))
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# In light_0000 we have another thing with negative amplitude that is a badly labeled currentpulsechange:
# currentpulsechange = (unlabeled_spont_events & (des_df.file_origin == 'light_0000.abf') & (des_df.amplitude < 0))
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# and the two larger-amp things are in fact light responses:
# lightresponses = (unlabeled_spont_events & (des_df.file_origin == 'light_0000.abf') & (des_df.amplitude > 5))
# singleneuron_data.depolarizing_events.loc[lightresponses, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()

# Now let's see the remaining events:
# plotting all as-yet unlabeled events parameters:
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
