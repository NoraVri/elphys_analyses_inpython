# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# %%
cell20190131B1 = SingleNeuron('20190131B1')
cell20190131B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing the channel B1 is not recorded on:
for blockname in cell20190131B1.get_blocknames(printing='off'):
    cell20190131B1.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# removing seal formation:
cell20190131B1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=616)
cell20190131B1.write_results()

# %%
cell20190131B2 = SingleNeuron('20190131B2')
# raw data cleanup:
# removing the channel B1 is not recorded on:
for blockname in cell20190131B2.get_blocknames(printing='off'):
    cell20190131B2.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
cell20190131B2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# removing seal formation:
cell20190131B2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=7.5)
# This neuron's a pretty nice recording initially (though some changes in the seal while the other neuron is getting patched),
# but then the seal goes bad during the last IV file (IV3); neuron kind of comes back during gapFree6, but looks like a partial break-in.
# removing all the parts where recording was more extracellular than intracellular:
cell20190131B2.rawdata_remove_nonrecordingblock('IV_0003.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0003.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0004.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0005.abf')
cell20190131B2.rawdata_remove_nonrecordingblock('gapFree_0006.abf')
cell20190131B2.write_results()

# %%
cell20190131C1 = SingleNeuron('20190131C1')
# very nice recording; no -DC current applied to keep baselineV in range and AP amp also quite stable
# raw data cleanup:
# removing the channel B1 is not recorded on:
for blockname in cell20190131C1.get_blocknames(printing='off'):
    cell20190131C1.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
cell20190131C1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# removing block where nothing is being recorded:
cell20190131C1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing seal formation:
cell20190131C1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=15)
cell20190131C1.write_results()

# %%
cell20190131C2 = SingleNeuron('20190131C2')
# nice long recording, though deteriorating over time - APs losing their Na-component at some point and baselinev deteriorating badly towards the end.
# Has intermittent wobbles of oscs, some fast-events and some fast-ish event that persists even after Na seems lost...
# raw data cleanup:
# removing the channel B1 is not recorded on:
for blockname in cell20190131C2.get_blocknames(printing='off'):
    cell20190131C2.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
cell20190131C2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# removing seal formation:
cell20190131C2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=5)
cell20190131C2.write_results()

# %%
cell20190206A1 = SingleNeuron('20190206A1')
# dual recording throughout, though by eye no evidence of coupling
# recording quality deteriorating a bit towards the end, but nice enough overall
blocknameslist = cell20190206A1.get_blocknames(printing='off')
for block in blocknameslist:
    cell20190206A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
cell20190206A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing block where cell is not being recorded yet:
cell20190206A1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing seal formation:
cell20190206A1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=49)
cell20190206A1.write_results()

# %%
cell20190206A2 = SingleNeuron('20190206A2')
cell20190206A2.plot_rawdatablocks(segments_overlayed=False)
# dual recording throughout, though by eye no evidence of coupling
# neuron not doing much of anything interesting; has a few events that could be fast-events or something else
# raw data cleanup:
# removing the non-recording channel:
blocknameslist = cell20190206A2.get_blocknames(printing='off')
for block in blocknameslist:
    cell20190206A2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing seal formation:
cell20190206A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=10.3)
cell20190206A2.write_results()

# %%
cell20190319A1 = SingleNeuron('20190319A1')
# dual recording only in gapFree files, all other files belong to A1 according to notes
# pretty neat recording, stable vrest and AP amp throughout (though not much of anything interesting happening overall)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
gapFreeblocks = cell20190319A1.get_blocknames(printing='off')[0:4]
for block in gapFreeblocks:
    cell20190319A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing seal formation:
cell20190319A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=732)
cell20190319A1.write_results()

# %%
cell20190319A2 = SingleNeuron('20190319A2')
# dual recording only in gapFree files, all other files belong to A1 according to notes
# nice enough recording with not much going on besides some fast-events until neuron dies (events stop coming suddenly)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
gapFreeblocks = cell20190319A2.get_blocknames(printing='off')[0:4]
for block in gapFreeblocks:
    cell20190319A2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing recording files not beloning to this neuron:
blocks_toremove = cell20190319A2.get_blocknames(printing='off')[4:]
for block in blocks_toremove:
    cell20190319A2.rawdata_remove_nonrecordingblock(block)
# removing parts of the recording where neuron is no longer alive:
cell20190319A2.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=125)
cell20190319A2.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
cell20190319A2.rawdata_remove_nonrecordingblock('gapFree_0003.abf')
cell20190319A2.write_results()

# %%
cell20190319C1 = SingleNeuron('20190319C1')
# dual recording throughout, but this recording seems to suffer from some electrode drift from time to time
# Vrest deteriorating badly towards the end (-DC to keep in range), but overall looks like an alright recording
cell20190319C1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190319C1.get_blocknames(printing='off'):
    cell20190319C1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing block where neuron is not yet being recorded from:
cell20190319C1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing seal formation:
cell20190319C1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=12)
cell20190319C1.write_results()

# %%
cell20190319C2 = SingleNeuron('20190319C2')
# dual recording throughout
# neuron not very happy initially, but settles into steady oscillating behavior not too long into the recording.
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190319C2.get_blocknames(printing='off'):
    cell20190319C2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
cell20190319C2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# removing seal formation:
cell20190319C2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=20)
cell20190319C2.write_results()

# %%
# cell20190325A1 = SingleNeuron('20190325A1')

# %%
# cell20190325A2 = SingleNeuron('20190325A2')

# %%
cell20190325B1 = SingleNeuron('20190325B1')
cell20190325B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# neuron dies suddenly not too long after getting patched. It's held with lots of -DC for longer, but its time of death is really clear so I will remove that.
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190325B1.get_blocknames(printing='off'):
    cell20190325B1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing seal formation and recording time where the neuron is dead:
cell20190325B1.rawdata_remove_nonrecordingsection('gapFree_0002.abf', trace_start_t=7, trace_end_t=387)
cell20190325B1.rawdata_remove_nonrecordingblock('gapFree_0003.abf')
cell20190325B1.rawdata_remove_nonrecordingblock('shortPulse_0000.abf')
cell20190325B1.write_results()

# %%
cell20190325B2 = SingleNeuron('20190325B2')
# not the healthiest neuron, but keeps a decent baselineV without -DC throughout
cell20190325B2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190325B2.get_blocknames(printing='off'):
    cell20190325B2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
cell20190325B2.write_results()

# %% !not an olive neuron!
cell20190325C1 = SingleNeuron('20190325C1')
# has lots of depolarizing events that may or may not be like the IO-neuron fast-events (up to ~5mV amp)
cell20190325C1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190325C1.get_blocknames(printing='off'):
    cell20190325C1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing seal formation:
cell20190325C1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=718)
# removing end of recording where cell got killed:
cell20190325C1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=200)
cell20190325C1.write_results()

# %% !not an olive neuron!
cell20190325C2 = SingleNeuron('20190325C2')
# not the greatest recording initially, but quite nice and steady once the other neuron is patched, too.
# has lots of depolarizing events that may or may not be like the IO-neuron fast-events (up to ~5mV amp)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190325C2.get_blocknames(printing='off'):
    cell20190325C2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing seal formation:
cell20190325C2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=7)
cell20190325C2.write_results()

# %%
cell20190325D1 = SingleNeuron('20190325D1')
# nothing actually patched on this electrode
cell20190325D1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing all blocks
for block in cell20190325D1.get_blocknames(printing='off'):
    cell20190325D1.rawdata_remove_nonrecordingblock(block)
cell20190325D1.write_results()
# %%
cell20190325D2 = SingleNeuron('20190325D2')
# very boring-looking neuron recording, not doing much of anything (though did see some depolarizing events, spikelets most likely)
# raw data cleanup:
# removing extra channel from the first block:
cell20190325D2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
# removing seal formation:
cell20190325D2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=4)
cell20190325D2.write_results()

# %%
cell20190331A1 = SingleNeuron('20190331A1')
# spont.break-in from not quite 1G seal and recording conditions are obviously not great initially, improve over the
# first 5 min. of intracellular recording, but then baselinev starts steadily deteriorating and is held in range with lots of -DC by the end
cell20190331A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190331A1.get_blocknames(printing='off'):
    cell20190331A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing seal formation/break-in:
cell20190331A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=1075)
# removing parts of the recording where cell totally is no longer there despite -DC (happens quite suddenly):
cell20190331A1.rawdata_remove_nonrecordingsection('shortPulse_0000.abf', remove_segments=[20, 21])
cell20190331A1.rawdata_remove_nonrecordingblock('shortPulse_0001.abf')
cell20190331A1.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
cell20190331A1.write_results()
# %%
cell20190331A2 = SingleNeuron('20190331A2')
# really nice recording for ~5min., then conditions become very variable and neuron is barely hanging on by the end.
cell20190331A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190331A2.get_blocknames(printing='off'):
    cell20190331A2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
cell20190331A2.write_results()


# %%
# cell20190331B1 = SingleNeuron('20190331B1')
# nothing actually patched
# %%
# cell20190331B2 = SingleNeuron('20190331B2')
# nothing actually patched
# %%
# cell20190331C1 = SingleNeuron('20190331C1')

# %%
# cell20190331C2 = SingleNeuron('20190331C2')

# %%
# cell20190331D1 = SingleNeuron('20190331D1')

# %%
# cell20190331D2 = SingleNeuron('20190331D2')


# %%
cell20190401A1 = SingleNeuron('20190401A1')
# looks like neuron may be losing its Na-currents towards the end, but other than that it's a very nice recording with
# everything - oscillations, APs, fast-events, ZAPs, steady baselinev for the most part.
cell20190401A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing non-recording channel from files recorded in dual-patch mode:
for block in cell20190401A1.get_blocknames(printing='off')[0:3]:
    cell20190401A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=False)
# removing file where neuron is not actually recorded yet:
cell20190401A1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing seal formation:
cell20190401A1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=6)
cell20190401A1.write_results()
# %%
cell20190401A2 = SingleNeuron('20190401A2')
# nothing actually recorded.
# raw data cleanup:
# removing all blocks:
for block in cell20190401A2.get_blocknames(printing='off'):
    cell20190401A2.rawdata_remove_nonrecordingblock(block)
cell20190401A2.write_results()

# %%
cell20190401B1 = SingleNeuron('20190401B1')
# nice recording for the most part; losing resting potential a bit throughout, faster at the end of recordings.
# very active in the first 10min. or so of recording, then stops doing APs and fast-events (still mostly oscillating though).
cell20190401B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
cell20190401B1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2, pairedrecording=False) # the other neuron is basically dead by the time this one gets patched
# removing seal formation/break-in:
cell20190401B1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=323)
cell20190401B1.write_results()
# %%
cell20190401B2 = SingleNeuron('20190401B2')
# neuron recorded only for a little bit, pretty much dies as the other one gets patched
# raw data cleanup:
# removing recording channel not beloning to this neuron:
cell20190401B2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1, pairedrecording=False)
# removing all the blocks where this neuron is not being recorded:
for block in cell20190401B2.get_blocknames(printing='off')[1:]:
    cell20190401B2.rawdata_remove_nonrecordingblock(block)
# removing seal formation and part of the recording where neuron is definitely all dead:
cell20190401B2.rawdata_remove_nonrecordingsection('gapFree_0000.abf',trace_start_t=15, trace_end_t=861)
cell20190401B2.write_results()
# %%
# cell20190401C1 = SingleNeuron('20190401C1')

# %%
# cell20190401C2 = SingleNeuron('20190401C2')

# %%
# cell20190401D1 = SingleNeuron('20190401D1')

# %%
# cell20190401D2 = SingleNeuron('20190401D2')

# %%
cell20190402A1 = SingleNeuron('20190402A1')
# long, but very boring recording - neuron can be made to spike with DC and it's getting spikelets, but that's all.
cell20190402A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing second recording channel from blocks that have it:
cell20190402A1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
cell20190402A1.rawdata_remove_nonrecordingchannel('gapFree_0001.abf', 2)
# removing termination of recording:
cell20190402A1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=330)
cell20190402A1.write_results()
# %%
cell20190402A2 = SingleNeuron('20190402A2')
# never actually got patched, just juxtacellular recording of neuron spiking a bunch.
# raw data cleanup:
# removing all blocks:
for block in cell20190402A2.get_blocknames(printing='off'):
    cell20190402A2.rawdata_remove_nonrecordingblock(block)
cell20190402A2.write_results()

# %%
# cell20190402B1 = SingleNeuron('20190402B1')

# %%
# cell20190402B2 = SingleNeuron('20190402B2')

# %%
# cell20190402C1 = SingleNeuron('20190402C1')

# %%
# cell20190402C2 = SingleNeuron('20190402C2')

# %%
# cell20190408A1 = SingleNeuron('20190408A1')

# %%
# cell20190408A2 = SingleNeuron('20190408A2')

# %%
# cell20190408B1 = SingleNeuron('20190408B1')

# %%
# cell20190408B2 = SingleNeuron('20190408B2')

# %%
# cell20190408C1 = SingleNeuron('20190408C1')

# %%
# cell20190408C2 = SingleNeuron('20190408C2')

# %%
cell20190409A1 = SingleNeuron('20190409A1')
# nice long recording with neuron oscillating throughout; however, it is losing baselinev towards the end, and it
# looks like the neuron may have lost all its active properties way before that already
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190409A1.get_blocknames(printing='off'):
    cell20190409A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing block where the neuron is not yet being recorded:
cell20190409A1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
cell20190409A1.write_results()

# %%
cell20190409A2 = SingleNeuron('20190409A2')
# never that great a cell, holding with lots of -DC for most of recordings. But since it was never that alive to begin with
# I can't point to any moment where it dies, and it does keep getting spikelets so I'll keep the recording.
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190409A2.get_blocknames(printing='off'):
    cell20190409A2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing seal formation:
cell20190409A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=7)
cell20190409A2.write_results()

# %%
cell20190409B1 = SingleNeuron('20190409B1')
# died pretty soon after getting patched, losing ~20mV vrest in just a few seconds
cell20190409B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190409B1.get_blocknames(printing='off'):
    cell20190409B1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing block where neuron is not yet being recorded:
cell20190409B1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing all blocks where neuron is dead already:
for block in cell20190409B1.get_blocknames(printing='off')[1:]:
    cell20190409B1.rawdata_remove_nonrecordingblock(block)
# removing the part of the recording where neuron dies:
cell20190409B1.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=720)
cell20190409B1.write_results()
# %%
cell20190409B2 = SingleNeuron('20190409B2')
# long recording of a neuron oscillating wackily (steadily, and doing not much of anything else)
# neuron loses ~15mV restingV quite suddenly in the last recording file, but recording is terminated before it dies.
cell20190409B2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron (it's there in every block except shortPulse):
for block in cell20190409B2.get_blocknames(printing='off'):
    if 'shortPulse' in block:
        continue
    else:
        cell20190409B2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing seal formation:
cell20190409B2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=7)
cell20190409B2.write_results()

# %%
cell20190410A1 = SingleNeuron('20190410A1')
# this neuron is only being recorded for about 2 minutes before it gives up on maintaining restingV pretty quickly; gets held with lots of -DC.
# Keeps doing fast-events though until -DC is removed, and has a handful each of APs, fast-events and spikelets before it dies
cell20190410A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing all blocks in which this neuron is no longer being held in range:
for block in cell20190410A1.get_blocknames(printing='off')[2:12]:
    cell20190410A1.rawdata_remove_nonrecordingblock(block)
# removing the recording channel not belonging to this neuron:
for block in cell20190410A1.get_blocknames(printing='off'):
    cell20190410A1.rawdata_remove_nonrecordingchannel(block, 2, pairedrecording=True)
# removing the block where neuron is not yet being recorded from:
cell20190410A1.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
cell20190410A1.write_results()

# %%
cell20190410A2 = SingleNeuron('20190410A2')

cell20190410A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing the recording channel not belonging to this neuron, from those blocks that have it:
for block in cell20190410A2.get_blocknames(printing='off'):
    if 'shortPulse' in block:
        continue
    else:
        cell20190410A2.rawdata_remove_nonrecordingchannel(block, 1, pairedrecording=True)
# removing seal formation:
cell20190410A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=11)
cell20190410A2.write_results()

# %%
# cell20190410B1 = SingleNeuron('20190410B1')

# %%
# cell20190410B2 = SingleNeuron('20190410B2')

# %%
# cell20190410C1 = SingleNeuron('20190410C1')

# %%
# cell20190410C2 = SingleNeuron('20190410C2')

# %%
# cell20190513A1 = SingleNeuron('20190513A1')

# %%
# cell20190513A2 = SingleNeuron('20190513A2')

# %%
# cell20190513B1 = SingleNeuron('20190513B1')

# %%
# cell20190513B2 = SingleNeuron('20190513B2')

# %%
cell20190513C = SingleNeuron('20190513C')
# very nice stable recording until towards the end, where neuron depolarizes slowly for ~10min. then suddenly loses a lot of restingV
cell20190513C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation:
cell20190513C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=20)
# removing part of the recording where neuron starts to lose baselinev fast, and dead cell recording:
cell20190513C.rawdata_remove_nonrecordingsection('gapFree_0002.abf', trace_end_t=895)
cell20190513C.rawdata_remove_nonrecordingblock('gapFree_0003.abf')
cell20190513C.write_results()

# %%
# cell20190513D = SingleNeuron('20190513D')


# %%
cell20190527A = SingleNeuron('20190527A')
# spont.activity and light pulses
# has some tiny (~1mV) oscillations here and there, as well as a strong resonance response to activating inputs
# also, it looks like depolarizing events of intermediate amplitude are quite often followed by an after-hyperpolarization/resonance response
# raw data cleanup:
cell20190527A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# removing seal formation; everything else looks OK
cell20190527A.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
                                                 trace_start_t=21.5)
cell20190527A.write_results()

# %% no light-evoked activity recorded
# cell20190527B = SingleNeuron('20190527B')
# just a single long trace of spont.activity: some depolarizing events and spikes, no oscillations.
# cell20190527B.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_start_t=20)
# cell20190527B.rawdata_remove_nonrecordingblock('light_wholeField_0000.abf')
# cell20190527B.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20190527B.write_results()
# %%
# cell20190527C = SingleNeuron('20190527C')
# spont. activity (with fast-events) and light pulses
# in the spont. activity there's depolarizing events of ~7mV amp that seem to have a bit of a 'shoulder'
# tuning pulses can drive the voltage to +50, yet no AP is evoked ever
# activating inputs often evokes a giant (25 mV) fast-event, and in the seconds after that there's
# some oscillations and tons of spikelets (otherwise nothing much of oscillations to be seen).
# %%
cell20190529A1 = SingleNeuron('20190529A1')
cell20190529A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# notes say only A2 was good, but that's not what it looks like in the data...
# confirmed and reconfirmed: notes are wrong, it's the neuron on channel1 that's good (at least for a few blocks).
# the neuron on channel2 was patched first, but lost not long after the neuron on ch1 was patched.
# spont. activity (with fast-events and APs) and light pulses; no oscillations.
# raw data cleanup:
# removing the other channel from the one dual-recorded file:
cell20190529A1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# removing time where neuron isn't patched yet/seal formation:
cell20190529A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=285)
# removing file in which it's just the dead neuron, and then the pipette removal getting recorded
cell20190529A1.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
cell20190529A1.write_results()

# %%
cell20190529A2 = SingleNeuron('20190529A2')
cell20190529A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# this neuron was recorded in only one block, all the other blocks belong to A1. Removing those:
# raw data cleanup:
# removing blocks where this neuron is not being recorded:
blocksnames_list = cell20190529A2.get_blocknames(printing='off')
blocksnames_list.__delitem__(0)
for blockname in blocksnames_list:
    cell20190529A2.rawdata_remove_nonrecordingblock(blockname)
# removing the recording channel not belonging to this neuron:
cell20190529A2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
# removing break-in and cell death:
cell20190529A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=21, trace_end_t=582)
cell20190529A2.write_results()

# %%
cell20190529B = SingleNeuron('20190529B')
# spont.activity and lots of light pulses; few spont. depolarizations and not oscillating.
# looks like activating axonal inputs evokes big, compound fast-events.
# raw data cleanup:
# removing seal formation; rest of the data all looks alright
cell20190529B.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
                                                 trace_start_t=18)
cell20190529B.write_results()

# %%
cell20190529C = SingleNeuron('20190529C')
# pretty leaky-looking cell but has some nice spont.activity and light pulses
# not oscillating, except for one trace where it oscillates whackily for a few s following a light pulse
# raw data cleanup:
# removing seal formation:
cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
                                                 trace_start_t=28)
# removing part of a recording where the cell is dying/dead:
cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
                                                 trace_end_t=101.5)
cell20190529C.write_results()

# %%
cell20190529D = SingleNeuron('20190529D')
# nice-looking recording, spont.activity and lots of light pulses
# not oscillating, just constantly being bombarded with depolarizations
# raw data cleanup:
# removing part of a recording where the cell is dying/dead:
cell20190529D.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
                                                 trace_end_t=395)
cell20190529D.write_results()

# %%
cell20190529E = SingleNeuron('20190529E')
# spont.activity and light pulses, until cell stops responding to them
# some interesting-looking depolarizing events in spont activity; evoked they are always clearly compound
# no real oscillatory activity of any sort
# raw data cleanup:
# removing seal formation:
cell20190529E.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
                                                 trace_start_t=13)
cell20190529E.write_results()

# %%
# 0722


# %%
cell20190729A = SingleNeuron('20190729A')
cell20190729A.plot_rawdatablocks()
# intermittently oscillating at first, but stops doing that a little bit before blockers get applied.
# NOTE: blocker solution contains higher K than the regular ACSF, that's why neuron needs to be held with -DC to keep the same baselinev
# raw data cleanup:
# removing a block that's a recording of a seal onto a dead cell:
cell20190729A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# marking blocks with glu-blockers applied:
cell20190729A.rawdata_note_chemicalinbath('withBlocker')
cell20190729A.write_results()
# %%
cell20190804A = SingleNeuron('20190804A')
cell20190804A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# not oscillating but getting tons of depolarizing events at first, then depolarizing a bit and starting to oscillate once blocker solution is applied.
# if it wasn't already dead at the end, it gets killed for sure with huge -DC pulses.
# raw data cleanup:
# removing block where nothing is getting recorded yet:
cell20190804A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing recording channel that the neuron is not being recorded on:
cell20190804A.rawdata_remove_nonrecordingchannel(file_origin='gapFree_0001.abf', non_recording_channel=2)
# removing seal formation:
cell20190804A.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=14.8)
# removing final killing of the cell:
cell20190804A.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0003.abf', trace_end_t=12)
# marking blocks with glu-blockers applied:
cell20190804A.rawdata_note_chemicalinbath('withBlocker')
cell20190804A.write_results()

# %%
cell20190804B = SingleNeuron('20190804B')
cell20190804B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# fairly boring neuron (not much of any inputs or anything, though I did see at least 1 that could be a fast-event)
# and it starts to depolarize slowly but surely pretty soon after getting patched.
# raw data cleanup:
# removing seal formation:
cell20190804B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=13)
# marking blocks with glu-blocker applied:
cell20190804B.rawdata_note_chemicalinbath('withBlocker')
cell20190804B.write_results()

# %%
cell20190804C = SingleNeuron('20190804C')
cell20190804C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# fairly boring neuron, spont.break-in and not the healthiest, not sure there are any spontaneous excitations at all.
# This neuron, too, depolarizes somewhat soon after blocker application, but its basically holding on throughout.
# raw data cleanup: none to do.
cell20190804C.write_results()

# %%
cell20190805A1 = SingleNeuron('20190805A1')
cell20190805A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# it's spiking and getting tons of fast-events but slowly depolarizing, then leaves all of a sudden.
# raw data cleanup:
# removing channel that the neuron is not being recorded on:
cell20190805A1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', non_recording_channel=2)
# removing seal formation and cell death:
cell20190805A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=11, trace_end_t=386)
# removing all blocks where neuron is not being recorded:
for block in cell20190805A1.get_blocknames(printing='off')[1:]:
    cell20190805A1.rawdata_remove_nonrecordingblock(block)
cell20190805A1.write_results()

# %%
cell20190805A2 = SingleNeuron('20190805A2')
cell20190805A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# nice recording, neuron is oscillating throughout mostly with sinusoids(ish);
# not sure if it has both giant fast-events and small-ish spikes or just fast-events.
# raw data cleanup:
# removing block where neuron is not yet being recorded:
cell20190805A2.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing recording channel not belonging to this neuron:
cell20190805A2.rawdata_remove_nonrecordingchannel('gapFree_0001.abf', 1)
# removing seal formation:
cell20190805A2.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=13)
# marking blocks with glu-blocker applied:
cell20190805A2.rawdata_note_chemicalinbath('withBlocker')
cell20190805A2.write_results()

# %%
cell20190805B1 = SingleNeuron('20190805B1')
cell20190805B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# oscillating, spiking here and there, and looking like it's still getting a lot of inputs
# also after blocker application (though they're definitely only smaller ones now)
# raw data cleanup:
# removing second recording channel:
cell20190805B1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2, pairedrecording=True)
cell20190805B1.rawdata_remove_nonrecordingchannel('gapFree_withBlockers_0001.abf', 2, pairedrecording=True)
# removing part of recording where neuron is not yet being recorded, and seal formation:
cell20190805B1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=445)
# marking blocks with glu-blocker applied:
cell20190805B1.rawdata_note_chemicalinbath('withBlockers')
cell20190805B1.write_results()

# %%
cell20190805B2 = SingleNeuron('20190805B2')
# oscillating, spiking here and there, not much else of activity going on.
# raw data cleanup:
# removing channel that the neuron is not being recorded on:
cell20190805B2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1, pairedrecording=True)
cell20190805B2.rawdata_remove_nonrecordingchannel('gapFree_withBlockers_0001.abf', 1, pairedrecording=True)
# removing part of recording where neuron is way depolarized:
cell20190805B2.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0001.abf', trace_end_t=222)
# marking blocks with glu-blocker applied:
cell20190805B2.rawdata_note_chemicalinbath('withBlocker')
cell20190805B2.write_results()

# %%
cell20190806A = SingleNeuron('20190806A')
cell20190806A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# nice long recording, cell mostly just oscillating steadily
# raw data cleanup:
# removing recording channel neuron is not on:
cell20190806A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
# removing seal formation:
cell20190806A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=37)
# marking blocks with glu-blocker applied:
cell20190806A.rawdata_note_chemicalinbath('withBlocker')
cell20190806A.write_results()

# %%
cell20190812A = SingleNeuron('20190812A')
cell20190812A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# doing all the things we like IO neurons to do; beating oscillations get smaller and then diappear slowly when blocker is applied.
# raw data cleanup:
# removing second recording channel from the first block:
cell20190812A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# removing seal formation:
cell20190812A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=98)
# marking blocks with glu-blocker applied:
cell20190812A.rawdata_note_chemicalinbath('withBlocker')
cell20190812A.write_results()

# %%
cell20190812B = SingleNeuron('20190812B')
cell20190812B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# pretty boring neuron, not much of fast-events except one that's very compound
# raw data cleanup:
# removing seal formation:
cell20190812B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=25)
# marking blocks with glu-blocker applied:
cell20190812B.rawdata_note_chemicalinbath('withBlocker')
cell20190812B.write_results()

# %%
cell20190813A = SingleNeuron('20190813A')
# two different neurons recorded under this name, second turned out not to be in the IO - keeping only the IO one
# not a very good cell, bad baselinev and weird oscs and then it totally dies.
cell20190813A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing blocks where non-IO neuron is being recorded:
for block in cell20190813A.get_blocknames(printing='off')[1:]:
    cell20190813A.rawdata_remove_nonrecordingblock(block)
# removing seal formation and cell death:
cell20190813A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=13, trace_end_t=245)
cell20190813A.write_results()

# %%
cell20190814A = SingleNeuron('20190814A')
cell20190814A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# spikes and some fast-events here and there, no oscs except some tiny ripples after blocker application
# raw data cleanup:
# removing failed patch attempt recording on the second channel:
cell20190814A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# removing seal formation:
cell20190814A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=15)
# marking blocks with glu-blockers applied:
cell20190814A.rawdata_note_chemicalinbath('withBlocker')
cell20190814A.write_results()

# %%
cell20190815C = SingleNeuron('20190815C')
# neuron kinda dying from the start; w/o -DC it's resting at -30mV; can't get it to spike yet it's doing a lot of fast-events.
cell20190815C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup: - nothing to do.
cell20190815C.write_results()

# %%
cell20190815D1 = SingleNeuron('20190815D1')
# oscillating quite a lot of the time (though it looks more like rhythmic Ca-spikes when there are no blockers)
cell20190815D1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20190815D1.get_blocknames(printing='off'):
    cell20190815D1.rawdata_remove_nonrecordingchannel(block, 2)
# removing time where neuron is not patched yet:
cell20190815D1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=289)
# removing time where cell suddenly dies:
cell20190815D1.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0006.abf', trace_end_t=88)
# marking blocks with glu-blocker applied:
cell20190815D1.rawdata_note_chemicalinbath('withBlocker')
cell20190815D1.write_results()

# %%
cell20190815D2 = SingleNeuron('20190815D2')
cell20190815D2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# not actually a good recording really, being held with lots of -DC throughout just to keep some semblance of baselineV
# raw data cleanup:
# removing channel not belonging to this neuron:
for block in cell20190815D2.get_blocknames(printing='off'):
    cell20190815D2.rawdata_remove_nonrecordingchannel(block, 1)
cell20190815D2.write_results()
# %%
cell20191105A1 = SingleNeuron('20191105A1')
# Not too much exciting going on in the spontaneous activity (just a few spikes and possibly a few small-ish events)
# but also one thing that looks rather like a fast-event in one of the files with blocker.
# Not the greatest recording: most of the time neuron is being held with -200pA to keep baselineV ~-50mV,
# and looks like either bridge is somewhat variable or neuron is slowly dying over recordings (or both);
# by the end it's definitely not doing anything besides holding a baselinev with help of -DC.
cell20191105A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for blockname in cell20191105A1.get_blocknames(printing=' off'):
    cell20191105A1.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# removing seal formation:
cell20191105A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=73)
# removing the neuron's final moments:
cell20191105A1.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0002.abf', trace_end_t=443)
# noting blocks with glu-blocker in the bath:
cell20191105A1.rawdata_note_chemicalinbath('withBlocker')
cell20191105A1.write_results()

# %%
cell20191105A2 = SingleNeuron('20191105A2')
# Break-in looks strange, spont. from <G seal; it's very hard to make it spike and APamp isn't great.
# Neuron has good Vrest throughout and lots of events, though the fastest ones tend to look somehow strange... noise?
# Also the slower events can get rather sizeable (3-4mV) while still looking like GJ spikelets.
cell20191105A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for blockname in cell20191105A2.get_blocknames(printing='off'):
    cell20191105A2.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# removing seal formation:
cell20191105A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=53)
# marking blocks with blocker in the bath:
cell20191105A2.rawdata_note_chemicalinbath('withBlocker')
cell20191105A2.write_results()

# %%
cell20191105C = SingleNeuron('20191105C')
# Neuron does not have all that much going on - literally just one or two events. (also lots of little negative noise).
# Rin increases and spikes become much easier to evoke after blocker application, and lose their spikeshoulderpeaks.
cell20191105C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation:
cell20191105C.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=14)
# marking blocks with blockers applied:
cell20191105C.rawdata_note_chemicalinbath('withBlocker')
cell20191105C.write_results()

# %%
cell20191106A1 = SingleNeuron('20191106A1')
# cell basically dies halfway through recordings, but with loads of -DC keeps something of a membranev so I cannot actually call a specific time of death.
cell20191106A1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
for blockname in cell20191106A1.get_blocknames(printing='off'):
    cell20191106A1.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# removing a block not belonging to this neuron:
cell20191106A1.rawdata_remove_nonrecordingblock('ggapFree_0000.abf')
# removing seal formation:
cell20191106A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=123)
# marking blocks with blockers applied:
cell20191106A1.rawdata_note_chemicalinbath('withBlocker')
cell20191106A1.write_results()

# %%
cell20191106A2 = SingleNeuron('20191106A2')
# not an olive neuron; interesting only because its depolarizing events look a lot like fast-events,
# and here, too, blocker seems to make them stop
cell20191106A2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for blockname in cell20191106A2.get_blocknames(printing='off'):
    cell20191106A2.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# removing a block not belonging to this neuron:
cell20191106A2.rawdata_remove_nonrecordingblock('ggapFree_0000.abf')
# removing seal formation:
cell20191106A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=135)
# marking blocks with blockers applied:
cell20191106A2.rawdata_note_chemicalinbath('withBlocker')
cell20191106A2.write_results()

# %%
cell20191119A = SingleNeuron('20191119A')
# neuron with not much at all going on, except for two sizeable depolarizing events in the blocker condition...
# also interestingly, APs evoked with SpikePulse before blocker have no shoulder at all, but with blocker it's very wide
cell20191119A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation:
cell20191119A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=13)
# marking blocks with blocker applied:
cell20191119A.rawdata_note_chemicalinbath('withBlocker')
cell20191119A.write_results()

# %%
# cell20191119B = SingleNeuron('20191119B')
# neuron died pretty much as blocker was getting to the bath; anyway it didn't have much of any activity going on.
# cell20191119B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# cell20191119B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', 11)
# cell20191119B.rawdata_remove_nonrecordingsection('spikePulse_withBlocker_0000.abf', remove_segments=[81, 82, 83])
# cell20191119B.rawdata_note_chemicalinbath('withBlocker')
# cell20191119B.write_results()
# %%
cell20191120A = SingleNeuron('20191120A')
cell20191120A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# has very clear depolarizations of 1 - 2 mV that look more like spikelets to me;
# there's depolarizations also in recordings with blockers, as well as some depolarizing noise-events.
# raw data cleanup:
# removing recording channel not belonging to this neuron:
cell20191120A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# removing seal formation:
cell20191120A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=15)
# marking blocks with blocker in the bath:
cell20191120A.rawdata_note_chemicalinbath('withBlocker')
cell20191120A.write_results()

# %%
cell20191120B1 = SingleNeuron('20191120B1')
# not much of any large depolarizations, but tons of spikelets that don't much come back after washing blocker
cell20191120B1.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for blockname in cell20191120B1.get_blocknames(printing='off'):
    cell20191120B1.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# removing seal formation:
cell20191120B1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=240)
# marking blocks with blockers applied:
cell20191120B1.rawdata_note_chemicalinbath('withBlocker_')
cell20191120B1.write_results()

# %%
cell20191120B2 = SingleNeuron('20191120B2')
# spont.break-in, and not much of depolarizations (though some seen in recordings with blockers) or anything else.
cell20191120B2.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for blockname in cell20191120B2.get_blocknames(printing='off'):
    cell20191120B2.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# marking blocks with blocker applied:
cell20191120B2.rawdata_note_chemicalinbath('withBlocker_')
cell20191120B2.write_results()

# %%
cell20191226A = SingleNeuron('20191226A')
# !not an IO neuron; pretty boring overall
cell20191226A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing recording channel not belonging to this neuron:
for block in cell20191226A.get_blocknames(printing='off'):
    cell20191226A.rawdata_remove_nonrecordingchannel(block, 1)
# removing block not belonging to this neuron:
cell20191226A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# removing seal formation:
cell20191226A.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=16)
cell20191226A.write_results()

# %%
cell20200102B = SingleNeuron('20200102B')

# %% experiment: RubiGlu-uncaging
# %% no light-evoked activity recorded
# cell20200306A = SingleNeuron('20200306A')
# cell died between run 10 and 11, yet for some reason 28 runs were recorded altogether
# altogether it's not a good recording; cell was pretty leaky from the start, and only deteriorating.
# spiking only in R1, still has depolarizations and small (~1/2mV) oscillations in R2, but after that it's dead.
# cell20200306A_allrunsnames = cell20200306A.get_blocknames(printing='off')
# for i in range(3, 29):
#     runtoexclude = 'R'+str(i)
#     fullrunname = [name for name in cell20200306A_allrunsnames
#                    if name.startswith(runtoexclude)][0]
#     cell20200306A.rawdata_remove_nonrecordingblock(fullrunname)
# cell20200306A.write_results()
# %% no light-evoked activity recorded
# cell20200306B = SingleNeuron('20200306B')
# just one block with some spontaneous activity, then it died; not much of any interesting activity
# cell20200306B.rawdata_remove_nonrecordingblock('R2_spontactivity_CCmode')
# cell20200306B.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=288)
# cell20200306B.write_results()
# %%
# cell20200306C = SingleNeuron('20200306C')
# cell20200306C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# lots of data, one block with lightpulses
# TODO: figure out what's going on with some blocks not getting imported
# R2, 9 and 11 are missing for some reason, even though there does seem to be a bunch of data there
# when I open the file in SutterPatch
# cell started doing badly in R12, and is pretty much dead in the blocks that follow
# cell20200306C_allrunsnames = cell20200306C.get_blocknames(printing='off')
# for i in range(13, 17):
#     runtoexclude = 'R'+str(i)
#     fullrunname = [name for name in cell20200306C_allrunsnames
#                    if name.startswith(runtoexclude)][0]
#     cell20200306C.rawdata_remove_nonrecordingblock(fullrunname)
#
# cell20200306C.rawdata_note_chemicalinbath('lighttriggered')
# cell20200306C.write_results()
# %% no light-evoked activity recorded
# cell20200307A = SingleNeuron('20200307A')
# spont activity and long-pulses; no oscillations, but it does seem to have all the
# kinds of depolarizations except APs (including things that look like dendritic Ca-spikes)
# %% no evoked activity recorded
# cell20200307B = SingleNeuron('20200307B')
# TODO: figure out what's going on with no data getting imported at all
# not a single block gets imported... It's a very small file so probably no real data there anyway, but still...
# %% no light-evoked activity recorded
# cell20200308A = SingleNeuron('20200308A')
# spont activity and some long-pulses (but cell was basically dying already);
# does have all the depolarizations (including APs).
# osc amp ~3mV at recordings start but soon deteriorating to ~1/2 mV
# cell20200308A.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308A.write_results()
# %%
# cell20200308B = SingleNeuron('20200308B')
# cell20200308B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# bunch of lighttriggered but no long-pulses; Vrest bad by the end but still has some depolarizing events
# TODO: figure out what's going on with data not getting imported
# R1 and R3 are missing for some reason even though in SutterPatch it looks like there is a bunch of nice data there
# cell20200308B.rawdata_note_chemicalinbath('R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11')
# cell20200308B.write_results()
# %%
# cell20200308C = SingleNeuron('20200308C')
# some spont.activity and one lighttriggered block; oscillating throughout with
# small (~1.5mV) amplitude despite pretty bad Vrest (~-26mV)
# cell thoroughly dead by the end.
# cell20200308C.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308C.rawdata_note_chemicalinbath('R')
# cell20200308C.write_results()
# %%
# cell20200308D = SingleNeuron('20200308D')
# some spont.activity and a single light pulse; has all the depolarizing events,
# oscillating with ~5mV amplitude initially but steadily losing amp with depolarizing resting potential
# cell20200308D.rawdata_remove_nonrecordingblock('R3_lighttriggered_CCmode')
# cell20200308D.rawdata_note_chemicalinbath('R')
# cell20200308D.write_results()
# %%
# cell20200308E = SingleNeuron('20200308E')
# spont. and light-triggered activity; APs only in R1, but all other depolarizations are happening throughout
# pretty bad Vrest (~-25mV) and not oscillating at any point
# cell20200308E.rawdata_remove_nonrecordingblock('R10_spontactivity_CCmode')
# cell20200308E.rawdata_note_chemicalinbath('R')
# cell20200308E.write_results()
# %% no light-evoked activity recorded
# cell20200308F = SingleNeuron('20200308F')
# a bit of spont.activity; nothing really in there except for two APs,
# pretty bad Vrest (~-25mV) throughout, not oscillating
# cell20200308F.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=150)
# cell20200308F.rawdata_note_chemicalinbath('R')
# cell20200308F.write_results()
# %% no light-evoked activity recorded
# cell20200310A = SingleNeuron('20200310A')
# !!not an olive cell; some spont.activity
# %% no light-evoked activity recorded
# cell20200310B = SingleNeuron('20200310B')
# !!not an olive cell; some spont.activity (not sure what's in there, no APs for sure) and long-pulses
# %% no light-evoked activity recorded
# cell20200310C = SingleNeuron('20200310C')
# TODO: R11 and 18 not imported for some reason, figure out what's up with that
# it's especially annoying because those are the blocks where the bath is switched from regular ACSF to RubiGlu-ACSF.
# spont.activity and long-pulses, lots of fast-events
# at first sight the effect of (old) RubiGlu in the bath is a decrease in depolarizing events frequency
# and increase in the neuron's Rin; however, this could also just be the recording going bad.
# cell20200310C.rawdata_note_chemicalinbath('12', '13', '14', '15', '16', '17')
# cell20200310C.write_results()
# %% no light-evoked activity recorded
# cell20200310D = SingleNeuron('20200310D')
# has some spont.activity with fast-events, but long-pulse responses look completely passive
# not sure how much to trust this data; bridge getting steadily worse throughout recording,
# and strangely low Vrest (<-75mV); not oscillating
# %% nothing real recorded
# cell20200310E = SingleNeuron('20200310E')
# not a good recording at all
# %% no light-evoked activity recorded
# cell20200310F = SingleNeuron('20200310F')
# a tiny bit of spont.activity; oscillating throughout with amp ~8mV initially, down to ~3mV by the end
# cell20200310F.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=74)
# cell20200310F.write_results()
# %%
# cell20200310G = SingleNeuron('20200310G')  # the single greatest cell with light
# cell20200310G.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# has all the kinds of depolarizations spontaneously occurring
# initially oscillating with ~15mV amp and steadily decreasing; Vrest staying ~-50mV throughout
# cell20200310G.rawdata_remove_nonrecordingsection('R21_lighttriggered_CCmode.ibw',
#                                                  segment_idx=1)
# for block in cell20200310G.blocks:
#     if 'R1_' in block.file_origin:
#         continue
#     else:
#         cell20200310G.rawdata_note_chemicalinbath(block.file_origin)
# cell20200310G.write_results()
# %% no light-evoked activity recorded
# cell20200312A = SingleNeuron('20200312A')  # this cell has a little more data recorded post-software-crash;
# has a couple more fast-events there though it lost >10mV of its resting
# some spont.activity and a bunch of long-pulses; depolarizing events occurring spontaneously and
# one single AP in a depolarizing pulse.
# oscillating with amp anywhere <2.5mV (though mostly sinusoidal-looking).
# TODO: R1 does not get imported, see what's up with that
#
# %% no light-evoked activity recorded
# cell20200312B = SingleNeuron('20200312B')
# single block of spont.activity; Vrest not great (~-31mV) but still has APs and other depolarizations
# not much of oscillations (here and there a short episode of amp <1mV)
# cell20200312B.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=200)
# cell20200312B.write_results()
# %%
# cell20200312C = SingleNeuron('20200312C')
# has a bunch of blocks with light, but it doesn't look like anything is
# going on in this neuron - at all... It starts at ~-50mV but soon goes down to <-70mV; in this
# state I saw one single believable spikelet, all other 'activity' seems to just be the cell slowly dying
# TODO: R6 is missing for some reason (the one where inflow is first switched), see what's up with that
# cell20200312C.rawdata_note_chemicalinbath('lighttriggered', 'R7_')
# cell20200312C.write_results()
# %%
# # 20200312D juxtacellular more than intracellular recording
# %% no light-evoked activity recorded
# cell20200312E = SingleNeuron('20200312E')  # another one of those where not a single block gets imported
# TODO: get data to be imported
# %% no light-evoked activity recorded
# cell20200312F = SingleNeuron('20200312F')
# one block of spont.activity, and a bunch of long-pulses runs
# not oscillating, does have all the depolarizations; both fast-events and APs
# look like they're almost always compound events
# a block got imported that doesn't contain any data at all (also not when I open the file in Igor)
# cell20200312F.rawdata_remove_nonrecordingblock('R1_spontactivity_CCmode')
# cell20200312F.write_results()
# %%
# cell20200312G = SingleNeuron('20200312G')
# cell20200312G.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# spont. and light-evoked activity, though it doesn't look like much at all happens in response
# (a tiny direct depolarization early on, but then that stops too).
# not oscillating, does have spont APs and fast-events and such; APs stop having an AHP by R3, interestingly
# TODO: get R2 (the one where inflow is first switched) imported
# its missing for some reason even though it IS there when I open the file in SutterPatch
# cell20200312G.rawdata_note_chemicalinbath('lighttriggered', 'R3_')
# cell20200312G.write_results()









# %% experiment: ChR activation in Thy1 mouse
# %%
# cell20200630A = SingleNeuron('20200630A')
# some spont.activity and light pulses, then cell dies
# there's some real bad noise events in there, including periods with bad 50Hz noise
# the evoked events look more like giant synapses, sometimes with a spike without shoulder riding them
# cell20200630A.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=14)
# cell20200630A.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
# for i in reversed(range(7, 11)):
#     cell20200630A.rawdata_remove_nonrecordingsection('light_0001.abf', segment_idx=i)
# cell20200630A.write_results()
# %%
# cell20200630B1 = SingleNeuron('20200630B1')
# some spont.activity and light pulses; cell stops responding in light_0006 (probably pretty dead but still has a Vrest)
# there's pretty bad 50Hz noise throughout (not very large amp (~1/4mV) but very visible) and
# nothing much of spontaneously occurring events
# light responses look like they're mostly synapses, though a couple of them may have (several) fast-events riding them.
# fileslist = cell20200630B1.get_blocknames(printing='off')
# for file in fileslist:
#     cell20200630B1.rawdata_remove_nonrecordingchannel(file, 2, pairedrecording=True)
# cell20200630B1.write_results()
# %%
# cell20200630B2 = SingleNeuron('20200630B2')
# some spont.activity and light pulses
# nothing much of spontaneously occurring events going on, but cell responds to light very consistently;
# it often fires an AP, but wherever it doesn't the fast-event(s) riding the synaptic potential look pretty clear
# fileslist = cell20200630B2.get_blocknames(printing='off')
# for file in fileslist:
#     cell20200630B2.rawdata_remove_nonrecordingchannel(file, 1, pairedrecording=True)
# cell20200630B2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=642)
# cell20200630B2.write_results()
# %%
cell20200630C = SingleNeuron('20200630C')
cell20200630C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# !! for some reason there are two segments in gapFree_0000 - can only be plotted with segments_overlayed=False.
# raw data cleanup:
# removing seal formation; other than that everything looks OK
cell20200630C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=14)
cell20200630C.write_results()
# %%
# cell20200630D = SingleNeuron('20200630D')
# spont.activity and light pulses
# there are some pretty big spontaneous fast-events, as well as a couple of APs, and cell responds to
# light consistently with an AP or with what looks like a fast-event at first but then turns out to rise too slow.
# cell loses potential rather suddently during light_0010, but still has a nice light-response there
# cell20200630D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=17)
# cell20200630D.write_results()
# %%
# cell20200701A = SingleNeuron('20200701A')
# some spont.activity and light pulses; not oscillating
# has spontaneous fast-events of ~12mV, and possibly these are the ones that are evoked at hyperpolarized potentials
# removing blocks that are (partially) in voltage-clamp-mode (there's nothing actually in there),
# and light file where there's no recorded data
# cell20200701A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=10)
# cell20200701A.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
# cell20200701A.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
# cell20200701A.rawdata_remove_nonrecordingblock('light_0003.abf')
# cell20200701A.write_results()
# %%
# cell20200701B = SingleNeuron('20200701B')
# spont.activity and light pulses; light pulses also in voltage clamp mode (different potentials, until cell dies).
# intermittently oscillating a little with very small amplitude,
# has some spont. fast-events of barely up to 3mV, no APs;
# responses to light look like they're usually just synapses, but occasionally there may be an actual fast-event there.
# patch sealing not recorded.
# %%
# cell20200701C = SingleNeuron('20200701C')
# single trace of spont.activity at different Vrest levels (through huge amounts of holding current);
# non-oscillating cell that seems not entirely unhappy with a Vrest of ~-10mV
# - it's firing off things that look like fast-events (amp. up to ~4mV) even at this voltage.
# patch sealing not recorded.
# %%
# cell20200701D = SingleNeuron('20200701D')
# spont.activity and light pulses, also in vclamp-mode (until the cell dies);
# non-oscillating cell that seems to have basically nothing going on spontaneously,
# but evoked events look kinda nice nonetheless.
# cell20200701D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=5)
# cell20200701D.rawdata_remove_nonrecordingblock('light_Vclamp_0002.abf')
# cell20200701D.rawdata_remove_nonrecordingblock('light_Vclamp_0003.abf')
# cell20200701D.write_results()
# %%
# cell20200706A = SingleNeuron('20200706A')
# just a single trace of spont. activity; has APs and oscillations, but no clear fast-events.
# cell20200706A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=26)
# cell20200706A.write_results()
# %%
# cell20200706B = SingleNeuron('20200706B')
# spont.activity and light pulses;
# oscillating pretty much throughout recordings (until it's basically dead) with amp 2 - 5 mV;
# has APs but they seem to lose their Na-component after about 5 minutes of recordings,
# there may be a couple of spont. fast-events of ~4mV, but evoked things all look like dendritic Ca-spikes.
# cell20200706B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=21)
# cell20200706B.write_results()
# %%
# cell20200706C = SingleNeuron('20200706C')
# just a single trace of spont.activity in a half-dead (Vrest ~-25mV) neuron; nothing much of interesting activity.
# %%
# cell20200706D = SingleNeuron('20200706D')
# some spont.activity and light pulses;
# not oscillating, does not seem to have anything of interesting spont.activity going on at all
# either cell or patch or both are badly deteriorated towards the end of recordings (but not so bad as to exclude)
# cell20200706D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=25)
# cell20200706D.write_results()
# %%
# cell20200706E = SingleNeuron('20200706E')
# spont.activity and light pulses;
# neuron is oscillating throughout (until it dies), and has APs and what seem like fast-events -
# though upon closer inspection though these often have a very broad, round peak.
# Events that have this shape are also occasionally evoked.
# cell20200706E.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=26)
# cell20200706E.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
# cell20200706E.write_results()
# %%
# cell20200707A = SingleNeuron('20200707A')
# just a single trace of some spont. activity at pretty bad Vrest;
# oscillating, and clearly has some fast-events (amp up to 8mV or so)
# cell20200707A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=137, trace_end_t=290)
# cell20200707A.write_results()
# %%
# cell20200707B = SingleNeuron('20200707B')
# !! not an olive neuron. spont.activity and light pulses;
# possibly, the neuron is somewhat quieter after pulses applied, but it'll be hard to really make that case.
# %%
# cell20200707C = SingleNeuron('20200707C')
# literally just 10s of recording after break-in; a single AP and some (tiny) oscillations.
# cell20200707C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=49, trace_end_t=59)
# cell20200707C.write_results()
# %%
# cell20200707D = SingleNeuron('20200707D')
# partial break-in into a dead cell; no real data recorded
# %%
# cell20200707E = SingleNeuron('20200707E')
# spont.activity and light pulses; not the greatest recording and nothing really going on spontaneously,
# but some of the evoked responses look like they could be fast-events
# patch sealing not recorded.
# %%
# cell20200708A = SingleNeuron('20200708A')
# spont.activity with some APs and things that look like fast-events;
# most of the fast-event-like things have those strangely broad, round peaks though.
# cell20200708A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=18)
# cell20200708A.write_results()
# %%
# cell20200708B = SingleNeuron('20200708B')
# spont.activity and light pulses; has APs and fast-events (at least 3 different amps) spontaneously,
# and looks like they may also be evoked by light. Too bad neuron dies after just a few repetitions
# cell20200708B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=24)
# cell20200708B.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
# cell20200708B.write_results()
# %%
# cell20200708C = SingleNeuron('20200708C')
# spont.activity and light pulses; not the greatest recording though, with basically nothing going on spontaneously,
# light-evoked activity is very small amp and looks like just a regular synapse
# cell20200708C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=46)
# cell20200708C.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
# cell20200708C.write_results()
# %%
# cell20200708D = SingleNeuron('20200708D')
# spont.activity and light pulses; oscillating vigorously and has tons of spont. fast-events and APs.
# light-evoked activity is usually an AP but there may be some fast-events in there
# cell20200708D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=28)
# cell20200708D.write_results()
# %%
# cell20200708E = SingleNeuron('20200708E')
# just a single trace of spont.activity with one AP and a few fast-events
# cell20200708E.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=40, trace_end_t=170)
# cell20200708E.write_results()
# %%
cell20200708F = SingleNeuron('20200708F')
# the neuron that's got everything: spont. activity and light pulses, both without and with NMDA blocker.
# it's also going in and out of all kinds of different oscillating modes, and definitely has
# some fast-events (though no big-amplitude ones that I saw in files before blocker application).
# removing seal formation and part of a recording where neuron is finally actually dead:
cell20200708F.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=10)
cell20200708F.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0006.abf', trace_end_t=565)
cell20200708F.rawdata_note_chemicalinbath('withBlocker')
cell20200708F.write_results()
# %%
# cell20200708G = SingleNeuron('20200708G')
# spont.activity and light pulses; cell has pretty bad Vrest and not much of any spont.activity going on,
# and light-evoked activity looks like a regular synapse that appears only after forcing V down with current.
# cell20200708G.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0000.abf', trace_start_t=16)
# cell20200708G.rawdata_note_chemicalinbath('withBlocker')
# cell20200708G.write_results()


# %%
# %%
cell20200818B = SingleNeuron('20200818B')
# quite a few fast-events and no fast-events in light-applied traces;
# too bad neuron starts dying pretty badly just as lightpulses are getting applied.
# removing seal formation and a block where recorded neuron is dead already:
cell20200818B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=27)
cell20200818B.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
cell20200818B.write_results()
# %%
# not a great recording at all; spont.break-in from <Gseal, not much of any activity going on,
# and starts dying really badly just as lightpulses are getting applied.
# cell20200818C = SingleNeuron('20200818C')
# cell20200818C.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20200818C.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=19)
# cell20200818C.rawdata_remove_nonrecordingsection('longPulses_0004.abf', trace_end_t=46)  # file misnamed at recordings
# cell20200818C.write_results()

# %% experiments with glutamate puff
# cell20201116A = SingleNeuron('20201116A')

# %%
# cell20201116B = SingleNeuron('20201116B')
# cell20201116B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# # cell (partially) re-sealed itself twice during the first few minutes of recording; cutting all that off the trace
# cell20201116B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=553.5)
# # cell starts to die in seg.5 already of the last puff-response file, but has one nice fast-event there so keeping it
# cell20201116B.rawdata_remove_nonrecordingsection('puffResponse_0002.abf', remove_segments=[6, 7, 8])
# cell20201116B.write_results()


# %%
cell20210105B = SingleNeuron('20210105B')
cell20210105B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# spont.break-in; removing the first part of the first recording where neuron is getting its bearings
# and removing the last recording where neuron is definitely all dead. Has some nice recordings in there
# but getting held with a lot of -DC for quite a lot of the time.
cell20210105B.rawdata_remove_nonrecordingblock('gapFree_0003.abf')
cell20210105B.write_results()

# %%
cell20210110A = SingleNeuron('20210110A')
cell20210110A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation; everything else looks OK
cell20210110A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_end_t=29)
cell20210110A.write_results()



# %%
cell20210110G = SingleNeuron('20210110G')
cell20210110G.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation, and a section from the last file where the pipette gets pulled out of the cell;
# other than that everything looks OK (VERY quiet neuron, not a lot of events happening at all).
cell20210110G.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=20)
cell20210110G.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_end_t=720)
cell20210110G.write_results()


# %%
cell20210113G = SingleNeuron('20210113G')
cell20210113G.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# nice enough recording overall, though cell is definitely deteriorating a bit over time
# non-oscillating, does have spontaneous spikes and fast-events
# note - there are three 'gapFree' files that actually have TTL-traces in them as well; light was not actually on
#   in these recordings though and there's nothing really of events going on in there, so leaving that as is.
# removing seal formation; all other recorded data looks good (enough)
cell20210113G.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=17)
cell20210113G.write_results()

# %%
cell20210113H = SingleNeuron('20210113H')
cell20210113H.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation; everything else looks good
cell20210113H.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=37)
cell20210113H.write_results()



# %%
cell20210123B = SingleNeuron('20210123B')
cell20210123B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# no seal formation recorded; removing final gapFree block where neuron is already dead:
cell20210123B.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
cell20210123B.write_results()


# %%
cell20210124A = SingleNeuron('20210124A')
cell20210124A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation; everything else looks good
cell20210124A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=17)
cell20210124A.write_results()


# %%
cell20210203C = SingleNeuron('20210203C')
cell20210203C.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
# raw data cleanup:
# removing seal formation; everything else looks good
cell20210203C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=48)
cell20210203C.write_results()
# note blocks with special chemicals added to bath:




# %%
# cell20210411A = SingleNeuron('20210411A')
# applying light just seems to turn on an oscillation (very wackily oscillating neuron)
# cell20210411A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %%
# cell20210411F = SingleNeuron('20210411F')
# cell20210411F.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# %%
# cell20210413A = SingleNeuron('20210413A')
# cell20210413A.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %%
# cell20210413B = SingleNeuron('20210413B')
# cell20210413B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# %%
# cell20210426B = SingleNeuron('20210426B')
# has a couple of traces with light applied, exactly one where no spike but a fast-event is evoked (hyperpolarizing the neuron doesn't help, then it dies)
# raw data cleanup:
# removing seal formation and another minute or so of recording where seal was not properly broken all the way in
# cell20210426B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=124)
# also removing last 3 traces where the neuron leaves suddenly and quickly
# cell20210426B.rawdata_remove_nonrecordingsection('light_0000.abf', remove_segments=[7, 8, 9, 10])
# cell20210426B.get_depolarizingevents_fromrawdata()
# cell20210426B.write_results()

# %%
# cell20210426C = SingleNeuron('20210426C')
# getting held with up to -2nA to maintain halfway decent baselineV, but other than that looks all good
# cell20210426C.get_depolarizingevents_fromrawdata()
# cell20210426C.write_results()

# %%
cell20210426D = SingleNeuron('20210426D')
# nice recording overall, even though cell is losing ~20mV of restingV over time (-50 to -30)
# raw data cleanup:
# removing seal formation, and some time from the end of the last recording where the neuron died
cell20210426D.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=35)
cell20210426D.rawdata_remove_nonrecordingsection('gapFree_0002.abf', trace_end_t=875)
cell20210426D.write_results()

# %%
# cell20210426E = SingleNeuron('20210426E')
# cell20210426E.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# %%
# cell20210426F = SingleNeuron('20210426F')
# cell20210426F.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# %%
# cell20210428B = SingleNeuron('20210428B')
# cell20210428B.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)



# %%

# raw data cleanup:
# cell.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
#note actual cleanups applied

# note blocks with special chemicals added to bath:

