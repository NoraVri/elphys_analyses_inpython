from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq

# %% experiment: ChR activation in Thy1 mouse
cell20190527A = SingleNeuron('20190527A')
# using block no.12 to find good parameter settings
# apsdict, depolsdict = cell20190527A.plot_eventdetecttraces_forsegment(12,9, return_dicts=True,
#                                                                       min_depolspeed=0.2,
#                                                                       peakwindow=4,
#                                                                       oscfilter_lpfreq=15,
#                                                                       ttleffect_windowinms=3)

# cell20190527A.get_depolarizingevents_fromrawdata(min_depolspeed=0.2,
#                                                   peakwindow=4,
#                                                   oscfilter_lpfreq=15,
#                                                   ttleffect_windowinms=3)
# cell20190527A.write_results()
# %%
#
evoked_aps = cell20190527A.action_potentials.applied_ttlpulse
spont_aps = ~cell20190527A.action_potentials.applied_ttlpulse
colorscalelims = [-60, -35]
cell20190527A.plot_depolevents_overlayed(evoked_aps,
                                         get_subthreshold_events=False,
                                         plt_title='evoked aps',
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         color_lims=colorscalelims)

cell20190527A.plot_depolevents_overlayed(spont_aps,
                                         get_subthreshold_events=False,
                                         plt_title='spontaneous aps',
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         color_lims=colorscalelims)

# %%
cell20190527C = SingleNeuron('20190527C')

cell20190529B = SingleNeuron('20190529B')

cell20190529C = SingleNeuron('20190529C')

cell20190529D = SingleNeuron('20190529D')

cell20190529E = SingleNeuron('20190529E')

