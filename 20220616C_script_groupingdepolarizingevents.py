# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220616C'
singleneuron_data = SingleNeuron(neuron_name)

# The first recording file (gapFree_0001) is >30min. long, rather heavy to plot so beware (unsuccesfully trying to evoke things by stimulating the slice with the other recording pipette).

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)





# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 to make sure we can separate between large spikelets and small fastevents

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: lots of things that could/should be APs on currentpulsechange didn't get picked up as such;
# it seems somewhat random, but understandable with the effect of TTX partially washing out. Didn't see anything
# labeled that shouldn't've been.
# aps_spont: occur only in the first recording file, before any TTX application; looks like these all got picked up OK.
# All other APs labeled spont are just ones that didn't get automatically labeled as being on currentpulse. Rectifying:
# currentevoked_aps = (aps_spont & (des_df.baselinev > -35))
# singleneuron_data.depolarizing_events.loc[currentevoked_aps, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(aps_spont,
                                   colorby_measure='baselinev')

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
blocknames = des_df[unlabeled_spont_events].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=unlabeled_spont_events,
                                         segments_overlayed=False)
# notes:
# in the first recording file, seems like stimulation did do something here and there, as evidenced by a weird
# artefact-ey looking things followed by synaptic depols/spikelets arriving in crazy patterns. Will deal with those later.
# Spont.events got picked up in three more files; in the first half of gapFree_withTTX_0000 there are still spont.events
# (as expected; file was started at time of switching solution at the inflow of the pump, it takes another ~3.5min from
# there to fill the bath); all others are slightly active things happening in response to currentpulsechanges.
# Labeling them accordingly:
# currentpulsechanges1 = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_withTTX_0000.abf') & (des_df.peakv_idx > (230 * 50000)))
# currentpulsechange_files  = ['gapFree_withTTXwash_0001.abf', 'gapFree_withTTXwash_0002.abf']
# currentpulsechanges2 = (unlabeled_spont_events & (des_df.file_origin.isin(currentpulsechange_files)))
# currentpulsechanges = (currentpulsechanges1 | currentpulsechanges2)
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()




