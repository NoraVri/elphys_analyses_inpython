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
def get_depolarizingevents_and_measures(single_segment,plotting='on'):
    # getting all the relevant data from the Neo/Segment object
    single_voltage_trace = single_segment.analogsignals[0]
    time_axis = single_voltage_trace.times
    time_axis = time_axis.rescale('ms').magnitude
    voltage_recording = np.squeeze(single_voltage_trace)
    current_recording = np.squeeze(single_segment.analogsignals[1])

    sampling_rate = float(single_voltage_trace.sampling_rate) #!Make sure it's in Hz
    samples_per_ms = int(sampling_rate / 1000)
    #parameter settings
    downsamplingfactor_number = [1, 2, 5, 10, 20]#1000
    downsamplingfactor_inms = downsamplingfactor_number * samples_per_ms

    for downsamplingfactor in downsamplingfactor_inms:

        peakwindow_inms = 5 #window from detected depolarization to depolarization peak
        peakwindow = int(sampling_rate*peakwindow_inms/1000)
        currentwindow_inms = 100 #event peak within 100ms from DC current change is probably something else
        currentwindow = int(sampling_rate*currentwindow_inms/1000)
        peakheight = 0.1

        # getting a differentiated voltage trace from which fast depolarizations can be picked up
        voltage_downsampled = sgnl.decimate(voltage_recording, downsamplingfactor)
        time_axis_downsampled = time_axis[0::downsamplingfactor]
        voltage_downsampled_derivative = np.diff(voltage_downsampled,append=voltage_downsampled[-1]) #appending the last value keeps the derivative-trace the same length as the original
        voltage_downsampled_derivative = np.where(voltage_downsampled_derivative<0,0,voltage_downsampled_derivative) #replacing all negative values with 0
        voltage_downsampled_secondderivative = np.diff(voltage_downsampled_derivative,append=voltage_downsampled_derivative[-1])
        #using findpeaks on differentiated voltage to pick up candidates for depolarizing events
        depolarizingevents_idcs_indownsampledtrace = sgnl.find_peaks(voltage_downsampled_secondderivative,
                                                                      height=peakheight)[0]

        depolarizingevents_idcs = depolarizingevents_idcs_indownsampledtrace * downsamplingfactor

        #plotting the voltagetrace with detected peaks, and the difftrace to see that things went well
        if plotting == 'on':
            figure,axes = plt.subplots(2,1,sharex=True)
            axes[0].plot(time_axis,voltage_recording,color='blue')
            axes[0].plot(time_axis_downsampled,voltage_downsampled,color='black')
            #axes[0].scatter(time_axis[depolarizingevents_peaksidcs],voltage_recording[depolarizingevents_peaksidcs],color='red')
            axes[0].scatter(time_axis[depolarizingevents_idcs],voltage_recording[depolarizingevents_idcs],color='green')
            axes[0].set_ylabel('voltage (mV)')
            axes[0].set_title('voltage trace (black: smoothed)')
            axes[1].plot(time_axis_downsampled,voltage_downsampled_derivative,color='blue')
            axes[1].plot(time_axis_downsampled,voltage_downsampled_secondderivative,color='black')
            axes[1].scatter(time_axis_downsampled[depolarizingevents_idcs_indownsampledtrace],
                            voltage_downsampled_secondderivative[depolarizingevents_idcs_indownsampledtrace],color='green')
            axes[1].set_xlabel('time (ms)')
            axes[1].set_title('first (blue) and second (black) derivative of voltage')
            figure.suptitle(single_segment.file_origin+'downsamplingfactor='+str(downsamplingfactor))


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