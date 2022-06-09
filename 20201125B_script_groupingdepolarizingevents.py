# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20201125B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# pretty nice recording: neuron is maintaining a resting baselineV very steadily (just over -50mV) and displays
# oscillations and spont. fastevents and APs throughout; however, I do see a significant drop in AP amp over the
# course of recordings.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise
# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True)


# %% summary plots - all events:
# histogram of baselinev in the entire recording:
# singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
# histograms of events parameters
nbins = 100
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')

# compound events - only 3 recorded in this neuron
# des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('compound events parameter distributions')


# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# scatters of events parameters:
# fast-events
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
# %% summary plots - neat events only:
nbins = 100  #
neat_events = singleneuron_data.depolarizing_events.neat_event
# fast-events
singleneuron_data.plot_depolevents((fastevents & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                        'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                        bins=nbins)
plt.suptitle('fast-events, neat ones only')

# aps
singleneuron_data.plot_depolevents((aps & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat aps'
                                   )
des_df[(aps & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                             bins=nbins)
plt.suptitle('aps, neat ones only')

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
# I found quite a number of aps labeled as being on_currentpulsechange that aren't actually that. Applying corrections:
# list of APs that got labeled as being on currentpulsechange but are in fact spontaneous:
# spont_ap1 = (aps_oncurrentpulsechange & (des_df.file_origin == 'gapFree_0001.abf')
#              & (des_df.peakv_idx > (149*20000)) & (des_df.peakv_idx < (149.2*20000)))  # this AP happens to occur just 1ms after release from a small depolarizing DC step: definitely spontaneous, not evoked
# spont_ap2 = (aps_oncurrentpulsechange & (des_df.file_origin == 'longPulses_0001.abf')
#              & (des_df.segment_idx == 5) & (des_df.applied_current < 10))  # this AP occurs spontaneously right before application of a long +DC pulse
# spont_ap3 = (aps_oncurrentpulsechange & (des_df.file_origin == 'longPulses_0003.abf')
#              & (des_df.segment_idx == 3))  # this AP occurs spontaneously right before release from small hyperpolarizing current pulse
# spont_ap4 = (aps_oncurrentpulsechange & (des_df.file_origin == 'longPulses_0005.abf')
#              & (des_df.segment_idx == 4) & (des_df.applied_current > 200))  # this AP occurs spontaneously right before release from long +DC step
# spont_ap5 = (aps_oncurrentpulsechange & (des_df.file_origin == 'shortPulses_0000.abf')
#              & (des_df.segment_idx == 10))  # this AP occurs just before shortPulse application (pulse ends up on the AHP phase of this AP)
# spont_aps6 = (aps_oncurrentpulsechange & (des_df.file_origin == 'shortPulses_0001.abf')
#              & (des_df.segment_idx < 36))  # three APs here that occur spontaneously just before shortPulse, or just after it decayed
# spont_aps = (spont_ap1 | spont_ap2 | spont_ap3 | spont_ap4 | spont_ap5 | spont_aps6)
# singleneuron_data.depolarizing_events.loc[spont_aps, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# two more events that got labeled AP but aren't that at all:
# not_aps = (aps_oncurrentpulsechange & (des_df.file_origin == 'longPulses_0007.abf')
#            & (des_df.segment_idx == 5) & (des_df.baselinev > 0))  # these two 'events' are definitely not APs - amp way too small (<3mV).
# singleneuron_data.depolarizing_events.loc[not_aps, 'event_label'] = None
# singleneuron_data.write_results()
# In light-evoked APs I did not see any mislabeled, but there are definitely some light responses that should
# get marked as AP but didn't (AP amp/peakV deteriorating pretty badly towards the end of recordings) - will get to those later.
# Same for spont.APs: definitely nothing that isn't actually a spont.AP got labeled as such, but I do see a bunch
# more events that are probably spont.APs that didn't get automatically labeled as such - will get to those later as well.
# Also, there are 4 APs in gapFree_0000 that got evoked by light accidentally being on (according to notes) but are labeled spont. because there is no TTL.
# Labeling those events (one AP has also spikeshoulderpeak) as lightevoked:
# block_name = 'gapFree_0000.abf'
# window_start_t = 376
# window_end_t = 378
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# if block_name in singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'].keys():
#     trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'][block_name]['t_start']
# else: trace_start_t = 0
# lightwindow_start_idx = (window_start_t - trace_start_t) * float(sampling_frequency)
# lightwindow_end_idx = (window_end_t - trace_start_t) * float(sampling_frequency)
# lightmade_events = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx >= lightwindow_start_idx)
#                        & (des_df.peakv_idx < lightwindow_end_idx)
#                        )
# singleneuron_data.depolarizing_events.loc[lightmade_events, 'applied_ttlpluse'] = True
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# far from all light-evoked responses got picked up: they are generally too slow-rising to get picked up by the
# algorithm, so also those peaks that did get picked up as a rule have bad baselinev-points.
# I did not see any events labeled 'evoked' that are actually spontaneous.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# well, that's a lot of mess. Early on in the recording things look very nice, but soon enough AP amplitude is so
# badly deteriorated that they don't get labeled as such anymore, and consequently also the second peak does not get
# labeled as spikeshoulderpeak automatically. Also, I saw at least one peak that got picked up as spont. even though
# its evoked - the rise is slow enough that the baselinepoint got put outside of the ttl-window.

# plotting all as-yet unlabeled events parameters:
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

# OK then, let's just go over these section by section, putting together blocks where recording conditions are similar.
# Starting from the first few blocks, where conditions are good:
# blocks_group = ['gapFree_0000.abf', 'gapFree_0001.abf', 'light_0000.abf',]
# events_underinvestigation = (unlabeled_spont_events & (des_df.file_origin.isin(blocks_group)))
# Well that definitely looks like practically all fastevents: out of 520 events just three have rise-time > 1ms.
# let's see those three events within the raw data:
# events_underinvestigation = (events_underinvestigation & (des_df.rise_time_20_80 > 1))
# blocknames = des_df[events_underinvestigation].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events_underinvestigation,
#                                          segments_overlayed=False)
# two of those events are sizeable spikelets occurring during gapFree_0001 (amp ~3mV); the other one occurs during
# light_0000 and is the peak of a light-evoked response. Labeling them accordingly:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.file_origin == 'gapFree_0001.abf')),
#                                           'event_label'] = 'spikelet'
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.file_origin == 'light_0000.abf')),
#                                           'applied_ttlpulse'] = True
# singleneuron_data.write_results()
# After a whole bunch of checking and seeing separately and seeing within the raw data, I am convinced that all
# remaining events are in fact fastevents. The waveform-identicalness is obviously screwed up somewhat by the
# presence of large oscillations; beyond that, there is one event that is directly preceded by a decent-sized (~2mV)
# spikelet and a couple that look to be much rounder than the rest (these occur during a period of recording where
# V was depolarized with DC). By measured parameters, they all fit well within the bill of being fastevents.
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# blocks_group = ['longPulses_0000.abf', 'longPulses_0001.abf', 'longPulses_0002.abf',
#                 'longPulses_0003.abf', 'longPulses_0004.abf', 'longPulses_0005.abf',
#                 'longPulses_0006.abf', 'shortPulses_0000.abf', 'shortPulses_0001.abf',] # I think this is where things start to go bad
# events_underinvestigation = (unlabeled_spont_events & (des_df.file_origin.isin(blocks_group)))
# # OK then, out of this next batch of 37 events three are clearly compound, one is obviously a mislabeled
# # currentpulsechange and the rest is likely to be all fastevents (aside from the one event of ~2mV that seems to have
# # a different rise - even more different than the slightly rounded peaks I'm starting to get used to seeing on events
# # occurring at depolarized potentials).
# currentpulsechange = (events_underinvestigation & (des_df.rise_time_20_80 < 0.2))
# compound_events = (events_underinvestigation & (des_df.baselinev > -30) & (des_df.amplitude > 8))
# singleneuron_data.depolarizing_events.loc[currentpulsechange, 'event_label'] = 'currentpulsechange'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# In the events that remain there is one with a longer rise-time than all the rest (>1.5ms, vs <=1ms for all other
# events); its amp is ~2mV and I'm not sure from looking at it whether it's a compound event or a spikelet, so I'll
# just leave it unlabeled. Anyway, all other events are definitely fastevents; labeling them as such:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.rise_time_20_80 < 1.5)),
#                                           'event_label'] = 'fastevent'
# singleneuron_data.write_results()
#
# des_df = singleneuron_data.depolarizing_events
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# blocks_group = ['light_0001.abf', 'light_0002.abf', 'light_0003.abf',
#                 'light_0004.abf', 'gapFree_0002.abf', 'longPulses_0007.abf',
#                 'longPulses_0008.abf', 'longPulses_0009.abf', 'longPulses_0010.abf',
#                 'longPulses_0011.abf', 'longPulses_0012.abf',] # I think this is where things start to go bad
# events_underinvestigation = (unlabeled_spont_events & (des_df.file_origin.isin(blocks_group)))
# there's definitely a whole bunch of proper fastevents in this group, but also degenerate APs and their
# spikeshoulderpeaks, as well as some other things that are probably currentpulsechanges.
# Let's start by seeing the two 'events' with baselinev > 20mV in the raw data:
# the one that has a negative amplitude is actually a currentpulsechange; the other one might actually be an event
# (though something is definitely very wrong with the recording by then...). Labeling accordingly:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.amplitude < 0)),
#                                           'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# Next up, events with -20 < baselinev < 0 are all clearly spikeshoulderpeaks. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation
#                                            & (des_df.baselinev < 0) & (des_df.baselinev > -20)),
#                                           'event_label'] = 'spikeshoulderpeak'
# singleneuron_data.write_results()
# In the now remaining events, there's a group with amp up to 12 mV, and a group with amp > 35mV that are clearly
# degenerate APs. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.amplitude > 35)),
#                                           'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# In the now remaining events, there are 7 that stand far out by their rise-time (>2.4ms, vs <1.4ms for all other
# events) that look like they are currentpulsechanges:
# events_underinvestigation = (events_underinvestigation & (des_df.rise_time_20_80 > 2))
# confirmed by seeing them in the raw data. Labeling as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# The now remaining events look like they could all be fastevents: there are just 4 with 1 <= rise-time < 1.3ms,
# the rest all has 0.5 < rise-time < 1ms. Having seen them plotted separately and within the raw data, I see no reason
# why those aren't just fastevents, too, maybe particularly distorted by ongoing oscillations and such (the most
# weirdly-shaped one occurred where baslineV was hyperpolarized to -80mV). So, labeling all remaining events as fastevents:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# des_df = singleneuron_data.depolarizing_events
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# blocks_group = ['shortPulse_0000.abf', 'shortPulse_0001.abf']  # this is where it starts to get really messy
# events_underinvestigation = (unlabeled_spont_events & (des_df.file_origin.isin(blocks_group)))
# Starting in these recording files APs become so far degenerate that sometimes baseline-points are in the wrong place;
# still APs are all recorded as having amp ~30-40mV, so they are easily separated from the subthreshold events.
# Labeling them as such:
# degenerate_aps = (events_underinvestigation & (des_df.amplitude > 25))
# singleneuron_data.depolarizing_events.loc[degenerate_aps, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# The remaining events should all be fastevents: amp is only ~2.5 - 3.5mV, but rise-time is fast (<1.15ms) and
# rising phase of normalized events is exactly identical (decay phase affected by oscillations starting 1ms after
# the peak). Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# des_df = singleneuron_data.depolarizing_events
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# blocks_group = ['gapFree_0003.abf',]  # here things are really just a huge mess.
# events_underinvestigation = (unlabeled_spont_events & (des_df.file_origin.isin(blocks_group)))
# Here it starts to be a real problem that AP peaks do not have good baseline-points associated with them; measured
# parameters cannot be trusted at all. I tried seeing if I could at least filter out AP peaks somehow, but while the
# first Na-peak of the AP is terribly degenerate, we do still get spikeshoulderpeaks, too, and it's impossible to
# distinguish between these and 'proper' AP peaks by any measured parameter. So, even just for tallying AP and
# fastevent frequencies, this recording file cannot be used without a whoooooooole lot more work put into manually
# labeling events. So I'm making the decision to label all events occurring in this final recording file as
# 'noiseevent', and not use them in analyses.
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()


# events_underinvestigation = unlabeled_spont_events
# blocknames = des_df[events_underinvestigation].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events_underinvestigation,
#                                          segments_overlayed=False)

# let's see remaining events split out per block (cause there's just SO MANY of them):
# for block in blocks_group:
#     singleneuron_data.plot_depolevents((events_underinvestigation & (des_df.file_origin == block)),
#                                        colorby_measure='baselinev',
#                                        plotwindow_inms=15,
#                                        do_baselining=True,
#                                        # do_normalizing=True,
#                                        plot_dvdt=True
#                                        )

# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# notes:
# It's hard to tell where 'neat' recording ends for this neuron: it's keeping a steady baselineV, and oscillating
# throughout which makes it hard to say whether fastevents are affected. Deterioration of AP amp becomes VERY
# apparent towards the end of recordings (which total >70min.), but early on it is decreasing very slowly. Still,
# looking for the highest-amp APs we find that they all (except 1) occur during the first three recording files. So
# I will use those to mark 'neat' events:

# neat_events = ((des_df.file_origin == 'gapFree_0000.abf')
#                | (des_df.file_origin == 'gapFree_0001.abf')
#                | (des_df.file_origin == 'light_0000.abf'))
# adding the neatevents-series to the depolarizing_events-df:
# neat_events.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neat_events)
# singleneuron_data.write_results()

