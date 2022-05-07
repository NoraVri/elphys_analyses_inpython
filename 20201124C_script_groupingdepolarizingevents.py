# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20201124C'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not the greatest recording in terms of baselineV and AP amp: resting just below -30mV and AP peakV ~20mV.
# Other than that though the recording seems to have everything: oscillations, spont. APs and fastevents,
# and light responses (APs evoked every time until baselineV hyperpolarized to -70mV).


# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned()


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
# aps_evokedbylight did not all get labeled as such automatically: AP amp decreasing too far in the final light-applied
# block (light_0002); also one spont.AP did not get labeled in this file. DC-evoked APs all got picked up.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# All light responses got picked up as evoked events; though as seen before, not all evoked APs got labeled correctly.
# Doing so now:
# evoked_aps = evoked_events & (des_df.file_origin == 'light_0002.abf') & (des_df.amplitude > 35)
# singleneuron_data.depolarizing_events.loc[evoked_aps, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# looks good - the smallest event I could see in the raw data is just >2mV amp, and as far as I can see all spont.
# events got picked up.
# Let's start by labeling the one event that's in fact an AP with bad amplitude:
# spont_ap = unlabeled_spont_events & (des_df.file_origin == 'light_0002.abf') & (des_df.amplitude > 35)
# singleneuron_data.depolarizing_events.loc[spont_ap, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()

# now let's see the remaining events:
# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# to my eye these events look a little more round and slow than the usual fastevents, but I guess that makes sense
# given the neuron's rather depolarized resting V (-40 - -30 for most of the recording). Also, by parameters they
# fit the bill perfectly (amps 2 - 6mV, rise-time < 0.8ms) and normalized decays very identical (despite oscillations).
# Labeling them all as fastevents:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# recording looks pretty nice for the most part, but bad baselineV (-40 - -30mV) and AP peakV (+10 - just below 0mV
# towards the end) say these data should not be included in 'neat' stuff.