# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns

# functions written just for this purpose
def make_lightONmeasures_dict():
    lighton_measures = {
        'file_origin': [],
        'segment_idx': [],

        'ttlon_duration_inms': [],
        'lighton_duration_inms': [],
        'lighton_offset_inms': [],

        'lighton_amplitude': [],

        'ttlon_idx': [],
        'ttloff_idx': [],
        'lighton_idx': [],
        'lightoff_idx': [],

    }
    return lighton_measures


def get_lightON_measures_perblock(block, ttlhigh_value=1, minlighton_value=0.007):
    lightonmeasures_dict = make_lightONmeasures_dict()
    for idx, segment in enumerate(block.segments):
        ttlout_rec = np.array(np.squeeze(segment.analogsignals[2]))
        light_rec = np.array(np.squeeze(segment.analogsignals[3]))
        nsamples_per_ms = int(1 / segment.analogsignals[0].sampling_period.rescale('ms'))

        ttlon_idcs = np.where((np.squeeze(ttlout_rec > ttlhigh_value)) == True)[0]
        lighton_idcs = np.where((np.squeeze(light_rec > minlighton_value)) == True)[0]

        if len(ttlon_idcs) > 0:
            ttlon_idx = ttlon_idcs[0]
            ttloff_idx = ttlon_idcs[-1]
            ttl_duration_inms = (ttloff_idx - ttlon_idx + 1) / nsamples_per_ms
        else:
            ttlon_idx = None
            ttloff_idx = None
            ttl_duration_inms = None

        if len(lighton_idcs) > 0:
            lighton_idx = lighton_idcs[0]
            lightoff_idx = lighton_idcs[-1]
            light_duration_inms = (lightoff_idx - lighton_idx + 1) / nsamples_per_ms
            light_amplitude = np.max(light_rec[lighton_idx:lightoff_idx])

            if ttlon_idx is not None:
                lightoffset_insamples = lighton_idx - ttlon_idx
                light_offset_inms = lightoffset_insamples / nsamples_per_ms
            else:
                light_offset_inms = None
        else:
            lighton_idx = None
            lightoff_idx = None
            light_duration_inms = None
            light_amplitude = None
            light_offset_inms = None

        lightonmeasures_dict['file_origin'].append(block.file_origin)
        lightonmeasures_dict['segment_idx'].append(idx)
        lightonmeasures_dict['ttlon_duration_inms'].append(ttl_duration_inms)
        lightonmeasures_dict['lighton_duration_inms'].append(light_duration_inms)
        lightonmeasures_dict['lighton_offset_inms'].append(light_offset_inms)
        lightonmeasures_dict['lighton_amplitude'].append(light_amplitude)
        lightonmeasures_dict['ttlon_idx'].append(ttlon_idx)
        lightonmeasures_dict['ttloff_idx'].append(ttloff_idx)
        lightonmeasures_dict['lighton_idx'].append(lighton_idx)
        lightonmeasures_dict['lightoff_idx'].append(lightoff_idx)

    return lightonmeasures_dict


def get_lightON_measures(data, **kwargs):
    all_lighton_measures_dict = make_lightONmeasures_dict()
    for block in data.blocks:
        print(block.file_origin)
        block_lighton_measures = get_lightON_measures_perblock(block, **kwargs)
        for key in all_lighton_measures_dict.keys():
            all_lighton_measures_dict[key] += block_lighton_measures[key]
    # converting to DataFrame:
    lighton_measures = pd.DataFrame(all_lighton_measures_dict).round(decimals=3)
    dtypes_dict = {}
    for key in lighton_measures.keys():
        if 'idx' in key:
            dtypes_dict[key] = 'Int64'
    lighton_measures = lighton_measures.astype(dtypes_dict)
    return lighton_measures


def plot_alignedto_light_onset(data, preonset_idcs=550, postonset_idcs=1500):
    lighton_measures_df = get_lightON_measures(data)
    lightontrials_measures_df = lighton_measures_df[~(lighton_measures_df.lighton_duration_inms.isna())]
    for blockname in lightontrials_measures_df.file_origin.unique():
        block_trials = lightontrials_measures_df[(lightontrials_measures_df.file_origin == blockname)]
        block_data = [block for block in data.blocks if block.file_origin == blockname][0]
        figure, axes = plt.subplots(2, 1, squeeze=False)
        figure.suptitle(blockname)
        axes = axes.squeeze(axis=1)
        axes[0].set_ylabel('TTL')
        axes[1].set_ylabel('light')
        axes[1].set_xlabel('indices')
        for _, trial in block_trials.iterrows():
            plotwindow_startidx = trial.lighton_idx - preonset_idcs
            plotwindow_endidx = trial.lighton_idx + postonset_idcs
            trial_segment_data = block_data.segments[trial.segment_idx]
            axes[0].plot(np.squeeze(trial_segment_data.analogsignals[2])[plotwindow_startidx:plotwindow_endidx])
            axes[1].plot(np.squeeze(trial_segment_data.analogsignals[3])[plotwindow_startidx:plotwindow_endidx])


# %% in this script:
# take measurements obtained from a detector mounted temporarily in the place of the condensor,
# show some plots to characterize the instability in onset and duration of the light

data = SingleNeuron('20240410testing_light')
# data.plot_rawdatablocks()
# The first two blocks were recorded with the detector OFF. When the light is on, a tiny response can sometimes be seen - not sure what's up with that
# conditions tested: 1ms and 10ms TTL pulse, at 5, 50 and 100% light intensity setting

lighton_measures_df = get_lightON_measures(data)
# whittle it down to blocks with detector on
lighton_measures_df = lighton_measures_df[lighton_measures_df.file_origin.str.contains('detectorON')]

# %% plotting results
# First let's see how steady the max.amplitude reached by the light pulse is:
# lighton_measures_df.plot.scatter('ttlon_duration_inms', 'lighton_amplitude')
# looks decently stable, there's a bit of jitter but the 5, 50 and 100% intensity levels tested here are very easy to tell apart
# conclusion: on means on, there's no light pulses that turn on but do not reach the maximum intensity level (and the maximum intensity level varies with the light % setting)


# let's look at the 1ms TTL-pulse data:
ttl1ms_lmdf = lighton_measures_df[(lighton_measures_df.ttlon_duration_inms < 2)]
# lots of 'nan's in there for lighton_duration - let's see the failure rate:
light_failure_rate = sum(ttl1ms_lmdf.lighton_duration_inms.isna()) / len(ttl1ms_lmdf)
# 87% failure rate!!

# now let's see light duration vs. onset relative to ttl
ttl1ms_lmdf.plot.scatter('lighton_offset_inms', 'lighton_duration_inms')
plt.suptitle('1ms TTL pulse')

# now let's take the 10ms TTL-pulse data:
ttl10ms_lmdf = lighton_measures_df[(lighton_measures_df.ttlon_duration_inms > 9)]
sum(ttl10ms_lmdf.lighton_duration_inms.isna())  # = 0  --> no failures

# let's see light duration vs. onset relative to ttl
ttl10ms_lmdf.plot.scatter('lighton_offset_inms', 'lighton_duration_inms')
plt.suptitle('10ms TTL pulse')

# it looks too weird to be real, but let's plot the traces aligned to light onset to see:
plot_alignedto_light_onset(data)



# %% new light box
data = SingleNeuron('20240419_newbox_testing_light')
# data.plot_rawdatablocks()
lighton_measures_df = get_lightON_measures(data)
# whittle it down to blocks with detector on
lighton_measures_df = lighton_measures_df[lighton_measures_df.file_origin.str.contains('detectorON')]

lighton_measures_df.plot.scatter('ttlon_duration_inms', 'lighton_amplitude')
# %%
sns.scatterplot(data=lighton_measures_df[lighton_measures_df.file_origin.str.contains('100')],
                x='ttlon_duration_inms', y='lighton_amplitude',)