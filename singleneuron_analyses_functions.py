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


# differentiating: getting the mV/ms change in voltage for each index on the recording trace
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
    """ This function loops over all peaks/baselines indices and measures parameters for each event.
    Events are sorted into action potentials and subthreshold events
    depending on event amplitude/peakv.
    """
    (actionpotentials_dictionary,
     depolarizingevents_dictionary) = make_depolarizingevents_measures_dictionaries()

    voltage_denoised = voltage_recording - voltage_noisetrace

    for baseline_idx, peak_idx in zip(depolswithpeaks_idcs, peaks_idcs):

        # baseline v: mean v in the ms before the event's baseline_idx
        baseline_v = np.mean(voltage_denoised[
                             baseline_idx - ms_insamples:baseline_idx])
        ed_baseline_v = np.mean(voltage_eventdetecttrace[
                                baseline_idx - ms_insamples:baseline_idx])

        # peak v: v at peak_idx as found by find_depols_with_peaks function
        peak_v = voltage_recording[peak_idx]
        ed_peakv = voltage_eventdetecttrace[peak_idx]

        # amplitude: peakv - baselinev
        peakamp = peak_v - baseline_v
        ed_peakamp = ed_peakv - ed_baseline_v

        # vslope: slope in voltage in the ms before the event's baseline_idx
        prebaseline_vslope = (voltage_oscillationstrace[baseline_idx] -
                              voltage_oscillationstrace[baseline_idx - ms_insamples])  # in mV/ms

        # current applied
        current_applied = np.mean(current_recording[baseline_idx:peak_idx])
        if abs(current_applied) <= 7:
            current_applied = 0

        # ttl applied (light or puff or whatever)
        if auxttl_recording is None:
            ttlpulse_applied = False
        else:
            if auxttl_recording[baseline_idx] > 1:
                ttlpulse_applied = True
            elif auxttl_recording[peak_idx] > 1:
                ttlpulse_applied = True
            elif ttleffectwindow_insamples is not None:
                auxttlsnippet = auxttl_recording[baseline_idx-ttleffectwindow_insamples:peak_idx]
                if (len(auxttlsnippet) > 0) and (np.amax(auxttlsnippet) > 1):
                    ttlpulse_applied = True
                else:
                    ttlpulse_applied = False
            else:
                ttlpulse_applied = False

        # approximate oscillation phase and instantaneous frequency
        approx_oscphase = voltage_approxphase[baseline_idx]
        approx_instfreq = voltage_approxinstfreq[baseline_idx]

        # rise-time: time from 10% - 90% of peak amp
        fullrisetrace = voltage_denoised[baseline_idx:peak_idx + 1]  # this way the snippet includes peak_idx
        risetrace_clipped1 = fullrisetrace[fullrisetrace >= baseline_v + 0.1 * peakamp]
        risestart_idx = int(peak_idx - len(risetrace_clipped1))
        risetrace_clipped2 = risetrace_clipped1[
            risetrace_clipped1 <= baseline_v + 0.9 * peakamp]
        rise_time = len(risetrace_clipped2) * sampling_period_inms
        # rise-time from 20% - 80% of peak amp
        rise20clipped_1 = fullrisetrace[fullrisetrace >= baseline_v + 0.2 * peakamp]
        rise20start_idx = int(peak_idx - len(rise20clipped_1))
        rise20_clipped2 = rise20clipped_1[rise20clipped_1 <= baseline_v + 0.8 * peakamp]
        rise_time_20_80 = len(rise20_clipped2) * sampling_period_inms
        # rise-time midpoint idx: point where event is at 50% of its amplitude
        risetrace_clipped50 = fullrisetrace[fullrisetrace >= baseline_v + 0.5 * peakamp]
        rise_midpoint_idx = int(peak_idx - len(risetrace_clipped50))

        # half-width: event width at 50% of amplitude
        halfhalfwidth_inidcs = len(fullrisetrace[
                                       fullrisetrace >= baseline_v + 0.5 * peakamp])
        half_width_startidx = int(peak_idx - halfhalfwidth_inidcs)
        descendtrace = voltage_denoised[peak_idx:peak_idx + spikewindow_insamples]
        secondhalfhalfwidth_inidcs = descend_vtrace_until(descendtrace,
                                                          baseline_v + 0.5 * peakamp)
        halfwidth_inidcs = halfhalfwidth_inidcs + secondhalfhalfwidth_inidcs
        half_width = halfwidth_inidcs * sampling_period_inms


# measures specific to action potentials:
        if (((peak_v > 10) and (baseline_v < -20)) or ed_peakamp > 50):
        # threshold: 10% of max. dV/dt
            fullspikev = voltage_denoised[
                         baseline_idx:peak_idx + spikewindow_insamples]
            fullspikev_diff = np.diff(fullspikev)
            maxdvdt = np.amax(fullspikev_diff)
            maxdvdt_idx = np.argmax(fullspikev_diff)
            thrshd_idx = maxdvdt_idx
            while fullspikev_diff[thrshd_idx] > 0.1 * maxdvdt:
                thrshd_idx += -1
            threshold_idx = baseline_idx + thrshd_idx
            threshold_v = voltage_denoised[threshold_idx]

        # threshold-width: AP width at threshold v
            returntothreshold_inidcs = descend_vtrace_until(descendtrace, threshold_v)
            thresholdwidth_inidcs = peak_idx + returntothreshold_inidcs - threshold_idx
            threshold_width = thresholdwidth_inidcs * sampling_period_inms

        # count spikelets on spike shoulder:
                # if voltage did not decay back down to threshold value, any peaks occurring
                # within 5 ms from the spike peak are taken to be spike-shoulder peaks
            if np.isnan(threshold_width):
                spikeshoulderpeaks = [idx for idx in peaks_idcs
                                      if peak_idx < idx < (peak_idx + 5 * ms_insamples)]
                n_spikeshoulderpeaks = len(spikeshoulderpeaks)
                # ahp parameters cannot be calculated
                ahpmin_idx = float('nan')
                ahpamplitude = float('nan')
                ahpend_idx = float('nan')
                ahp_width = float('nan')
            else:
                # any peaks occurring before v decays back down to threshold are taken to be spike-shoulder peaks
                spikeshoulderpeaks = [idx for idx in peaks_idcs
                                      if peak_idx < idx < peak_idx + returntothreshold_inidcs]
                n_spikeshoulderpeaks = len(spikeshoulderpeaks)

    # after-hyperpolarization measures
                ahptrace = voltage_denoised[
                           (threshold_idx + thresholdwidth_inidcs):(threshold_idx
                                                                    + thresholdwidth_inidcs
                                                                    + spikeahpwindow_insamples)]

                if len(ahptrace) > spikeahpwindow_insamples - 2 and np.amin(ahptrace) < baseline_v:
        # ahp min and amplitude
                    ahpmin_idx_inahptrace = np.argmin(ahptrace)
                    ahpmin_idx = int(ahpmin_idx_inahptrace + threshold_idx + thresholdwidth_inidcs)
                    ahpamplitude = baseline_v - np.amin(ahptrace)

        # ahp width
                    ahpwidth_inidcs = ahpmin_idx_inahptrace
                    while ahptrace[ahpwidth_inidcs] < baseline_v and ahpwidth_inidcs < len(ahptrace) - 1:
                        ahpwidth_inidcs += 1
                    ahpend_idx = int(threshold_idx + thresholdwidth_inidcs + ahpwidth_inidcs + 1)
                    if voltage_denoised[ahpend_idx] < baseline_v:
                        ahpend_idx = float('nan')
                    ahp_totalwidth_inidcs = ahpend_idx - threshold_idx + thresholdwidth_inidcs
                    ahp_width = ahp_totalwidth_inidcs * sampling_period_inms

                elif len(ahptrace) > spikewindow_insamples and np.amin(ahptrace) <= threshold_v:
                    ahp_width = 0  # set to 0 if v decayed back to below threshold value
                    ahpmin_idx = float('nan')
                    ahpamplitude = float('nan')
                    ahpend_idx = float('nan')

                else:  # set measures to nan if they cannot be taken
                    ahpmin_idx = float('nan')
                    ahpamplitude = float('nan')
                    ahpend_idx = float('nan')
                    ahp_width = float('nan')

            # adding all the measures into the dictionary
            actionpotentials_dictionary['peakv'].append(peak_v)
            actionpotentials_dictionary['baselinev'].append(baseline_v)
            actionpotentials_dictionary['amplitude'].append(peakamp)
            actionpotentials_dictionary['rise_time'].append(rise_time)
            actionpotentials_dictionary['rise_time_20_80'].append(rise_time_20_80)
            actionpotentials_dictionary['half_width'].append(half_width)
            actionpotentials_dictionary['thresholdv'].append(threshold_v)
            actionpotentials_dictionary['threshold_width'].append(threshold_width)
            actionpotentials_dictionary['spikeshoulderpeaks_idcs'].append(spikeshoulderpeaks)
            actionpotentials_dictionary['n_spikeshoulderpeaks'].append(n_spikeshoulderpeaks)
            actionpotentials_dictionary['ahp_amplitude'].append(ahpamplitude)
            actionpotentials_dictionary['ahp_width'].append(ahp_width)

            actionpotentials_dictionary['applied_current'].append(current_applied)
            actionpotentials_dictionary['applied_ttlpulse'].append(ttlpulse_applied)

            actionpotentials_dictionary['approx_oscslope'].append(prebaseline_vslope)
            actionpotentials_dictionary['approx_oscinstphase'].append(approx_oscphase)
            actionpotentials_dictionary['approx_oscinstfreq'].append(approx_instfreq)

            actionpotentials_dictionary['peakv_idx'].append(peak_idx)
            actionpotentials_dictionary['baselinev_idx'].append(baseline_idx)
            actionpotentials_dictionary['rt_start_idx'].append(risestart_idx)
            actionpotentials_dictionary['rt_midpoint_idx'].append(rise_midpoint_idx)
            actionpotentials_dictionary['rise20start_idx'].append(rise20start_idx)
            actionpotentials_dictionary['hw_start_idx'].append(half_width_startidx)
            actionpotentials_dictionary['threshold_idx'].append(threshold_idx)
            actionpotentials_dictionary['ahp_min_idx'].append(ahpmin_idx)
            actionpotentials_dictionary['ahp_end_idx'].append(ahpend_idx)

# measures specific to depolarizing events:
        else:
        # rise-time in the event-detect trace
            ed_fullrisetrace = voltage_eventdetecttrace[baseline_idx:peak_idx]
            ed_risetrace_clipped1 = ed_fullrisetrace[
                                    ed_fullrisetrace >= ed_baseline_v + 0.1 * ed_peakamp]
            ed_risestart_idx = peak_idx - len(ed_risetrace_clipped1)
            ed_risetrace_clipped2 = ed_risetrace_clipped1[
                            ed_risetrace_clipped1 <= ed_baseline_v + 0.9 * ed_peakamp]
            ed_rise_time = len(ed_risetrace_clipped2) * sampling_period_inms

        # half-width in the event-detect trace
            ed_descendtrace = voltage_eventdetecttrace[
                              peak_idx:peak_idx + spikewindow_insamples]
            ed_halfhalfwidth_inidcs = len(ed_fullrisetrace[
                                              ed_fullrisetrace >= ed_baseline_v + 0.5 * ed_peakamp])
            ed_halfwidth_startidx = peak_idx - ed_halfhalfwidth_inidcs
            ed_secondhalfhalfwidth_inidcs = descend_vtrace_until(ed_descendtrace,
                                                                 ed_baseline_v + 0.5 * ed_peakamp)
            ed_half_width = (ed_halfhalfwidth_inidcs + ed_secondhalfhalfwidth_inidcs) * sampling_period_inms

        # width: time from rise-start (@10% of amp) until rise-start_v re-reached
            pastpeakwidth_inidcs = descend_vtrace_until(descendtrace,
                                                        baseline_v + 0.1 * peakamp)
            width = (peak_idx - risestart_idx + pastpeakwidth_inidcs) * sampling_period_inms
            ed_pastpeakwidth_inidcs = descend_vtrace_until(ed_descendtrace,
                                                           ed_baseline_v + 0.1 * ed_peakamp)
            ed_width = (peak_idx - ed_risestart_idx + ed_pastpeakwidth_inidcs) * sampling_period_inms

        # label: if the event is on the last-identified AP's spikeshoulderpeaks list, update label accordingly
            if not actionpotentials_dictionary['spikeshoulderpeaks_idcs']:
                event_label = ''
            elif peak_idx in actionpotentials_dictionary['spikeshoulderpeaks_idcs'][-1]:
                event_label = 'spikeshoulderpeak'
            else:
                event_label = ''

            # adding all the measures into the dictionary
            depolarizingevents_dictionary['peakv'].append(peak_v)
            depolarizingevents_dictionary['baselinev'].append(baseline_v)
            depolarizingevents_dictionary['amplitude'].append(peakamp)
            depolarizingevents_dictionary['rise_time'].append(rise_time)
            depolarizingevents_dictionary['rise_time_20_80'].append(rise_time_20_80)
            depolarizingevents_dictionary['half_width'].append(half_width)
            depolarizingevents_dictionary['width_at10%amp'].append(width)

            depolarizingevents_dictionary['applied_current'].append(current_applied)
            depolarizingevents_dictionary['applied_ttlpulse'].append(ttlpulse_applied)

            depolarizingevents_dictionary['approx_oscslope'].append(prebaseline_vslope)
            depolarizingevents_dictionary['approx_oscinstphase'].append(approx_oscphase)
            depolarizingevents_dictionary['approx_oscinstfreq'].append(approx_instfreq)

            depolarizingevents_dictionary['edtrace_baselinev'].append(ed_baseline_v)
            depolarizingevents_dictionary['edtrace_amplitude'].append(ed_peakamp)
            depolarizingevents_dictionary['edtrace_rise_time'].append(ed_rise_time)
            depolarizingevents_dictionary['edtrace_half_width'].append(ed_half_width)
            depolarizingevents_dictionary['edtrace_width_at10%amp'].append(ed_width)

            depolarizingevents_dictionary['event_label'].append(event_label)
            depolarizingevents_dictionary['peakv_idx'].append(peak_idx)
            depolarizingevents_dictionary['baselinev_idx'].append(baseline_idx)
            depolarizingevents_dictionary['rt_start_idx'].append(risestart_idx)
            depolarizingevents_dictionary['rt_midpoint_idx'].append(rise_midpoint_idx)
            depolarizingevents_dictionary['rise20start_idx'].append(rise20start_idx)
            depolarizingevents_dictionary['edtrace_rt_start_idx'].append(ed_risestart_idx)
            depolarizingevents_dictionary['hw_start_idx'].append(half_width_startidx)
            depolarizingevents_dictionary['edtrace_hw_start_idx'].append(ed_halfwidth_startidx)

    return actionpotentials_dictionary, depolarizingevents_dictionary


# helper-functions:
# making empty dictionaries with keys for all events measures
def make_depolarizingevents_measures_dictionaries():
    """This function creates 'empty' dictionaries with
    a key for each measure that will be taken for each event. """
    actionpotentials_measures = {
        'peakv': [],
        'baselinev': [],
        'amplitude': [],
        'rise_time': [],
        'rise_time_20_80': [],
        'half_width': [],
        'thresholdv': [],
        'threshold_width': [],
        'n_spikeshoulderpeaks': [],
        'spikeshoulderpeaks_idcs': [],
        'ahp_amplitude': [],
        'ahp_width': [],
        'applied_current': [],
        'applied_ttlpulse': [],

        'approx_oscslope': [],
        'approx_oscinstphase': [],
        'approx_oscinstfreq': [],

        'peakv_idx': [],
        'baselinev_idx': [],
        'rt_start_idx': [],
        'rt_midpoint_idx': [],
        'rise20start_idx': [],
        'hw_start_idx': [],
        'threshold_idx': [],
        'ahp_min_idx': [],
        'ahp_end_idx': [],
        'file_origin': [],
        'segment_idx': [],
    }

    depolarizingevents_measures = {
        'peakv': [],
        'baselinev': [],
        'amplitude': [],
        'rise_time': [],
        'rise_time_20_80': [],
        'half_width': [],
        'width_at10%amp': [],
        'applied_current': [],
        'applied_ttlpulse': [],

        'approx_oscslope': [],
        'approx_oscinstphase': [],
        'approx_oscinstfreq': [],

        'edtrace_baselinev': [],
        'edtrace_amplitude': [],
        'edtrace_rise_time': [],
        'edtrace_half_width': [],
        'edtrace_width_at10%amp': [],

        'event_label': [],
        'peakv_idx': [],
        'baselinev_idx': [],
        'rt_start_idx': [],
        'rt_midpoint_idx': [],
        'rise20start_idx': [],
        'edtrace_rt_start_idx': [],
        'hw_start_idx': [],
        'edtrace_hw_start_idx': [],
        'file_origin': [],
        'segment_idx': [],
    }
    return actionpotentials_measures, depolarizingevents_measures


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
