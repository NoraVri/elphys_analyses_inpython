# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:02:46 2020

@author: neert

This file defines a class for importing and looking at raw data I recorded,
whether in pClamp (or SutterPatch or LabView - under construction)

Right now it works for single-neuron recordings done in pClamp.



In my naming convention, a 'signal' is a set of traces that are recorded together;
in other words, a 'signal' is a single column of datapoints for each of the channels
active in the recording.

Each signal has at least two channel_indexes: the voltage (V) and current (I) channels.
Additional channel_indexes can be used for other signals, for example carrying TTL pulse times.

In my raw recordings, there are two types of files containing RawData signals:
"GapFree" and "Fixed-length" (following pClamp conventions).

A GapFree signal is acquired continuously; it is a single set of (V and I) traces of arbitrary length.
A Fixed-length signal set is acquired consecutively; it is a collection of traces all of the same length,
and usually has some manipulation occurring at a fixed time from the start of the signals.


Inventory of functions in this file/class:
    1. get_singleneuron_rawdata for finding the path to the raw data file(s) of the neuron
    2. files_reader - either abf or pxp, for actually reading the raw data and returning it in standardized format
    3. functions for plotting and displaying summary information.

2. writing functions for displaying useful summary information,
that can be called on the raw data contained in the class instance
    i] plotting: all raw data per file, all GapFree files in one window, specified files only, ...
    ii] displaying basic recording stats: start time, end time, total time recorded, V start & end, total time DC held, ...
"""
# %% imports
import os
from neo import io
#from neo.core import Block, Segment, ChannelIndex
import matplotlib.pyplot as plt
import numpy as np


# %% the SingleNeuron_RawData class definition:
class SingleNeuron_RawData:
    """
    This class imports raw data I recorded using my conventions, consistently,
    independent of the software used for acquisition.

    Grouping of signals and assignment of channel_indexes will always follow
    the conventions set by pClamp and Neo/AxonIO:
        - one block = one file, where a file is either:
            - one GapFree signal (of indefinite length; block has only one segment), or
            - a set of Fixed-length signals (all of the same length; block has multiple segments).
        - channel_indexes[0] is voltage in mV,
        - channel_indexes[1] is current in pA.
        - channel_indexes[n] where n>1 represent timing of stimuli applied (usually, TTL high for the duration of stimulus)

    It currently works only for data I acquired in pClamp.

    The rawdata_remove_nonrecordingchannel method is intended for clipping away
    any recording channels that are active but not actually recording from a neuron. (This happens a lot when double-patch attempts go awry.)

    The class also has attached plotting functions for displaying the raw data,
    in various configurations.
    """
    # init
    def __init__(self, singleneuron_name, path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):
    # path should be to a folder containing sub-folders containing raw data.
    # path gets updated to absolute path of the folder/file containing the raw data recorded for singleneuron
        self.name = singleneuron_name
        self.file_path = path #gets updated by get_singleneuron_rawdata
        self.type = None #raw data file(s) type; gets updated once data files are found
        self.rawdata_blocks = []
        self.get_singleneuron_rawdata()

    def get_singleneuron_rawdata(self):
    # this function uses neuron_name to find a path to the raw data file(s) recorded for that neuron;
    # once the right path(s) are found, it calls on files_reader to read the data in as Neo blocks.
    # !! it currently only works for single-cell recordings in abf format !!
        for folder_name in os.listdir(self.file_path):
            subdirectory_path = self.file_path + '\\' + folder_name
            if self.name in os.listdir(subdirectory_path):
                self.type = 'abf'
                self.file_path = subdirectory_path+'\\'+self.name
                self.files_reader_abf()

            elif (self.name + '.pxp') in os.listdir(subdirectory_path):
                self.type = 'pxp'
                self.file_path = subdirectory_path
                self.files_reader_pxp()
            else:
                continue
            break
        if not self.type:
            print('files matching neuron name exactly were not found')


    # the actual reading in of raw data from files
    def files_reader_abf(self):
        """This function changes the current directory to the folder containing
        the .abf raw data files recorded for singleneuron, and returns the
        recorded data as a list of neo blocks.

        By my conventions, all abf-files recorded from a neuron are stored together
        in a folder named SingleNeuron_name (or DoubleNeuron_name, but code does not deal with that for now.)
        and are recorded either in Gap-free or in Fixed-length mode.

        By the pClamp and Neo/AxonIO conventions, one abf-file is read as one block;
        each block has at least two channel_indexes where
            channel_index[0] is voltage in mV and
            channel_index[1] is current in pA;
        and Gap-free blocks have only one segment (of indefinite length) while
            Fixed-length blocks can have multiple segments (where each segment has the same length)
        """
        os.chdir(self.file_path)
        for file in os.listdir():
            if file.endswith(".abf"):
                reader = io.AxonIO(filename=file)

                block = reader.read()[0] #the general read function returns one block per file, with segments/channel_indexes assigned automatically.
                epoch_infos = reader._axon_info['dictEpochInfoPerDAC'] #returns some more metadata on stimulus waveforms
                block.annotate(epoch_infos=epoch_infos)

                self.rawdata_blocks.append(block)

    def files_reader_pxp(self):
        """This function changes the current directory to the folder containing
        the .pxp raw data file recorded for singleneuron, and returns the
        recorded data as a list of neo blocks.

        reading pxp-files using Neo.io:
        by my convention, files are recorded with 'consecutive-mode' on or off.
        each pxp-subdirectory contains a single signal (either V, I or other AuxIn);
        it is stored in a matrix form, with each row (?!!) in the matrix representing a consecutive segment.
        GapFree signals are constructed by redimensioning matrices of data acquired in 'continuous mode'.

        Information on segments and channel_indexes needs to be deduced from available metadata. Some things about subdirectory naming are systematic:
        Simultaneously acquired signals can be recognized by matching run indices (_R1_,_R2_,...)
        Signal names are systematic (_S1_ is V, _S2_ is C, _S3_ is AuxIn (!check correctness))
        Each subdirectory name starts with a protocol (P) number and name.

        """
        os.chdir(self.file_path)
        file_name = self.file_path+'\\'+self.name+'.pxp'
        reader = io.IgorIO(filename=file_name)
        # TODO:
        #first, read the experimentstructure file somehow and
        #reconstruct from it what the run names are

        #then, write code for going over the runs and group them same as pClamp files (with all the right annotations)
        # !!notes on things that are important for consistency:
            #segments and channel_indexes - indexes and units (on analogsignals)
            #block.file_origin as a unique pointer to the original raw data files
        print('this code is under construction')


    def rawdata_remove_nonrecordingchannel(self, file_origin, non_recording_channel):
    #this function takes a file name and the number of the channel
    #that singleneuron is not recorded on (1 or 2, following my home rig conventions),
    #and removes superfluous traces from the corresponding block's channel_indexes and segments
        for block in self.rawdata_blocks:
            if block.file_origin == file_origin:
                if non_recording_channel == 1:
                    block.channel_indexes[0:2] = []
                    for segment in block.segments:
                        segment.analogsignals[0:2] = []
                elif non_recording_channel == 2:
                    block.channel_indexes[2:4] = []
                    for segment in block.segments:
                        segment.analogsignals[2:4] = []

    @staticmethod
    def plot_block(block):
        """ takes a block and plots all analogsignals, one subplot per channel_index.
        """
        #getting the time axis all traces have in common
        time_axis = block.channel_indexes[0].analogsignals[0].times
        time_axis = time_axis.rescale('ms')
        #making one subplot per active recording channel
        nsubplots = len(block.channel_indexes)
        figure,axes = plt.subplots(nrows=nsubplots,ncols=1,sharex=True)
        for i in range(nsubplots):
            traces = np.transpose(np.squeeze(np.array(list(iter(
                                    block.channel_indexes[i].analogsignals)))))
            traces_unit = block.channel_indexes[i].analogsignals[0].units
            axes[i].plot(time_axis,traces)
            axes[i].set_xlabel('time (ms)')
            axes[i].set_ylabel(str(traces_unit))

    def plot_allrawdata(self):
        """plots all blocks of raw traces imported for singleneuron;
        one figure per block, separate subplots for each channel_index.
        """
        for block in self.rawdata_blocks:
            SingleNeuron_RawData.plot_block(block)
            plt.suptitle(self.name+' raw data file '+block.file_origin)

    def plot_block_byname(self,block_file_origin):
        """takes the name of the file from which the rawdata_block was created
        and plots only that block (separate subplots for each channel_index).
        """
        for block in self.rawdata_blocks:
            if block.file_origin == block_file_origin:
                SingleNeuron_RawData.plot_block(block)
                plt.suptitle(self.name+' raw data file '+block.file_origin)


    #TODO: plotting code that takes a specific subset of the list of blocks
