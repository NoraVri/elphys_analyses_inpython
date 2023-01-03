# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221227E'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# decent enough recording starting out at baselineV ~-50mV, AP peakV almost +50mV;
# according to experiment day notes, cell clearly labeled in QX-color as well by just 15 minutes into recording
# Electrical stimulation device ran out of battery at some point, got replaced

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)



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
# aps_evokedbyttl = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: debatable whether current pulses continue to elicit APs; but I definitely didn't see anything getting picked up that wasn't on currentpulse.
# aps_evokedbyttl: yup, anything AP-like that's sitting on ttl got picked up now that negative ttl also gets recognized by my algorithm (change to snafs where TTLon is determined)
# aps_spont: just one that got picked up as such, but really it's evoked by the electricalStim (can tell from the artefact that precedes it, and the fact that I was clearly playing with the 'one shot' button in this stretch of recording).
# Re-labeling it as such:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(aps_oncurrentpulsechange, #aps_evokedbyttl,  #aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=50,
#                                    prealignpoint_window_inms=20,
#                                    do_baselining=False,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# singleneuron_data.plot_depolevents(aps_oncurrentpulsechange, #aps_evokedbyttl,  #aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=50,
#                                    prealignpoint_window_inms=20,
#                                    do_baselining=False,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )


