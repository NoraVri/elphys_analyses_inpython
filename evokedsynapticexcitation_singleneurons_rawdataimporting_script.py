# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
# %% experiment: RubiGlu-uncaging

# cell20200306A = SingleNeuron('20200306A')
# # cell died between run 10 and 11, yet for some reason 28 runs were recorded altogether
# cell20200306A_allrunsnames = cell20200306A.get_blocknames(printing='off')
# for i in range(11,29):
#     runtoexclude = 'R'+str(i)
#     fullrunname = [name for name in cell20200306A_allrunsnames
#                    if name.startswith(runtoexclude)][0]
#     cell20200306A.rawdata_remove_nonrecordingblock(fullrunname)
# cell20200306A.write_results()
#
# cell20200306B = SingleNeuron('20200306B')
# #just one block with some spontaneous activity, then it died
# cell20200306B.rawdata_remove_nonrecordingblock('R2_spontactivity_CCmode')
# cell20200306B.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=288)
# cell20200306B.write_results()

cell20200306C = SingleNeuron('20200306C')  # lots of data, one block with lightpulses
# # cell started doing badly in R13, then finally died all the way during R16
# cell20200306C.rawdata_remove_nonrecordingblock('R13_longpulses_CCmode')  # single pulse, V cut off at -100 mV
# cell20200306C.rawdata_remove_nonrecordingblock('R15_longpulses_CCmode')  # some of the traces in this block are actually OK, just don't feel like plotting them separately right now
# cell20200306C.rawdata_remove_nonrecordingsection('R16_spontactivity_CCmode',
#                                                  trace_end_t=200)
# cell20200306C.write_results()

# cell20200307A = SingleNeuron('20200307A')  # spont activity and long-pulses

# cell20200307B = SingleNeuron('20200307B')
# not a single block gets imported... It's a very small file so probably no real data there anyway, but still, it's weird and should see what's up with that at some point

# cell20200308A = SingleNeuron('20200308A')  # spont activity and some long-pulses (but cell was basically dying already)
# cell20200308A.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308A.write_results()

cell20200308B = SingleNeuron('20200308B')  # bunch of lighttriggered but no long-pulses; Vrest bad by the end but keeping trace nonetheless

cell20200308C = SingleNeuron('20200308C')  # some spont.activity and one lighttriggered block
# # cell thoroughly dead by the end
# cell20200308C.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308C.write_results()

cell20200308D = SingleNeuron('20200308D')  # some spont.activity and a single light pulse
# cell20200308D.rawdata_remove_nonrecordingblock('R3_lighttriggered_CCmode')
# cell20200308D.write_results()

cell20200308E = SingleNeuron('20200308E')  # spont. and light-triggered activity
# cell20200308E.rawdata_remove_nonrecordingblock('R10_spontactivity_CCmode')
# cell20200308E.write_results()

# cell20200308F = SingleNeuron('20200308F')  # a bit of spont.activity
# cell20200308F.rawdata_remove_nonrecordingblock('R1_spontactivity_CCmode')
# cell20200308F.write_results()

# cell20200310A = SingleNeuron('20200310A') #!!not an olive cell; some spont.activity

# cell20200310B = SingleNeuron('20200310B') #!!not an olive cell; some spont.activity and long-pulses

# cell20200310C = SingleNeuron('20200310C')  # spont.activity and long-pulses, lots of fast-events

# cell20200310D = SingleNeuron('20200310D')  # has some spont.activity with fast-events, but long-pulse responses look completely passive

# cell20200310E = SingleNeuron('20200310E')  # not a good recording at all

# cell20200310F = SingleNeuron('20200310F')  # a tiny bit of spont.activity
# cell20200310F.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',trace_end_t=74)
# cell20200310F.write_results()

cell20200310G = SingleNeuron('20200310G')  # the single greatest cell with light
# cell20200310G.rawdata_remove_nonrecordingsection('R21_lighttriggered_CCmode.ibw',
#                                                  segment_idx=1)
# cell20200310G.write_results()

cell20200312A = SingleNeuron('20200312A')  # this cell has a little more data recorded post-software-crash; has a couple more fast-events there even though it lost >10mV of its resting

cell20200312B = SingleNeuron('20200312B')

cell20200312C = SingleNeuron('20200312C')

# 20200312D juxtacellular more than intracellular recording

# 20200312E - another one of those where not a single block gets imported

cell20200312F = SingleNeuron('20200312F')
# cell20200312F.rawdata_remove_nonrecordingblock('R1_spontactivity_CCmode')  # a block got imported but doesn't seem to contain any data at all

cell20200312G = SingleNeuron('20200312G')