# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
# %% experiment: ChR activation in Thy1 mouse
# %%
cell20190527A = SingleNeuron('20190527A')
# spont.activity and light pulses
# has some tiny (~1mV) oscillations here and there, as well as a strong
# resonance response to activating inputs
# also, it looks like depolarizing events of intermediate amplitude are quite often followed by
# an after-hyperpolarization/resonance response
# cell20190527A.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=21.5)
# cell20190527A.write_results()
# %% no light-evoked activity recorded
cell20190527B = SingleNeuron('20190527B')
# just a single long trace of spont.activity: some depolarizing events and spikes, no oscillations.
# cell20190527B.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_start_t=20)
# cell20190527B.rawdata_remove_nonrecordingblock('light_wholeField_0000.abf')
# cell20190527B.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20190527B.write_results()
# %%
cell20190527C = SingleNeuron('20190527C')
# spont. activity (with fast-events) and light pulses
# in the spont. activity there's depolarizing events of ~7mV amp that seem to have a bit of a 'shoulder'
# tuning pulses can drive the voltage to +50, yet no AP is evoked ever
# activating inputs often evokes a giant (25 mV) fast-event, and in the seconds after that there's
# some oscillations and tons of spikelets (otherwise nothing much of oscillations to be seen).
# %%
cell20190529A1 = SingleNeuron('20190529A')
# notes say only A2 was good, but that's not what it looks like in the data...
# TODO: figure out what to do with this data
# %%
cell20190529B = SingleNeuron('20190529B')
# spont.activity and lots of light pulses; few spont. depolarizations and not oscillating.
# looks like activating axonal inputs evokes big, compound fast-events.
# cell20190529B.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=18)
# cell20190529B.write_results()
# %%
cell20190529C = SingleNeuron('20190529C')
# pretty leaky-looking cell but has some nice spont.activity and light pulses
# not oscillating, except for one trace where it oscillates whackily for a few s following a light pulse
# cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=28)
# cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_end_t=101.5)
# cell20190529C.write_results()
# %%
cell20190529D = SingleNeuron('20190529D')
# nice-looking recording, spont.activity and lots of light pulses
# not oscillating, just constantly being bombarded with depolarizations
# cell20190529D.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_end_t=395)
# cell20190529D.write_results()
# %%
cell20190529E = SingleNeuron('20190529E')
# spont.activity and light pulses, until cell stops responding to them
# some interesting-looking depolarizing events in spont activity; evoked they are always clearly compound
# no real oscillatory activity of any sort
# cell20190529E.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=13)
# cell20190529E.write_results()
# %%
# %% experiment: RubiGlu-uncaging
# %% no light-evoked activity recorded
cell20200306A = SingleNeuron('20200306A')
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
cell20200306B = SingleNeuron('20200306B')
# just one block with some spontaneous activity, then it died; not much of any interesting activity
# cell20200306B.rawdata_remove_nonrecordingblock('R2_spontactivity_CCmode')
# cell20200306B.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=288)
# cell20200306B.write_results()
# %%
cell20200306C = SingleNeuron('20200306C')
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
cell20200307A = SingleNeuron('20200307A')
# spont activity and long-pulses; no oscillations, but it does seem to have all the
# kinds of depolarizations except APs (including things that look like dendritic Ca-spikes)
# %% no evoked activity recorded
cell20200307B = SingleNeuron('20200307B')
# TODO: figure out what's going on with no data getting imported at all
# not a single block gets imported... It's a very small file so probably no real data there anyway, but still...
# %% no light-evoked activity recorded
cell20200308A = SingleNeuron('20200308A')
# spont activity and some long-pulses (but cell was basically dying already);
# does have all the depolarizations (including APs).
# osc amp ~3mV at recordings start but soon deteriorating to ~1/2 mV
# cell20200308A.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308A.write_results()
# %%
cell20200308B = SingleNeuron('20200308B')
# bunch of lighttriggered but no long-pulses; Vrest bad by the end but still has some depolarizing events
# R1 and R3 are missing for some reason even though in SutterPatch it looks like there is a bunch of nice data there
# cell20200308B.rawdata_note_chemicalinbath('R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11')
# cell20200308B.write_results()
# %%
cell20200308C = SingleNeuron('20200308C')
# some spont.activity and one lighttriggered block; oscillating throughout with
# small (~1.5mV) amplitude despite pretty bad Vrest (~-26mV)
# cell thoroughly dead by the end.
# cell20200308C.rawdata_remove_nonrecordingblock('R3_spontactivity_CCmode')
# cell20200308C.rawdata_note_chemicalinbath('R')
# cell20200308C.write_results()
# %%
cell20200308D = SingleNeuron('20200308D')
# some spont.activity and a single light pulse; has all the depolarizing events,
# oscillating with ~5mV amplitude initially but steadily losing amp with depolarizing resting potential
# cell20200308D.rawdata_remove_nonrecordingblock('R3_lighttriggered_CCmode')
# cell20200308D.rawdata_note_chemicalinbath('R')
# cell20200308D.write_results()
# %%
cell20200308E = SingleNeuron('20200308E')
# spont. and light-triggered activity; APs only in R1, but all other depolarizations are happening throughout
# pretty bad Vrest (~-25mV) and not oscillating at any point
# cell20200308E.rawdata_remove_nonrecordingblock('R10_spontactivity_CCmode')
# cell20200308E.rawdata_note_chemicalinbath('R')
# cell20200308E.write_results()
# %% no light-evoked activity recorded
cell20200308F = SingleNeuron('20200308F')
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
cell20200310C = SingleNeuron('20200310C')
# TODO: R11 and 18 not imported for some reason, figure out what's up with that
# it's especially annoying because those are the blocks where the bath is switched from regular ACSF to RubiGlu-ACSF.
# spont.activity and long-pulses, lots of fast-events
# at first sight the effect of (old) RubiGlu in the bath is a decrease in depolarizing events frequency
# and increase in the neuron's Rin; however, this could also just be the recording going bad.
# cell20200310C.rawdata_note_chemicalinbath('12', '13', '14', '15', '16', '17')
# cell20200310C.write_results()
# %% no light-evoked activity recorded
cell20200310D = SingleNeuron('20200310D')
# has some spont.activity with fast-events, but long-pulse responses look completely passive
# not sure how much to trust this data; bridge getting steadily worse throughout recording,
# and strangely low Vrest (<-75mV); not oscillating
# %% nothing real recorded
# cell20200310E = SingleNeuron('20200310E')
# not a good recording at all
# %% no light-evoked activity recorded
cell20200310F = SingleNeuron('20200310F')
# a tiny bit of spont.activity; oscillating throughout with amp ~8mV initially, down to ~3mV by the end
# cell20200310F.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
#                                                  trace_end_t=74)
# cell20200310F.write_results()
# %%
cell20200310G = SingleNeuron('20200310G')  # the single greatest cell with light
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
cell20200312A = SingleNeuron('20200312A')  # this cell has a little more data recorded post-software-crash;
# has a couple more fast-events there though it lost >10mV of its resting
# some spont.activity and a bunch of long-pulses; depolarizing events occurring spontaneously and
# one single AP in a depolarizing pulse.
# oscillating with amp anywhere <2.5mV (though mostly sinusoidal-looking).
# TODO: R1 does not get imported, see what's up with that
#
# %% no light-evoked activity recorded
cell20200312B = SingleNeuron('20200312B')
# single block of spont.activity; Vrest not great (~-31mV) but still has APs and other depolarizations
# not much of oscillations (here and there a short episode of amp <1mV)
cell20200312B.rawdata_remove_nonrecordingsection('R1_spontactivity_CCmode',
                                                 trace_end_t=200)
cell20200312B.write_results()
# %%
cell20200312C = SingleNeuron('20200312C')
# has a bunch of blocks with light, but it doesn't look like anything is
# going on in this neuron - at all... It starts at ~-50mV but soon goes down to <-70mV; in this
# state I saw one single believable spikelet, all other 'activity' seems to just be the cell slowly dying
# TODO: R6 is missing for some reason (the one where inflow is first switched), see what's up with that
# cell20200312C.rawdata_note_chemicalinbath('lighttriggered', 'R7_')
# cell20200312C.write_results()
# %%
# # 20200312D juxtacellular more than intracellular recording
# %% no light-evoked activity recorded
cell20200312E = SingleNeuron('20200312E')  # another one of those where not a single block gets imported
# TODO: get data to be imported
# %% no light-evoked activity recorded
cell20200312F = SingleNeuron('20200312F')
# one block of spont.activity, and a bunch of long-pulses runs
# not oscillating, does have all the depolarizations; both fast-events and APs
# look like they're almost always compound events
# a block got imported that doesn't contain any data at all (also not when I open the file in Igor)
# cell20200312F.rawdata_remove_nonrecordingblock('R1_spontactivity_CCmode')
# cell20200312F.write_results()
# %%
cell20200312G = SingleNeuron('20200312G')
# spont. and light-evoked activity, though it doesn't look like much at all happens in response
# (a tiny direct depolarization early on, but then that stops too).
# not oscillating, does have spont APs and fast-events and such; APs stop having an AHP by R3, interestingly
# TODO: get R2 (the one where inflow is first switched) imported
# its missing for some reason even though it IS there when I open the file in SutterPatch
# cell20200312G.rawdata_note_chemicalinbath('lighttriggered', 'R3_')
# cell20200312G.write_results()
