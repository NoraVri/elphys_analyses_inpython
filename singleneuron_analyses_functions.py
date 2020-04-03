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
def get_depolarizingevents(single_segment,plotting='on'):
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.squeeze(single_voltage_trace)
    current_recording = np.squeeze(single_segment.analogsignals[1])

    sampling_rate = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz
    #parameter settings - finding depolarizations in the raw voltage trace
    decimateby_number = 5 #the function includes a filter, too, but basically we're downsampling by this number
    voltage_downsampled = sgnl.decimate(voltage_recording, decimateby_number)
    time_axis_downsampled = time_axis[::decimateby_number]
#finding depolarizing events in downsampled trace:
    window_inms = 1
    window_insamples = int(sampling_rate / 1000 * window_inms)
    window_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * window_inms)
    print('window in samples in downsampled trace = '+str(window_indownsampledsamples))
    decaywindow_inms = 20
    decaywindow_insamples = int(sampling_rate / 1000 * decaywindow_inms)
    decaywindow_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * decaywindow_inms)
    baselinewindow_inms = 5
    baselinewindow_insamples = int(sampling_rate / 1000 * baselinewindow_inms)
    baselinewindow_indownsampledsamples = int(sampling_rate / 1000 / decimateby_number * baselinewindow_inms)
    # stepwindow_inms = 0.25
    # stepwindow_insamples = int(sampling_rate / 1000 * stepwindow_inms)
    # stepwindow_indownsampedsamples = int(sampling_rate / 1000 / decimateby_number * stepwindow_inms)
    # print('stepwindow in samples in downsampled trace = '+str(stepwindow_indownsampedsamples))
    mindepolamp = 0.1 #mV/ms
    depolamp = 0.25

    # voltage_per2msderivative = []
    voltage_permsderivative = []
    for idx in range(0,len(voltage_downsampled)-window_indownsampledsamples*10):
        v_slope_approx = voltage_downsampled[idx+window_indownsampledsamples] - voltage_downsampled[idx]
        voltage_permsderivative.append(v_slope_approx)
        # v_2msslope_approx = voltage_downsampled[idx+window_indownsampledsamples*2] - voltage_downsampled[idx]
        # v_2msslope_approx = v_2msslope_approx / 2
        # voltage_per2msderivative.append(v_2msslope_approx)
        # v_10msslope_approx = voltage_downsampled[idx+window_indownsampledsamples*2] - voltage_downsampled[idx]
        # v_10msslope_approx = v_10msslope_approx / 10
        # voltage_per10msderivative.append(v_10msslope_approx)
    voltage_permsderivative = np.array(voltage_permsderivative)
    time_axis_derivative = time_axis_downsampled[:len(voltage_permsderivative):]

    depolarizations_indownsampledtrace = []
    depolarizations = []
    maxderivpoints = []
    smalldepolarizations_indownsampledtrace = []
    smalldepolarizations = []

    sample_no = 0
    keep_looping = True
    while sample_no < len(voltage_permsderivative) - 2*window_indownsampledsamples:
        ms1_meanvderivative = np.mean(voltage_permsderivative[sample_no:sample_no + window_indownsampledsamples])
        ms2_maxvderivative = np.amax(
            voltage_permsderivative[sample_no + window_indownsampledsamples:sample_no + window_indownsampledsamples * 2])
        if ms2_maxvderivative >= depolamp + ms1_meanvderivative:
            depolarizations_indownsampledtrace.append(sample_no)
            depolarizations.append(sample_no * decimateby_number)
            ms2_maxvderivative_idx = np.argmax(
                voltage_permsderivative[
                sample_no + window_indownsampledsamples:sample_no + window_indownsampledsamples * 2])
            maxvderiv_sample = sample_no + ms2_maxvderivative_idx
            while voltage_permsderivative[maxvderiv_sample+1] >= voltage_permsderivative[maxvderiv_sample] and maxvderiv_sample < len(voltage_permsderivative) - 1:
                maxvderiv_sample += 1
            skip_samples = maxvderiv_sample - sample_no
            maxderivpoints.append(maxvderiv_sample * decimateby_number)
            sample_no += skip_samples
        elif ms2_maxvderivative >= mindepolamp + ms1_meanvderivative:
            smalldepolarizations_indownsampledtrace.append(idx)
            smalldepolarizations.append(idx * decimateby_number)
            sample_no += 1
        sample_no += 1
    # for idx in range(len(voltage_permsderivative) - window_indownsampledsamples*2):
    #     ms1_meanvderivative = np.mean(voltage_permsderivative[idx:idx+window_indownsampledsamples])
    #     ms2_maxvderivative = np.amax(voltage_permsderivative[idx+window_indownsampledsamples:idx+window_indownsampledsamples*2])
    #     if ms2_maxvderivative >= depolamp + ms1_meanvderivative:
    #         maxvderivative_idx = np.argmax(voltage_permsderivative[idx+window_indownsampledsamples:idx+window_indownsampledsamples*2])
    #         depolarizations_indownsampledtrace.append(idx)
    #         depolarizations.append(idx * decimateby_number)
    #     elif ms2_maxvderivative >= mindepolamp + ms1_meanvderivative:
    #         smalldepolarizations_indownsampledtrace.append(idx)
    #         smalldepolarizations.append(idx * decimateby_number)


    # sample_no = baselinewindow_indownsampledsamples
    # keep_looping = True
    # while keep_looping:
    #     decaystart_idx = 0
    #     postpeak_decay_v = []
    #     if sample_no + decaywindow_indownsampledsamples >= len(voltage_permsderivative):
    #         keep_looping = False
    #         print('reached loop end')
    #         break
    #     if voltage_permsderivative[sample_no] >= mindepolamp * 2:
    #         cleardepolarizations_indownsampledtrace.append(sample_no)
    #         cleardepolarizations.append(sample_no * decimateby_number)
    #         sample_no += 1
    #     if voltage_permsderivative[sample_no] >= mindepolamp:
    #         postsample_riseanddecay_v = voltage_downsampled[sample_no:sample_no+decaywindow_indownsampledsamples]
    #         postsample_riseanddecay_vdiff = voltage_per2msderivative[sample_no:sample_no+decaywindow_indownsampledsamples]
    #         vdiff_smallestvalue = np.amin(voltage_per2msderivative[sample_no:sample_no+decaywindow_indownsampledsamples])
    #         presample_meanvderiv = np.mean(
    #             voltage_per2msderivative[sample_no-baselinewindow_indownsampledsamples:sample_no])
    #
    #         if vdiff_smallestvalue < 0:
    #             maximaldecay_idx = np.argmin(postsample_riseanddecay_vdiff)
    #             peakvidx = np.argmax(postsample_riseanddecay_v)
    #             postpeak_decay_v = postsample_riseanddecay_v[peakvidx::]
    #         elif presample_meanvderiv > 0 and vdiff_smallestvalue < presample_meanvderiv:
    #             maximaldecay_idx = np.argmin(postsample_riseanddecay_vdiff)
    #             approxslope_duringdecay = np.linspace(0,decaywindow_inms*presample_meanvderiv,decaywindow_indownsampledsamples)
    #             peakvidx = np.argmax(postsample_riseanddecay_v-approxslope_duringdecay)
    #             postpeak_decay_v = postsample_riseanddecay_v[peakvidx::]
    #
    #         smalldepolarizations_candidates_indownsampledtrace.append(sample_no)
    #         smalldepolarizations_candidates.append(sample_no * decimateby_number)
    #
    #     if len(postpeak_decay_v) > 0 and maximaldecay_idx > 0:
    #         depolarizations_in_downsampledtrace.append(sample_no)
    #         depolarizations.append(sample_no*5)
    #         sample_no += maximaldecay_idx
    #         print(sample_no)
    #     else:
    #         sample_no += 1


    if plotting == 'on':
        figure,axes = plt.subplots(2,1,sharex=True)
        axes[0].plot(time_axis,voltage_recording,color='blue')
        axes[0].plot(time_axis[::5],voltage_downsampled,color='black')
        # axes[0].scatter(time_axis[depolarizations_twicepremeansize],voltage_recording[depolarizations_twicepremeansize],
        #                 color='green')
        axes[0].scatter(time_axis[depolarizations], voltage_recording[depolarizations],
                        color='red')
        axes[0].scatter(time_axis[smalldepolarizations], voltage_recording[smalldepolarizations],
                        color='black')
        axes[0].set_ylabel('voltage (mV)')
        axes[0].set_title('voltage trace (black: smoothed)')

        # axes[1].plot(time_axis_downsampled,np.diff(voltage_downsampled,append=voltage_downsampled[-1]),
        #              color='black')
        axes[1].plot(time_axis_derivative,voltage_permsderivative,
                     color='green')
        # axes[1].scatter(time_axis_derivative[depolarizations_twicepremeansize_indownsampledtrace],
        #                 voltage_permsderivative[depolarizations_twicepremeansize_indownsampledtrace],
        #                 color='blue')
        axes[1].scatter(time_axis_derivative[depolarizations_indownsampledtrace],
                        voltage_permsderivative[depolarizations_indownsampledtrace],
                        color='red')
        axes[1].set_xlabel('time (ms)')
        axes[1].set_title('first derivative of downsampled voltage')
        plt.suptitle(single_segment.file_origin)
    return depolarizations



# def get_depolarizingevents(single_segment,plotting='on'):
#     # getting all the relevant data from the Neo/Segment object
#     single_voltage_trace = single_segment.analogsignals[0]
#     time_axis = single_voltage_trace.times
#     time_axis = time_axis.rescale('ms').magnitude
#     voltage_recording = np.squeeze(single_voltage_trace)
#     current_recording = np.squeeze(single_segment.analogsignals[1])

#     sampling_rate = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz
#     #parameter settings - finding depolarizations in the raw voltage trace
#     filter_cutofffreq = 2000
#     filter_params = sgnl.butter(10, filter_cutofffreq, 'lowpass', fs=sampling_rate, output='sos')
#     voltage_filtered = sgnl.sosfilt(filter_params, voltage_recording)
#     filterartifact_window_inms = 4
#     filterartifact_window = int(sampling_rate/1000 * filterartifact_window_inms)
# #depolarization condition: wherever diff(filtered_voltage) > 0 for >0.5 ms
# #and there is a minimal change in voltage of 0.1mV in the 10ms window around the marked idx
#     consistentdepolarization_duration_inms = 0.5
#     consistentdepolarization_duration = int(sampling_rate/1000 * consistentdepolarization_duration_inms -1)#-1 to account for taking derivative
#     consistentdepolarization_vchangewindow_inms = 5
#     consistentdepolarization_vchangewindow = int(sampling_rate/1000 * consistentdepolarization_vchangewindow_inms)
#     consistentdepolarization_minvchange = 0.1

#     voltage_filtered_derivative = np.diff(voltage_filtered,append=voltage_filtered[-1])
#     derivativeconsistentlypositive_idcs = [] #any idx in voltage_filtered_derivative where the next ... idcs also have a positive value.
#     for i, idx in enumerate(voltage_filtered_derivative):
#         if idx >= 0 and i+consistentdepolarization_duration < len(voltage_filtered_derivative):
#             if np.amin(voltage_filtered_derivative[i:i+consistentdepolarization_duration]) >= 0:
#                 derivativeconsistentlypositive_idcs.append(i)
#     depolarizingevents_candidates = []
#     for idx in derivativeconsistentlypositive_idcs:
#         if idx+consistentdepolarization_vchangewindow < len(voltage_recording) and idx-consistentdepolarization_vchangewindow >= 0:
#             # print('idx = '+str(idx))
#             vsnippet1 = voltage_recording[idx-consistentdepolarization_vchangewindow:idx]
#             vsnippet2 = voltage_recording[idx:idx+consistentdepolarization_vchangewindow]
#             # print(np.mean(vsnippet))
#             if np.amax(vsnippet1) - np.amin(vsnippet1) > consistentdepolarization_minvchange and np.amax(vsnippet2) - np.amin(vsnippet2) > consistentdepolarization_minvchange:
#                 maxv_insnippet_idx = np.argmax(voltage_recording[idx-consistentdepolarization_vchangewindow:idx+consistentdepolarization_vchangewindow])
#                 eventpeakcandidate_idx = idx - consistentdepolarization_vchangewindow + maxv_insnippet_idx
#                 depolarizingevents_candidates.append(eventpeakcandidate_idx)
#     depolarizingevents_candidates = list(set(depolarizingevents_candidates))

#     if plotting == 'on':
#         figure,axes = plt.subplots(2,1,sharex=True)
#         axes[0].plot(time_axis,voltage_recording,color='blue')
#         axes[0].plot(time_axis,voltage_filtered,color='black')
#         axes[0].plot(time_axis[::5],sgnl.decimate(voltage_recording,5),color='red')
#         axes[0].scatter(time_axis[derivativeconsistentlypositive_idcs],voltage_recording[derivativeconsistentlypositive_idcs],color='green')
#         axes[0].scatter(time_axis[depolarizingevents_candidates],voltage_recording[depolarizingevents_candidates],color='red')
#         axes[0].set_ylabel('voltage (mV)')
#         axes[0].set_title('voltage trace (black: smoothed)')

#         axes[1].plot(time_axis,voltage_filtered_derivative,color='black')
#         axes[1].scatter(time_axis[derivativeconsistentlypositive_idcs],
#                         voltage_filtered_derivative[derivativeconsistentlypositive_idcs],color='green')
#         axes[1].scatter(time_axis[depolarizingevents_candidates],
#                         voltage_filtered_derivative[depolarizingevents_candidates],color='red')
#         axes[1].set_xlabel('time (ms)')
#         axes[1].set_title('first derivative of voltage')

#     return depolarizingevents_candidates




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