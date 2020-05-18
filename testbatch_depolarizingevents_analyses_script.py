# in this script: an initial batch of neurons representing all the different types of experiments
# (RubiGlu-uncaging; blocking synaptic inputs; exciting the (synaptic inputs to) the neurons).

# %% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantities as pq

from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_depolarizingevents
# %% RubiGlu-uncaging example
# %% importing the raw data for the first time and cleaning it
plt.close('all')
cell20200310G = SingleNeuron('20200310G')
# cell20200310G.plot_allrawdata()
# cell20200310G.rawdata_remove_nonrecordingsection('R21_lighttriggered_CCmode.ibw',
#                                                  segment_idx=1)
# cell20200310G.plot_blocks_byname('R21_lighttriggered_CCmode.ibw', segments_overlayed=False)
# cell20200310G.write_results()
# %% finding good (enough) parameter settings for finding depolarizing events, and then getting them
# allblocks_names = cell20200310G.get_blocknames(printing='off')
# spontactivity_blocksnames = [blockname for blockname in allblocks_names
#                              if 'spontactivity' in blockname]
# for block in spontactivity_blocksnames:
#     block_idx = allblocks_names.index(block)
#     a_segment = cell20200310G.blocks[block_idx].segments[0].time_slice(t_start=30*pq.s,
#                                                                        t_stop=50*pq.s)
#     apsdict, depolsdict = get_depolarizingevents(a_segment,
#                                                  oscfilter_lpfreq=30,
#                                                  min_depolamp=0.15,
#                                                  spikeahpwindow=125,
#                                                  plot='on')

# cell20200310G.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=30)
# cell20200310G.write_results()
# %% checking that extracted depolarizing events look OK
all_blocks = cell20200310G.get_blocknames(printing='off')
# cell20200310G.plot_blocks_byname(*all_blocks,
#                                  events_to_mark=cell20200310G.depolarizing_events)

# blocks_withspikes = list(set(cell20200310G.action_potentials.file_origin))
# cell20200310G.plot_blocks_byname(*blocks_withspikes,
#                                  events_to_mark=cell20200310G.action_potentials)
spontactivity_blocks = [block for block in all_blocks if 'spont' in block]
# cell20200310G.plot_blocks_byname(*spontactivity_blocks,
#                                  events_to_mark=cell20200310G.depolarizing_events)

# %% taking a look at all the events by their measurements
cell20200310G.depolarizing_events.plot.scatter(x='rise_time',
                                               y='amplitude',
                                               c='half_width',
                                               colormap='viridis')
plt.suptitle('all detected events')

cell20200310G.depolarizing_events.plot.scatter(x='edtrace_rise_time',
                                               y='edtrace_amplitude',
                                               c='edtrace_half_width',
                                               colormap='viridis')
plt.suptitle('all detected events')

cell20200310G.depolarizing_events.plot.scatter(x='rise_time',
                                               y='amplitude',
                                               c='baselinev',
                                               colormap='viridis')
plt.suptitle('all detected events')

# %% getting only events from the cleanest (parts of), longest traces for (initial) analyses
# plt.close('all')
# i = 3
# cell20200310G.plot_eventdetecttraces_forsegment(all_blocks.index(spontactivity_blocks[i]),0)

# %%
sliceendtime = 295 # seconds; after this time the phase as gotten from the hilbert-transform looks messed-up
sliceendidx = (float(cell20200310G.blocks[
                        all_blocks.index(spontactivity_blocks[0])].segments[0].analogsignals[0].sampling_rate)
               * sliceendtime)
cleansegment1_events = ((cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[0])
                    & (cell20200310G.depolarizing_events.baselinev_idx < sliceendidx))
cleansegment2_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[1])
# ! In this following segment, 'leftovers' of oscillations/dendritic spiking are consistently
# picked up as events of ~1 - 1.5 mV. It is also the one spontactivity recording before bath-application of RubiGlu.
cleansegment3_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[2])
# ! In this following segment, RubiGlu reaches the bath after ~10 min. (no qualitative change in behavior, in my eyes.)
cleansegment4_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[3])

cleansegments_events = (cleansegment1_events | cleansegment2_events | cleansegment3_events | cleansegment4_events)

# %% taking a look at event-measures distributions
cell20200310G.depolarizing_events[cleansegments_events].plot.scatter(x='rise_time',
                                                                     y='amplitude',
                                                                     c='half_width',
                                                                     colormap='viridis')
plt.suptitle('events detected in spont.activity traces')
cell20200310G.depolarizing_events[cleansegments_events].plot.scatter(x='edtrace_rise_time',
                                                                     y='edtrace_amplitude',
                                                                     c='edtrace_half_width',
                                                                     colormap='viridis')
plt.suptitle('events detected in spont.activity traces')

# %% from the ed-trace scatter there is clearly a group of fast-events: rise-time < 1ms, amp > 1mV (both raw and ed)
fastevents = ((cell20200310G.depolarizing_events.edtrace_rise_time < 1)
              & (cell20200310G.depolarizing_events.edtrace_amplitude > 1)
              & (cell20200310G.depolarizing_events.baselinev < -30))

# plotting the events themselves, baselined, colored by baselinev
cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
                                         do_baselining=True,
                                         colorby_measure='baselinev')
cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         get_measures_type='edtrace')

# seeing the histogram of event amplitudes:
# (there should be clear peaks for distinct groups)
bins_sequence = np.arange(0, int(cell20200310G.depolarizing_events.amplitude.max() + 1), 0.25)

cell20200310G.depolarizing_events[cleansegments_events & fastevents].hist('amplitude',
                                                                          bins=bins_sequence)
plt.suptitle('fast events from clean data')

# seeing the normalized waveform:
# (the waveforms should be identical, though lower baselinev should lead to slower decay)
cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
                                         do_baselining=True,
                                         do_normalizing=True,
                                         colorby_measure='baselinev')

# seeing the relationship between rise-time and half-width:
# (there should be no relationship, though lower baselinev should lead to increased half-width)
cell20200310G.depolarizing_events[cleansegments_events
                                  & fastevents].plot.scatter(x='rise_time',
                                                             y='half_width',
                                                             c='baselinev',
                                                             colormap='viridis')

# %% generalizing to all data
# plotting the events themselves, baselined, colored by baselinev
cell20200310G.plot_depolevents_overlayed((fastevents),
                                         do_baselining=True,
                                         colorby_measure='baselinev')
cell20200310G.plot_depolevents_overlayed((fastevents),
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         get_measures_type='edtrace')

# seeing the histogram of event amplitudes:
# (there should be clear peaks for distinct groups)
cell20200310G.depolarizing_events[fastevents].hist('amplitude',
                                                   bins=bins_sequence)

# seeing the normalized waveform:
# (the waveforms should be identical, though lower baselinev should lead to slower decay)
cell20200310G.plot_depolevents_overlayed((fastevents),
                                         do_baselining=True,
                                         do_normalizing=True,
                                         colorby_measure='baselinev')

# seeing the relationship between rise-time and half-width:
# (there should be no relationship, though lower baselinev should lead to increased half-width)
cell20200310G.depolarizing_events[fastevents].plot.scatter(x='rise_time',
                                                           y='half_width',
                                                           c='baselinev',
                                                           colormap='viridis',
                                                           title='fast events from all data')


# %% don't forget about looking at things relative to oscs eventually
# cell20200310G.depolarizing_events[cleansegments_events & fastevents].hist('approx_oscinstphase',
#                                                                           bins=20,
#                                                                           range=[-3.2, 3.2])



