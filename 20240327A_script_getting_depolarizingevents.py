# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %%
neuron_name = '20240327A'
# sulpiride applied and washed out again
# spont.activity, longPulses and optoStim
# neuron looks a little unsteady at first, then settles in to baselineV ~-65mV and stays steady throughout recordings
# spont.activity looks distinctly different to me between drug and no drug conditions - with drug there seem to be more and larger EPSPs.
# response to opto stim. may have gotten up to 50% larger after drug application, or not changed at all - gonna have to do statistics on that
singleneuron_data = SingleNeuron(neuron_name)

# %% getting depolarizing events
# # let's see how my algorithm does by default
#
# singleneuron_data.plot_eventdetecttraces_forsegment(0, 0, time_slice=[190, 220],
#                                                     oscfilter_lpfreq=1,
#                                                     depol_to_peak_window=10)
#
# # looked at a few different places in two different traces and honestly, it's looking pretty good
# # maybe with better filter settings it'll be easier to pick up slightly slower depolarizations as well
# # Definitely the low-pass filter should be way lowered compared to IO neurons, as we're not dealing with oscillating baseline voltage here
# # and with that and a wider depol-to-peak window it looks like we're picking up practically all things that could be called depolarizing events.
#
# # Let's run it for all the data:
# singleneuron_data.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=1, depol_to_peak_window=10)
# singleneuron_data.write_results()

nbins = 100
des_df = singleneuron_data.depolarizing_events
unlabeled_events = des_df.event_label.isna()
# %% quick and dirty comparison: representative traces of equal length before and after sulpiride

# singleneuron_data.plot_rawdatablocks('gapFree_0001', 'gapFree_withSulpirideWashout_0000',
#                                      events_to_mark=unlabeled_events)

# 'representative' traces: 125-225s in each file

beforedrug_events = (des_df.file_origin.str.contains('gapFree_0001')) & (des_df.peakv_idx > (20000 * 125)) & (des_df.peakv_idx < (20000 * 225))
afterdrug_events = (des_df.file_origin.str.contains('gapFree_withSulpirideWashout_0000')) & (des_df.peakv_idx > (20000 * 125)) & (des_df.peakv_idx < (20000 * 225))
larger_events = des_df.amplitude > 0.55
beforedrug_events = beforedrug_events & larger_events
afterdrug_events = afterdrug_events & larger_events
# singleneuron_data.plot_rawdatablocks('gapFree_0001', 'gapFree_withSulpirideWashout_0000',
#                                      events_to_mark=(beforedrug_events | afterdrug_events))

singleneuron_data.scatter_depoleventsgroups_overlayed('rise_time_10_90', 'amplitude',
                                                      plt_title='events from 100s representative spont.activity',
                                                      before_drug=beforedrug_events, after_drug=afterdrug_events)

des_df[beforedrug_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev',],
                                bins=nbins)
plt.suptitle('parameter distributions of events before drug')

des_df[afterdrug_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev',],
                                bins=nbins)
plt.suptitle('parameter distributions of events after drug')

des_df[beforedrug_events].amplitude.mean()
des_df[afterdrug_events].amplitude.mean()

# a case could be made that events with amp >2mV occur only in the presence of drug;
# however, these events are very few and far between (4 in 100s) and it looks like that's
# far from frequent enough to change the statistics of the depolarizing events population.

# %% sorting through extracted depolarizing events
# %% part 0: checking that automatic labeling of events went right
# APs
# current pulse changes
# light-evoked events
# %% part 1: labeling obvious noise-events as such

des_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev',],
                                bins=nbins)
plt.suptitle('parameter distributions of all events')

des_df[unlabeled_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev',],
                                bins=nbins)
plt.suptitle('parameter distributions of all unlabeled events')

singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'width_50', cmeasure='baselinev',
                                                      unlabeled_events=unlabeled_events)
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80', cmeasure='baselinev',
                                                      unlabeled_events=unlabeled_events)

# let's check out the cloud of events with amp>30mV
