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


Goals: 
1. creating a CellName_RawData object that reads in all raw data traces of that neuron
and stores them in homologous Neo objects regardless of which acquisition software was used.

Procedure when reading in pClamp data:
    - on a directory containing folders named CellName*, go into the relevant folder
        *if the folder contains a dual-patch recording, files have to be separated accordingly
    - get a list of all .abf-files in the folder
    - for each file, read the raw data using Neo.AxonIO to get one Block per file.

Procedure when reading in SutterPatch data:
    - in a folder containing files named CellName.pxp, find the relevant one
    - recreate the internal file structure to get paths to each data-containing subdirectory 
    - for each subdirectory, read the raw data using Neo.IgorIO 
    - create one Block per subdirectory, assigning* V and I to Segments and ChannelIndexes systematically
        *each subdirectory contains a single signal only, so relationships between signals have to be assigned 'manually'
        *to get GapFree traces from 'continuous recordings', traces have to be redimensioned. 


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
    
    # init
    def __init__(self, singleneuron_name, path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\\elphysData_recordedByMe"):
        self.name = singleneuron_name
        self.rawdata_blocks = []
        self.path = path
        self.type = None
        self.find_cell_path()
    
    # using neuron_name to navigate to the right raw data file(s), deducing whether it's gonna be abf or pxp/ibw)
    def find_cell_path(self):
        for item in os.listdir(self.path):
            for filename in os.listdir(self.path + '\\' + item):
                filename_split = filename.split('.')
                if len(filename_split) == 2 and filename_split[0] == self.name and filename_split[1] == 'pxp':
                    self.type = 'pxp'
                    
                elif len(filename_split) == 1 and filename_split[0] == self.name:
                    self.type = 'abf' 
                    
                else:
                    continue
                self.path += f'\\{item}\\{filename}'
                break
            
        if not self.type:
            print('No file matching filename found')
            exit
        elif self.type == 'abf':
            self.files_reader_abf()
        elif self.type == 'pxp':
            self.files_reader_pxp()
            
                
                
    
    # the actual reading in of raw data from files
    def files_reader_abf(self):
        """Takes a list of abf-file names; returns the recorded data as a list of neo blocks.
        filenames_list should be a list of abf-file names on the current directory path.
        
        reading abf-files using Neo.io:
        each abf-file contains either a single set (V and I) of GapFree signals, 
        or sets of Fixed-length signals.
        Information on segments and channel_indexes is read from the abf file directly by AxonIO. 
        """
        os.chdir(self.path)
        for file in os.listdir():
            if file.endswith(".abf"):
                reader = io.AxonIO(filename=file)
                
                block = reader.read()[0] #the general read function returns one block per file, with segments/channel_indexes assigned automatically.
                epoch_infos = reader._axon_info['dictEpochInfoPerDAC'] #returns some more metadata on stimulus waveforms
                block.annotate(epoch_infos=epoch_infos)
                
                self.rawdata_blocks.append(block)
    
    def files_reader_pxp(self):
        """Takes a list of pxp-file subdirectory names; returns the recorded data as a list of neo blocks.
        directorynames_list should be a list of pxp-subdirectory names existing inside the pxp-file.
        
        reading pxp-files using Neo.io: 
        each pxp-subdirectory contains a single signal (either V, I or other AuxIn);
        it is stored in a matrix form, with each row (?!!) in the matrix representing a consecutive segment.
        GapFree signals are constructed by redimensioning matrices of data acquired in 'continuous mode'.
        
        Information on segments and channel_indexes needs to be deduced from available metadata. Some things about subdirectory naming are systematic:
        Simultaneously acquired signals can be recognized by matching run indices (_R1_,_R2_,...)
        Signal names are systematic (_S1_ is V, _S2_ is C, _S3_ is AuxIn (!check correctness))
        Each subdirectory name starts with a protocol (P) number and name.
        
        """
        
