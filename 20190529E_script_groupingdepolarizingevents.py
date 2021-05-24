# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190529E'
singleneuron_data = SingleNeuron(neuron_name)


# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# starting the analysis I wasn't all that sure it has any real events at all so much (neuron was patched more than 6 hours after slicing).
# Then I found 6 events with amp 0.4 - 1.25mV that have exactly the same normalized waveform.

# summary plots:


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.2 to find good parameter settings; playing with parameter settings was done elsewhere,
# re-creating data table with stored settings:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Looks like the algorithm did its job, but nothing too exciting is getting excited to begin with
# and then the neuron stops responding altogether.


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# Lots of stuff got picked up, most of it takes quite a bit of squinting to say that it's not just noise (though there
# definitely are some real spikelets and such in there).

# Let's see amplitude and rise-time to narrow down from there:
# There's a small handful of events with surprisingly large amp for their rise-time, clearly visible in the
# amp/rise-time scatters; let's see them:
possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 < 0.2)
                            & (des_df.amplitude > 0.3))  # too much noise below that
# well dang - aside from two events that aren't behaving, these all have exactly the same normalized waveform
# (amps going from 0.4 - 1.25 mV).
# There's only 6 of them though, are they really worth it?
plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
plt.title('spont. events, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
plt.title('spont. events, rise-time (20-80%)')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
plt.title('spont. events, rise-time (10-90%)')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True
                                   )

