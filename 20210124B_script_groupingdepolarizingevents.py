# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124B'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# pretty boring neuron for the most part, has some spikelets and just one spont. fast-event as far as my eye
# could see (~5mV). Not an overly noisy recording for the most part, but picking up events <1mV amp seems silly
# (things that clearly look like spikelets are larger than that). Other than that, default parameters will do.

# block_no = 0
# segment_no = 0
# time_slice = [4, 154]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# # this neuron doesn't have any spont.APs, only ones driven by huge +DC (no discernible AHP)
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
# singleneuron_data.write_results()

# following extraction, I was clearly wrong about this neuron having just one fast-event: there's clearly
# at least a handful of them, mostly 5-6mV and one example of 3mV, all occurring at resting baselinev. Then there's
# some more compound events (3 - 5mV amp and fast enough rise) occurring at baselinevs as low as -80.
