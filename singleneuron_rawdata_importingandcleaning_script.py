"""
In this script: importing raw data recorded from individual neurons,
and cleaning away any non-recording blocks/channels
"""
import matplotlib.pyplot as plt
from singleneuron_class import SingleNeuron
# %% recordings done by me on the Smith lab rig
# %%
cell20191124B = SingleNeuron('20191124B')
# cell20191124B.plot_allrawdata(time_axis_unit='s')
cell20191124B.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
cell20191124B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=18)
# cell20191124B.plot_blocks_byname('spikePulse_0002.abf', segments_overlayed=False)
cell20191124B.rawdata_remove_nonrecordingsection('spikePulse_0002.abf', segment_idx=16)
# cell20191124B.plot_allrawdata()
cell20191124B.write_results()
# %%
cell20191124C = SingleNeuron('20191124C')
cell20191124C.plot_allrawdata()
# not a good recording

# %%
cell20200102A = SingleNeuron('20200102A')
cell20200102A.plot_allrawdata(time_axis_unit='s')
cell20200102A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=52)
cell20200102A.rawdata_remove_nonrecordingblock('light_wideField_0000.abf')
cell20200102A.write_results()

# %%
cell20200102B = SingleNeuron('20200102B')
cell20200102B.plot_allrawdata(time_axis_unit='s')
cell20200102B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=19)
cell20200102B.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=359)
cell20200102B.write_results()

# %%
cell20200102C = SingleNeuron('20200102C')
cell20200102C.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
cell20200102C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=6)
cell20200102C.plot_allrawdata(time_axis_unit='s')
cell20200102C.write_results()

# %%
cell20200106A = SingleNeuron('20200106A')
cell20200106A.plot_allrawdata(time_axis_unit='s')
# single file of dual-channel recording with neither channel recording something patched

# %%
cell20200106B = SingleNeuron('20200106B')
cell20200106B.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
cell20200106B.rawdata_remove_nonrecordingblock('gapFree_0001.abf')  # the first two files in this folder were bad patches
cell20200106B.rawdata_remove_nonrecordingsection('gapFree_0002.abf', trace_start_t=42)
cell20200106B.plot_allrawdata(time_axis_unit='s')
cell20200106B.write_results()

# %%
cell20200106C = SingleNeuron('20200106C')
# cell20200106C.plot_allrawdata(time_axis_unit='s')
cell20200106C.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
cell20200106C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=6)
cell20200106C.rawdata_remove_nonrecordingchannel('gapFree_0001.abf', 1)
cell20200106C.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=41)
cell20200106C.write_results()

# %%
cell20200106D = SingleNeuron('20200106D')
cell20200106D.plot_allrawdata(time_axis_unit='s')
cell20200106D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=21)  # before that is seal formation
cell20200106D.plot_blocks_byname('gapFree_0000.abf')
cell20200106D.plot_blocks_byname('shortPulse_0003.abf', segments_overlayed=False)
cell20200106D.rawdata_remove_nonrecordingblock('shortPulse_0003.abf')  # neuron was basically dead at this point
cell20200106D.write_results()






# %% recordings done by me on the nRiM lab rig
# moved to "evokedsynapticexcitation" importing script
