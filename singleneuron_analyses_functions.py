# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:33:29 2020

@author: neert

This file defines a class for working with depolarizing events.
"""
# %% imports
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgnl
import quantities as pq

# %%
def get_depolarizingevents(single_segment,
                           min_depolspeed=0.1,
                           min_depolamp=0.1,
                           mswindow=1,
                           peakwindow=10,
                           fullspikewindow=40,
                           downsample_number=4,
                           plotting='on'):
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.squeeze(single_voltage_trace)
    current_recording = np.squeeze(single_segment.analogsignals[1])
    sampling_rate = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz

    #parameter settings - defaults:
    decimateby_number = downsample_number #the function includes a filter, too, but basically we're downsampling by this number
    mindepol = min_depolspeed  # mV/ms
    depol_minamplitude = min_depolamp  # mV
    #time windows
    window_inms = mswindow #window used for calculating the 'rough' derivative and candidate-depolarizations points
    window_insamples = int(sampling_rate / 1000 * window_inms)
    window_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * window_inms)
    peakwindow_inms = peakwindow
    peakwindow_insamples = int(sampling_rate / 1000 * peakwindow_inms)
    peakwindow_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * peakwindow_inms)
    fullspikewindow_inms = fullspikewindow
    fullspikewindow_insamples = int(sampling_rate / 1000 * fullspikewindow_inms)
    fullspikewindow_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * fullspikewindow_inms)

    #prep:
    #downsampling/filtering the raw voltage
    voltage_downsampled = sgnl.decimate(voltage_recording, decimateby_number)
    time_axis_downsampled = time_axis[::decimateby_number]
    #taking the ms-by-ms derivative
    voltage_permsderivative = []
    for idx in range(0,len(voltage_downsampled)-window_indownsampledsamples):
        v_slope_approx = voltage_downsampled[idx+window_indownsampledsamples] - voltage_downsampled[idx]
        voltage_permsderivative.append(v_slope_approx)
    voltage_permsderivative = np.array(voltage_permsderivative)
    time_axis_derivative = time_axis_downsampled[:len(voltage_permsderivative):]

    #actually collecting points of interest
    depolarizations_indownsampledtrace = []
    depols_with_peaks = []
    peaks_idcs = []
    peaks_risecorrected_idcs = []
    spikes_baseline_idcs = []
    baseline_rereached_idcs = []
    actionpotentials_dictionary = {}
    subthresholddepolarizations_dictionary = {}
    for idx in range(len(voltage_permsderivative) - peakwindow_indownsampledsamples):
        #skip points that refer to places on already-identified events
        if peaks_idcs and idx < peaks_idcs[-1]:
            continue
        elif baseline_rereached_idcs and idx < baseline_rereached_idcs[-1]:
            continue
        else:
        #1. identify depolarizations of mindepol(=0.1)mV/ms or more (relative to the 'general' depolarization rate, for example on an oscillation)
            w1_meanvderivative = np.mean(voltage_permsderivative[idx:idx+window_indownsampledsamples])
            w1_minderivative = np.amin(voltage_permsderivative[idx:idx+window_indownsampledsamples])
            w2_maxvderivative = np.amax(voltage_permsderivative[idx+window_indownsampledsamples:idx+(2*window_indownsampledsamples)])
            #points qualify as depolarizations if:
                # - dV/dt_ms in the first 1ms window is not too variable (mean-min < mindepol)
                # - max dVdt_ms in the second 1ms window is > mindepol + mean dVdt_ms in the first 1ms window
                # - dVdt_ms in the second 1ms window is > mean dVdt_ms in the first 1ms window (for each point in the window)
            if w1_meanvderivative-w1_minderivative < mindepol \
                and w2_maxvderivative >= mindepol+w1_meanvderivative\
                and [dvdt >= w1_meanvderivative for dvdt in voltage_permsderivative[
                                                            idx+window_indownsampledsamples:idx+(2*window_indownsampledsamples)]
                     ]:
                depol_idx = idx+window_indownsampledsamples #depol_idx will mark the baseline_v point, if a proper peak can be found to go with it
                depolarizations_indownsampledtrace.append(depol_idx)

                baselinev = np.mean(voltage_downsampled[depol_idx - window_indownsampledsamples:depol_idx])
                peakvtrace = voltage_downsampled[depol_idx:depol_idx+peakwindow_indownsampledsamples]
                peakv = np.amax(peakvtrace)
                peakv_idx = np.argmax(peakvtrace)

        # 2. identify depolarizations that are followed by a peak in voltage
            # 2a. action potentials: get baseline_v-point and return-to-baseline_v-point (detailed measures will be taken from voltage_recording, not voltage_downsampled)
                if peakv > 0:
                    #TODO
                    #switch out the following code with a function that returns one entry of the actionpotentials_dictionary
                    baseline_rereached_idx = peakv_idx
                    while depol_idx + baseline_rereached_idx < len(
                            voltage_downsampled) and baseline_rereached_idx <= fullspikewindow_indownsampledsamples and \
                            voltage_downsampled[depol_idx + baseline_rereached_idx] > baselinev:
                        baseline_rereached_idx += 1
                    if voltage_downsampled[depol_idx + baseline_rereached_idx] > baselinev:
                        # if v does not go back to baseline after spike, take peakwindow instead
                        baseline_rereached_idcs.append(depol_idx + peakwindow_indownsampledsamples)
                    else:
                        baseline_rereached_idcs.append(depol_idx + baseline_rereached_idx)
                    spikes_baseline_idcs.append(depol_idx)

            # 2b. subthreshold depolarizations: check if they are > depol_minamplitude(=0.1)mV relative to baseline V
                # and if they (probably) have a peak occurring within peakwindow
                elif peakv >= baselinev + depol_minamplitude \
                    and 0.5*window_indownsampledsamples < peakv_idx < 0.75*peakwindow_indownsampledsamples:
                    depols_with_peaks.append(depol_idx)
                    peaks_idcs.append(depol_idx + peakv_idx)
            #2c. subthreshold depolarizations that get lost in oscillations: check if they are > depol_minamplitude(=0.1)mV relative to baseline V
                # in vtrace corrected for pre-baseline avg rise
                else:
                    avgrise = w1_meanvderivative
                    avgrisetrace = np.linspace(start=0,
                                               stop=avgrise * peakwindow_inms,
                                               num=peakwindow_indownsampledsamples)
                    peakvtrace_avgrisesubstracted = peakvtrace - avgrisetrace
                    peakv_risecorrected = np.amax(peakvtrace_avgrisesubstracted)
                    peakv_risecorrected_idx = np.argmax(peakvtrace_avgrisesubstracted)

                    if peakv_risecorrected >= baselinev + depol_minamplitude \
                        and 0.5*window_indownsampledsamples < peakv_risecorrected_idx < 0.75*peakwindow_indownsampledsamples:
                        depols_with_peaks.append(depol_idx)
                        peaks_risecorrected_idcs.append(depol_idx + peakv_risecorrected_idx)

                        # plt.figure()
                        # plt.plot(time_axis_downsampled[
                        #          depol_idx - window_indownsampledsamples:depol_idx + peakwindow_indownsampledsamples],
                        #          voltage_downsampled[
                        #          depol_idx - window_indownsampledsamples:depol_idx + peakwindow_indownsampledsamples],
                        #          color='black')
                        # plt.plot(time_axis_downsampled[depol_idx:depol_idx + peakwindow_indownsampledsamples],
                        #          peakvtrace_avgrisesubstracted,
                        #          color='green')


                        # plt.scatter(time_axis_downsampled[depol_idx], voltage_downsampled[depol_idx],
                        #             color='blue')
                        # plt.scatter(time_axis_downsampled[depol_idx + peakv_idx],
                        #             voltage_downsampled[depol_idx + peakv_idx], color='red')

                        # elif peakv_idx >= 0.75*peakwindow_indownsampledsamples \
                        #     or peakv_risecorrected_idx >= 0.75*peakwindow_indownsampledsamples:
                        #
                        #     # plt.scatter(time_axis_downsampled[depol_idx], voltage_downsampled[depol_idx],
                        #     #             color='blue')
                        #     alternative_peakv = np.amax(peakvtrace[:int(0.75*window_indownsampledsamples):])
                        #     alternative_peakv_idx = np.argmax(peakvtrace[:int(0.75*peakwindow_indownsampledsamples):])
                        #     alternative_peakv_trendcorrected = np.amax(peakvtrace_avgrisesubstracted[:int(0.75*peakwindow_indownsampledsamples):])
                        #     alternative_peakv_trendcorrected_idx = np.argmax(peakvtrace_avgrisesubstracted[:int(0.75*peakwindow_indownsampledsamples):])
                        #     if np.amax([alternative_peakv,alternative_peakv_trendcorrected]) > baselinev + depol_minamplitude \
                        #         and 0.5*window_indownsampledsamples < np.amin([alternative_peakv_idx,alternative_peakv_trendcorrected_idx]) < 0.75*peakwindow_indownsampledsamples:
                        #         depols_with_peaks.append(depol_idx)
                        #         peaks_idcs.append(depol_idx + np.amin([alternative_peakv_idx,alternative_peakv_trendcorrected_idx]))

                            # plt.scatter(time_axis_downsampled[depol_idx + peakv_idx],
                            #             voltage_downsampled[depol_idx + peakv_idx],
                            #             color='yellow')



    depolarizations = np.array(depolarizations_indownsampledtrace) * decimateby_number
    depols_with_peaks = np.array(depols_with_peaks) * decimateby_number
    peaks_idcs = np.array(peaks_idcs) * decimateby_number
    peaks_risecorrected_idcs = np.array(peaks_risecorrected_idcs) * decimateby_number
    spikes_baseline_idcs = np.array(spikes_baseline_idcs) * decimateby_number
    baseline_rereached_idcs = np.array(baseline_rereached_idcs) * decimateby_number



    if plotting == 'on':
        figure,axes = plt.subplots(2,1,sharex=True)
        axes[0].plot(time_axis,voltage_recording,color='blue')
        axes[0].plot(time_axis[::decimateby_number],voltage_downsampled,color='black')
        # axes[0].scatter(time_axis[depolarizations_twicepremeansize],voltage_recording[depolarizations_twicepremeansize],
        #                 color='green')
        # axes[0].scatter(time_axis[depolarizations], voltage_recording[depolarizations],
        #                 color='black')
        axes[0].scatter(time_axis[depols_with_peaks], voltage_recording[depols_with_peaks],
                        color='red')
        axes[0].scatter(time_axis[peaks_idcs], voltage_recording[peaks_idcs],
                        color='green')
        axes[0].scatter(time_axis[peaks_risecorrected_idcs], voltage_recording[peaks_risecorrected_idcs],
                        color='yellow')
        if len(spikes_baseline_idcs) > 0:
            axes[0].scatter(time_axis[spikes_baseline_idcs], voltage_recording[spikes_baseline_idcs],
                            color='black')
            axes[0].scatter(time_axis[baseline_rereached_idcs], voltage_recording[baseline_rereached_idcs],
                            color='blue')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title('voltage trace (black: smoothed)')

        # axes[1].plot(time_axis_downsampled,np.diff(voltage_downsampled,append=voltage_downsampled[-1]),
        #              color='black')
        axes[1].plot(time_axis_derivative,voltage_permsderivative,
                     color='black')
        # axes[1].scatter(time_axis_derivative[smalldepolarizations_indownsampledtrace],
        #                 voltage_permsderivative[smalldepolarizations_indownsampledtrace],
        #                 color='green')
        axes[1].scatter(time_axis_derivative[depolarizations_indownsampledtrace],
                        voltage_permsderivative[depolarizations_indownsampledtrace],
                        color='red')
        axes[1].set_xlabel('time (ms)')
        axes[1].set_title('first derivative of downsampled voltage')
        plt.suptitle(single_segment.file_origin)
    return depols_with_peaks






# %%
#function for finding depolarizing events in a single voltage trace
def singlevoltagetrace_find_depolarizingevents_peaksidcs(single_segment,
                                                         min_event_amplitude=0.5,
                                                         peakheight=0.15,
                                                         plotting='on'):
    #notes for me:
    #(1) the downsampling function (scipy.signal.decimate) includes smoothing as well; I'm using the function's default setting for now.
    #(2) peakheight refers to height of the event in the second derivative of the voltage trace;
    #    min_event_amplitude refers to the height of the actual event in the voltage trace.
    #TODO code improvement ideas: use std as a measure of noise level, and set params accordingly
    """
    Parameters
    ----------
    single_voltage_trace :
        TYPE: AnalogSignal object (as defined in the Neo-IO module).
        Must have sampling rate information, and have unit of mV.
        DESCRIPTION: a single, intracellularly recorded voltage trace.
    min_event_amplitude:
        TYPE: float, optional
        DESCRIPTION: minimal difference between minV and maxV around a (potential) voltage peak.
        The default is 0.5 (mV)
    peakheight :
        TYPE: float, optional
        DESCRIPTION: minimal height of peaks in the second derivative of voltage
        for detection of sub-threshold depolarizing events. The default is 0.15.

    Returns
    -------
    depolarizingevents_peaksidcs :
        TYPE: list of integers
        DESCRIPTION: A list of indices, where each index is unique and corresponds
        to the peak of a sub-threshold depolarizing event.
    also makes a new figure of the voltage trace and derivatives,
    with detected peaks marked.

    """
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.squeeze(single_voltage_trace)
    single_current_trace = single_segment.analogsignals[1]
    current_recording = np.squeeze(single_current_trace)

    #scaling parameters relative to trace sampling rate
    sampling_rate = float(single_voltage_trace.sampling_rate)
    smoothingfactor1 = int(sampling_rate/1000) #smoothingfactor is the window size for the filter applied in the downsampling.
    peakwindow = int(sampling_rate*5/1000) #a fastevent peak should be within 5 ms from the peak-point in the voltage derivative
    currentchange_aroundevent_window = int(sampling_rate*100/1000) #an event peak should not be within 100 ms from DC current step being applied

    # getting a differentiated voltage trace from which fast depolarizations can be picked up
    voltage_downsampled = sgnl.decimate(voltage_recording, smoothingfactor1)
    time_axis_downsampled = time_axis[0::smoothingfactor1]
    voltage_downsampled_derivative = np.diff(voltage_downsampled,append=voltage_downsampled[-1]) #appending the last value keeps the derivative-trace the same length as the original
    voltage_downsampled_derivative = np.where(voltage_downsampled_derivative<0,0,voltage_downsampled_derivative) #replacing all negative values with 0
    voltage_downsampled_secondderivative = np.diff(voltage_downsampled_derivative,append=voltage_downsampled_derivative[-1])
    #using findpeaks on differentiated voltage to pick up candidates for depolarizing events
    depolarizingevents_idcs_indownsampledtrace = sgnl.find_peaks(voltage_downsampled_secondderivative,
                                                                  height=peakheight)[0]

    depolarizingevents_idcs = depolarizingevents_idcs_indownsampledtrace * smoothingfactor1

    # picking up voltage peaks belonging to fast depolarizations, based on some criteria
    depolarizingevents_peaksidcs = []
    #testing each peak on basic criteria; move on to the next idx if criterium isn't met
    for idx in depolarizingevents_idcs:
        voltagesnippet = voltage_recording[idx:idx+peakwindow]
        maxv_insnippet_index = np.argmax(voltagesnippet)
        maxv_insnippet = np.amax(voltagesnippet)
        minv_insnippet = np.amin(voltagesnippet)
        vdiff_insnippet = maxv_insnippet - minv_insnippet

        #check if it's a response to DC current (in window before eventidx)
        if idx < currentchange_aroundevent_window:
            currentsnippet_startidx = 0
        else:
            currentsnippet_startidx = idx - currentchange_aroundevent_window
        currentsnippet = current_recording[currentsnippet_startidx:idx]
        currentchange_insnippet = np.amax(currentsnippet) - np.amin(currentsnippet)
        if currentchange_insnippet > 20:
            continue

        #it's a spike
        if maxv_insnippet > 0:
            continue

        #"peak" is at the start of the window therefore not actually a peak
        if maxv_insnippet_index < 5:
            continue

        #"peak" is at the end of the window therefore not actually a peak
        if maxv_insnippet_index > peakwindow - 5:
            continue

        #peak is on a spike shoulder
        if minv_insnippet > -20:
            continue

        #difference between min and max is too small for it to be a proper event
        if vdiff_insnippet < min_event_amplitude:
        #!! assumes that v is in mV (but does not actually check if that's true right now)
            continue

        depolarizingevent_peakidx = idx + maxv_insnippet_index
#write depolarizing-events parameters-finding function here, such that it's called on a single peakidx
        depolarizingevents_peaksidcs.append(depolarizingevent_peakidx)

    depolarizingevents_peaksidcs = list(set(depolarizingevents_peaksidcs)) #removing duplicates


    #plotting the voltagetrace with detected peaks, and the difftrace to see that things went well
    if plotting == 'on':
        figure,axes = plt.subplots(2,1,sharex=True)
        axes[0].plot(time_axis,voltage_recording,color='blue')
        axes[0].plot(time_axis_downsampled,voltage_downsampled,color='black')
        axes[0].scatter(time_axis[depolarizingevents_peaksidcs],voltage_recording[depolarizingevents_peaksidcs],color='red')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title('voltage trace (black: smoothed)')
        axes[1].plot(time_axis_downsampled,voltage_downsampled_derivative,color='blue')
        axes[1].plot(time_axis_downsampled,voltage_downsampled_secondderivative,color='black')
        axes[1].scatter(time_axis_downsampled[depolarizingevents_idcs_indownsampledtrace],
                        voltage_downsampled_secondderivative[depolarizingevents_idcs_indownsampledtrace],color='green')
        axes[1].set_xlabel('time (ms)')
        axes[1].set_title('first (blue) and second (black) derivative of voltage')
        figure.suptitle(single_segment.file_origin)

    return depolarizingevents_peaksidcs


def singlevoltagetrace_get_depolarizingevents_measures(single_segment,
                                                       depolarizingevents_peaksidcs):

    voltage_recording = np.squeeze(single_segment.analogsignals[0])
    voltage_recording = voltage_recording.rescale('mV')
    sampling_rate = float(single_segment.analogsignals[0].sampling_rate)

    #windows and other static parameters
    window_10ms = int(sampling_rate*10/1000) #the 10 ms before the peak-point
    window_6ms = int(sampling_rate*6/1000)
    window_3ms = int(sampling_rate*3/1000)
    mV_2 = 2 * pq.mV

    depolarizingevents_withmeasures_dictionary = {}
    #finding measures to go with each peakidx, but only if measures pass tests for being 'clean'
    for peakidx in depolarizingevents_peaksidcs:
        baseline = None
        amp = None
        rise_time = None
        decay_time = None

        if peakidx - window_10ms < 0:
            #skip any peaks that are less than 10ms from trace start
            continue

        peak_v = voltage_recording[peakidx]
        vsnippet_inprepeakwindow = voltage_recording[peakidx - window_10ms : peakidx - window_3ms]
        minv_inprepeakwindow = np.amin(vsnippet_inprepeakwindow)
        if peak_v < minv_inprepeakwindow:
            #v in the window 10 - 3 ms before event-peak is higher than event-peak
            continue

        vsnippet_inbaselinewindow = voltage_recording[peakidx - window_6ms : peakidx - window_3ms]
        baseline_v = np.mean(vsnippet_inbaselinewindow)
        if (baseline_v > (minv_inprepeakwindow - mV_2)) & (baseline_v < (minv_inprepeakwindow + mV_2)):
            #mean_v 6-3ms before the peak is +/- 2mV from min_v 10-3 ms before the peak
            baseline = baseline_v
            amp = peak_v - baseline_v

        #code for getting rise_time and decay_time goes here

        depolarizingevents_withmeasures_dictionary[peakidx] = {'baseline_v' : baseline ,
                                          'amplitude' : amp,
                                          'risetime' : rise_time,
                                          'decaytime' : decay_time}
    return depolarizingevents_withmeasures_dictionary