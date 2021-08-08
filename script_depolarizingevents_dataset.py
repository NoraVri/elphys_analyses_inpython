# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')
# %%
# in principle any IO neuron could have fast-events, but let's first select only the most relevant ones.
# So, let's first narrow down the dataset to neurons where we somehow try to manipulate the fast-events:
# - experiments in Thy1 mice where inputs from all over the brain are activated
# - experiments in RBP mice where inputs from the neocortex are activated
### - experiments where blockers of synaptic inputs are applied
# and let's take only neurons that were recorded for >10min. (since from my notes it seems that
# fast-events can sometimes suddenly be 'turned on' after a few min. of recording, and because
# 10min of recordings seems like a decent start for estimating the overall frequency of events occurring).

# 1. selecting only neuron recordings done on relevant experiment days (evoked synaptic excitation or blocker applied)
# listing the mice with light-evoked excitations experiments
MDJ_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',
                    'HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
RBP_mice = ['RBP', 'RBP4-cre/Ai32']
Thy1_mice = ['Thy1', 'thy1']
# listing mice with blocker-applied experiments
# blockersapplied_mice = experimentdays_metadata.specialchemicals_type.str.contains('AP5')
# blockersapplied_mice[blockersapplied_mice.isna()] = False

# getting a list of all neurons recorded on the days that those mice were used
injected_mice_condition = experimentdays_metadata.virusinjection_ID.isin(MDJ_mice)
injected_mice_experiments_dates = experimentdays_metadata[injected_mice_condition].date
injected_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(injected_mice_experiments_dates)]
injected_mice_neuronrecordings_names = injected_mice_neuronrecordings.name.dropna()

RBP_mice_condition = experimentdays_metadata.genetics.isin(RBP_mice)
RBP_mice_experiments_dates = experimentdays_metadata[RBP_mice_condition].date
RBP_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(RBP_mice_experiments_dates)]
RBP_mice_neuronrecordings_names = RBP_mice_neuronrecordings.name.dropna()

Thy1_mice_condition = experimentdays_metadata.genetics.isin(Thy1_mice)
Thy1_mice_experiments_dates = experimentdays_metadata[Thy1_mice_condition].date
Thy1_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(Thy1_mice_experiments_dates)]
Thy1_mice_neuronrecordings_names = Thy1_mice_neuronrecordings.name.dropna()

lightevokedexcitations_experiments_dates = experimentdays_metadata[
    (injected_mice_condition | RBP_mice_condition | Thy1_mice_condition)].date
lightevokedexcitations_experimentdays_recordings = recordings_metadata[
    recordings_metadata.date.isin(lightevokedexcitations_experiments_dates)]
lightevokedneuronrecordings_names = lightevokedexcitations_experimentdays_recordings.name.dropna()
# print(lightevokedneuronrecordings_names)

# %% getting all IO neuron recordings (skipping Yarom lab rig recordings (at RT) for now)
IOrecordings_dates = experimentdays_metadata[
    experimentdays_metadata.slicing_target_structure == 'inferior_olive'].date
IOslices_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(IOrecordings_dates)]
IOslices_neuronrecordings_names = IOslices_neuronrecordings.name.dropna()
smithlabrecordings_names = IOslices_neuronrecordings_names.loc[~IOslices_neuronrecordings_names.str.startswith('2016')]

# %%
# 2. selecting only neuron recordings where manipulations were actually applied, and that were recorded
# for at least 10min/30min (in case of blockers applied, this requires that the raw data has been annotated appropriately;
# in case of light-evoked excitation we can rely on 'light' appearing in the block name).
relevantneuronrecordings_names = smithlabrecordings_names

# evokedexcitations_singleneurons = []
# atleast10minrecording_singleneurons = []
atleast30minrecording_singleneurons = []

for neuron in relevantneuronrecordings_names:
    print('importing ' + neuron)
    neuron_data = SingleNeuron(neuron)
    # check time recorded
    rec_time = float(neuron_data.get_timespentrecording()/60)
    if rec_time >= 30:
        atleast30minrecording_singleneurons.append(neuron)
    # elif rec_time >= 10:
    #     atleast10minrecording_singleneurons.append(neuron)
    # check whether light pulses have been applied
    # blocknames_list = neuron_data.get_blocknames(printing='off')
    # lightactivated_list = [block for block in blocknames_list if 'light' in block]
    # if len(lightactivated_list) > 0:
    #     evokedexcitations_singleneurons.append(neuron)
    # check whether chemicals were actually applied in any of the singleneuron's recordings
    # if neuron_data.rawdata_readingnotes \
    #         and ('chemicalsapplied_blocks' in neuron_data.rawdata_readingnotes.keys()):
    #     blockedexcitations_singleneurons.append(neuron)


print('total no. of neurons in the data set: '
      + str(len(relevantneuronrecordings_names)))
# print('no. of neurons that have light-evoked excitations: '
#       + str(len(evokedexcitations_singleneurons)))
# print('no. of neurons that have at least 10 min. of recording: ' +
#       str(len(atleast10minrecording_singleneurons)))
# print('no. of neurons that have at least 10 min. of recording AND light-evoked excitations: '
#       + str(len(list(set(atleast10minrecording_singleneurons) & set(evokedexcitations_singleneurons)))))
print('no. of neurons that have at least 30 min. of recording: ' +
      str(len(atleast30minrecording_singleneurons)))
# print('no. of neurons that have at least 30 min. of recording AND light-evoked excitations: '
#       + str(len(list(set(atleast30minrecording_singleneurons) & set(evokedexcitations_singleneurons)))))

# %% selected lists of neurons
# list of neurons manually picked out for having LOTS of fast-events:
frequent_fastevents_neurons = [
'20190331A1', #-long recording but not always of great quality; still, high frequency of fast-events and compound events; honestly, perfect example of how measured parameters can vary but still reflect fast-events (it has MANY neat fast-events that adhere perfectly to how we like to see them)
'20190331A2', #-what a fucking mess.... high frequency of fast-events, but recording quality far from great and not very neat data; another good example of how fast-events parameters can vary with changing recording conditions
'20190401A1', # we like this example. -nicely extracting depolevents: done, still to sort through.
'20190401B1', # -nicely extracting depolevents: done, still to sort through.
'20190410A2', # not very frequent -nicely extracting depolevents: done, still to sort through.
'20190527A',  # this one's a winner. - Indeed, except for the stretches of time where it's making fast-events of a different shape than the classic ones (though there's still plenty of those).
'20190805A2', # intriguing example because of its oscillations. phase relationship? - Looks like not.
'20190812A',  # interesting.
'20190815C',  #-
'20200708F'   
'20210113H',  # not very frequent
'20210124A',  #
]

# compare between oscillating and non-oscillating neurons;
# separate out fast-events during oscillations and periods of not oscillating;
# separate by phase of oscillation.
# %%
# The list of neurons with >30min. recording and (not RBP) light-evoked excitations:
# ['20190527A',  # has fast-events and loads of them, 'second type' got filtered out by excluding last 20min. of recording (out of >90 min).
# '20190529B',   # just over 30 min. of recording, not a single spont fast-event.
# '20190529D',   # 9 fast-events in 45min. of recording
# '20200630C',   # 22 fast-events in 42min. of recording, 7 amplitude groups and rise-time variability much wider in low-amp than high-amp events
# '20200708F',   # work ongoing - loads of fast-events but also lots of compound ones, those all need to be filtered out first before variability in simple-events parameters can be addressed
# '20210110G',   # 3 events in 39min. of recording, all at the same amplitude (~3mV)
# '20210113H',   # has 45min. of recording and about one gross of fast-events, still needing cleanup
# '20210124A',   # almost 1.5hr of recording, hundreds of fast-events, and spont.APs that all look triggered from fast-event.
# '20210426D']   # has almost 40min. recording and some neat fast-events, but also still a lot of cleanup to do

# list of (mostly) IO neurons with > 30min. recording (not including neurons recorded in Yarom lab rig):
# ['20190319A1',
# '20190319C1',
# '20190319C2',
# '20190325B2',
# '20190325C1',
# '20190325C2',
# '20190325D2',
# '20190331A1', #
# '20190331A2', #
# '20190401A1', #
# '20190401B1', #
# '20190402A1',
# '20190409A1',
# '20190409A2',
# '20190409B2',
# '20190410A2', # not very frequent
# '20190513C',
# '20190527A',  #
# '20190529B',
# '20190529D',
# '20190729A',
# '20190804A',
# '20190804B',
# '20190804C',
# '20190805A2', #
# '20190805B1',
# '20190806A',
# '20190812A',  #
# '20190812B',
# '20190814A',
# '20190815C',  #
# '20190815D2',
# '20191105A1',
# '20191105A2',
# '20191105C',
# '20191106A1',
# '20191106A2',
# '20191119A',
# '20191120A',
# '20191120B1',
# '20191120B2',
# '20200102B',
# '20200310G',
# '20200630C',
# '20200708F',
# '20201125B',
# '20201125C',
# '20201228B',
# '20210110G',
# '20210113H',  # not very frequent
# '20210124A',  #
# '20210426D']

# list of (mostly) IO neurons recorded in Smith lab and nRiM lab, with >30min. recording (before raw data cleanup):
# ['20190131B1',# nice enough recording with what looks like LOADS of fast-events
# '20190131B2', # not a lot of fast-events (not a good recording for the most part)
# '20190131C1', # very nice recording with what looks like LOADS of fast-events
# '20190131C2', # not a lot of fast-events in this recording, but it's not a great one
# '20190206A1', # not a lot of fast-events in this recording (though did see at least 3 different amps)
# '20190206A2', # has a couple of spont.APs and events (though most of the events look rather strange)
# '20190319A1', # very clearly fast-events of multiple (large) amplitudes, but only a handful of them
# '20190319A2', # very clearly fast-events of multiple (large) amplitudes, but only a handful of them
# '20190319C1', # not a lot of fast-events, looks like they may all be the same amplitude
# '20190319C2', # no fast-events seen (oscillating neuron with plenty of spikelets)
# '20190325B1', # not a lot of fast-events, looks like they may all be the same amplitude and they have a very strange, slow decay
# '20190325B2', # not a lot of fast-events in this recording (though did see a few different amps)
# '20190325C1', # not IO neuron, but does have lots of rather large depolarizing events that may or may not be like the fast-events
# '20190325C2', # not IO neuron, but does have lots of rather large depolarizing events that may or may not be like the fast-events
# '20190325D1', # nothing actually recorded
# '20190325D2', # depolarizing things not very numerous, and look more like spikelets (amp up to ~2mV)
# '20190331A1', # not the nicest recording, but neuron for sure has LOTS of fast-events (and most of them look compound)
# '20190331A2', # not the nicest recording, but neuron does have quite a lot of fast-events (rather round peak shape relative to usual, but otherwise fitting all criteria)
# '20190401A1', # very nice recording with what looks like LOADS of fast-events
# '20190401A2', # nothing actually recorded
# '20190401B1', # nice enough recording with what looks like LOADS of fast-events in the first 10min. (and then they stop coming, as do the spont.APs)
# '20190401B2', # not actually a long recording; there's a handful of events there but they don't look like fast-events at all (except for rising pretty fast)
# '20190402A1', # did not see any fast-events (cell does seem to have spikelets and can be made to fire APs with DC)
# '20190402A2', # nothing actually recorded intracellularly
# '20190409A1', # has a handful of fast-events, mostly early on in the recording
# '20190409A2', # cell pretty much dead from the beginning, might have an event or two but not sure whether those aren't just big spikelets
# '20190409B1', # not a long recording, saw just one fast-event (mostly large-amp wacky oscillations)
# '20190409B2', # has some events before it starts oscillating (and doing nothing much else) that I'd say are spikelets, if it weren't for the fact that there's also two of 10mV amp that have the same shape (quite fast rise but very round peak)
# '20190410A1', # has some fast-events, not very frequent, but they keep coming even though the cell is pretty dead (held with lots of -DC)
# '20190410A2', # has some fast-events, not very frequent, more of them towards the end of recordings when neuron no longer oscillating much
# '20190513C',  # nice long recording but not a lot of fast-events (definitely few different amps though)
# '20190527A', # - has light-evoked excitations, too
# '20190529B', # - has light-evoked excitations, too
# '20190529D', # - has light-evoked excitations, too
# '20190729A',  # has glu-blockers applied for much of the recording, but wasn't doing any fast-events before that either
# '20190804A',  # nice recording, neuron has LOTS of fast-events (until glu-blocker is applied)
# '20190804B',  # saw 2 fast-events (same amp) before blocker getting applied
# '20190804C',  # not the nicest recording, and didn't really see any fast-events before or after blocker
# '20190805A1', # only about 5min. recording and not the most stable, but LOTS of fast-events with many different amplitudes
# '20190805A2', # quite nice recording with LOTS of fast-events especially early on (osc amp gets bigger, seeing fewer of them)
# '20190805B1', # few events even before blockers get applied; looks like the smallest ones (~2mV) may always be doubles
# '20190805B2', # has a handful of spont.APs, didn't see any fast-events though
# '20190806A',  # mostly just oscillating, not a lot of events going on by eye
# '20190812A',  # nice long recording with LOTS of fast-events (until blocker reaches the bath)
# '20190812B',  # a single fast-event, if at all (and one spont.AP, but only after glu-blocker applied).
# '20190813A',  # not actually a good recording, few minutes of a dying neuron with barely any events (if at all)
# '20190814A',  # nice recording, not so many fast-events (at least not big ones; there's an event of ~2mV that's always compound that occurs quite often)
# '20190815C',  # not a very nice recording, but has LOTS of fast-events anyhow
# '20190815D1', # it really likes to do Ca-spikes but not fast-events; weird APs with main AP having almost the same peakv as spikeshoulderpeaks
# '20190815D2', # not a nice recording, getting held with loads of -DC to keep any semblance of baselinev. Barely doing anything else.
# '20191105A1', # not a very nice recording, holding with -DC most of the time, maybe has some fast-events.
# '20191105A2', # not a very nice recording, has some fast-events (before blocker applied) but with strange shapes - very fast initial decay followed by very slow actual return to baselinev
# '20191105C',  # very boring neuron - keeps baselinev just great, but all I saw was just one fast-event
# '20191106A1', # not a very nice recording, didn't really see much of fast-events
# '20191106A2', # not IO neuron, but has a handful events with rise-time, shape and amp (2 and 6mV) matching the criteria
# '20191119A',  # nice enough recording, just doesn't have anything interesting going on
# '20191120A',  # nice enough recording, didn't really see any fast-events
# '20191120B1', # nice enough recording, didn't really see any fast-events
# '20191120B2', # nice enough recording, didn't really see any fast-events
# '20191226A',  # not IO neuron, and very boring in its activity
# '20200102B',  # nice long recording of oscillating neuron, didn't see any fast-events
# '20200306A',  # not actually a long recording or a very good one; has lots of spont APs but didn't see a lot of fast-events
# '20200310G', # has glu-uncaging-evoked excitations, too; very nice long recording with some fast-events, but cell is mostly busy oscillating
# '20200630C', # - has light-evoked excitations, too
# '20200708F', # - has light-evoked excitations, too
# '20201125B',  # nice long recording with LOADS of spont.APs and fast-events (RBP mouse, lots of light applied conditions)
# '20201125C',  # nice long recording, didn't see a lot of fast-events
# '20201228B',  # nice enough recording, didn't really see any fast-events though (cell mostly just wants to oscillate)
# '20210110G', # - has light-evoked excitations, too
# '20210113H', # - has light-evoked excitations, too
# '20210124A', # - has light-evoked excitations, too
# '20210216A',  # neuron not doing much of anything at all, not fast-events either.
# '20210426D'] # - has light-evoked excitations, too



# %% other notes:
# other things to look for (later):
# neurons recorded for > 10 min. and at RT
# select further down also by whether light application was done at different baselinev.


# workflow from here:
# for each neuron, examining depolarizing events (_script_groupingdepolarizingevents):
# - (re-)extracting depolarizing events > 2mV  # in the range below that we find also lots of spikelets and such which are not the focus of this investigation
# - annotating events with appropriate labels (fastevent, other_fastevent, compound_event, other_event, noiseevent,)
#   manually for each neuron in the dataset
# We will start with the neurons that have >30min. of recording (and at least _some number_ of fast-events),
# and determine from there what are the parameter distributions of each of the groups of events
# (mean and variance in each neuron, and in the population).   # optionally, we can extend the dataset to include neurons recorded on other experiment days (to get more that have long recording times, and to get some that were recorded at RT)
# Parameter distributions will have to be split out by baselinev, and possibly other things - this will be determined
# based on the thorough examination of these lengthy-recording examples.
# Then, we will examine neurons with >10min. of recording and see if they have any events that fall within those parameters.

# %% getting info on neurons recorded from known locations


frequent_fastevents_neurons_df = recordings_metadata.loc[
                                    recordings_metadata.name.isin(frequent_fastevents_neurons)]

