"""
In this script: importing raw data recorded from individual neurons,
and cleaning away any non-recording blocks/channels
"""
import matplotlib.pyplot as plt
from singleneuron_class import SingleNeuron
#%% nRiM rig recordings done by me
#%%
cell20200306A = SingleNeuron('20200306A')
# cell20200306A.plot_allrawdata()
# cell20200306A.save_rawdata_settings()

cell20200306B = SingleNeuron('20200306B') #just one block with some spontaneous activity, then it died
cell20200306B.rawdata_remove_nonrecordingblock('R2_spontactivity_CCmode')

cell20200306C = SingleNeuron('20200306C') #lots of data, one block with lightpulses

cell20200307A = SingleNeuron('20200307A') #spont activity and long-pulses

#20200307B - not a single block gets imported... It's a very small file so probably no real data there anyway, but still, it's weird and should see what's up with that at some point

cell20200308A = SingleNeuron('20200308A') #spont activity and long-pulses

cell20200308B = SingleNeuron('20200308B') #bunch of lighttriggered but no long-pulses

cell20200308C = SingleNeuron('20200308C') #some spont.activity and one lighttriggered block

cell20200308D = SingleNeuron('20200308D') #some spont.activity and a single light pulse

cell20200308E = SingleNeuron('20200308E') #spont. and light-triggered activity
cell20200308E.rawdata_remove_nonrecordingblock('R10_spontactivity_CCmode')

cell20200308F = SingleNeuron('20200308F') #some spont.activity

# cell20200310A = SingleNeuron('20200310A') #!!not an olive cell; some spont.activity

# cell20200310B = SingleNeuron('20200310B') #!!not an olive cell; some spont.activity and long-pulses

cell20200310C = SingleNeuron('20200310C') #spont.activity and long-pulses

cell20200310D = SingleNeuron('20200310D')

cell20200310E = SingleNeuron('20200310E')

cell20200310F = SingleNeuron('20200310F')

# cell20200310G = SingleNeuron('20200310G') - this is the problematic one, where we can't seem to get the filesystem out

cell20200312A = SingleNeuron('20200312A') #this cell has a little more data recorded post-software-crash; has a couple more fast-events there even though it lost >10mV of its resting

cell20200312B = SingleNeuron('20200312B')

cell20200312C = SingleNeuron('20200312C')

# 20200312D juxtacellular more than intracellular recording

# 20200312E - another one of those where not a single block gets imported

cell20200312F = SingleNeuron('20200312F')
cell20200312F.rawdata_remove_nonrecordingblock('R1_spontactivity_CCmode') #a block got imported but doesn't seem to contain any data at all

cell20200312G = SingleNeuron('20200312G')