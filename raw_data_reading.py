# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:02:46 2020

@author: neert

This file defines a class for importing and looking at raw data I recorded, 
whether in pClamp or SutterPatch (or LabView - to be added)

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


# %% the SingleNeuron_RawData class definition:
class SingleNeuron_RawData:
    """
    This class imports raw data I recorded using my conventions, independent of 
    the software used for acquisition. 
    
    Some of the main differences between acquisition systems that my code accounts for:
        
    An singleneuron_name pxp-file recorded in SutterPatch corresponds to 
    an singleneuron_name folder containing all recorded files for a single neuron in pClamp.
    
    The 'continuous-mode' recording setting in SutterPatch corresponds to 
    'gap-free' mode in pClamp, though data have to be redimensioned (from matrix to single trace) 
    to look the same.
    
    Grouping of signals and assignment of channel_indexes
    is built into Neo/AxonIO to happen systematically per file,
    whereas Neo/IgorIO reads only individual traces and requires grouping into signals
    following my conventions.
    """
    
    # init
    def __init__(self, singleneuron_name, path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\\elphysData_recordedByMe"):
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
                self.rawdata_blocks = self.files_reader_abf()
            elif (self.name + '.pxp') in os.listdir(subdirectory_path):
                self.type = 'pxp'
                self.file_path = subdirectory_path
                self.rawdata_blocks = self.files_reader_pxp()
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
        
        reading abf-files using Neo.io:
        by my convention, files are recorded either in Gap-free mode or in Fixed-length mode.
        A file recorded in Gap-free mode contains a single set (V and I) of signals (of indefinite length)
        and is read by Neo.AxonIO as a single segment with two channel_indexes (V and I).
        A file recorded in Fixed-length mode contains multiple sets (V, I and possibly other) signals (of fixed length)
        and is read by Neo.AxonIO as consecutive segments, each with two or more channel_indexes (V, I and other [usually TTL]).
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
