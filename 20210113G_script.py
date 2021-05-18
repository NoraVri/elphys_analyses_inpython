# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

neuron_name = '20210113G'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

# %% extracting depolarizing events
# notes:
# in light-applied files, stimulus goes to as short as 1ms; the effect is rather immediate but can be longer
# (up to 20ms maybe), so setting ttleffect window at 15ms (that should pick up the peaks of all light responses)
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=15)


# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events


# 1. seeing that light-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# sub-threshold depolarizations get picked up weirdly sometimes (weird baselinepoints because compound responses),
# but definitely everything that's evoked got labeled as such so I think it'll do.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
definitelynot_fastevents = des_df.event_label.isin(['actionpotential', 'spikeshoulderpeak', 'currentpulsechange'])
possibly_spontfastevents = (spont_events & ~definitelynot_fastevents)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# LOADS of things got extracted, mostly tiny stuff (spikelets and noisy things).
# The neuron clearly has spont.events of amp > 5mV,
# and there are a few things that are definitely APs (got a shoulder and everything)
# that didn't get labeled a such and have to get picked out manually.
# Let's filter down to things with amp > 2mV, and see amplitude and rise-time for the rest to narrow down from there:
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))
plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60)
plt.title('all spont. events >2mV, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
plt.title('all spont. events >2mV, rise-time')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# Let's see the events with amp > 50mV first:
# singleneuron_data.plot_depolevents((possibly_spontfastevents & (des_df.amplitude > 50)),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms=100,
#                                    plt_title='possibly unlabeled APs'
#                                    )
# I'm pretty sure those are actually currentpulsechanges: - indeed:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(possibly_spontfastevents & (des_df.amplitude > 50)))
# Let's label them as such:
# singleneuron_data.depolarizing_events.loc[
#     (possibly_spontfastevents & (des_df.amplitude > 50)), 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()






# %%



aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
singleneuron_data.plot_depolevents((aps & ~des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='spontaneous APs')

