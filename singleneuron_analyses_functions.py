# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:33:29 2020

@author: neert

This file defines a class for working with depolarizing events.
"""
# %% imports
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import quantities as pq

# %%
def get_depolarizingevents(single_segment,
                           min_depolspeed=0.1,
                           min_depolamp=0.1,
                           peakwindow=10,
                           spikewindow=40,
                           noisefilter_hpfreq = 3000,
                           oscfilter_lpfreq = 20,
                           plot = 'on'):
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.array(np.squeeze(single_voltage_trace)) #!Make sure it's in mV
    current_recording = np.array(np.squeeze(single_segment.analogsignals[1])) #!Make sure it's in pA
    sampling_frequency = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz
    sampling_period_inms = float(single_voltage_trace.sampling_period) * 1000 *pq.ms

    #parameter settings - default time windows:
    window_inms = 1 #window used for calculating the 'rough' derivative and candidate-depolarizations points
    window_insamples = int(sampling_frequency / 1000 * window_inms)
    peakwindow_inms = peakwindow #distance from depol_idx to potential peak
    peakwindow_insamples = int(sampling_frequency / 1000 * peakwindow_inms)
    spikewindow_inms = spikewindow
    spikewindow_insamples = int(sampling_frequency / 1000 * spikewindow_inms)

    #prep:
    #filtering the raw voltage twice: high-pass to get 'only the noise', and low-pass to get 'only the STOs'.
    #subtract both from raw voltage to get trace for event-detection
    lowpass_sos = signal.butter(2, oscfilter_lpfreq, btype='lowpass', fs=sampling_frequency, output='sos')
    voltage_oscillationstrace = signal.sosfiltfilt(lowpass_sos, voltage_recording)
    highpass_sos = signal.butter(1, noisefilter_hpfreq, btype='highpass', fs=sampling_frequency, output='sos')
    voltage_noisetrace = signal.sosfiltfilt(highpass_sos, voltage_recording)
    voltage_eventdetecttrace = voltage_recording - voltage_oscillationstrace - voltage_noisetrace

    #taking the ms-by-ms derivative
    voltage_permsderivative = []
    for idx in range(0,len(voltage_eventdetecttrace)-window_insamples):
        v_slope_approx = voltage_eventdetecttrace[idx+window_insamples] - voltage_eventdetecttrace[idx]
        voltage_permsderivative.append(v_slope_approx)
    voltage_permsderivative = np.array(voltage_permsderivative)
    time_axis_derivative = time_axis[:len(voltage_permsderivative):]

    #actually collecting points of interest: peaks of depolarizations, and their baseline-points
    depolarizations = []
    depols_with_peaks = []
    peaks_idcs = []
    for idx in range(len(voltage_permsderivative) - peakwindow_insamples):
        #skip points that refer to places on already-identified events
        if peaks_idcs and idx < peaks_idcs[-1]:
            continue
        else:
    #1. identify depolarizations of mindepol mV/ms or more
        # points qualify as depolarizations if:
        # - dV/dt_ms in the first 1ms window is not too variable (mean-min < mindepol)
        # - mean dVdt_ms in the second 1ms window is > mindepol + mean dVdt_ms in the first 1ms window
            w1_meanvderivative = np.mean(voltage_permsderivative[idx:idx+window_insamples])
            w1_minderivative = np.amin(voltage_permsderivative[idx:idx+window_insamples]) #as approximation of 'remaining noise'
            w2_meanvderivative = np.mean(voltage_permsderivative[idx+window_insamples:idx+(2*window_insamples)])
            if w1_meanvderivative-w1_minderivative < min_depolspeed \
                and w2_meanvderivative >= min_depolspeed+w1_meanvderivative:
                depol_idx = idx+window_insamples #depol_idx will mark the baseline_v point, if a proper peak can be found to go with it
                depolarizations.append(depol_idx)

    # 2. identify depolarizations that are followed by a peak in voltage
        #points qualify as having a peak if:
        # - peakv (within 10ms from depol_idx) > baselinev + mindepolamp in the event-detect trace
        # - minv after peakv goes back down to <80% of peak amp
        # - maxv after peakv is less than peakv+50% of peak amp from baseline
        # - applied current does not change between the baseline- and peak-points
                ed_baselinev = np.mean(voltage_eventdetecttrace[depol_idx-window_insamples:depol_idx])
                ed_peakvtrace = voltage_eventdetecttrace[depol_idx:depol_idx+peakwindow_insamples]
                ed_peakv = np.amax(ed_peakvtrace)
                ed_peakamp = ed_peakv - ed_baselinev
                peakv_idx = np.argmax(ed_peakvtrace) + depol_idx
                ed_postpeaktrace = voltage_eventdetecttrace[peakv_idx:peakv_idx+peakwindow_insamples]
                ed_postpeakmin = np.amin(ed_postpeaktrace)
                ed_postpeakmax = np.amax(ed_postpeaktrace)
                current_atbaseline = np.mean(current_recording[depol_idx-window_insamples:depol_idx])
                current_atpeak = np.mean(current_recording[peakv_idx:peakv_idx+peakwindow_insamples])
                if ed_peakamp >= min_depolamp \
                    and ed_postpeakmin < ed_baselinev+(0.8*ed_peakamp) \
                    and ed_postpeakmax < ed_baselinev+(1.5*ed_peakamp) \
                    and abs(current_atbaseline - current_atpeak) < 20:
                    depols_with_peaks.append(depol_idx)
                    peaks_idcs.append(peakv_idx)

    #3. get event parameters (for APs and subthreshold depolarizations separately).
    actionpotentials_dictionary = {}
    depolarizingevents_dictionary = {}
    for i, peak_idx in enumerate(peaks_idcs):
        baseline_idx = depols_with_peaks[i]

        ed_baselinev = np.mean(voltage_eventdetecttrace[baseline_idx-window_insamples:baseline_idx])
        ed_peakv = voltage_eventdetecttrace[peak_idx]
        ed_peakamp = ed_peakv - ed_baselinev

        if ed_peakamp > 40: #get action potential parameters
            #baseline v: meanv in the ms before baseline_idx
            baseline_v = np.mean(voltage_recording[baseline_idx-window_insamples:baseline_idx])
            #peak v: v at peak_idx (as found on ed-trace)
            peak_v = voltage_recording[peak_idx]
            #amplitude from baseline to peak
            spikeamp = peak_v - baseline_v
            #rise-time: time from 10% - 90% of peak amp
            risetrace = voltage_recording[baseline_idx:peak_idx]
            risetrace_clipped = risetrace[risetrace >= baseline_v+0.1*spikeamp]
            risestart_idx = peak_idx - len(risetrace_clipped)
            risetrace_clipped = risetrace_clipped[risetrace_clipped <= baseline_v+0.9*spikeamp]
            rise_time = len(risetrace_clipped) * sampling_period_inms
            #half-width: AP width at 50% of amplitude
            halfhalfwidth_inidcs = len(risetrace[risetrace > baseline_v + 0.5*spikeamp])
            additional_idcs = peak_idx
            while voltage_recording[additional_idcs] >= baseline_v + 0.5*spikeamp:
                additional_idcs += 1
            additional_idcs = additional_idcs - peak_idx
            halfwidth_inidcs = halfhalfwidth_inidcs + additional_idcs
            half_width = halfwidth_inidcs * sampling_period_inms
            #threshold: 10% of max. dV/dt
            fullspikev = voltage_recording[baseline_idx:peak_idx + spikewindow_insamples]
            fullspikev_diff = np.diff(fullspikev)
            maxdvdt = np.amax(fullspikev_diff)
            maxdvdt_idx = np.argmax(fullspikev_diff)
            thrshd_idx = maxdvdt_idx
            while fullspikev_diff[thrshd_idx] > 0.1*maxdvdt and thrshd_idx >= 0:
                thrshd_idx += -1
            spikethreshold_idx = baseline_idx + thrshd_idx
            spikethreshold_v = voltage_recording[spikethreshold_idx]
            #threshold-width: AP width at threshold v
            thrshld2_idx = peak_idx-baseline_idx
            while fullspikev[thrshld2_idx] > spikethreshold_v and thrshld2_idx < spikewindow_insamples:
                thrshld2_idx += 1
            thresholdwidth_inidcs = thrshld2_idx-thrshd_idx
            if fullspikev[thrshld2_idx] <= spikethreshold_v:
                threshold_width = thresholdwidth_inidcs * sampling_period_inms
            else:
                threshold_width = None

            actionpotentials_dictionary[peak_idx] = {
                'baselinev_idx' : baseline_idx,
                'baselinev' : baseline_v,
                'peakv' : peak_v,
                'amplitude' : spikeamp,
                'rise-time' : rise_time,
                'half-width' : half_width,
                'thresholdv_idx' : spikethreshold_idx,
                'thresholdv' : spikethreshold_v,
                'thresholdrereached-time' : threshold_width
                #don't forget about current
            }

            if plot == 'on':
                plt.figure()
                plt.plot(time_axis[baseline_idx-window_insamples:peak_idx+spikewindow_insamples],
                        voltage_recording[baseline_idx-window_insamples:peak_idx+spikewindow_insamples],
                         color='blue')
                plt.scatter(time_axis[baseline_idx], voltage_recording[baseline_idx],
                            color='red')
                plt.scatter(time_axis[peak_idx], voltage_recording[peak_idx],
                            color='green')
                plt.scatter(time_axis[spikethreshold_idx], spikethreshold_v,
                            color='black')
                plt.hlines(y=baseline_v+0.5*spikeamp,
                           xmin=time_axis[peak_idx-halfhalfwidth_inidcs],xmax=time_axis[peak_idx+additional_idcs],
                           color='green',
                           label='half-width')
                plt.hlines(baseline_v+0.1*spikeamp,
                           xmin=time_axis[risestart_idx],xmax=time_axis[risestart_idx+len(risetrace_clipped)],
                           color='red',
                           label='rise-time')
                plt.hlines(spikethreshold_v,
                           xmin=time_axis[spikethreshold_idx],xmax=time_axis[spikethreshold_idx+thresholdwidth_inidcs],
                           color='black',
                           label='threshold-width')
                plt.legend()


        else: #subthreshold event
            depolarizingevents_dictionary[peak_idx] = {
            }

    if plot == 'on':
        voltage_zerocentered = voltage_recording - np.mean(voltage_recording)
        figure,axes = plt.subplots(2,1,sharex=True)
        axes[0].plot(time_axis,voltage_zerocentered,color='blue',label='raw data (mean subtracted)')
        axes[0].plot(time_axis,voltage_eventdetecttrace,color='black',label='filtered data')
        axes[0].scatter(time_axis[depols_with_peaks], voltage_zerocentered[depols_with_peaks],
                        color='red')
        axes[0].scatter(time_axis[peaks_idcs], voltage_zerocentered[peaks_idcs],
                        color='green')
        axes[0].scatter(time_axis[depols_with_peaks], voltage_eventdetecttrace[depols_with_peaks],
                        color='red')
        axes[0].scatter(time_axis[peaks_idcs], voltage_eventdetecttrace[peaks_idcs],
                        color='green')
        axes[0].legend()
        # if len(spikes_baseline_idcs) > 0:
        #     axes[0].scatter(time_axis[spikes_baseline_idcs], voltage_zerocentered[spikes_baseline_idcs],
        #                     color='black')
        #     axes[0].scatter(time_axis[baseline_rereached_idcs], voltage_zerocentered[baseline_rereached_idcs],
        #                     color='blue')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title(single_segment.file_origin)

        axes[1].plot(time_axis_derivative,voltage_permsderivative,
                     color='black')
        # axes[1].set_ylim(-1, 2)
        axes[1].scatter(time_axis_derivative[depolarizations],
                        voltage_permsderivative[depolarizations],
                        color='red')
        axes[1].set_xlabel('time (ms)')
        axes[1].set_title('ms-by-ms derivative of filtered voltage')

    return actionpotentials_dictionary, depolarizingevents_dictionary