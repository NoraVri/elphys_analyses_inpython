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
                           depol_to_peak_window=5, event_width_window=40, ahp_width_window=150,
                           noisefilter_hpfreq=3000, oscfilter_lpfreq=20,
                           ttleffect_window=None,
                           plot='off'):
    """ This function finds depolarizing events, and constructs a dictionary containing
    the locations and measured parameters of all detected events.
    It also returns a label for clearly identifyable events (all other events are labeled 'None').
    Depolarizations are detected and measured in multiple steps:
    First, the event-detect- (ed-)trace is created by taking the the raw voltage trace and subtracting
    oscillations (as gotten by low-pass filtering V) and noise (as gotten by high-pass filtering V) from it.
    Then, points where the ms-by-ms derivative of the event-detect voltage
    is larger than min_depolspeed are examined, and baseline- and peak-points marked if a peak
    and then a decay in voltage after the peak are found.
    Finally, the baseline- and peak-point are used to measure event parameters (as constrained by the relevant windows).
    Measures are collected into one dictionary per segment.
    If plot is 'on', all traces and points gotten along the way from raw data to detected events are plotted.

    This function assumes the following conventions:
    In the input raw data: voltage in mV and current in pA
    In the outputted results: voltage in mV, current in pA and time-units in ms.
    """
    #step1] prep:
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    sampling_period_inms = single_voltage_trace.sampling_period.rescale('ms')   # keeps its pq-properties for now
    voltage_recording = np.array(np.squeeze(single_voltage_trace))              # !should be in mV
    current_recording = np.array(np.squeeze(single_segment.analogsignals[1]))   # !should be in pA
    if len(single_segment.analogsignals) == 3:
        auxttl_recording = np.array(np.squeeze(single_segment.analogsignals[2]))
    else:
        auxttl_recording = None

    ms_insamples = int(1 / (sampling_period_inms))

    # filtering the raw voltage twice: high-pass to get 'only the noise', and low-pass to get 'only the STOs'.
    voltage_oscillationstrace, voltage_noisetrace = apply_filters_to_vtrace(voltage_recording,
                                                                            oscfilter_lpfreq,
                                                                            noisefilter_hpfreq,
                                                                            float(single_voltage_trace.sampling_rate.rescale('Hz')),
                                                                            plot)
    # Subtract both from raw voltage to get trace for event-detection.
    voltage_eventdetecttrace = voltage_recording - voltage_oscillationstrace - voltage_noisetrace
    # plotting the raw and filtered data
    if plot == 'on':
        figure, axes = plt.subplots(2, 1, sharex='all')
        axes[0].plot(time_axis, voltage_recording,
                     color='blue',
                     label='raw voltage recording')
        axes[0].plot(time_axis, voltage_oscillationstrace,
                     color='black',
                     label='voltage, lp-filtered at ' + str(oscfilter_lpfreq) + 'Hz')
        axes[0].legend()
        axes[1].plot(time_axis, voltage_noisetrace,
                     color='black',
                     label='voltage, hp-filtered at ' + str(noisefilter_hpfreq) + 'Hz')
        axes[1].legend()

    #taking the ms-by-ms derivative, and adjusting time axis accordingly
    voltage_permsderivative = make_derivative_per_ms(voltage_eventdetecttrace, ms_insamples)

    #step2] collecting points of interest:
    # peaks and baseline-points of 'proper' depolarizations (as determined by upstroke parameters,
    # and the presence of some voltage decay after a detected peak)
    # (and all depolarizations that are picked up from the derivative-trace alone)
    (depolswithpeaks_idcs, peaks_idcs,
     alldepols_idcs) = find_depols_with_peaks(voltage_eventdetecttrace,
                                              voltage_permsderivative,
                                              ms_insamples,
                                              depol_to_peak_window,
                                              min_depolspeed, min_depolamp)
    # plotting the data with scatters of detected depolarizations peaks and baselines
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

        axes[2].plot(time_axis[:len(voltage_permsderivative):],voltage_permsderivative,
                     color='black',
                     label='event-detect trace derivative')
        axes[2].scatter(time_axis[alldepols_idcs], voltage_permsderivative[alldepols_idcs],
                        color='blue',
                        label='depolarizations-candidates')
        axes[2].set_xlabel('time (ms)')
        axes[2].legend()

    #step3] taking the measurements of each event - osc. phase and inst.freq estimation only in traces where
    # probably no large current step(s) is/are applied
    # (trace is longer than 2 minutes, or the mean current value is no more than 20pA away from current at the start of the trace)
    if single_segment.t_stop.rescale('s') < 120 \
            and ((np.mean(current_recording) < (np.mean(current_recording[0:ms_insamples]) - 20))
                or (np.mean(current_recording) > (np.mean(current_recording[0:ms_insamples]) + 20))):
        voltage_approxphase = None
        voltage_approxinstfreq = None
    else:
        voltage_approxphase, voltage_approxinstfreq = apply_hilberttransform_to_vtrace(voltage_oscillationstrace,
                                                                                       time_axis,
                                                                                       float(single_voltage_trace.sampling_rate.rescale('Hz')),
                                                                                       plot)
    # constructing the dictionary of peaks_idcs with all related measurements
    voltage_trace = voltage_recording - voltage_noisetrace
    eventsmeasures_dictionary = get_events_measures(peaks_idcs, depolswithpeaks_idcs,
                                                    voltage_trace,
                                                    voltage_oscillationstrace,
                                                    voltage_eventdetecttrace,
                                                    current_recording,
                                                    auxttl_recording,
                                                    float(sampling_period_inms),
                                                    ms_insamples,
                                                    event_width_window,
                                                    ahp_width_window,
                                                    ttleffect_window,
                                                    voltage_approxphase,
                                                    voltage_approxinstfreq)
    # adding file_origin and segment_idx information
    trace_origin = [block_file_origin]
    segidx = [segment_idx]
    n_depolevents = len(eventsmeasures_dictionary['peakv'])
    eventsmeasures_dictionary['file_origin'] = trace_origin * n_depolevents
    eventsmeasures_dictionary['segment_idx'] = segidx * n_depolevents

    return eventsmeasures_dictionary


# sub-functions:

# finding depolarizing events that have a peak in voltage succeeding them
def find_depols_with_peaks(voltage_eventdetecttrace, voltage_derivative,
                           ms_insamples, peakwindow,
                           min_depolspeed, min_depolamp):
    """ This function finds and returns points where depolarizations occur in the voltage derivative,
    as well as the baseline-points and peak-points of any depolarizations that are found to have these.
    """
    peakwindow_insamples = peakwindow * ms_insamples
    depolarizations = []
    depols_with_peaks = []
    peaks_idcs = []
    for idx in range(ms_insamples, len(voltage_derivative) - peakwindow_insamples):
        if peaks_idcs and idx < peaks_idcs[-1]:
            continue  # skip points that refer to places on already-identified events
        # 1. identify possible depolarizing event-start points:
        # - dV/dt > 2 * min_depolspeed, or:
        # - dV/dt > min_depolspeed
        # AND dV/dt < 10% of min_depolspeed some time in the ms before idx
        # AND dV/dt > min_depolspeed for a duration of at least 0.5ms after idx
        elif voltage_derivative[idx] > 2 * min_depolspeed or \
                (voltage_derivative[idx] >= min_depolspeed
                    and np.min(voltage_derivative[idx-ms_insamples:idx]) < 0.1 * min_depolspeed
                    and [v_diff >= min_depolspeed
                         for v_diff in voltage_derivative[idx:idx + int(ms_insamples/2)]]):

            depol_idx = idx  # depol_idx will mark the baseline_v point, if a proper peak can be found to go with it
            depolarizations.append(depol_idx)

            # 2. identify spontaneous depolarizations that are followed by a peak in voltage
            # points qualify if:
            # - peakv > baselinev + mindepolamp in the event-detect trace,
            # - maxv after peakv is smaller than peakv, and
            # - minv after peakv goes back down to <90% of peak amp within peakwindow
            ed_baselinev = np.mean(voltage_eventdetecttrace[
                                   depol_idx - ms_insamples:depol_idx])
            ed_peakvtrace = voltage_eventdetecttrace[
                            depol_idx:depol_idx + peakwindow_insamples]
            ed_peakv = np.amax(ed_peakvtrace)

            if ed_peakv < ed_baselinev + min_depolamp:
                continue  # skip points where peakv < baselinev + mindepolamp

            peakv_idx = np.argmax(ed_peakvtrace) + depol_idx
            ed_postpeaktrace = voltage_eventdetecttrace[
                               peakv_idx + 1:peakv_idx + peakwindow_insamples + 1]

            ed_postpeakmax = np.amax(ed_postpeaktrace)
            if ed_postpeakmax > ed_peakv:
                continue  # skip points where peakv < maxv post peak

            ed_postpeakmin = np.amin(ed_postpeaktrace)
            if ed_postpeakmin > ed_baselinev + 0.9 * (ed_peakv - ed_baselinev):
                continue  # skip points where minv post peak > baselinev + 0.9 * peak amp
            else:
                depols_with_peaks.append(depol_idx)
                peaks_idcs.append(peakv_idx)

    return depols_with_peaks, peaks_idcs, depolarizations


# taking measures of events based on their baseline- and peak-points
def get_events_measures(peaks_idcs,
                        depolswithpeaks_idcs,
                        voltage_trace,
                        voltage_oscillationstrace,
                        voltage_eventdetecttrace,
                        current_recording,
                        auxttl_recording,
                        sampling_period_inms,
                        ms_insamples,
                        event_width_window,
                        ahp_width_window,
                        ttleffect_window,
                        voltage_approxphase,
                        voltage_approxinstfreq):
    """ This function loops over all peaks/baselines indices, computes the measurable parameters for each event
    and collects these in a dictionary.
    Also, a label is added to the event if it is recognized as being one of the following:
    -actionpotential (by event amplitude or peakv value);
    -spikeshoulderpeak (by occurrence directly after an actionpotential but before return to thresholdv)
    -currentpulsechange (by occurrence directly after a change in the applied current value)
    """
    eventwidthwindow_insamples = event_width_window * ms_insamples
    ahpwindow_insamples = ahp_width_window * ms_insamples
    if not ttleffect_window is None:
        ttleffectwindow_insamples = ms_insamples * ttleffect_window
    else:
        ttleffectwindow_insamples = None

    eventsmeasures_dictionary = make_eventsmeasures_dictionary()
    allspikeshoulderpeaks_idcs = []  # this list is used locally only, for labeling events that are spikeshoulderpeaks

    for baseline_idx, peak_idx in zip(depolswithpeaks_idcs, peaks_idcs):
# calculate measures and add them into the dictionary.
# baseline, peak and amplitude
        # baseline v: mean v in the ms before the event's baseline_idx
        eventsmeasures_dictionary['baselinev_idx'].append(baseline_idx)
        baseline_v = np.mean(voltage_trace[baseline_idx - ms_insamples:baseline_idx])
        ed_baseline_v = np.mean(voltage_eventdetecttrace[baseline_idx - ms_insamples:baseline_idx])
        eventsmeasures_dictionary['baselinev'].append(baseline_v)
        eventsmeasures_dictionary['ed_baselinev'].append(ed_baseline_v)

        # peak v: v at peak_idx as found by find_depols_with_peaks function
        eventsmeasures_dictionary['peakv_idx'].append(peak_idx)
        peak_v = voltage_trace[peak_idx]
        ed_peakv = voltage_eventdetecttrace[peak_idx]
        eventsmeasures_dictionary['peakv'].append(peak_v)
        eventsmeasures_dictionary['ed_peakv'].append(ed_peakv)

        # amplitude: peakv - baselinev
        peakamp = peak_v - baseline_v
        ed_peakamp = ed_peakv - ed_baseline_v
        eventsmeasures_dictionary['amplitude'].append(peakamp)
        eventsmeasures_dictionary['ed_amplitude'].append(ed_peakamp)

# applied stimuli
        # current_applied
        current_applied = np.mean(current_recording[baseline_idx:peak_idx])
        if abs(current_applied) <= 7:  # current in the range of abs(7)pA means no current is being applied
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

# measures describing ongoing oscillations
        # approx.osc slope: slope in voltage in the ms before the event's baseline_idx
        prebaseline_vslope = (voltage_oscillationstrace[baseline_idx] -
                              voltage_oscillationstrace[baseline_idx - ms_insamples])
        edtrace_prebaseline_vslope = (voltage_eventdetecttrace[baseline_idx] -
                                      voltage_eventdetecttrace[baseline_idx - ms_insamples])
        eventsmeasures_dictionary['approx_oscslope'].append(prebaseline_vslope)
        eventsmeasures_dictionary['edtrace_approx_oscslope'].append(edtrace_prebaseline_vslope)

        # approximate oscillation phase (at baseline)
        if not voltage_approxphase is None:
            approx_oscphase = voltage_approxphase[baseline_idx]
        else:
            approx_oscphase = float('nan')
        eventsmeasures_dictionary['approx_oscinstphase'].append(approx_oscphase)

        # approximate instantaneous frequency (at baseline)
        if not voltage_approxinstfreq is None:
            approx_instfreq = voltage_approxinstfreq[baseline_idx]
        else:
            approx_instfreq = float('nan')
        eventsmeasures_dictionary['approx_oscinstfreq'].append(approx_instfreq)

# measures describing the rising phase of the event
        # max dV/dt between baseline and peak
        upstrokev = voltage_trace[baseline_idx:peak_idx + 1]
        upstrokev_diff = np.diff(upstrokev)
        maxdvdt = np.amax(upstrokev_diff)
        maxdvdt_idx = int(baseline_idx + np.argmax(upstrokev_diff))
        eventsmeasures_dictionary['maxdvdt'].append(maxdvdt)
        eventsmeasures_dictionary['maxdvdt_idx'].append(maxdvdt_idx)

        ed_upstrokev = voltage_eventdetecttrace[baseline_idx:peak_idx + 1]
        ed_upstrokev_diff = np.diff(ed_upstrokev)
        ed_maxdvdt = np.amax(ed_upstrokev_diff)
        ed_maxdvdt_idx = int(baseline_idx + np.argmax(ed_upstrokev_diff))
        eventsmeasures_dictionary['ed_maxdvdt'].append(ed_maxdvdt)
        eventsmeasures_dictionary['ed_maxdvdt_idx'].append(ed_maxdvdt_idx)

        # threshold: 10% of max.dV/dt; value and idx
        upstrokev_diff_baselinetomax = upstrokev_diff[0:(maxdvdt_idx-baseline_idx)]
        if len(upstrokev_diff_baselinetomax) > 2:
            maxdvdttothreshold_inidcs = descend_trace_until(np.flip(upstrokev_diff_baselinetomax), (0.1 * maxdvdt))
        else:
            maxdvdttothreshold_inidcs = float('nan')

        threshold_idx = maxdvdt_idx - maxdvdttothreshold_inidcs

        if not np.isnan(threshold_idx):
            threshold_idx = int(threshold_idx)
            threshold_v = voltage_trace[threshold_idx]
        else:
            threshold_idx = None
            threshold_v = float('nan')
        eventsmeasures_dictionary['thresholdv'].append(threshold_v)
        eventsmeasures_dictionary['threshold_idx'].append(threshold_idx)

        # finding the point where dV/dt = 10mV/ms (a common definition of AP threshold); V value and idx
        if maxdvdt >= 10 and len(upstrokev_diff_baselinetomax) > 2:
            maxdvdt_to_dvdt10_inidcs = descend_trace_until(np.flip(upstrokev_diff_baselinetomax), 10)
        else:
            maxdvdt_to_dvdt10_inidcs = float('nan')
        dvdt10_idx = maxdvdt_idx - maxdvdt_to_dvdt10_inidcs

        if not np.isnan(dvdt10_idx):
            dvdt10_idx = int(dvdt10_idx)
            dvdt10_v = voltage_trace[dvdt10_idx]
        else:
            dvdt10_idx = None
            dvdt10_v = float('nan')
        eventsmeasures_dictionary['dvdt10_v'].append(dvdt10_v)
        eventsmeasures_dictionary['dvdt10_idx'].append(dvdt10_idx)

        # rise-time: time from 10% - 90% of peak amp; value and start_idx
        fullrisetrace = voltage_trace[baseline_idx:peak_idx + 1]  # this way the snippet includes peak_idx
        risetrace_clipped1 = fullrisetrace[fullrisetrace >= baseline_v + 0.1 * peakamp]
        risestart_idx = int(peak_idx - len(risetrace_clipped1))
        risetrace_clipped2 = risetrace_clipped1[risetrace_clipped1 <= baseline_v + 0.9 * peakamp]
        rise_time = len(risetrace_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['rise_time_10_90'].append(rise_time)
        eventsmeasures_dictionary['rt10_start_idx'].append(risestart_idx)

        # rise-time from 20% - 80% of peak amp; value and start_idx
        rise20clipped_1 = fullrisetrace[fullrisetrace >= baseline_v + 0.2 * peakamp]
        rise20start_idx = int(peak_idx - len(rise20clipped_1))
        rise20_clipped2 = rise20clipped_1[rise20clipped_1 <= baseline_v + 0.8 * peakamp]
        rise_time_20_80 = len(rise20_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['rise_time_20_80'].append(rise_time_20_80)
        eventsmeasures_dictionary['rt20_start_idx'].append(rise20start_idx)

        ed_fullrisetrace = voltage_eventdetecttrace[baseline_idx:peak_idx + 1]
        ed_rise20clipped_1 = ed_fullrisetrace[ed_fullrisetrace >= ed_baseline_v + 0.2 * ed_peakamp]
        ed_rise20start_idx = int(peak_idx - len(ed_rise20clipped_1))
        ed_rise20_clipped2 = ed_rise20clipped_1[ed_rise20clipped_1 <= ed_baseline_v + 0.8 * ed_peakamp]
        ed_rise_time_20_80 = len(ed_rise20_clipped2) * sampling_period_inms
        eventsmeasures_dictionary['ed_rise_time_20_80'].append(ed_rise_time_20_80)
        eventsmeasures_dictionary['ed_rt20_start_idx'].append(ed_rise20start_idx)

        # rise-time from maxdVdt to peak
        rt_maxdvdt_to_peak = (peak_idx - maxdvdt_idx) * sampling_period_inms
        eventsmeasures_dictionary['rise_time_maxdvdt_peak'].append(rt_maxdvdt_to_peak)

# measures describing the shape of the event (= width at various % of amplitude)
        descendtrace = voltage_trace[peak_idx:peak_idx + eventwidthwindow_insamples]
        # event width at 10% of peak amplitude; value and start_idx
        risephase_width_at10_inidcs = len(fullrisetrace[fullrisetrace >= baseline_v + 0.1 * peakamp])
        width_10_start_idx = int(peak_idx - risephase_width_at10_inidcs)
        descendphase_width_at10_inidcs = descend_trace_until(descendtrace, baseline_v + 0.1 * peakamp)
        width_10 = (risephase_width_at10_inidcs + descendphase_width_at10_inidcs) * sampling_period_inms
        eventsmeasures_dictionary['width_10'].append(width_10)
        eventsmeasures_dictionary['width_10_start_idx'].append(width_10_start_idx)

        # event width at 30% of peak amplitude; value and start_idx
        risephase_width_at30_inidcs = len(fullrisetrace[fullrisetrace >= baseline_v + 0.3 * peakamp])
        width_30_start_idx = int(peak_idx - risephase_width_at30_inidcs)
        descendphase_width_at30_inidcs = descend_trace_until(descendtrace, baseline_v + 0.3 * peakamp)
        width_30 = (risephase_width_at30_inidcs + descendphase_width_at30_inidcs) * sampling_period_inms
        eventsmeasures_dictionary['width_30'].append(width_30)
        eventsmeasures_dictionary['width_30_start_idx'].append(width_30_start_idx)

        # half-width: event width at 50% of amplitude; value and start_idx
        risephase_width_at50_inidcs = len(fullrisetrace[fullrisetrace >= baseline_v + 0.5 * peakamp])
        half_width_startidx = int(peak_idx - risephase_width_at50_inidcs)
        descendphase_width_at50_inidcs = descend_trace_until(descendtrace, baseline_v + 0.5 * peakamp)
        width_50 = (risephase_width_at50_inidcs + descendphase_width_at50_inidcs) * sampling_period_inms
        eventsmeasures_dictionary['width_50'].append(width_50)
        eventsmeasures_dictionary['width_50_start_idx'].append(half_width_startidx)

        # event width at 70% of peak amplitude; value and start_idx
        risephase_width_at70_inidcs = len(fullrisetrace[fullrisetrace >= baseline_v + 0.7 * peakamp])
        width_70_start_idx = int(peak_idx - risephase_width_at70_inidcs)
        descendphase_width_at70_inidcs = descend_trace_until(descendtrace, baseline_v + 0.7 * peakamp)
        width_70 = (risephase_width_at70_inidcs + descendphase_width_at70_inidcs) * sampling_period_inms
        eventsmeasures_dictionary['width_70'].append(width_70)
        eventsmeasures_dictionary['width_70_start_idx'].append(width_70_start_idx)

        # width_at_baseline
        returntobaseline_inidcs = descend_trace_until(descendtrace, baseline_v)
        if not np.isnan(returntobaseline_inidcs):
            baseline_width = (peak_idx - baseline_idx + returntobaseline_inidcs) * sampling_period_inms
        else:
            baseline_width = float('nan')
        eventsmeasures_dictionary['width_baseline'].append(baseline_width)

        # event-detect trace: half-width of the event
        ed_descendtrace = voltage_eventdetecttrace[peak_idx:peak_idx + eventwidthwindow_insamples]
        ed_risephase_width_at50_inidcs = len(ed_fullrisetrace[ed_fullrisetrace >= ed_baseline_v + 0.5 * ed_peakamp])
        ed_half_width_startidx = int(peak_idx - ed_risephase_width_at50_inidcs)
        ed_descendphase_width_at50_inidcs = descend_trace_until(ed_descendtrace, ed_baseline_v + 0.5 * ed_peakamp)
        ed_width_50 = (ed_risephase_width_at50_inidcs + ed_descendphase_width_at50_inidcs) * sampling_period_inms
        eventsmeasures_dictionary['ed_half_width'].append(ed_width_50)
        eventsmeasures_dictionary['ed_hw_start_idx'].append(ed_half_width_startidx)

        # event-detect trace: baseline-width of the event
        ed_returntobaseline_inidcs = descend_trace_until(ed_descendtrace, ed_baseline_v)
        if not np.isnan(ed_returntobaseline_inidcs):
            ed_baseline_width = (peak_idx - baseline_idx + ed_returntobaseline_inidcs) * sampling_period_inms
        else:
            ed_baseline_width = float('nan')
        eventsmeasures_dictionary['ed_baseline_width'].append(ed_baseline_width)

 # measures describing the after-hyperpolarization (AHP)
        if not np.isnan(baseline_width):  # if it didn't return to baseline there's definitely no AHP
            ahptrace = voltage_trace[(peak_idx+returntobaseline_inidcs):(peak_idx
                                                                         +returntobaseline_inidcs
                                                                         +ahpwindow_insamples)]
        else:
            ahptrace = None

        # AHP amplitude (= baselinev - ahpmin_v), value and idx
        ahpmin_v = np.amin(ahptrace)
        if not (ahpmin_v is None) and (ahpmin_v < baseline_v):
            ahpamplitude = baseline_v - ahpmin_v
            ahpmin_idx = int(peak_idx + returntobaseline_inidcs + np.argmin(ahptrace))
        # AHP width, value and end idx
            ahpwidth_inidcs = np.argmin(ahptrace)
            while (ahptrace[ahpwidth_inidcs] < baseline_v) and (ahpwidth_inidcs < len(ahptrace) - 2):
                ahpwidth_inidcs += 1
            ahpend_idx = int(peak_idx + returntobaseline_inidcs + ahpwidth_inidcs)
            if ahpend_idx < len(voltage_trace) - 1 \
                    and voltage_trace[ahpend_idx] > baseline_v - (0.1 * ahpamplitude):
                ahp_width = ahpwidth_inidcs * sampling_period_inms
            else:
                ahpend_idx = None
                ahp_width = float('nan')
        else:
            ahpmin_idx = None
            ahpamplitude = float('nan')
            ahpend_idx = None
            ahp_width = float('nan')
        eventsmeasures_dictionary['ahp_amplitude'].append(ahpamplitude)
        eventsmeasures_dictionary['ahp_min_idx'].append(ahpmin_idx)
        eventsmeasures_dictionary['ahp_width'].append(ahp_width)
        eventsmeasures_dictionary['ahp_end_idx'].append(ahpend_idx)

            # also in the event-detect trace
        if not np.isnan(ed_baseline_width):  # if it didn't return to baseline there's definitely no AHP
            ed_ahptrace = voltage_trace[(peak_idx + ed_returntobaseline_inidcs):(peak_idx
                                                                           + ed_returntobaseline_inidcs
                                                                           + ahpwindow_insamples)]
        else:
            ed_ahptrace = None

        # AHP amplitude (= baselinev - ahpmin_v), value and idx
        ed_ahpmin_v = np.amin(ed_ahptrace)
        if not (ed_ahpmin_v is None) and (ed_ahpmin_v < ed_baseline_v):
            ed_ahpamplitude = ed_baseline_v - ed_ahpmin_v
            ed_ahpmin_idx = int(peak_idx + ed_returntobaseline_inidcs + np.argmin(ed_ahptrace))
            # AHP width, value and end idx
            ed_ahpwidth_inidcs = np.argmin(ed_ahptrace)
            while (ed_ahptrace[ed_ahpwidth_inidcs] < ed_baseline_v) \
                    and (ed_ahpwidth_inidcs < len(ed_ahptrace) - 2):
                ed_ahpwidth_inidcs += 1
            ed_ahpend_idx = int(peak_idx + ed_returntobaseline_inidcs + ed_ahpwidth_inidcs + 1)
            if ed_ahpend_idx < len(voltage_eventdetecttrace) - 1 \
                    and voltage_eventdetecttrace[ed_ahpend_idx] > ed_baseline_v - (0.1 * ed_ahpamplitude):
                ed_ahp_width = ed_ahpwidth_inidcs * sampling_period_inms
            else:
                ed_ahpend_idx = None
                ed_ahp_width = float('nan')
        else:
            ed_ahpmin_idx = None
            ed_ahpamplitude = float('nan')
            ed_ahpend_idx = None
            ed_ahp_width = float('nan')
        eventsmeasures_dictionary['ed_ahp_amplitude'].append(ed_ahpamplitude)
        eventsmeasures_dictionary['ed_ahp_min_idx'].append(ed_ahpmin_idx)
        eventsmeasures_dictionary['ed_ahp_width'].append(ed_ahp_width)
        eventsmeasures_dictionary['ed_ahp_end_idx'].append(ed_ahpend_idx)

# labeling three specific types of clearly identifyable cases:
# 1. action potentials (events with high peak v or large peak amplitude)
# 2. spikeshoulderpeaks (events that occur before ahp_width_window on the previous event runs out)
# 3. events on top of/evoked by current pulse change (diff(current) > 8 in the window from 20ms before until after the event);
        # creating empty labels for all events
        event_label = None
        spikeshoulderpeaks = []
        n_spikeshoulderpeaks = None

        # labeling actionpotentials (and collecting spikeshoulderpeaks)
        if (peak_v > 5) or (peakamp > 60) or (ed_peakamp > 70):
            event_label = 'actionpotential'
            if np.isnan(baseline_width):
                search_width = ahpwindow_insamples
            else:
                search_width = returntobaseline_inidcs
            spikeshoulderpeaks = [idx for idx in peaks_idcs if peak_idx < idx < (peak_idx + search_width)]
            for peak in spikeshoulderpeaks:
                allspikeshoulderpeaks_idcs.append(peak)
            n_spikeshoulderpeaks = len(spikeshoulderpeaks)

        # labeling spikeshoulderpeaks
        if peak_idx in allspikeshoulderpeaks_idcs:
            event_label = 'spikeshoulderpeak'

        # labeling events that occur on a current pulse change
        preevent_idx = int(baseline_idx - (20 * ms_insamples))
        if preevent_idx < 0:
            preevent_idx = 0
        didt_around_event = np.diff(current_recording[preevent_idx:int(baseline_idx + ahpwindow_insamples)])
        if len(didt_around_event) > 2 and np.amax(np.abs(didt_around_event)) > 8:
            event_label = 'currentpulsechange'

        eventsmeasures_dictionary['event_label'].append(event_label)
        eventsmeasures_dictionary['spikeshoulderpeaks_idcs'].append(spikeshoulderpeaks)
        eventsmeasures_dictionary['n_spikeshoulderpeaks'].append(n_spikeshoulderpeaks)

    return eventsmeasures_dictionary


# helper-functions:

# applying filters
def apply_filters_to_vtrace(voltage_recording,
                            oscfilter_lpfreq, noisefilter_hpfreq,
                            sampling_frequency,
                            plot='off'):
    """ This function takes the raw voltage recording and applies filtering and the hilbert transform
    to get traces for use in event-detection.
    """
    # applying filters to the raw data
    lowpass_sos = signal.butter(2, oscfilter_lpfreq, btype='lowpass',
                                fs=sampling_frequency, output='sos')
    voltage_oscillationstrace = signal.sosfiltfilt(lowpass_sos, voltage_recording)

    highpass_sos = signal.butter(1, noisefilter_hpfreq, btype='highpass',
                                 fs=sampling_frequency, output='sos')
    voltage_noisetrace = signal.sosfiltfilt(highpass_sos, voltage_recording)

    if plot == 'on':
        # plotting the filters' impulse response functions:
        lowpass_dlti = signal.dlti(*signal.butter(2, oscfilter_lpfreq, btype='lowpass',
                                                  fs=sampling_frequency, output='ba'))
        t_lp, y_lp = lowpass_dlti.impulse(n=2000)
        highpass_dlti = signal.dlti(*signal.butter(1, noisefilter_hpfreq, btype='highpass',
                                                   fs=sampling_frequency, output='ba'))
        t_hp, y_hp = highpass_dlti.impulse(n=2000)
        plt.figure()
        plt.plot(t_lp, np.squeeze(y_lp), label='low-pass filter')
        plt.plot(t_hp, np.squeeze(y_hp), label='high-pass filter')
        plt.ylim(np.min(y_lp), np.max(y_lp))
        plt.legend()
        plt.xlabel('n [samples]')
        plt.ylabel('amplitude')
        plt.title('impulse response functions')

    return voltage_oscillationstrace, voltage_noisetrace


# applying the hilbert transform
def apply_hilberttransform_to_vtrace(voltage_trace, time_axis, sampling_frequency, plot='off'):

    # getting the instantaneous phase and frequency from the hilbert transform of the data
    # TODO: replace the line below with code that does proper mean-centering (in traces with current pulses applied this gives particularly unreliable results)
    centering_value = np.mean(voltage_trace)
    voltage_trace_meancentered = voltage_trace - centering_value
    voltage_trace_analyticsignal = signal.hilbert(voltage_trace_meancentered)
    voltage_approxphase = np.angle(voltage_trace_analyticsignal)
    voltage_approxinstfreq = ((np.diff(np.unwrap(voltage_approxphase))
                               / (2.0*np.pi) * sampling_frequency))
    voltage_approxphase = np.angle(voltage_trace_analyticsignal)

    if plot == 'on':
        figure, axes = plt.subplots(2, 1, sharex='all')
        axes[0].plot(time_axis, voltage_approxphase, label='phase')
        axes[0].set_ylim([-3.5, 3.5])
        axes[0].legend()
        axes[1].plot(time_axis[1:], voltage_approxinstfreq,
                     color='black',
                     label='inst.freq.')
        axes[1].set_ylim([-5, 40])
        axes[1].legend()

    return voltage_approxphase, voltage_approxinstfreq


# differentiating: getting the mV/ms change in voltage for each point on the recorded trace
def make_derivative_per_ms(recording_trace, ms_insamples):
    permsderivative = []
    for idx in range(0, len(recording_trace) - ms_insamples):
        slope_approx = recording_trace[idx + ms_insamples] - recording_trace[idx]
        permsderivative.append(slope_approx)
    return np.array(permsderivative)


# making empty dictionaries with keys for all events measures
def make_eventsmeasures_dictionary():
    """This function creates an 'empty' dictionary with
    a key for each measure that will be taken for each event. """

    events_measures = {
        'event_label': [],
        'file_origin': [],
        'segment_idx': [],
        'applied_current': [],
        'applied_ttlpulse': [],

        'baselinev': [],
        'peakv': [],
        'amplitude': [],
        'maxdvdt': [],
        'thresholdv': [],
        'dvdt10_v': [],
        'rise_time_10_90': [],
        'rise_time_20_80': [],
        'rise_time_maxdvdt_peak': [],
        'width_10': [],
        'width_30': [],
        'width_50': [],
        'width_70': [],
        'width_baseline': [],
        'ahp_amplitude': [],
        'ahp_width': [],
        'n_spikeshoulderpeaks': [],
        'spikeshoulderpeaks_idcs': [],

        'peakv_idx': [],
        'baselinev_idx': [],
        'maxdvdt_idx': [],
        'threshold_idx': [],
        'dvdt10_idx': [],
        'rt10_start_idx': [],
        'rt20_start_idx': [],
        'width_10_start_idx': [],
        'width_30_start_idx': [],
        'width_50_start_idx': [],
        'width_70_start_idx': [],
        'ahp_min_idx': [],
        'ahp_end_idx': [],

        'approx_oscslope': [],
        'approx_oscinstphase': [],
        'approx_oscinstfreq': [],
        'edtrace_approx_oscslope': [],

        'ed_peakv': [],
        'ed_baselinev': [],
        'ed_amplitude': [],
        'ed_maxdvdt': [],
        'ed_rise_time_20_80': [],
        'ed_half_width': [],
        'ed_baseline_width': [],
        'ed_ahp_amplitude': [],
        'ed_ahp_width': [],

        'ed_maxdvdt_idx': [],
        'ed_rt20_start_idx': [],
        'ed_hw_start_idx': [],
        'ed_ahp_min_idx': [],
        'ed_ahp_end_idx': [],
    }
    return events_measures


# descending along a v-trace snippet until a value is reached
def descend_trace_until(tracesnippet, stop_value):

    idx = 0
    while idx < len(tracesnippet) - 2 \
        and (tracesnippet[idx] >= stop_value
             or tracesnippet[idx + 1] >= stop_value):
        idx += 1

    if tracesnippet[idx] <= stop_value:
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
