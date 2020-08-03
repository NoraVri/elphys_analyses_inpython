# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:33:29 2020

@author: neert

This file contains functions for analyzing singleneuron (raw) data.
"""
# %% imports


import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import quantities as pq

# %% depolarizing events


# the main function:
# return all depolarizing events and action potentials for a single segment,
# with measures, in two dictionaries (one for subtheshold events and one for APs).
def get_depolarizingevents(block_file_origin, segment_idx, single_segment,
                           min_depolspeed=0.1, min_depolamp=0.2,
                           peakwindow=5, spikewindow=40, spikeahpwindow=150,
                           noisefilter_hpfreq=3000, oscfilter_lpfreq=20,
                           ttleffect_windowinms=None,
                           plot='off'):
    """ This function finds depolarizing events and returns two dictionaries,
    containing the locations and measured parameters of action potentials
    and depolarizing events, respectively.
    Depolarizations are extracted in multiple steps:
    First, the event-detect trace is created by subtracting oscillations
    and noise from the raw voltage.
    Then, points where the ms-by-ms derivative of the event-detect voltage
    is larger than min_depolspeed are examined, and baseline- and peak-points marked
    if a peak, and then a decay in voltage after the peak are found.
    Finally, if event passes criteria for being marked as an
    action potential or a depolarizing event, the event and its measures are
    added to the relevant dictionary.
    If plot is not 'off', all traces and points gotten along the way from raw data to
    detected events are plotted.

    This function assumes the following conventions:
    In the input raw data: voltage in mV, current in pA, and time-units in s.
    In the outputted results: voltage in mV, current in pA and time-units in ms.
    """
    # step1] prep:
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.array(np.squeeze(single_voltage_trace))              # !Make sure it's in mV
    current_recording = np.array(np.squeeze(single_segment.analogsignals[1]))   # !Make sure it's in pA
    if len(single_segment.analogsignals) == 3:
        auxttl_recording = np.array(np.squeeze(single_segment.analogsignals[2]))
    else:
        auxttl_recording = None
    sampling_frequency = float(single_voltage_trace.sampling_rate)              # !Make sure it's in Hz
    sampling_period_inms = float(single_voltage_trace.sampling_period) * 1000

    # parameter settings - default time windows:
    ms_insamples = int(sampling_frequency / 1000)
    peakwindow_insamples = int(sampling_frequency / 1000 * peakwindow) # max distance from depol_idx to peak
    spikewindow_insamples = int(sampling_frequency / 1000 * spikewindow)
    spikeahpwindow_insamples = int(sampling_frequency / 1000 * spikeahpwindow)
    if not ttleffect_windowinms is None:
        ttleffect_windowinsamples = int(sampling_frequency / 1000 * ttleffect_windowinms)
    else:
        ttleffect_windowinsamples = None

    # filtering the raw voltage twice: high-pass to get 'only the noise',
    # and low-pass to get 'only the STOs'.
    # Subtract both from raw voltage to get trace for event-detection.
    (voltage_eventdetecttrace,
     voltage_oscillationstrace, voltage_noisetrace,
     voltage_approxphase, voltage_approxinstfreq) = apply_rawvtrace_manipulations(
                                                        voltage_recording,
                                                        oscfilter_lpfreq,
                                                        noisefilter_hpfreq,
                                                        sampling_frequency,
                                                        time_axis,
                                                        plot)

    #taking the ms-by-ms derivative, and adjusting time axis accordingly
    voltage_permsderivative = make_derivative_per_ms(voltage_eventdetecttrace,
                                                     ms_insamples)
    time_axis_derivative = time_axis[:len(voltage_permsderivative):]

    # step2] actually collecting points of interest:
    # peaks of depolarizations, and their baseline-points (and all depolarizations
    # that are picked up from the derivative-trace alone)
    (depolswithpeaks_idcs, peaks_idcs,
     alldepols_idcs) = find_depols_with_peaks(voltage_eventdetecttrace,
                                              voltage_permsderivative,
                                              current_recording,
                                              ms_insamples, peakwindow_insamples,
                                              min_depolspeed, min_depolamp)

    #step3] taking the measurements of each event:
    # constructing a dictionary of peaks_idcs, with all related measurements
    # (separately for APs and for subthreshold depolarizations)
    (actionpotentials_resultsdictionary,
     depolarizingevents_resultsdictionary) = get_events_measures(
                                                peaks_idcs,
                                                depolswithpeaks_idcs,
                                                voltage_recording,
                                                voltage_oscillationstrace,
                                                voltage_noisetrace,
                                                voltage_eventdetecttrace,
                                                voltage_approxphase,
                                                voltage_approxinstfreq,
                                                current_recording,
                                                ms_insamples,
                                                spikewindow_insamples,
                                                spikeahpwindow_insamples,
                                                sampling_period_inms,
                                                auxttl_recording,
                                                ttleffect_windowinsamples)
    # adding file_origin and segment_idx information
    trace_origin = [block_file_origin]
    segidx = [segment_idx]
    actionpotentials_resultsdictionary['file_origin'] = \
        trace_origin * len(actionpotentials_resultsdictionary['peakv'])
    actionpotentials_resultsdictionary['segment_idx'] = \
        segidx * len(actionpotentials_resultsdictionary['peakv'])
    depolarizingevents_resultsdictionary['file_origin'] = \
        trace_origin * len(depolarizingevents_resultsdictionary['peakv'])
    depolarizingevents_resultsdictionary['segment_idx'] = \
        segidx * len(depolarizingevents_resultsdictionary['peakv'])

    # if required, plotting the data (in all its shapes from raw to filtered to derivative)
    # with scatters of detected depolarizations peaks and baselines
    if plot == 'on':
        figure,axes = plt.subplots(3,1,sharex='all')
        axes[0].plot(time_axis,voltage_recording,
                     color='blue',label='raw data')
        axes[0].scatter(time_axis[depolswithpeaks_idcs], voltage_recording[depolswithpeaks_idcs],
                        color='green')
        axes[0].scatter(time_axis[peaks_idcs], voltage_recording[peaks_idcs],
                        color='red')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title(single_segment.file_origin)
        axes[0].legend()

        axes[1].plot(time_axis, voltage_eventdetecttrace,
                     color='blue',
                     linewidth=2,
                     label='event-detect trace')
        axes[1].scatter(time_axis[depolswithpeaks_idcs], voltage_eventdetecttrace[depolswithpeaks_idcs],
                        color='green',
                        label='event baseline point')
        axes[1].scatter(time_axis[peaks_idcs], voltage_eventdetecttrace[peaks_idcs],
                        color='red',
                        label='event peak')
        axes[1].legend()

        axes[2].plot(time_axis_derivative,voltage_permsderivative,
                     color='black',
                     label='event-detect trace derivative')
        axes[2].scatter(time_axis_derivative[alldepols_idcs], voltage_permsderivative[alldepols_idcs],
                        color='blue',
                        label='depolarizations-candidates')
        axes[2].set_xlabel('time (ms)')
        axes[2].legend()

    return actionpotentials_resultsdictionary, depolarizingevents_resultsdictionary


# sub-functions:
# applying filters and getting the event-detect trace
def apply_rawvtrace_manipulations(voltage_recording,
                                  oscfilter_lpfreq, noisefilter_hpfreq,
                                  sampling_frequency, time_axis,
                                  plot='off'):
    """ This function takes the raw voltage recording and applies filtering and the hilbert transform
    to get traces for use in event-detection.
    """
    # plotting the filters' impulse response functions:
    lowpass_dlti = signal.dlti(*signal.butter(2, oscfilter_lpfreq, btype='lowpass',
                                              fs=sampling_frequency, output='ba'))
    t_lp, y_lp = lowpass_dlti.impulse(n=2000)
    highpass_dlti = signal.dlti(*signal.butter(1, noisefilter_hpfreq, btype='highpass',
                                               fs=sampling_frequency, output='ba'))
    t_hp, y_hp = highpass_dlti.impulse(n=2000)
    if plot == 'on':
        plt.figure()
        plt.plot(t_lp, np.squeeze(y_lp), label='low-pass filter')
        plt.plot(t_hp, np.squeeze(y_hp), label='high-pass filter')
        plt.ylim(np.min(y_lp), np.max(y_lp))
        plt.legend()
        plt.xlabel('n [samples]')
        plt.ylabel('amplitude')
        plt.title('impulse response functions')

    # applying filters to the raw data
    lowpass_sos = signal.butter(2, oscfilter_lpfreq, btype='lowpass',
                                fs=sampling_frequency, output='sos')
    voltage_oscillationstrace = signal.sosfiltfilt(lowpass_sos, voltage_recording)

    highpass_sos = signal.butter(1, noisefilter_hpfreq, btype='highpass',
                                 fs=sampling_frequency, output='sos')
    voltage_noisetrace = signal.sosfiltfilt(highpass_sos, voltage_recording)
    # subtracting the filtered data from the raw
    voltage_eventdetecttrace = (voltage_recording
                                - voltage_oscillationstrace
                                - voltage_noisetrace)

    # getting the instantaneous phase and frequency from the hilbert transform of the data
    # TODO: replace the line below with code that does proper mean-centering (in traces with current pulses applied this gives particularly unreliable results)
    centering_value = np.mean(voltage_recording)
    voltage_osctrace_meancentered = voltage_oscillationstrace - centering_value
    voltage_osctrace_analyticsignal = signal.hilbert(voltage_osctrace_meancentered)
    voltage_approxphase = np.angle(voltage_osctrace_analyticsignal)
    voltage_approxinstfreq = ((np.diff(np.unwrap(voltage_approxphase))
                               / (2.0*np.pi) * sampling_frequency))

    voltage_meancentered = voltage_recording - voltage_noisetrace - centering_value
    voltage_analyticsignal = signal.hilbert(voltage_meancentered)
    vraw_approxphase = np.angle(voltage_analyticsignal)

    if plot == 'on':
        figure, axes = plt.subplots(2, 1, sharex='all')
        axes[0].plot(time_axis, voltage_recording - centering_value,
                     color='blue',
                     label='raw recording, mean centered')
        axes[0].plot(time_axis, voltage_oscillationstrace - centering_value,
                     color='black',
                     label='lp-filtered at '+str(oscfilter_lpfreq)+'Hz')
        axes[0].legend()
        axes[0].plot(time_axis, voltage_noisetrace,
                     label='hp-filtered at '+str(noisefilter_hpfreq)+'Hz')
        axes[0].set_ylabel('mean V = '+ str(centering_value))
        axes[0].legend()
        axes[1].plot(time_axis, vraw_approxphase, label='de-noised v phase')
        axes[1].plot(time_axis, voltage_approxphase, label='osctrace phase',
                     linewidth=2)
        # axes[1].plot(time_axis[1:], voltage_approxinstfreq,
        #              color='black',
        #              label='osctrace inst.freq.')
        # axes[1].set_ylim([-5, 40])
        axes[1].legend()

    return voltage_eventdetecttrace, \
           voltage_oscillationstrace, \
           voltage_noisetrace, \
           voltage_approxphase, \
           voltage_approxinstfreq


# differentiating: getting the mV/ms change in voltage for each point on the recorded trace
def make_derivative_per_ms(recording_trace, ms_insamples):
    permsderivative = []
    for idx in range(0, len(recording_trace) - ms_insamples):
        slope_approx = recording_trace[idx + ms_insamples] - recording_trace[idx]
        permsderivative.append(slope_approx)
    return np.array(permsderivative)


# finding depolarizing events that have a peak in voltage succeeding them
def find_depols_with_peaks(voltage_eventdetecttrace, voltage_derivative,
                           current_recording,
                           ms_insamples, peakwindow_insamples,
                           min_depolspeed, min_depolamp):
    """ This function finds and returns points where depolarizations occur in the voltage derivative,
    as well as the baseline-points and peak-points of any depolarizations that are found to have these.
    """
    depolarizations = []
    depols_with_peaks = []
    peaks_idcs = []
    for idx in range(ms_insamples, len(voltage_derivative) - peakwindow_insamples):
        # skip points that refer to places on already-identified events
        if peaks_idcs and idx < peaks_idcs[-1]:
            continue
        # 1. identify possible depolarizing event-start points:
        # - dV/dt > 2 * min_depolspeed, or:
        # - dV/dt < 10% of min_depolspeed some time in the ms before idx
        # - dV/dt > min_depolspeed for a duration of at least 0.5ms
        elif voltage_derivative[idx] > 2 * min_depolspeed \
            or (voltage_derivative[idx] >= min_depolspeed
            and np.min(voltage_derivative[idx-ms_insamples:idx]) < 0.1 * min_depolspeed
            and [v_diff >= min_depolspeed
                 for v_diff in voltage_derivative[idx:idx + int(ms_insamples/2)]]):

            depol_idx = idx  # depol_idx will mark the baseline_v point, if a proper peak can be found to go with it
            depolarizations.append(depol_idx)

            # 2. identify spontaneous depolarizations that are followed by a peak in voltage
            # points qualify if:
            # - applied current does not change within 50 ms before and after peak,
            # - peakv > baselinev + mindepolamp in the event-detect trace,
            # - maxv after peakv is larger than peakv, and
            # - minv after peakv goes back down to <80% of peak amp within peakwindow
            current_predepolarization = current_recording[
                                        int(depol_idx - (50 * ms_insamples)):
                                        int(depol_idx + (50 * ms_insamples))]
            currentchange_predepolarization = np.diff(current_predepolarization)
            if len(currentchange_predepolarization) >= peakwindow_insamples \
            and np.amax(np.abs(currentchange_predepolarization)) > 8:
                continue
            else:
                ed_baselinev = np.mean(voltage_eventdetecttrace[
                                       depol_idx - ms_insamples:depol_idx])
                ed_peakvtrace = voltage_eventdetecttrace[
                                depol_idx:depol_idx + peakwindow_insamples]
                ed_peakv = np.amax(ed_peakvtrace)

            if ed_peakv < ed_baselinev + min_depolamp:
                continue
            else:
                peakv_idx = np.argmax(ed_peakvtrace) + depol_idx
                ed_postpeaktrace = voltage_eventdetecttrace[
                                   peakv_idx + 1:peakv_idx + peakwindow_insamples + 1]
                ed_postpeakmin = np.amin(ed_postpeaktrace)
                ed_postpeakmax = np.amax(ed_postpeaktrace) - 0.05 # allow for a bit of noise

            if ed_postpeakmax > ed_peakv:
                continue

            if ed_postpeakmin > ed_baselinev + 0.8 * (ed_peakv - ed_baselinev):
                continue
            else:
                depols_with_peaks.append(depol_idx)
                peaks_idcs.append(peakv_idx)

    return depols_with_peaks, peaks_idcs, depolarizations


# taking measures of events based on their baseline- and peak-points
def get_events_measures(peaks_idcs,
                        depolswithpeaks_idcs,
                        voltage_recording,
                        voltage_oscillationstrace,
                        voltage_noisetrace,
                        voltage_eventdetecttrace,
                        voltage_approxphase,
                        voltage_approxinstfreq,
                        current_recording,
                        ms_insamples, spikewindow_insamples, spikeahpwindow_insamples,
                        sampling_period_inms,
                        auxttl_recording, ttleffectwindow_insamples):
    """ This function loops over all peaks/baselines indices and collects all data and measures contained
    in the depolarizingevents_df into a dictionary.
    Events are labeled as:
    -actionpotential by event amplitude/peakv;
    -spikeshoulderpeak by occurrence directly after an actionpotential but before return to thresholdv
    -subthresholdevent otherwise.
    """
    eventsmeasures_dictionary = make_eventsmeasures_dictionary()

    voltage_denoised = voltage_recording - voltage_noisetrace

    for baseline_idx, peak_idx in zip(depolswithpeaks_idcs, peaks_idcs):
        # adding into dictionary: baseline and peak idcs
        eventsmeasures_dictionary['peakv_idx'].append(peak_idx)
        eventsmeasures_dictionary['baselinev_idx'].append(baseline_idx)

        # current_applied
        current_applied = np.mean(current_recording[baseline_idx:peak_idx])
        if abs(current_applied) <= 7:
            current_applied = 0
        eventsmeasures_dictionary['applied_current'].append(current_applied)

        # ttl applied
        if auxttl_recording is None:
            auxttlsnippet = None
        elif ttleffectwindow_insamples is not None:
            auxttlsnippet = auxttl_recording[baseline_idx-ttleffectwindow_insamples:peak_idx]
        else:
            auxttlsnippet = auxttl_recording[baseline_idx:peak_idx]

        if (auxttlsnippet is not None) and (len(auxttlsnippet) > 0) and (np.amax(auxttlsnippet) > 1):
            ttlpulse_applied = True
        else:
            ttlpulse_applied = False
        eventsmeasures_dictionary['applied_ttlpulse'].append(ttlpulse_applied)

        # baseline v: mean v in the ms before the event's baseline_idx
        baseline_v = np.mean(voltage_denoised[baseline_idx - ms_insamples:baseline_idx])
        eventsmeasures_dictionary['baselinev'].append(baseline_v)

        ed_baseline_v = np.mean(voltage_eventdetecttrace[baseline_idx - ms_insamples:baseline_idx])
        eventsmeasures_dictionary['edtrace_baselinev'].append(ed_baseline_v)

        # peak v: v at peak_idx as found by find_depols_with_peaks function
        peak_v = voltage_recording[peak_idx]
        eventsmeasures_dictionary['peakv'].append(peak_v)

        ed_peakv = voltage_eventdetecttrace[peak_idx]
        eventsmeasures_dictionary['edtrace_peakv'].append(ed_peakv)

        # amplitude: peakv - baselinev
        peakamp = peak_v - baseline_v
        eventsmeasures_dictionary['amplitude'].append(peakamp)

        ed_peakamp = ed_peakv - ed_baseline_v
        eventsmeasures_dictionary['edtrace_amplitude'].append(ed_peakamp)

        # approx.osc slope: slope in voltage in the ms before the event's baseline_idx
        prebaseline_vslope = (voltage_oscillationstrace[baseline_idx] -
                              voltage_oscillationstrace[baseline_idx - ms_insamples])  # in mV/ms
        eventsmeasures_dictionary['approx_oscslope'].append(prebaseline_vslope)

        edtrace_prebaseline_vslope = (voltage_eventdetecttrace[baseline_idx] -
                                      voltage_eventdetecttrace[baseline_idx - ms_insamples])
        eventsmeasures_dictionary['edtrace_approx_oscslope'].append(edtrace_prebaseline_vslope)

        # approximate oscillation phase and instantaneous frequency
        approx_oscphase = voltage_approxphase[baseline_idx]
        eventsmeasures_dictionary['approx_oscinstphase'].append(approx_oscphase)

        # approximate instantaneous frequency (at baselinev)
        approx_instfreq = voltage_approxinstfreq[baseline_idx]
        eventsmeasures_dictionary['approx_oscinstfreq'].append(approx_instfreq)

        # rise-time: time from 10% - 90% of peak amp; value and start_idx
        fullrisetrace = voltage_denoised[baseline_idx:peak_idx + 1]  # this way the snippet includes peak_idx
        risetrace_clipped1 = fullrisetrace[fullrisetrace >= baseline_v + 0.1 * peakamp]
        risestart_idx = int(peak_idx - len(risetrace_clipped1))
        risetrace_clipped2 = risetrace_clipped1[risetrace_clipped1 <= baseline_v + 0.9 * peakamp]
        rise_time = len(risetrace_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['rise_time'].append(rise_time)
        eventsmeasures_dictionary['rt_start_idx'].append(risestart_idx)

        ed_fullrisetrace = voltage_eventdetecttrace[baseline_idx:peak_idx + 1]
        ed_risetrace_clipped1 = ed_fullrisetrace[ed_fullrisetrace > ed_baseline_v + 0.1 * ed_peakamp]
        ed_risestart_idx = int(peak_idx - len(ed_risetrace_clipped1))
        ed_risetrace_clipped2 = ed_risetrace_clipped1[ed_risetrace_clipped1 <= ed_baseline_v + 0.9 * ed_peakamp]
        ed_rise_time = len(ed_risetrace_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['ed_rise_time'].append(ed_rise_time)
        eventsmeasures_dictionary['ed_rt_start_idx'].append(ed_risestart_idx)

        # rise-time from 20% - 80% of peak amp; value and start_idx
        rise20clipped_1 = fullrisetrace[fullrisetrace >= baseline_v + 0.2 * peakamp]
        rise20start_idx = int(peak_idx - len(rise20clipped_1))
        rise20_clipped2 = rise20clipped_1[rise20clipped_1 <= baseline_v + 0.8 * peakamp]
        rise_time_20_80 = len(rise20_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['rise_time_20_80'] = rise_time_20_80
        eventsmeasures_dictionary['rt20_start_idx'] = rise20start_idx

        ed_rise20clipped_1 = ed_fullrisetrace[ed_fullrisetrace >= ed_baseline_v + 0.2 * ed_peakamp]
        ed_rise20start_idx = int(peak_idx - len(ed_rise20clipped_1))
        ed_rise20_clipped2 = ed_rise20clipped_1[ed_rise20clipped_1 <= ed_baseline_v + 0.8 * ed_peakamp]
        ed_rise_time_20_80 = len(ed_rise20_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['ed_rise_time_20_80'] = ed_rise_time_20_80
        eventsmeasures_dictionary['ed_rt20_start_idx'] = ed_rise20start_idx

        # half-width: event width at 50% of amplitude; value and start_idx
        halfhalfwidth_inidcs = len(fullrisetrace[fullrisetrace >= baseline_v + 0.5 * peakamp])
        half_width_startidx = int(peak_idx - halfhalfwidth_inidcs)
        descendtrace = voltage_denoised[peak_idx:peak_idx + spikewindow_insamples]
        secondhalfhalfwidth_inidcs = descend_vtrace_until(descendtrace, baseline_v + 0.5 * peakamp)
        halfwidth_inidcs = halfhalfwidth_inidcs + secondhalfhalfwidth_inidcs
        half_width = halfwidth_inidcs * sampling_period_inms
        eventsmeasures_dictionary['half_width'] = half_width
        eventsmeasures_dictionary['hw_start_idx'] = half_width_startidx

        ed_halfhalfwidth_inidcs = len(ed_fullrisetrace[ed_fullrisetrace >= ed_baseline_v + 0.5 * ed_peakamp])
        ed_half_width_startidx = int(peak_idx - ed_halfhalfwidth_inidcs)
        ed_descendtrace = voltage_eventdetecttrace[peak_idx:peak_idx + spikewindow_insamples]
        ed_secondhalfhalfwidth_inidcs = descend_vtrace_until(ed_descendtrace, ed_baseline_v + 0.5 * ed_peakamp)
        ed_halfwidth_inidcs = ed_halfhalfwidth_inidcs + ed_secondhalfhalfwidth_inidcs
        ed_half_width = ed_halfwidth_inidcs * sampling_period_inms
        eventsmeasures_dictionary['ed_half_width'] = ed_half_width
        eventsmeasures_dictionary['ed_hw_start_idx'] = ed_half_width_startidx

        # max dV/dt between baseline and peak
        upstrokev = voltage_denoised[baseline_idx:peak_idx + 1]
        upstrokev_diff = np.diff(upstrokev)
        maxdvdt = np.amax(upstrokev_diff)
        maxdvdt_idx = int(baseline_idx + np.argmax(upstrokev_diff))
        eventsmeasures_dictionary['maxdvdt'] = maxdvdt
        eventsmeasures_dictionary['maxdvdt_idx'] = maxdvdt_idx

        ed_upstrokev = voltage_eventdetecttrace[baseline_idx:peak_idx + 1]
        ed_upstrokev_diff = np.diff(ed_upstrokev)
        ed_maxdvdt = np.amax(ed_upstrokev_diff)
        ed_maxdvdt_idx = int(baseline_idx + np.argmax(ed_upstrokev_diff))
        eventsmeasures_dictionary['ed_maxdvdt'] = ed_maxdvdt
        eventsmeasures_dictionary['ed_maxdvdt_idx'] = ed_maxdvdt_idx

        # calculation of thresholds (only for those events that are likely to have one)
        if maxdvdt >= 10:
            idx = maxdvdt_idx - baseline_idx
            idx2 = idx
            ed_idx = ed_maxdvdt_idx - baseline_idx
            ed_idx2 = ed_idx

        # point where dV/dt = 10mV/ms; V value and idx
            while upstrokev_diff[idx] >= 10:
                idx += -1
            dvdt10_idx = int(baseline_idx + idx)
            dvdt10_v = voltage_denoised[dvdt10_idx]

            while ed_upstrokev_diff[ed_idx] >= 10:
                ed_idx += -1
            ed_dvdt10_idx = int(baseline_idx + ed_idx)
            ed_dvdt10_v = voltage_denoised[ed_dvdt10_idx]

        # threshold: V at 10% of max.dV/dt (if max dV/dt > 10); value and idx
            while upstrokev_diff[idx2] >= (0.1 * maxdvdt):
                idx2 += -1
            threshold_idx = int(baseline_idx + idx2)
            threshold_v = voltage_denoised[threshold_idx]

            while ed_upstrokev_diff[ed_idx2] >= (0.1 * ed_maxdvdt):
                ed_idx2 += -1
            ed_threshold_idx = int(baseline_idx + ed_idx2)
            ed_threshold_v = voltage_eventdetecttrace[ed_threshold_idx]

        else:  # filling in 'nan' for events where these measures cannot be taken
            dvdt10_idx = float('nan')
            ed_dvdt10_idx = float('nan')
            dvdt10_v = float('nan')
            ed_dvdt10_v = float('nan')
            threshold_idx = float('nan')
            ed_threshold_idx = float('nan')
            threshold_v = float('nan')
            ed_threshold_v = float('nan')

        eventsmeasures_dictionary['dvdt10v'] = dvdt10_v
        eventsmeasures_dictionary['dvdt10_idx'] = dvdt10_idx
        eventsmeasures_dictionary['thresholdv'] = threshold_v
        eventsmeasures_dictionary['threshold_idx'] = threshold_idx

        eventsmeasures_dictionary['ed_dvdt10v'] = ed_dvdt10_v
        eventsmeasures_dictionary['ed_dvdt10_idx'] = ed_dvdt10_idx
        eventsmeasures_dictionary['ed_thresholdv'] = ed_threshold_v
        eventsmeasures_dictionary['ed_threshold_idx'] = ed_threshold_idx

        # threshold-width: time from threshold reached until return to threshold V
        if threshold_v is not np.nan:
            returntothreshold_inidcs = descend_vtrace_until(descendtrace, threshold_v)
            thresholdwidth_inidcs = peak_idx - threshold_idx + returntothreshold_inidcs
            threshold_width = thresholdwidth_inidcs * sampling_period_inms
        else:
            threshold_width = float('nan')
        eventsmeasures_dictionary['threshold_width'] = threshold_width

        if ed_threshold_v is not np.nan:
            ed_returntothreshold_inidcs = descend_vtrace_until(ed_descendtrace, ed_threshold_v)
            ed_thresholdwidth_inidcs = peak_idx - ed_threshold_idx + ed_returntothreshold_inidcs
            ed_threshold_width = ed_thresholdwidth_inidcs * sampling_period_inms
        else:
            ed_threshold_width = float('nan')
        eventsmeasures_dictionary['ed_threshold_width'] = ed_threshold_width

        # baseline-width: time from baseline_idx until baselinev re-reached after event peak
        returntobaseline_inidcs = descend_vtrace_until(descendtrace, baseline_v)
        baselinewidth_inidcs = peak_idx - baseline_idx + returntobaseline_inidcs
        baseline_width = baselinewidth_inidcs * sampling_period_inms
        eventsmeasures_dictionary['baseline_width'] = baseline_width

        ed_returntobaseline_inidcs = descend_vtrace_until(ed_descendtrace, ed_baseline_v)
        ed_baselinewidth_inidcs = peak_idx - baseline_idx + ed_returntobaseline_inidcs
        ed_baseline_width = ed_baselinewidth_inidcs * sampling_period_inms
        eventsmeasures_dictionary['ed_baseline_width'] = ed_baseline_width

        # calculation of AHP measures
        if baseline_width is np.nan:
            ahpmin_idx = float('nan')
            ahpamplitude = float('nan')
            ahpend_idx = float('nan')
            ahp_width = float('nan')
        else:
            ahptrace = voltage_denoised[(baseline_idx + baselinewidth_inidcs):(baseline_idx
                                                                               + baselinewidth_inidcs
                                                                               + spikeahpwindow_insamples)]
            # AHP min., value and idx
            ahpmin_v = np.amin(ahptrace)
            if (ahpmin_v < baseline_v) and (len(ahptrace) > spikeahpwindow_insamples - 2):
                ahpamplitude = baseline_v - ahpmin_v
                ahpmin_idx_inahptrace = np.argmin(ahptrace)
                ahpmin_idx = int(baseline_idx + baselinewidth_inidcs + ahpmin_idx_inahptrace)
                # AHP width, value and end idx
                ahpwidth_inidcs = ahpmin_idx_inahptrace
                while (ahptrace[ahpwidth_inidcs] < baseline_v) and (ahpwidth_inidcs < len(ahptrace) - 1):
                    ahpwidth_inidcs += 1
                ahpend_idx = int(baseline_idx + baselinewidth_inidcs + ahpwidth_inidcs)
                if voltage_denoised[ahpend_idx] < baseline_v:
                    ahpend_idx = float('nan')
                ahp_totalwidth_inidcs = baseline_idx + baselinewidth_inidcs - ahpend_idx
                ahp_width = ahp_totalwidth_inidcs * sampling_period_inms
            else:
                ahpamplitude = float('nan')
                ahpmin_idx = float('nan')
                ahp_width = float('nan')
                ahpend_idx = float('nan')

        eventsmeasures_dictionary['ahp_amplitude'] = ahpamplitude
        eventsmeasures_dictionary['ahp_width'] = ahp_width
        eventsmeasures_dictionary['ahp_min_idx'] = ahpmin_idx
        eventsmeasures_dictionary['ahp_end_idx'] = ahpend_idx

        if ed_baseline_width is np.nan:
            ed_ahpmin_idx = float('nan')
            ed_ahpamplitude = float('nan')
            ed_ahpend_idx = float('nan')
            ed_ahp_width = float('nan')
        else:
            ed_ahptrace = voltage_eventdetecttrace[(baseline_idx + ed_baselinewidth_inidcs):(baseline_idx
                                                                               + ed_baselinewidth_inidcs
                                                                               + spikeahpwindow_insamples)]
        # AHP min., value and idx
            ed_ahpmin_v = np.amin(ed_ahptrace)
            if (ed_ahpmin_v < ed_baseline_v) and (len(ed_ahptrace) > spikeahpwindow_insamples - 2):
                ed_ahpamplitude = baseline_v - ed_ahpmin_v
                ed_ahpmin_idx_inahptrace = np.argmin(ed_ahptrace)
                ed_ahpmin_idx = int(baseline_idx + ed_baselinewidth_inidcs + ed_ahpmin_idx_inahptrace)
        # AHP width, value and end idx
                ed_ahpwidth_inidcs = ed_ahpmin_idx_inahptrace
                while (ed_ahptrace[ed_ahpwidth_inidcs] < ed_baseline_v) and (ed_ahpwidth_inidcs < len(ed_ahptrace) - 1):
                    ed_ahpwidth_inidcs += 1
                ed_ahpend_idx = int(baseline_idx + ed_baselinewidth_inidcs + ed_ahpwidth_inidcs)
                if voltage_eventdetecttrace[ed_ahpend_idx] < ed_baseline_v:
                    ed_ahpend_idx = float('nan')
                ed_ahp_totalwidth_inidcs = baseline_idx + ed_baselinewidth_inidcs - ed_ahpend_idx
                ed_ahp_width = ed_ahp_totalwidth_inidcs * sampling_period_inms
            else:
                ed_ahpamplitude = float('nan')
                ed_ahpmin_idx = float('nan')
                ed_ahp_width = float('nan')
                ed_ahpend_idx = float('nan')

        eventsmeasures_dictionary['ed_ahp_amplitude'] = ed_ahpamplitude
        eventsmeasures_dictionary['ed_ahp_width'] = ed_ahp_width
        eventsmeasures_dictionary['ed_ahp_min_idx'] = ed_ahpmin_idx
        eventsmeasures_dictionary['ed_ahp_end_idx'] = ed_ahpend_idx

        # labeling clearly identifiable events: action potentials and AP shoulder peaks
        event_label = 'none'
        spikeshoulderpeaks = []
        n_spikeshoulderpeaks = float('nan')
        if (peakamp > 30) and (peak_v > 0):
            event_label = 'actionpotential'
        # for APs, get the number of spikeshoulderpeaks and their idcs
        if event_label == 'actionpotential' and np.isnan(threshold_width):
            spikeshoulderpeaks = [idx for idx in peaks_idcs if peak_idx < idx < (peak_idx + 5 * ms_insamples)]
            n_spikeshoulderpeaks = len(spikeshoulderpeaks)
        elif event_label == 'actionpotential':
            spikeshoulderpeaks = [idx for idx in peaks_idcs if peak_idx < idx < (peak_idx + returntobaseline_inidcs)]
            n_spikeshoulderpeaks = len(spikeshoulderpeaks)
        elif peak_idx in eventsmeasures_dictionary['spikeshoulderpeaks_idcs'][-1]:
            event_label = 'spikeshoulderpeak'

        eventsmeasures_dictionary['event_label'].append(event_label)
        eventsmeasures_dictionary['spikeshoulderpeaks'].append(spikeshoulderpeaks)
        eventsmeasures_dictionary['n_spikeshoulderpeaks'].append(n_spikeshoulderpeaks)

    return eventsmeasures_dictionary


# helper-functions:
# making empty dictionaries with keys for all events measures
def make_eventsmeasures_dictionary():
    """This function creates 'empty' dictionaries with
    a key for each measure that will be taken for each event. """
    events_measures = {
        'event_label': [],
        'file_origin': [],
        'segment_idx': [],
        'applied_current': [],
        'applied_ttlpulse': [],
        'approx_oscslope': [],
        'approx_oscinstphase': [],
        'approx_oscinstfreq': [],
        'edtrace_approx_oscslope': [],

        'peakv': [],
        'baselinev': [],
        'amplitude': [],
        'rise_time': [],
        'rise_time_20_80': [],
        'maxdvdt': [],
        'dvdt10v': [],
        'thresholdv': [],
        'half_width': [],
        'threshold_width': [],
        'baseline_width': [],
        'ahp_amplitude': [],
        'ahp_width': [],
        'n_spikeshoulderpeaks': [],
        'spikeshoulderpeaks_idcs': [],

        'peakv_idx': [],
        'baselinev_idx': [],
        'rt_start_idx': [],
        'rt20_start_idx': [],
        'maxdvdt_idx': [],
        'dvdt10_idx': [],
        'threshold_idx': [],
        'hw_start_idx': [],
        'ahp_start_idx': [],
        'ahp_min_idx': [],

        'edtrace_peakv': [],
        'edtrace_baselinev': [],
        'edtrace_amplitude': [],
        'edtrace_rise_time': [],
        'edtrace_rise_time_20_80': [],
        'edtrace_maxdvdt': [],
        'edtrace_dvdt10v': [],
        'edtrace_thresholdv': [],
        'edtrace_half_width': [],
        'edtrace_threshold_width': [],
        'edtrace_baseline_width': [],
        'edtrace_ahp_amplitude': [],
        'edtrace_ahp_width': [],

        'edtrace_rt_start_idx': [],
        'edtrace_rt20_start_idx': [],
        'edtrace_maxdvdt_idx': [],
        'edtrace_dvdt10_idx': [],
        'edtrace_threshold_idx': [],
        'edtrace_hw_start_idx': [],
        'edtrace_ahp_start_idx': [],
        'edtrace_ahp_min_idx': [],
    }
    return events_measures


# descending along a v-trace snippet until a value is reached
def descend_vtrace_until(vtracesnippet, v_stop_value):

    idx = 0
    while idx < len(vtracesnippet) - 2 \
        and (vtracesnippet[idx] >= v_stop_value
             or vtracesnippet[idx + 1] >= v_stop_value):
        idx += 1

    if vtracesnippet[idx] <= v_stop_value:
        return idx

    else:
        return float('nan')

# %% long-pulse response properties

# the main function:
# return all long-pulse related measurements for a single segment in a dictionary.
def get_longpulsemeasures(block, segment_idx,
                          maxresponse_timewindow=20,
                          pulse_applied_window=[]):

    # step1] prep:
    # getting all the relevant data from the Neo/Block object
    single_segment = block.segments[segment_idx]
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.array(np.squeeze(single_voltage_trace))              # !Make sure it's in mV
    current_recording = np.array(np.squeeze(single_segment.analogsignals[1]))   # !Make sure it's in pA
    sampling_frequency = float(single_voltage_trace.sampling_rate)              # !Make sure it's in Hz
    sampling_period_inms = float(single_voltage_trace.sampling_period) * 1000

    # parameter settings - default time windows:
    ms_insamples = int(sampling_frequency / 1000)
    maxresponsewindow_insamples = int(sampling_frequency / 1000 * maxresponse_timewindow) # max distance from depol_idx to peak

    longpulsesmeasures_resultsdictionary = make_longpulsesmeasures_dictionary()

    # step2] determining where exactly the current pulse starts and ends

    # step3] taking all the measurements

    # finally] adding file_origin and segment_idx information
    trace_origin = [block.file_origin]
    segidx = [segment_idx]
    longpulsesmeasures_resultsdictionary['file_origin'] = \
        trace_origin * len(list(longpulsesmeasures_resultsdictionary.values())[0])
    longpulsesmeasures_resultsdictionary['segment_idx'] = \
        segidx * len(list(longpulsesmeasures_resultsdictionary.values())[0])

    return longpulsesmeasures_resultsdictionary

# helper-functions:
# making an empty dictionary with keys for all long-pulses measures
def make_longpulsesmeasures_dictionary():
    longpulses_measures = {
        # basic bookkeeping:
        'file_origin': [],
        'segment_idx': [],
        'c_prepulse': [],                       # holding current before pulse
        'c_pulse': [],                          # current applied during the pulse
        'c_postpulse': [],                      # holding current after pulse
        'c_stepsize': [],                       # current step size
        'pulse_start_t': [],                    # time where current pulse starts (in ms relative to trace start)
        'pulse_end_t': [],                      # time where current pulse ends
        # measures common to all long-pulse traces:
        'v_prepulse': [],                       # 'resting' voltage before pulse
        'v_pulse_maxresponse': [],              # voltage at the maximal initial deflection after pulse applied
        'v_pulse_maxresponse_t': [],            # time from pulse applied until maximal response reached
        'v_pulse_maxresponse_stepsize': [],     # voltage step size from 'rest' to maximal initial deflection
        'v_pulse_ss': [],                       # voltage at steady-state during pulse application
        'v_pulse_ss_stepsize': [],              # voltage step size from 'rest' to steady-state
        'v_postpulse_maxresponse': [],          # voltage at the maximal deflection after release from pulse
        'v_postpulse_maxresponse_t': [],        # time from pulse released until maximal response reached
        'v_postpulse_maxresponse_stepsize': [], # voltage step size from 'rest' to maximal deflection after pulse release
        # measures for (some) hyperpolarizing pulses only:
        'v_postpulse_adhp_max': [],             # voltage at the maximal after-depolarization-hyperpolarization
        'v_postpulse_adhp_max_t': [],           # time from postpulse_maxresponse_t until postpulse_adhp_max
        'v_postpulse_adhp_stepsize': [],        # voltage step size from 'rest' to maximal adhp value
        'v_postpulse_adhp_total_t': [],         # time from postpulse_maxresponse_t to 'rest'v re-reached
        # measures for (some) depolarizing pulses only:
        'n_aps': [],                            # total number of action potentials fired during pulse
        'aps_peaks': [],                        # list of peaks_idcs for aps fired during pulse
        'aps_isi_min': [],                      # smallest inter-spike-interval
        'aps_isi_max': [],                      # largest inter-spike interval
        'aps_isi_mean': []                      # mean inter-spike interval
    }

    return longpulses_measures
