# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210113A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not a great recording: baselineV rather unsteady at times, kinda noisy all around, and includes some very
# strange events (sudden hyperolarization of 10-15mV from -45mV resting). Still, light response always includes (a) fastevent(s).

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
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
# one of the APs that got marked spont. is very much evoked by the currentpulse it's sitting on; labeling it as such:
# ap_oncurrent = (aps_spont & (des_df.peakv_idx > (20000 * 100)))
# singleneuron_data.depolarizing_events.loc[ap_oncurrent, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()
# And the one AP that is actually spont. might in fact be evoked by some noise caused by touching the rig (upstroke looks weird).
# no light-evoked APs recorded in this neuron; other DC-evoked APs got picked up alright.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# looks like evoked things all got picked up quite nicely; did not see anything labeled that is in fact spont.

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# some cleanup to do -
# in gapFree_0000, the start of one of those hyperolarizing events got picked up as an event with no amplitude and
# another 'event' with large amp but relatively slow rise got picked up with bad baselineV.
# And in light_0000 there's a whole bunch of noise-things that got picked up as events, concentrated into three specific segments
# noiseevent = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0000.abf') & (des_df.amplitude < 0.5))
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'light_0000.abf')
#                & (des_df.segment_idx >= 30) & (des_df.segment_idx <= 32))
# noiseevents = (noiseevents | noiseevent)
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

events_underinvestigation = (unlabeled_spont_events ) #& (des_df.))
singleneuron_data.plot_depolevents(events_underinvestigation,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=15,
                                   plotwindow_inms=50,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# not sure about fastevents: most of the events that got picked up are 2-3mV and not very identical in normalized
# decay waveform; and the events that are larger than that don't look like real events to me (way too fast or
# way too slow rise).








#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
