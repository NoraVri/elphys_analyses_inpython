import numpy as np
import quantities as pq
import matplotlib.pyplot as plt
import pandas as pd

from singleneuron_class import SingleNeuron
# %%
cell20190805A1 = SingleNeuron('20190805A1')
# all_blocks = cell20190805A1.get_blocknames(printing='off')
# recording_block = all_blocks[0]
# nonrecording_blocks = all_blocks[1:]
# for block in nonrecording_blocks:
#     cell20190805A1.rawdata_remove_nonrecordingblock(block)
# cell20190805A1.rawdata_remove_nonrecordingchannel(recording_block,2)
#
# cell20190805A1.plot_allrawdata()
# cell20190805A1.rawdata_remove_nonrecordingtimeslice(recording_block,trace_start_t=11,
#                                                     trace_end_t=38.5)
# cell20190805A1.get_depolarizingevents_fromrawdata()
# cell20190805A1.write_results()
# %%
cell20190805A2 = SingleNeuron('20190805A2')
cell20190805A2.plot_depolevents_overlayed(get_subthreshold_events=False,
                                          do_baselining=True,
                                          colorby_measure='baselinev')
cell20190805A2.plot_depolevents_overlayed(cell20190805A2.depolarizing_events.amplitude > 3,
                                          do_baselining=True,
                                          colorby_measure='baselinev')
# all_blocks = cell20190805A2.get_blocknames(printing='off')
# nonrecording_block = all_blocks[0]
# recording_blocks = all_blocks[1:]
# cell20190805A2.rawdata_remove_nonrecordingblock(nonrecording_block)
# cell20190805A2.rawdata_remove_nonrecordingchannel(recording_blocks[0],1)
#
# cell20190805A2.plot_allrawdata(time_axis_unit='s')
# cell20190805A2.rawdata_remove_nonrecordingtimeslice(recording_blocks[0],trace_start_t=12.7)
# cell20190805A2.rawdata_note_chemicalinbath('withBlocker')
# cell20190805A2.get_depolarizingevents_fromrawdata()