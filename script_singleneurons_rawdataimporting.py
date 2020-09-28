# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
# %%
# intermittently oscillating at first, but stops doing that a little bit before blockers get applied.
# NOTE: blocker solution contains higher K than the regular ACSF,
# that's why neuron needs to be held with -DC to keep the same baselinev
# cell20190729A = SingleNeuron('20190729A')
# cell20190729A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20190729A.rawdata_note_chemicalinbath('withBlocker')
# cell20190729A.write_results()
# %%
# not oscillating but getting tons of depolarizing events at first,
# then depolarizing a bit and starting to oscillate once blocker solution is applied.
# cell20190804A = SingleNeuron('20190804A')
# cell20190804A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20190804A.rawdata_remove_nonrecordingchannel(file_origin='gapFree_0001.abf', non_recording_channel=2)
# cell20190804A.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=14.8)
# cell20190804A.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0003.abf', trace_end_t=12)
# cell20190804A.rawdata_note_chemicalinbath('withBlocker')
# cell20190804A.write_results()
# %%
# fairly boring neuron (not much of any inputs or anything, though I did see at least 1 that could be a fast-event)
# and it starts to depolarize slowly but surely pretty soon after getting patched.
# cell20190804B = SingleNeuron('20190804B')
# cell20190804B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=13)
# cell20190804B.rawdata_note_chemicalinbath('withBlocker')
# cell20190804B.write_results()
# %%
# fairly boring neuron again, not sure there are any spontaneous excitations at all.
# This neuron, too, depolarizes somewhat soon after blocker application
# cell20190804C = SingleNeuron('20190804C')
# cell20190804C.rawdata_remove_nonrecordingsection('IV_withBlocker_0003.abf', remove_segments=[0, 1, 2])
# cell20190804C.write_results()
# %%
# it's spiking and getting tons of fast-events but slowly depolarizing, then leaves all of a sudden.
# cell20190805A1 = SingleNeuron('20190805A1')
# cell20190805A1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', non_recording_channel=2)
# cell20190805A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=11, trace_end_t=386)
# blocknames_list = cell20190805A1.get_blocknames()
# blocknames_list = blocknames_list[1:]
# for name in blocknames_list:
#     cell20190805A1.rawdata_remove_nonrecordingblock(name)
# cell20190805A1.write_results()
# %%
# nice recording, neuron is oscillating throughout mostly with sinusoids(ish);
# not sure if it has both giant fast-events and small-ish spikes or just fast-events.
# cell20190805A2 = SingleNeuron('20190805A2')
# cell20190805A2.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# cell20190805A2.rawdata_remove_nonrecordingsection('gapFree_0001.abf', trace_start_t=13)
# cell20190805A2.rawdata_note_chemicalinbath('withBlocker')
# cell20190805A2.write_results()
# %%
# oscillating, spiking here and there, and looking like it's still getting a lot of inputs
# also after blocker application (though they're definitely only smaller ones now)
# cell20190805B1 = SingleNeuron('20190805B1')
# cell20190805B1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2, pairedrecording=True)
# cell20190805B1.rawdata_remove_nonrecordingchannel('gapFree_withBlockers_0001.abf', 2, pairedrecording=True)
# cell20190805B1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=445)
# cell20190805B1.rawdata_note_chemicalinbath('withBlockers')
# cell20190805B1.write_results()
# %%
# oscillating, spiking here and there, not much else of activity going on.
# cell20190805B2 = SingleNeuron('20190805B2')
# cell20190805B2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1, pairedrecording=True)
# cell20190805B2.rawdata_remove_nonrecordingchannel('gapFree_withBlockers_0001.abf', 1, pairedrecording=True)
# cell20190805B2.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0001.abf', trace_end_t=222)
# cell20190805B2.write_results()
# %%
# doing all the things we like IO neurons to do; beating oscillations get smaller
# and then diappear slowly when blocker is applied.
# cell20190812A = SingleNeuron('20190812A')
# cell20190812A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# cell20190812A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=98)
# cell20190812A.write_results()
# %%
# pretty boring neuron, not much of fast-events except one that's very compound
# cell20190812B = SingleNeuron('20190812B')
# cell20190812B.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=25)
# cell20190812B.write_results()
# %%
# spikes and some fast-events here and there, no oscs except some tiny ripples after blocker application
# cell20190814A = SingleNeuron('20190814A')
# cell20190814A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# cell20190814A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=15)
# cell20190814A.write_results()
# %%
# oscillating quite a lot of the time (though it looks more like rhythmic Ca-spikes when there are no blockers)
# cell20190815D1 = SingleNeuron('20190815D1')
# allblocks_names = cell20190815D1.get_blocknames(printing='off')
# for block in allblocks_names:
#     cell20190815D1.rawdata_remove_nonrecordingchannel(block, 2)
# cell20190815D1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=289)
# cell20190815D1.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0006.abf', trace_end_t=88)
# cell20190815D1.write_results()
# %%
# not actually a good recording really, being held with lots of -DC throughout just to keep some semblance of baselineV
# cell20190815D2 = SingleNeuron('20190815D2')
#
# %%
#
cell20191105A1 = SingleNeuron('20191105A1')

# # %%
# #
# cell20191105A2 = SingleNeuron('20191105A2')
#
# # %%
# #
# cell20191105C = SingleNeuron('20191105C')
#
# # %%
# #
# cell20191106A1 = SingleNeuron('20191106A1')
#
# # %%
# #
# cell20191106A2 = SingleNeuron('20191106A2')
# # %%
# #
# cell20191119A = SingleNeuron('20191119A')
#
# # %%
# #
# cell20191119B = SingleNeuron('20191119B')
#
# # %%
# #
# cell20191120A = SingleNeuron('20191120A')
#
# # %%
# #
# cell20191120B1 = SingleNeuron('20191120B1')
#
# # %%
# #
# cell20191120B2 = SingleNeuron('20191120B2')
#
# # %%
# #
# cell20200818B = SingleNeuron('20200818B')
#
# # %%
# #
# cell20200818C = SingleNeuron('20200818C')
#
# # %%
# #
# cell = SingleNeuron('')
# cell.plot_rawdatablocks()


# %% experiment: ChR activation in Thy1 mouse
# %%
# cell20190527A = SingleNeuron('20190527A')
# spont.activity and light pulses
# has some tiny (~1mV) oscillations here and there, as well as a strong
# resonance response to activating inputs
# also, it looks like depolarizing events of intermediate amplitude are quite often followed by
# an after-hyperpolarization/resonance response
# cell20190527A.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=21.5)
# cell20190527A.write_results()
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
# cell20190529A1 = SingleNeuron('20190529A1')
# notes say only A2 was good, but that's not what it looks like in the data...
# confirmed and reconfirmed: notes are wrong, it's the neuron on channel1 that's good (at least for a few blocks).
# the neuron on channel2 was patched first, but lost not long after the neuron on ch1 was patched.
# spont. activity (with fast-events and APs) and light pulses; no oscillations.
# cell20190529A1.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# cell20190529A1.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=285)
# cell20190529A1.rawdata_remove_nonrecordingblock('gapFree_0001.abf')
# cell20190529A1.write_results()
# %% no light-evoked activity recorded
# cell20190529A2 = SingleNeuron('20190529A2')
# some spont. activity with clear fast-events and spikelets; no oscillations
# blocksnames_list = cell20190529A2.get_blocknames(printing='off')
# blocksnames_list.__delitem__(0)
# for blockname in blocksnames_list:
#     cell20190529A2.rawdata_remove_nonrecordingblock(blockname)
# cell20190529A2.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 1)
# cell20190529A2.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=21, trace_end_t=582)
# cell20190529A2.write_results()
# %%
# cell20190529B = SingleNeuron('20190529B')
# spont.activity and lots of light pulses; few spont. depolarizations and not oscillating.
# looks like activating axonal inputs evokes big, compound fast-events.
# cell20190529B.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=18)
# cell20190529B.write_results()
# %%
# cell20190529C = SingleNeuron('20190529C')
# pretty leaky-looking cell but has some nice spont.activity and light pulses
# not oscillating, except for one trace where it oscillates whackily for a few s following a light pulse
# cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=28)
# cell20190529C.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_end_t=101.5)
# cell20190529C.write_results()
# %%
# cell20190529D = SingleNeuron('20190529D')
# nice-looking recording, spont.activity and lots of light pulses
# not oscillating, just constantly being bombarded with depolarizations
# cell20190529D.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
#                                                  trace_end_t=395)
# cell20190529D.write_results()
# %%
# cell20190529E = SingleNeuron('20190529E')
# spont.activity and light pulses, until cell stops responding to them
# some interesting-looking depolarizing events in spont activity; evoked they are always clearly compound
# no real oscillatory activity of any sort
# cell20190529E.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                  trace_start_t=13)
# cell20190529E.write_results()









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
# bunch of lighttriggered but no long-pulses; Vrest bad by the end but still has some depolarizing events
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
# cell20200630C = SingleNeuron('20200630C')
# spont.activity and light pulses
# there are some pretty big spontaneous fast-events, as well as a couple of APs, and cell responds to
# light consistently with an AP or what looks like a whole bunch of fast-events together
# !! for some reason there are two segments in gapFree_0000 - can only be plotted with segments_overlayed=False.
# cell20200630C.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=14)
# cell20200630C.write_results()
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
# cell20200708F = SingleNeuron('20200708F')
# the neuron that's got everything: spont. activity and light pulses, both without and with NMDA blocker.
# it's also going in and out of all kinds of different oscillating modes, and definitely has
# some fast-events (though no big-amplitude ones that I saw in files before blocker application).
# cell20200708F.rawdata_remove_nonrecordingsection('gapFree_0000.abf', trace_start_t=10)
# cell20200708F.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0006.abf', trace_end_t=565)
# cell20200708F.rawdata_note_chemicalinbath('withBlocker')
# cell20200708F.write_results()
# %%
# cell20200708G = SingleNeuron('20200708G')
# spont.activity and light pulses; cell has pretty bad Vrest and not much of any spont.activity going on,
# and light-evoked activity looks like a regular synapse that appears only after forcing V down with current.
# cell20200708G.rawdata_remove_nonrecordingsection('gapFree_withBlocker_0000.abf', trace_start_t=16)
# cell20200708G.rawdata_note_chemicalinbath('withBlocker')
# cell20200708G.write_results()
# %%