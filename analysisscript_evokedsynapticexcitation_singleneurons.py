# %% putative axonal spine responses in IO neurons.
# focus of this investigation: fast, depolarizing events of highly consistent waveform (as reflected by near-identical
# rise-time and half-width), that fall into groups of different specific amplitudes.

# Running this script will produce a set of figures summarizing the performed analyses;
# full analyses can be found in an individual script per neuron.

# Questions:
# Q1: can (a) group(s) of such fast-events be identified in the neuron's ongoing spontaneously occurring activity?
# if yes: what are the rise_time / half_width / amplitude parameters that define these events in this neuron?

# Q2: are fast-events included in the neuron's response to synaptic inputs?
# if yes: how reliably are they evoked? Does it depend on light intensity?

# Q3: what is the effect of baselinev on the appearance of fast-events?
# if they indeed represent APs triggered by synaptic inputs in axonal spines, then
# - reducing baselinev should increase the occurrence of large-amplitude fast-events (since they no longer trigger APs)
# - increasing baselinev should increase the overall frequency of fast-events and fast-event-triggered APs

# doublets: possibly one of the axonal spines is capable of activating the AIS
# should always see the same two amplitude events stacked together.

# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS

# %% the list of neurons in the dataset (evoked synaptic excitations / axons activated by light in Thy1-mouse IO)
singleneurons_list = [
                        '20190527A',
                        '20190527C',
                        '20190529A1',
                        '20190529B',
                        '20190529C',
                        '20190529D',
                        '20190529E',
                        '20200630A',
                        '20200630B1',
                        '20200630B2',
                        '20200630C',
                        '20200630D'
                      ]

# list of all neurons recorded on those experiment days:
allneurons_list = [
                    '20190527A',
                    '20190527B'
                    '20190527C',
                    '20190529A1',
                    '20190529A2',
                    '20190529B',
                    '20190529C',
                    '20190529D',
                    '20190529E',
                    '20200630A',
                    '20200630B1',
                    '20200630B2',
                    '20200630C',
                    '20200630D'
                   ]

# %%
for neuron in singleneurons_list:
    singleneuron_rawdata = SingleNeuron(neuron)
    singleneuron_evoked_events = singleneuron_rawdata.depolarizing_events.applied_ttlpulse
    singleneuron_spont_events = ~singleneuron_rawdata.depolarizing_events.applied_ttlpulse

    singleneuron_rawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time',
                                                             cmeasure='baselinev',
                                                             evokedevents=singleneuron_evoked_events,
                                                             spontevents=singleneuron_spont_events)
    plt.suptitle(singleneuron_rawdata.name)

    singleneuron_rawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                             cmeasure='baselinev',
                                                             evokedevents=singleneuron_evoked_events,
                                                             spontevents=singleneuron_spont_events)
    plt.suptitle(singleneuron_rawdata.name)

    singleneuron_rawdata.scatter_depolarizingevents_measures('amplitude', 'half_width',
                                                             cmeasure='baselinev',
                                                             evokedevents=singleneuron_evoked_events,
                                                             spontevents=singleneuron_spont_events)
    plt.suptitle(singleneuron_rawdata.name)

    spontevents_df = singleneuron_rawdata.depolarizing_events[singleneuron_spont_events]
    evokedevents_df = singleneuron_rawdata.depolarizing_events[singleneuron_evoked_events]
    maxeventamp = singleneuron_rawdata.depolarizing_events.amplitude.max()
    _, axes = plt.subplots(1, 2, sharex='row', sharey='row')
    spontevents_df.hist('amplitude', ax=axes[0], bins=np.arange(0, maxeventamp, 0.1))
    axes[0].set_title(singleneuron_rawdata.name + 'spont events')
    evokedevents_df.hist('amplitude', ax=axes[1], bins=np.arange(0, maxeventamp, 0.1))
    axes[1].set_title(singleneuron_rawdata.name + 'evoked events')

# %% notes on singleneuron data, and getting data individually per neuron
# (neurons that aren't listed here have moved to their own individual analysis script)


singleneuron_rawdata = SingleNeuron('20190527C')
# from the amplitude histogram and the rise-time scatters it looks like this neuron should have some fast-events,
# but a clear boundary between groups of fast-events and other events is not evident by eye


# singleneuron_rawdata = SingleNeuron('20190529A1')


# singleneuron_rawdata = SingleNeuron('20190529B')
# there's just two events that may be spontaneously occurring fast-events (the other larger-amp events that
# are detected are in fact oscillation leftovers), but the evoked events are pretty cool:
# all very close in rise-time, but half-widths group into 3 groups. Is this expected of stacked fast-events?


# singleneuron_rawdata = SingleNeuron('20190529C')
# looks like it may have a couple of spontaneously occurring fast-events, but they are not activated by light.


# singleneuron_rawdata = SingleNeuron('20190529D')
# also seems to have the ~5mV fast but not fast-event depolarization that 0527A has,
# and just one single spontaneous actual fast-event (14mV)
# If fast-events are being evoked, looks like they're always compound (half-width > twice that of spont ones)


# singleneuron_rawdata = SingleNeuron('20190529E')
# from the amplitude histogram it looks like two or three different fast-events may be activated by light,
# but spontaneous fast-events are very rare


singleneuron_evoked_events = singleneuron_rawdata.depolarizing_events.applied_ttlpulse
singleneuron_spont_events = ~singleneuron_rawdata.depolarizing_events.applied_ttlpulse

spontevents_df = singleneuron_rawdata.depolarizing_events[(
        (~singleneuron_rawdata.depolarizing_events.applied_ttlpulse)
)]
# %% Q1: can (groups of) fast-events be identified in the neuron's ongoing spontaneous activity?
# steps:
# 1] seeing the distributions of the main parameters that we expect divide events into groups:
#       rise-time, amplitude and half-width (and baselinev) to confirm that we can expect to see fast-events groups
# 2] applying clustering/PCA to find (groups of) different types of events
# - based on amplitude(&baselinev);
#   exclude the cluster of smallest-amp events and spikeshoulderpeaks (based on baselinev),
#   and maybe also non-clustered points (depending on overall number of events&clustering method used)
# - based on rise-time, 20-80%rise-time and half-width;
# in neurons with lots of spontaneous events, fast-events should become evident as a cluster of events
#   with (almost) identical rise-time and half-width but varying amplitude.


# %% seeing rise-time, half-width, amplitude and baselinev distributions (spontaneous events only)
# histograms of event parameters
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

# scatters of event parameters
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

# %% selecting out some events that are definitely not gonna be fast-events
spontevents_df = singleneuron_rawdata.depolarizing_events[(
        (~singleneuron_rawdata.depolarizing_events.applied_ttlpulse)
)]

spontevents_df = spontevents_df[(
        (spontevents_df.amplitude > 0.6)
        & (spontevents_df.baselinev < -40)
        & (spontevents_df.baselinev > -73)
        & (~spontevents_df.half_width.isna())
)]

# %% using OPTICS to find clusters of events in the data (spontaneous events only)
clustering_eventparams = spontevents_df[['rise_time',
                                         'rise_time_20_80',
                                         'half_width',
                                         # 'amplitude',
                                         'baselinev']].to_numpy()

clustering = OPTICS(min_samples=2)
clustering.fit(clustering_eventparams)
# %% looking at clustering results
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
           cmap='prism')

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


# %%
probablyfastevents_df = spontevents_df[(
    (clustering.labels_ == 422)
    | (clustering.labels_ == 388)
    | (clustering.labels_ == 389)
)]
condition_probablyfastevent = singleneuron_rawdata.depolarizing_events.index.map(
                                lambda x: x in list(probablyfastevents_df.index) )

singleneuron_rawdata.plot_depolevents_overlayed(condition_probablyfastevent,
                                                # do_normalizing=True,
                                                do_baselining=True,
                                                colorby_measure='baselinev')


# %%

# step1: OPTICS clustering by amplitude & baselinev
# clusteringbyvoltage_data = spontevents_df.amplitude.to_numpy().reshape(-1, 1)
clusteringbyvoltage_data = spontevents_df[['amplitude', 'baselinev']].to_numpy()
clusterbyvoltage = OPTICS(min_samples=2,
                          max_eps=0.1,
                          # xi=0.01
                          )
clusterbyvoltage.fit(clusteringbyvoltage_data)

# %% seeing the results: amplitude/baselinev scatter colored by clusters, and reachability plot
_, axes = plt.subplots(1, 2)
xrange = np.arange(len(clusteringbyvoltage_data))
clusterordered_reachability = clusterbyvoltage.reachability_[clusterbyvoltage.ordering_]
clusterordered_labels = clusterbyvoltage.labels_[clusterbyvoltage.ordering_]
axes[0].scatter(xrange[clusterordered_labels == -1], clusterordered_reachability[clusterordered_labels == -1],
            c='k', marker='+')
axes[0].scatter(xrange[clusterordered_labels > -1], clusterordered_reachability[clusterordered_labels > -1],
            c=clusterordered_labels[clusterordered_labels > -1], cmap='prism')
axes[0].set_ylabel('reachability (epsilon distance)')
axes[0].set_xlabel('event no.')

axes[1].scatter(spontevents_df.baselinev[clusterbyvoltage.labels_ == -1],
                spontevents_df.amplitude[clusterbyvoltage.labels_ == -1],
                c='k', marker='+')
axes[1].scatter(spontevents_df.baselinev[clusterbyvoltage.labels_ > -1],
                spontevents_df.amplitude[clusterbyvoltage.labels_ > -1],
                c=clusterbyvoltage.labels_[clusterbyvoltage.labels_ > -1], cmap='prism')
axes[1].set_xlabel('baselinev')
axes[1].set_ylabel('amplitude')


# %%





# %%
clusterpoints = allspontevents_df[clust_class.labels_ > -1]
clusterpoints_labels = clust_class.labels_[clust_class.labels_ > -1]
noclusterpoints = allspontevents_df[clust_class.labels_ == -1]

# %%
_, axes = plt.subplots(1, 1, sharey='all', sharex='all')
axes.scatter(x=clusterpoints.amplitude, y=clusterpoints.baselinev,
                c=clusterpoints_labels)
axes.scatter(x=noclusterpoints.amplitude, y=noclusterpoints.baselinev,
                c='k', marker='+')

# %%
# rise-time vs amp, rise-time vs half_width, half_width vs amp scatters colored by clusters
figure, axes = plt.subplots(2, 2, sharex='col', sharey='row')
axes[0,0].scatter(x=noclusterpoints.rise_time_20_80, y=noclusterpoints.amplitude,
                  c='k',
                  marker='+')
axes[0,0].scatter(x=clusterpoints.rise_time_20_80, y=clusterpoints.amplitude,
                  c=clusterpoints_labels,
                  cmap='viridis')
axes[1,0].scatter(x=noclusterpoints.rise_time_20_80, y=noclusterpoints.half_width,
                  c='k',
                  marker='+')
axes[1,0].scatter(x=clusterpoints.rise_time_20_80, y=clusterpoints.half_width,
                  c=clusterpoints_labels,
                  cmap='viridis')
axes[1,1].scatter(x=noclusterpoints.amplitude, y=noclusterpoints.half_width,
                  c='k',
                  marker='+')
axes[1,1].scatter(x=clusterpoints.amplitude, y=clusterpoints.half_width,
                  c=clusterpoints_labels,
                  cmap='viridis')
axes[0,0].set_ylabel('amplitude')
axes[1,0].set_xlabel('rise_time_20_80')
axes[1,0].set_ylabel('half_width')
axes[1,1].set_xlabel('amplitude')
# %%
# plotting - 3d scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# plot non-assigned points as black +'s
nocluster_points = allspontevents_df[clust_class.labels_ == -1]
ax.scatter(xs=nocluster_points.rise_time_20_80,
           ys=nocluster_points.amplitude,
           zs=nocluster_points.half_width,
           c='k',
           marker='+')
# plot up to 15 clusters in colors
if max(clust_class.labels_) <= 15:
    clustered_points = allspontevents_df[clust_class.labels_ >= 0]
    ax.scatter(xs=clustered_points.rise_time_20_80,
               ys=clustered_points.amplitude,
               zs=clustered_points.half_width,
               c=clust_class.labels_[(clust_class.labels_ >= 0)],
               colormap='viridis')
if max(clust_class.labels_) > 15:
    first15clusters_points = allspontevents_df[((clust_class.labels_ <= 15) & (clust_class.labels_ >= 0))]
    ax.scatter(xs=first15clusters_points.rise_time_20_80,
               ys=first15clusters_points.amplitude,
               zs=first15clusters_points.half_width,
               c=clust_class.labels_[((clust_class.labels_ <= 15) & (clust_class.labels_ >= 0))])
# plot points belonging to all other clusters as empty circles
    otherclusters_points = allspontevents_df[clust_class.labels_ > 15]
    ax.scatter(xs=otherclusters_points.rise_time_20_80,
               ys=otherclusters_points.amplitude,
               zs=otherclusters_points.half_width,
               c='k',
               marker='o')



# %% scatter plot: amplitude vs rise-time
singleneuron_rawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                         cmeasure='half_width',
                                                         spontevents=singleneuron_spont_events,
                                                         evokedevents=singleneuron_evoked_events)
# plt.suptitle('all detected events')

# %% scatter plot: half-width vs rise-time
singleneuron_rawdata.scatter_depolarizingevents_measures('half_width', 'rise_time_20_80',
                                                         cmeasure='amplitude',
                                                         spontevents=singleneuron_spont_events)
singleneuron_rawdata.scatter_depolarizingevents_measures('half_width', 'rise_time_20_80',
                                                         cmeasure='amplitude',
                                                         evokedevents=singleneuron_evoked_events)

# %% 3D scatter of spontaneous events measures
spontevents_df = singleneuron_rawdata.depolarizing_events[singleneuron_spont_events]
spontevents_df = spontevents_df[spontevents_df.amplitude > 1.8]
xdata = spontevents_df.rise_time
ydata = spontevents_df.rise_time_20_80
zdata = spontevents_df.half_width
cdata = spontevents_df.amplitude

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xdata, ydata, zdata, c=cdata)
ax.set_xlabel(xdata.name)
ax.set_ylabel(ydata.name)
ax.set_zlabel(zdata.name)
plt.colorbar()
# %% excluding groups of events that definitely do not meet criteria
# events with baselinev > -25mV are in fact spike-shoulder peaks:
spikeshoulderpeaks = singleneuron_rawdata.depolarizing_events.baselinev > -25
# cell20190527Arawdata.plot_depolevents_overlayed(spikeshoulderpeaks,
#                                                 colorby_measure='baselinev',
#                                                 prealignpoint_window_inms=20)
# updating events-tables accordingly:
singleneuron_evoked_events = singleneuron_evoked_events \
                             & (~spikeshoulderpeaks)
singleneuron_spont_events = singleneuron_spont_events \
                            & (~spikeshoulderpeaks)

# both in spont. and evoked events there is one single one with a much larger amplitude than all the others
# the evoked one looks like it could be real, though it's coming from baselinev ~-30;
# the spont. one looks like a weird noise
verylargeampevents = (singleneuron_rawdata.depolarizing_events.amplitude > 15) & (~spikeshoulderpeaks)
# cell20190527Arawdata.plot_depoleventsgroups_overlayed((verylargeampevents&cell20190527Aspont_events),
#                                                       (verylargeampevents&cell20190527Aevoked_events),
#                                                       group_labels=['spont', 'evoked'],
#                                                       plt_title='strangely large-amp events')
# updating events-tables accordingly:
singleneuron_spont_events = singleneuron_spont_events \
                            & (~verylargeampevents)

# 2mV is the smallest amplitude at which a somewhat clear grouping of fast rise_time (20_80 < 0.6 ms) events
# can be seen in the rise-time/amplitude scatter of spontaneous events
# TODO: revisit this criterion to see if there are more fast-events to be fished out of the small depolarizations
# updating events-tables accordingly:
amptoosmall = singleneuron_rawdata.depolarizing_events.amplitude < 2
singleneuron_evoked_events = singleneuron_evoked_events \
                             & (~amptoosmall)
singleneuron_spont_events = singleneuron_spont_events \
                            & (~amptoosmall)

# the string of spontaneous events in different amplitude-groups all seems to have rise_time_20_80 < 1ms
# in the evoked responses, there may be some that are a spikelet+fast-event;
# in the spontaneous responses there are some intriguing large-amplitude (>5mV) ones that definitely aren't fast-events
# TODO: revisit this criterion to include evoked responses that are fast-event + something
risetimetoolong = singleneuron_rawdata.depolarizing_events.rise_time_20_80 > 1
# cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events & risetimetoolong),
#                                                 colorby_measure='baselinev',
#                                                 do_baselining=True,
#                                                 # do_normalizing=True,
#                                                 total_plotwindow_inms=15
#                                                 )
# plt.suptitle('>1ms rise-time_20_80 events, spontaneous only')
# cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aevoked_events & risetimetoolong),
#                                                 colorby_measure='baselinev',
#                                                 do_baselining=True,
#                                                 # do_normalizing=True,
#                                                 total_plotwindow_inms=15
#                                                 )
# plt.suptitle('>1ms rise-time_20_80 events, evoked only')
# updating events-tables accordingly:
singleneuron_evoked_events = singleneuron_evoked_events \
                             & (~risetimetoolong)
singleneuron_spont_events = singleneuron_spont_events \
                            & (~risetimetoolong)














# %% line-plots of subsets of events
# first, let's see the large-amplitude events and yet do not have very fast rise-time:
largeampevents = (singleneuron_rawdata.depolarizing_events.amplitude > 10) \
                 & (singleneuron_rawdata.depolarizing_events.amplitude < 15)
singleneuron_rawdata.plot_depolevents_overlayed((singleneuron_spont_events & largeampevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=10,
                                                total_plotwindow_inms=50
                                                )
plt.suptitle('large amplitude events')
# the largest one of those looks like a weird noise, updating events-table accordingly
singleneuron_spont_events = singleneuron_spont_events & (singleneuron_rawdata.depolarizing_events.amplitude < 15)
# the others look like compound fast-events where the first one has an amplitude of ~5mV and
# doesn't decay until another event is triggered.
#
# let's see if this is also the case for other relatively large-amp but slow rise events:
bigbutslowevents = (singleneuron_rawdata.depolarizing_events.amplitude > 2) \
                   & (singleneuron_rawdata.depolarizing_events.rise_time_20_80 > 1.5) \
                   & (singleneuron_rawdata.depolarizing_events.baselinev < -45)
singleneuron_rawdata.plot_depolevents_overlayed((singleneuron_spont_events & bigbutslowevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=10,
                                                total_plotwindow_inms=30
                                                )
plt.suptitle('big yet relatively slow events')
# yea pretty much looks like exactly that, every one of these events looks compound, though it doesn't seem like
# each of these necessarily has a fast-event in there...
# %% now let's see things that really should be fast-events
probablyfastevents = (singleneuron_rawdata.depolarizing_events.amplitude > 3) \
                     & (singleneuron_rawdata.depolarizing_events.rise_time_20_80 < 1.5) \
                     & (singleneuron_rawdata.depolarizing_events.baselinev < -50)  # just to see fewer lines
singleneuron_rawdata.plot_depolevents_overlayed((singleneuron_spont_events & probablyfastevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=15,
                                                timealignto_measure='rt_midpoint_idx'
                                                )
plt.suptitle('should-be fast-events')
# at the intersection of rise_time_20_80 = ~1ms and amplitude =~5-6mV there seems to be a group of events that is
# too large to be a spikelet but just a bit too slow to be a fast-event, and from the line plot it looks like
# this event also comes in amplitude =~2mV.
# %% narrowing it down to things that are definitely fast-events
definitelyfastevents = (singleneuron_rawdata.depolarizing_events.amplitude > 4) \
                       & (singleneuron_rawdata.depolarizing_events.rise_time_20_80 <= 0.7) \
                       & (singleneuron_rawdata.depolarizing_events.half_width < 4)
singleneuron_rawdata.plot_depolevents_overlayed((singleneuron_evoked_events & definitelyfastevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=15,
                                                timealignto_measure='rt_midpoint_idx'
                                                )
plt.suptitle('fast-events only')
