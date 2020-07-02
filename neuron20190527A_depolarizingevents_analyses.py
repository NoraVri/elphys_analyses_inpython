# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

# getting neuron20190527A data (including APs and depolarizing events)
singleneuron_rawdata = SingleNeuron('20190527A')

singleneuron_evoked_events = singleneuron_rawdata.depolarizing_events.applied_ttlpulse
singleneuron_spont_events = ~singleneuron_rawdata.depolarizing_events.applied_ttlpulse

# general notes single neuron data & analyses:
# This neuron definitely has fast-events in a few different amplitude, and tons of APs.

# The histogram of spontaneous events quite clearly delineates multiple groups, and the
# rise-time/half-width/amplitude scatters clearly show a string of events with highly similar
# rise-time and half-width but varying amplitudes.
# The amplitude histogram suggests that there are evoked events in the same amplitude-range as spontaneous ones,
# however the scatters indicate that the kinetics of evoked events differ from spontaneous ones.

# Other noteworthy things:
# - There appears to be another kind of relatively fast and large event, with slightly slower rise and different decay
#   (as can be seen in the scatters).
# - The neuron is transiently oscillating quite a lot of the time, and there's depolarizing events that seem to be
#   followed by hyperpolarization/epochs of oscillation surprisingly often.

# %% Q1: can different groups of depolarizing events be identified in the neuron's spontaneously occurring activity?
# %% getting a df of 'proper' spontaneous depolarizing events by filtering the depolarizingevents-table for:
# - ttl pulse applied (otherwise it's evoked)
# - spikeshoulderpeaks
# - small events, that clearly fall within the smallest amplitude-group of events (as seen in histogram)
# - events whose half-width could not be determined (nan's cannot be included in data for clustering)
# - events with half-width > 12 ms (these are all rather small relative to their slow decay)
spontevents_conditions = (
        (~singleneuron_rawdata.depolarizing_events.applied_ttlpulse)
        & ~(singleneuron_rawdata.depolarizing_events.event_label == 'spikeshoulderpeak')
        & (singleneuron_rawdata.depolarizing_events.amplitude > 0.6)
        & ~singleneuron_rawdata.depolarizing_events.half_width.isna()
        & (singleneuron_rawdata.depolarizing_events.half_width < 12)
)

spontevents_df = singleneuron_rawdata.depolarizing_events[spontevents_conditions]

# %%
singleneuron_rawdata.plot_depolevents_overlayed((spontevents_conditions
                                                 & (singleneuron_rawdata.depolarizing_events.half_width > 10)
                                                 & (singleneuron_rawdata.depolarizing_events.half_width < 12)
                                                 & (singleneuron_rawdata.depolarizing_events.amplitude > 0.5)),
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                colorby_measure='half_width')


# %% overview-plots of spontaneous depolarizing events parameters
# histograms:
# amplitude
maxeventamp = spontevents_df.amplitude.max()
plot1, axes = plt.subplots(1, 2, sharex='row', sharey='row')
spontevents_df.hist('amplitude', ax=axes[0], bins=np.arange(0, maxeventamp, 0.1))
axes[0].set_title('amplitude, 0.1mV bins')
spontevents_df.hist('amplitude', ax=axes[1], bins=np.arange(0, maxeventamp, 0.05))
axes[1].set_title('amplitude, 0.05mV bins')
plot1.suptitle(singleneuron_rawdata.name + ' spont. events')

# rise-time (20-80%) and half-width
maxeventrisetime = spontevents_df.rise_time_20_80.max()
plot2, axes = plt.subplots(1, 2, sharey='row')
spontevents_df.hist('rise_time_20_80', ax=axes[0], bins=np.arange(0, maxeventrisetime, 0.1))
axes[0].set_title('rise_time (20-80%)')
maxeventhalfwidth = spontevents_df.half_width.max()
spontevents_df.hist('half_width', ax=axes[1], bins=np.arange(0, maxeventhalfwidth, 0.1))
axes[1].set_title('half-width')
plot2.suptitle(singleneuron_rawdata.name + ' spont. events')

# scatter plots:
# rise-time and half-width vs amplitude
_, axes = plt.subplots(1, 2, sharey='all')
spontevents_df.plot.scatter('rise_time_20_80', 'amplitude', c='half_width', colormap='viridis', ax=axes[0])
spontevents_df.plot.scatter('half_width', 'amplitude', c='rise_time_20_80', colormap='viridis', ax=axes[1])
plt.suptitle(singleneuron_rawdata.name)

# rise-time, half-width and amplitude (3D scatter)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs=spontevents_df.rise_time_20_80,
           ys=spontevents_df.half_width,
           zs=spontevents_df.amplitude,
           c=spontevents_df.baselinev,
           cmap='viridis')
ax.set_xlabel('rise-time (20-80%)')
ax.set_ylabel('half-width')
ax.set_zlabel('amplitude')
plt.suptitle(singleneuron_rawdata.name)

# amplitude vs baselinev
_, axes = plt.subplots(1, 2, sharey='all', sharex='all')
spontevents_df.plot.scatter('baselinev', 'amplitude', c='half_width', colormap='viridis', ax=axes[0])
spontevents_df.plot.scatter('baselinev', 'amplitude', c='rise_time_20_80', colormap='viridis', ax=axes[1])
plt.suptitle(singleneuron_rawdata.name)

# %% clustering the 'clean' events by parameters describing their waveform
clustering_eventparams = spontevents_df[['rise_time',
                                         'rise_time_20_80',
                                         'half_width',
                                         # 'amplitude',
                                         'baselinev']].to_numpy()

clustering = OPTICS(min_samples=10)
clustering.fit(clustering_eventparams)

# looking at clustering results
# reachability plot
xrange = np.arange(len(clustering_eventparams))
clusterordered_reachability = clustering.reachability_[clustering.ordering_]
clusterordered_labels = clustering.labels_[clustering.ordering_]
plt.figure()
plt.scatter(xrange[clusterordered_labels == -1], clusterordered_reachability[clusterordered_labels == -1],
            c='k', marker='+')
plt.scatter(xrange[clusterordered_labels > -1], clusterordered_reachability[clusterordered_labels > -1],
            c=clusterordered_labels[clusterordered_labels > -1], cmap='prism')
plt.ylabel('reachability (epsilon distance)')
plt.xlabel('event no.')

# rise-time, half-width and amplitude 3D scatter, colored by clusters
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs=spontevents_df.rise_time_20_80[clustering.labels_ == -1],
           ys=spontevents_df.half_width[clustering.labels_ == -1],
           zs=spontevents_df.amplitude[clustering.labels_ == -1],
           c='k',
           marker='+')
ax.scatter(xs=spontevents_df.rise_time_20_80[clustering.labels_ > -1],
           ys=spontevents_df.half_width[clustering.labels_ > -1],
           zs=spontevents_df.amplitude[clustering.labels_ > -1],
           c=clustering.labels_[clustering.labels_ > -1],
           cmap='Set3')

ax.set_xlabel('rise-time (20-80%)')
ax.set_ylabel('half-width')
ax.set_zlabel('amplitude')
plt.suptitle(singleneuron_rawdata.name)

# event amplitude vs cluster no., colored by rise-time/half-width
figure, axes = plt.subplots(1, 2, sharex='all', sharey='all')
axes[0].scatter(clustering.labels_[clustering.labels_ == -1], spontevents_df.amplitude[clustering.labels_ == -1],
                c='k', marker='+')
axes[0].scatter(clustering.labels_[clustering.labels_ > -1], spontevents_df.amplitude[clustering.labels_ > -1],
                c=spontevents_df.rise_time_20_80[clustering.labels_ > -1], cmap='viridis')
axes[0].set_xlabel('cluster #')
axes[0].set_ylabel('event amplitude')
axes[0].set_title('colored by rise-time')
axes[1].scatter(clustering.labels_[clustering.labels_ == -1], spontevents_df.amplitude[clustering.labels_ == -1],
                c='k', marker='+')
axes[1].scatter(clustering.labels_[clustering.labels_ > -1], spontevents_df.amplitude[clustering.labels_ > -1],
                c=spontevents_df.half_width[clustering.labels_ > -1], cmap='viridis')
axes[1].set_xlabel('cluster #')
axes[1].set_ylabel('event amplitude')
axes[1].set_title('colored by half-width')


