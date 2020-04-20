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

# %% depolarizing events
def get_depolarizingevents(single_segment,
                           min_depolspeed=0.1,
                           min_depolamp=0.2,
                           peakwindow=5,
                           spikewindow=40,
                           noisefilter_hpfreq = 3000,
                           oscfilter_lpfreq = 20,
                           plot = 'on'):
    # step1] prep:
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.array(np.squeeze(single_voltage_trace)) #!Make sure it's in mV
    current_recording = np.array(np.squeeze(single_segment.analogsignals[1])) #!Make sure it's in pA
    sampling_frequency = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz
    sampling_period_inms = float(single_voltage_trace.sampling_period) * 1000 #*pq.ms

    #parameter settings - default time windows:
    window_inms = 1 #window used for calculating the 'rough' derivative and candidate-depolarizations points
    ms_insamples = int(sampling_frequency / 1000 * window_inms)
    peakwindow_inms = peakwindow #max distance from depol_idx to peak
    peakwindow_insamples = int(sampling_frequency / 1000 * peakwindow_inms)
    spikewindow_inms = spikewindow
    spikewindow_insamples = int(sampling_frequency / 1000 * spikewindow_inms)

    #filtering the raw voltage twice: high-pass to get 'only the noise', and low-pass to get 'only the STOs'.
    #subtract both from raw voltage to get trace for event-detection
    (voltage_eventdetecttrace,
     voltage_oscillationstrace,
     voltage_noisetrace) = apply_filters_torawdata(voltage_recording,
                                                   oscfilter_lpfreq,
                                                   noisefilter_hpfreq,
                                                   sampling_frequency,
                                                   plot)
    #taking the ms-by-ms derivative
    voltage_permsderivative = make_derivative_per_ms(voltage_eventdetecttrace,
                                                     ms_insamples)
    time_axis_derivative = time_axis[:len(voltage_permsderivative):]

    #step2] actually collecting points of interest:
    # peaks of depolarizations, and their baseline-points (and all depolarizations that are picked up from the derivative-trace alone)
    (depolswithpeaks_idcs,
     peaks_idcs,
     alldepols_idcs) = find_depols_with_peaks(voltage_eventdetecttrace,
                                              voltage_permsderivative,
                                              current_recording,
                                              ms_insamples, peakwindow_insamples,
                                              min_depolspeed, min_depolamp)

    #step3] taking the measurements of each event:
    #constructing a dictionary of peaks_idcs, with all related measurements (separately for APs and one for subthreshold depolarizations)
    (actionpotentials_dictionary,
     depolarizingevents_dictionary) = get_events_measures(peaks_idcs, depolswithpeaks_idcs,
                        voltage_recording, voltage_noisetrace, voltage_eventdetecttrace,
                        current_recording,
                        ms_insamples, spikewindow_insamples, sampling_period_inms,
                        time_axis, plot)

    #plotting the data (in all its shapes from raw to filtered to derivative)
    #with scatters of detected depolarizations and events
    if plot == 'on':
        figure,axes = plt.subplots(3,1,sharex=True)
        axes[0].plot(time_axis,voltage_recording,
                     color='blue',label='raw data')
        axes[0].plot(time_axis, voltage_oscillationstrace,
                     color='green', label='low-pass filtered data')
        axes[0].plot(time_axis, voltage_recording-voltage_noisetrace,
                     color='grey', label='high-pass filtered data subtracted')


        axes[0].scatter(time_axis[depolswithpeaks_idcs], voltage_recording[depolswithpeaks_idcs],
                        color='red')
        axes[0].scatter(time_axis[peaks_idcs], voltage_recording[peaks_idcs],
                        color='green')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title(single_segment.file_origin)
        axes[0].legend()

        axes[1].plot(time_axis, voltage_eventdetecttrace,
                     color='black', label='event-detect trace')
        axes[1].scatter(time_axis[depolswithpeaks_idcs], voltage_eventdetecttrace[depolswithpeaks_idcs],
                        color='red')
        axes[1].scatter(time_axis[peaks_idcs], voltage_eventdetecttrace[peaks_idcs],
                        color='green')
        axes[1].legend()

        axes[2].plot(time_axis_derivative,voltage_permsderivative,
                     color='black')
        # axes[2].set_ylim(-1, 2)
        axes[2].scatter(time_axis_derivative[alldepols_idcs], voltage_permsderivative[alldepols_idcs],
                        color='red')
        axes[2].set_xlabel('time (ms)')
        axes[2].set_title('ms-by-ms derivative of filtered voltage')

    return actionpotentials_dictionary, depolarizingevents_dictionary



def apply_filters_torawdata(voltage_recording,
                            oscfilter_lpfreq, noisefilter_hpfreq,
                            sampling_frequency,
                            plot):
    lowpass_dlti = signal.dlti(*signal.butter(2, oscfilter_lpfreq, btype='lowpass', fs=sampling_frequency, output='ba'))
    t_lp, y_lp = lowpass_dlti.impulse(n=2000)
    highpass_dlti = signal.dlti(*signal.butter(1, noisefilter_hpfreq, btype='highpass', fs=sampling_frequency, output='ba'))
    t_hp, y_hp = highpass_dlti.impulse(n=2000)
    if plot == 'on':
        plt.figure()
        plt.plot(t_lp,np.squeeze(y_lp),label='low-pass filter')
        plt.plot(t_hp,np.squeeze(y_hp),label='high-pass filter')
        plt.ylim(np.min(y_lp),np.max(y_lp))
        plt.legend()
        plt.xlabel('n [samples]')
        plt.ylabel('amplitude')
        plt.title('impulse response functions')

    lowpass_sos = signal.butter(2, oscfilter_lpfreq, btype='lowpass', fs=sampling_frequency, output='sos')
    voltage_oscillationstrace = signal.sosfiltfilt(lowpass_sos, voltage_recording)
    highpass_sos = signal.butter(1, noisefilter_hpfreq, btype='highpass', fs=sampling_frequency, output='sos')
    voltage_noisetrace = signal.sosfiltfilt(highpass_sos, voltage_recording)
    voltage_eventdetecttrace = voltage_recording - voltage_oscillationstrace - voltage_noisetrace

    return voltage_eventdetecttrace, voltage_oscillationstrace, voltage_noisetrace


def make_derivative_per_ms(recording_trace, ms_insamples):
    permsderivative = []
    for idx in range(0, len(recording_trace) - ms_insamples):
        slope_approx = recording_trace[idx + ms_insamples] - recording_trace[idx]
        permsderivative.append(slope_approx)
    return np.array(permsderivative)


def find_depols_with_peaks(voltage_eventdetecttrace, voltage_derivative, current_recording,
                           ms_insamples, peakwindow_insamples,
                           min_depolspeed, min_depolamp):
    depolarizations = []
    depols_with_peaks = []
    peaks_idcs = []
    for idx in range(ms_insamples, len(voltage_derivative)-peakwindow_insamples):
        # skip points that refer to places on already-identified events
        if peaks_idcs and idx < peaks_idcs[-1]:
            continue
        #1. identify points where depolarizing events start
        elif voltage_derivative[idx] >= min_depolspeed \
        and [v_diff >= min_depolspeed for v_diff in voltage_derivative[idx:idx+ms_insamples]]:

            depol_idx = idx  # depol_idx will mark the baseline_v point, if a proper peak can be found to go with it
            depolarizations.append(depol_idx)

        # 2. identify depolarizations that are followed by a peak in voltage
        # points qualify as having a peak if:
        # - peakv is indeed a local peak (voltage goes down again at peakv_idx + 1)
        # - peakv > baselinev + mindepolamp in the event-detect trace
        # - minv after peakv goes back down to at <90% of peak amp
        # - applied current does not change between the baseline- and peak-points
            ed_baselinev = np.mean(
                voltage_eventdetecttrace[depol_idx - ms_insamples:depol_idx])
            ed_peakvtrace = voltage_eventdetecttrace[depol_idx:depol_idx + peakwindow_insamples]
            ed_peakv = np.amax(ed_peakvtrace)
            ed_peakamp = ed_peakv - ed_baselinev
            peakv_idx = np.argmax(ed_peakvtrace) + depol_idx
            ed_postpeaktrace = voltage_eventdetecttrace[peakv_idx:peakv_idx + peakwindow_insamples]
            ed_postpeakmin = np.amin(ed_postpeaktrace)
            current_atbaseline = np.mean(current_recording[depol_idx - ms_insamples:depol_idx])
            current_atpeak = np.mean(current_recording[peakv_idx:peakv_idx + peakwindow_insamples])
            if ed_peakamp >= min_depolamp \
                    and voltage_eventdetecttrace[peakv_idx+1] <= voltage_eventdetecttrace[peakv_idx] \
                    and ed_postpeakmin < ed_baselinev + (0.9 * ed_peakamp) \
                    and abs(current_atbaseline - current_atpeak) < 20:
                depols_with_peaks.append(depol_idx)
                peaks_idcs.append(peakv_idx)
    return depols_with_peaks, peaks_idcs, depolarizations


def get_events_measures(peaks_idcs, depolswithpeaks_idcs,
                        voltage_recording, voltage_noisetrace, voltage_eventdetecttrace,
                        current_recording,
                        ms_insamples, spikewindow_insamples, sampling_period_inms,
                        time_axis, plot):

    actionpotentials_dictionary = {}
    depolarizingevents_dictionary = {}
    for i, peak_idx in enumerate(peaks_idcs):
        baseline_idx = depolswithpeaks_idcs[i]

        ed_baseline_v = np.mean(voltage_eventdetecttrace[baseline_idx-ms_insamples:baseline_idx])
        ed_peakv = voltage_eventdetecttrace[peak_idx]
        ed_peakamp = ed_peakv - ed_baseline_v

        if ed_peakamp > 40 and peak_idx < len(voltage_recording)-spikewindow_insamples: #get action potential parameters
            #baseline v: meanv in the 2ms around baseline_idx
            baseline_v = np.mean(voltage_recording[baseline_idx-ms_insamples:baseline_idx+ms_insamples])
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
            half_width_startidx = peak_idx - halfhalfwidth_inidcs
            descendtrace = voltage_recording[peak_idx:peak_idx+spikewindow_insamples]
            secondhalfhalfwidth_inidcs = descend_vtrace_until(descendtrace, baseline_v + 0.5*spikeamp)
            halfwidth_inidcs = halfhalfwidth_inidcs + secondhalfhalfwidth_inidcs
            half_width = halfwidth_inidcs * sampling_period_inms
            #threshold: 10% of max. dV/dt
            fullspikev = voltage_recording[baseline_idx:peak_idx + spikewindow_insamples]
            fullspikev_diff = np.diff(fullspikev)
            maxdvdt = np.amax(fullspikev_diff)
            maxdvdt_idx = np.argmax(fullspikev_diff)
            thrshd_idx = maxdvdt_idx
            while fullspikev_diff[thrshd_idx] > 0.1*maxdvdt:
                thrshd_idx += -1
            threshold_idx = baseline_idx + thrshd_idx
            threshold_v = voltage_recording[threshold_idx]
            #threshold-width: AP width at threshold v
            returntothreshold_inidcs = descend_vtrace_until(descendtrace, threshold_v)
            if isinstance(returntothreshold_inidcs,str):
                threshold_width = returntothreshold_inidcs
            else:
                thresholdwidth_inidcs = peak_idx + returntothreshold_inidcs - threshold_idx
                threshold_width = thresholdwidth_inidcs * sampling_period_inms
            #current applied
            current_applied = np.mean(current_recording[baseline_idx:peak_idx+returntothreshold_inidcs])
            if abs(current_applied) <= 10:
                current_applied = 0
            #approximate slope (of STO) just before the AP
            #number of spikelet-peaks on AP shoulder
            #after-hyperpolarization parameters:
            #start_idx (or:return to baseline_v), min value and idx, amplitude, width

            actionpotentials_dictionary[peak_idx] = {
                'baselinev': baseline_v,
                'peakv': peak_v,
                'amplitude': spikeamp,
                'rise-time': rise_time,
                'half-width': half_width,
                'thresholdv': threshold_v,
                'threshold-width': threshold_width,
                'applied_current' : current_applied,

                'baselinev_idx' : baseline_idx,
                'rt_startidx': risestart_idx,
                'hw_startidx': half_width_startidx,
                'threshold_idx': threshold_idx,
                # 'prespike_approxslope' : slopeapprox,
                # 'applied_current' : current_applied,
                # 'peaksonshoulder' : no_of_spikelets,
                # 'AHPstart_idx' : AHPstart_idx,
                # 'AHPmin_idx' : AHPmin_idx,
                # 'AHP_amplitude' : AHPamp,
                # 'AHP-width' : AHP_width
            }

            if plot == 'on':
                plt.figure()
                plt.plot(time_axis[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                        voltage_recording[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                         color='blue',
                         label='raw data')
                plt.scatter(time_axis[baseline_idx], voltage_recording[baseline_idx],
                            color='red')
                plt.scatter(time_axis[peak_idx], voltage_recording[peak_idx],
                            color='green')
                plt.scatter(time_axis[threshold_idx], threshold_v,
                            color='black')
                plt.hlines(y=baseline_v+0.5*spikeamp,
                           xmin=time_axis[half_width_startidx], xmax=time_axis[half_width_startidx+halfwidth_inidcs],
                           color='green',
                           label='half-width')
                plt.hlines(baseline_v+0.1*spikeamp,
                           xmin=time_axis[risestart_idx], xmax=time_axis[risestart_idx+len(risetrace_clipped)],
                           color='red',
                           label='rise-time')
                if not isinstance(threshold_width, str):
                    plt.hlines(threshold_v,
                               xmin=time_axis[threshold_idx], xmax=time_axis[threshold_idx+thresholdwidth_inidcs],
                               color='black',
                               label='threshold-width')
                plt.legend()


        elif voltage_recording[peak_idx] < -10: #subthreshold event
            voltage_denoised = voltage_recording - voltage_noisetrace

            # baseline v: meanv in the ms before baseline_idx
            baseline_v = np.mean(voltage_denoised[baseline_idx-ms_insamples:baseline_idx])
            ed_baseline_v = np.mean(voltage_eventdetecttrace[baseline_idx-ms_insamples:baseline_idx])

            # peak v: v at peak_idx (as found on ed-trace)
            peak_v = voltage_denoised[peak_idx]
            ed_peak_v = voltage_eventdetecttrace[peak_idx]

            # amplitude from baseline to peak
            amplitude = peak_v - baseline_v
            ed_amplitude = ed_peak_v - ed_baseline_v

            #rise-time: time to get from 10% to 90% of peak amp
            #especially for the very small events, may have to adjust this code to make sure that small fluctuations after baseline-point but before rise-time-start don't contaminate measurement
            risetrace = voltage_denoised[baseline_idx:peak_idx]
            risetrace_clipped = risetrace[risetrace >= baseline_v + 0.1 * amplitude]
            risestart_idx = peak_idx - len(risetrace_clipped)
            risetrace_clipped = risetrace_clipped[risetrace_clipped <= baseline_v + 0.9 * amplitude]
            rise_time = len(risetrace_clipped) * sampling_period_inms
            ed_risetrace = voltage_eventdetecttrace[baseline_idx:peak_idx]
            ed_risetrace_clipped = ed_risetrace[ed_risetrace >= ed_baseline_v + 0.1*ed_amplitude]
            ed_risestart_idx = peak_idx - len(ed_risetrace_clipped)
            ed_risetrace_clipped = ed_risetrace_clipped[ed_risetrace_clipped <= ed_baseline_v + 0.9*ed_amplitude]
            ed_rise_time = len(ed_risetrace_clipped) * sampling_period_inms

            # half-width: width at 50% of amplitude
            descendtrace = voltage_denoised[peak_idx:peak_idx+spikewindow_insamples]
            halfhalfwidth_inidcs = len(risetrace[risetrace >= baseline_v + 0.5*amplitude])
            halfwidth_startidx = peak_idx - halfhalfwidth_inidcs
            secondhalfhalfwidth_inidcs = descend_vtrace_until(descendtrace,baseline_v+0.5*amplitude)
            if isinstance(secondhalfhalfwidth_inidcs,str):
                half_width = secondhalfhalfwidth_inidcs
            else:
                half_width = (halfhalfwidth_inidcs + secondhalfhalfwidth_inidcs) * sampling_period_inms
            ed_descendtrace = voltage_eventdetecttrace[peak_idx:peak_idx+spikewindow_insamples]
            ed_halfhalfwidth_inidcs = len(ed_risetrace[ed_risetrace >= ed_baseline_v + 0.5*ed_amplitude])
            ed_halfwidth_startidx = peak_idx - ed_halfhalfwidth_inidcs
            ed_secondhalfhalfwidth_inidcs = descend_vtrace_until(ed_descendtrace,ed_baseline_v+0.5*ed_amplitude)
            if isinstance(ed_secondhalfhalfwidth_inidcs,str):
                ed_half_width = ed_secondhalfhalfwidth_inidcs
            else:
                ed_half_width = (ed_halfhalfwidth_inidcs + ed_secondhalfhalfwidth_inidcs) * sampling_period_inms

            # width: time from rise-start (@10% of amp) until rise-start_v re-reached
            pastpeakwidth_inidcs = descend_vtrace_until(descendtrace,baseline_v+0.1*amplitude)
            if isinstance(pastpeakwidth_inidcs,str):
                width = pastpeakwidth_inidcs
            else:
                width = (peak_idx - risestart_idx + pastpeakwidth_inidcs) * sampling_period_inms
            ed_pastpeakwidth_inidcs = descend_vtrace_until(ed_descendtrace,ed_baseline_v+0.1*ed_amplitude)
            if isinstance(ed_pastpeakwidth_inidcs,str):
                ed_width = ed_pastpeakwidth_inidcs
            else:
                ed_width = (peak_idx - ed_risestart_idx + ed_pastpeakwidth_inidcs) * sampling_period_inms

            #applied current
            current_applied = np.mean(current_recording[baseline_idx-ms_insamples:peak_idx])
            if abs(current_applied) <= 10:
                current_applied = 0


            depolarizingevents_dictionary[peak_idx] = {
                'baselinev' : baseline_v,
                'peakv' : peak_v,
                'amplitude' : amplitude,
                'rise-time' : rise_time,
                'half-width' : half_width,
                'width_at10%amp' : width,
                # 'preevent_approxslope' : slopeapprox,
                'applied_current' : current_applied,

                'edtrace_baselinev' : ed_baseline_v,
                'edtrace_amplitude': ed_amplitude,
                'edtrace_rise-time' : ed_rise_time,
                'edtrace_half-width' : ed_half_width,
                'edtrace_width_at10%amp' : ed_width,

                'baselinev_idx': baseline_idx,
                'rt_start_idx' : risestart_idx,
                'edtrace_rt_start_idx' : ed_risestart_idx,
                'hw_start_idx' : halfwidth_startidx,
                'edtrace_hw_start_idx' : ed_halfwidth_startidx
            }

            if plot == 'on':
                figure,axes = plt.subplots(1,2,sharex='all')
                axes[0].plot(time_axis[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                        voltage_recording[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                             color='blue',
                             label='raw voltage')
                axes[0].plot(time_axis[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                        voltage_denoised[baseline_idx-ms_insamples:peak_idx+spikewindow_insamples],
                             color='black',
                             linewidth=2,
                             label='noise-subtracted voltage')
                axes[0].scatter(time_axis[baseline_idx], voltage_denoised[baseline_idx],
                            color='red')
                axes[0].scatter(time_axis[peak_idx], voltage_denoised[peak_idx],
                            color='green')
                axes[0].hlines(y=baseline_v + 0.1 * amplitude,
                               xmin=time_axis[risestart_idx],
                                    xmax=time_axis[risestart_idx] + rise_time,
                               color='red',
                               label='rise-time')
                if not isinstance(half_width, str):
                    axes[0].hlines(y=baseline_v+0.5*amplitude,
                               xmin=time_axis[halfwidth_startidx],
                                   xmax=time_axis[halfwidth_startidx] + half_width,
                               color='green',
                               label='half-width')
                if not isinstance(width, str):
                    axes[0].hlines(y=baseline_v+0.09*amplitude,
                               xmin=time_axis[risestart_idx],
                                   xmax=time_axis[risestart_idx] + width,
                               color='black',
                               label='90%-width')
                axes[0].legend()
                axes[0].set_xlabel('time (ms)')
                axes[0].set_ylabel('voltage (mv)')

                axes[1].plot(time_axis[baseline_idx - ms_insamples:peak_idx + spikewindow_insamples],
                             voltage_eventdetecttrace[baseline_idx - ms_insamples:peak_idx + spikewindow_insamples],
                             color='black')
                axes[1].scatter(time_axis[baseline_idx], voltage_eventdetecttrace[baseline_idx],
                                color='red')
                axes[1].scatter(time_axis[peak_idx], voltage_eventdetecttrace[peak_idx],
                                color='green')
                axes[1].hlines(y=ed_baseline_v + 0.1 * ed_amplitude,
                               xmin=time_axis[ed_risestart_idx],
                               xmax=time_axis[ed_risestart_idx + len(ed_risetrace_clipped)],
                               color='red',
                               label='rise-time')
                if not isinstance(ed_half_width,str):
                    axes[1].hlines(y=ed_baseline_v + 0.5 * ed_amplitude,
                                   xmin=time_axis[ed_halfwidth_startidx],
                                   xmax=time_axis[ed_halfwidth_startidx] + ed_half_width,
                                   color='green',
                                   label='half-width')
                if not isinstance(ed_width,str):
                    axes[1].hlines(y=ed_baseline_v + 0.09 * ed_amplitude,
                                   xmin=time_axis[ed_risestart_idx],
                                   xmax=time_axis[ed_risestart_idx] + ed_width,
                                   color='black',
                                   label='90%-width')
                axes[1].legend()
                axes[1].set_xlabel('time (ms)')
                axes[1].set_ylabel('filtered voltage')

    return actionpotentials_dictionary, depolarizingevents_dictionary

def descend_vtrace_until(vtracesnippet,v_stop_value):
    idx = 0
    while idx < len(vtracesnippet)-3 \
    and (vtracesnippet[idx] >= v_stop_value or vtracesnippet[idx+1] >= v_stop_value):
        idx += 1
    if vtracesnippet[idx] <= v_stop_value:
        return idx
    else:
        return 'no value found'