# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210413B'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True, postttl_t_inms=20)
# separately by conditions: low/high light intensity
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000',
                                                color_lims=[-75, -35],
                                                plt_title='high light intensity')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001',
                                                color_lims=[-75, -35],
                                                plt_title='low light intensity')

# %% plotting spontaneous events
des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)

singleneuron_data.plot_depolevents((unlabeled_spontevents),
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

singleneuron_data.plot_depolevents((aps & spont_events),
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# exttracting with standard parameters, min_depolamp 1mV (from seeing the raw data there's a spikelet of ~1mV, and nothing smaller)
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# for each category of APs, see that they are indeed that:
events = aps_spont   #aps_oncurrentpulsechange  #aps_evokedbylight
blocknames = des_df[events].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=events,
                                         segments_overlayed=False)
# I saw one spont.AP in the data that did not get labeled as anything; it's easily found among unlabeled events by amplitude.
# Labeling it as actionpotential:
# unlabeled_ap = unlabeled_spontevents & (des_df.amplitude > 30)
# singleneuron_data.depolarizing_events.loc[unlabeled_ap, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# all evoked things got extracted quite nicely, and with good baseline-points, too

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# Definitely all fast-events that my eye picked up got picked up by the algorithm, too; also some
# spikelets (~1mV) got picked up and in very short stretches of recording also some noise-things.

# Finding and labeling fast-events (and other types of events encountered along the way):
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
# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
# There's a group of events with amp 5 - 10mV that also have fast max.dVdt - these are probably all fastevents.
# There is also a group of events with amp < 2mV; by rise-time, it is possible that some of these are also fastevents
# (if only because the fastest-rising events do not occur at hyperpolarized baselineV).

# Let's start by seeing all the larger events:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 4))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# Indeed - even though most of these events have a way rounder and wider peak than we're used to seeing, I see no reason
# why these things wouldn't all be fastevents (fast rise-time and maxdvdt). Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Now let's see all remaining events:
# events_underinvestigation = (unlabeled_spont_events )
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# Between the noise in the recording and the small amplitude of these things (<1.6mV) I think it's safest to just leave these all be.
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not marking neat events for this neuron.
# notes:
# BaselineV right around -30mV w/o DC injection, and at times even worse than that; also AP peakV going from bad to
# worse over the course of recordings. Plus from what I saw, these fastevents would definitely be outliers in their
# width. So, I see no reason to include data from this neuron in neat_events.