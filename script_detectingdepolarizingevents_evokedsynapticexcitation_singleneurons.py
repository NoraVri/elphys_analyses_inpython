from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# %% list of neurons with light-evoked responses recordings
# %% experiment: ChR activation in Thy1 mouse (experiment days 20190527 and 20190529)
# singleneuron_data = SingleNeuron('20190527A')
#
# singleneuron_data = SingleNeuron('20190527C')
#
singleneuron_data = SingleNeuron('20190529A1')
#
# singleneuron_data = SingleNeuron('20190529B')
#
# singleneuron_data = SingleNeuron('20190529C')
#
# singleneuron_data = SingleNeuron('20190529D')
#
# singleneuron_data = SingleNeuron('20190529E')

# %% experiment: RubiGlu uncaging (experiment days 20200306, 20200308, 20200310 and 20200312)
#
# singleneuron_data = SingleNeuron('20200306C')
#
# singleneuron_data = SingleNeuron('20200308B')
#
# singleneuron_data = SingleNeuron('20200308C')
#
# singleneuron_data = SingleNeuron('20200308D')
#
# singleneuron_data = SingleNeuron('20200308E')
#
# singleneuron_data = SingleNeuron('20200310G')
#
# singleneuron_data = SingleNeuron('20200312C')
#
# singleneuron_data = SingleNeuron('20200312G')

# %% setting parameters for get_depolarizingevents for each neuron
# neuron20190527A: used block no.12 to find good parameter settings
# neuron20190527B: used block no.2 to find good parameter settings
# neuron20190529A1: used block no.2  to find good parameter settings
# neuron20190529B: used block no.14 to find good parameter settings
# neuron20190529C: used block no.3 to find good parameter settings
# neuron20190529D: used block no.2 to find good parameter settings
# neuron20190529E: used block no.2 to find good parameter settings

# apsdict, depolsdict = singleneuron_data.plot_eventdetecttraces_forsegment(2, 8, return_dicts=True,
#                                                                           min_depolspeed=0.2,
#                                                                           min_depolamp=0.3,
#                                                                           peakwindow=7,
#                                                                           noisefilter_hpfreq=2000,
#                                                                           oscfilter_lpfreq=10,
#                                                                           # ttleffect_windowinms=3
#                                                                           )

singleneuron_data.get_depolarizingevents_fromrawdata(
                                                    min_depolspeed=0.2,
                                                    min_depolamp=0.3,
                                                    peakwindow=7,
                                                    noisefilter_hpfreq=2000,
                                                    oscfilter_lpfreq=10,
                                                    ttleffect_windowinms=3
                                                     )
singleneuron_data.write_results()
# %% seeing all detected APs
evoked_aps = singleneuron_data.action_potentials.applied_ttlpulse
spont_aps = ~singleneuron_data.action_potentials.applied_ttlpulse
# colorscalelims = [-60, -35]
singleneuron_data.plot_depolevents_overlayed(evoked_aps,
                                             get_subthreshold_events=False,
                                             plt_title='evoked aps',
                                             do_baselining=True,
                                             colorby_measure='baselinev',
                                             # color_lims=colorscalelims
                                             prealignpoint_window_inms=20,
                                             total_plotwindow_inms=40,
                                             )

singleneuron_data.plot_depolevents_overlayed(spont_aps,
                                             get_subthreshold_events=False,
                                             plt_title='spontaneous aps',
                                             do_baselining=True,
                                             colorby_measure='baselinev',
                                             # color_lims=colorscalelims,
                                             prealignpoint_window_inms=20,
                                             total_plotwindow_inms=40,
                                             )

singleneuron_data.plot_depoleventsgroups_overlayed(evoked_aps, spont_aps,
                                                   group_labels=['evoked', 'spontaneous'],
                                                   get_subthreshold_events=False,
                                                   do_baselining=True,
                                                   prealignpoint_window_inms=20,
                                                   total_plotwindow_inms=40,
                                                   plt_title='all APs')
# %% looking at detected depolarizations
# scatters of all subthreshold events measures
# singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time',
#                                                       cmeasure='baselinev')
evoked_events = singleneuron_data.depolarizing_events.applied_ttlpulse
spont_events = ~singleneuron_data.depolarizing_events.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time',
                                                      cmeasure='baselinev',
                                                      evokedevents=evoked_events,
                                                      spontevents=spont_events)
# %% a quick look to see if we can isolate fast-events from among all depolarizations
# neuron20190527A: baselinev < -25, amplitude > 1.5, rise_time < 1
# neuron20190527C: -80 < baselinev < -30, amplitude > 2, rise_time < 2
# neuron20190529B: amplitude > 1 - basically all evoked responses look like stacked fast-events
# neuron20190529D: amplitude > 3, rise_time < 2 - but also: amplitude > 0.5, rise_time < 0.3
# neuron20190529E: amplitude > 0.4, rise_time < 0.5

fastevents_largerthan_params = {
                                'amplitude':1.5,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 'baselinev':-25,
                                 'rise_time':1,
                                 }

possiblyfastevents_spont = spont_events
possiblyfastevents_evoked = evoked_events
for key, value in fastevents_largerthan_params.items():
    possiblyfastevents_spont = (possiblyfastevents_spont
                                & (singleneuron_data.depolarizing_events[key] > value))
    possiblyfastevents_evoked = (possiblyfastevents_evoked
                                 & (singleneuron_data.depolarizing_events[key] > value))
for key, value in fastevents_smallerthan_params.items():
    possiblyfastevents_spont = (possiblyfastevents_spont
                                & (singleneuron_data.depolarizing_events[key] < value))
    possiblyfastevents_evoked = (possiblyfastevents_evoked
                                 & (singleneuron_data.depolarizing_events[key] < value))

singleneuron_data.plot_depolevents_overlayed(possiblyfastevents_spont,
                                             colorby_measure='baselinev',
                                             do_baselining=True,
                                             # do_normalizing=True,
                                             prealignpoint_window_inms=10,
                                             total_plotwindow_inms=25,
                                             # newplot_per_block=True,
                                             # blocknames_list=['light_wholeField_0009.abf']
                                             )


singleneuron_data.plot_depolevents_overlayed(possiblyfastevents_evoked,
                                             colorby_measure='baselinev',
                                             do_baselining=True,
                                             do_normalizing=True,
                                             prealignpoint_window_inms=10,
                                             total_plotwindow_inms=25,
                                             )
plt.suptitle('evoked events')

singleneuron_data.plot_depoleventsgroups_overlayed(possiblyfastevents_spont,
                                                   possiblyfastevents_evoked,
                                                   group_labels=['spontaneous', 'evoked'],
                                                   # blocknames_list=blocksnames_list,
                                                   do_baselining=True, do_normalizing=True,
                                                   plt_title='presumably all fast-events')
