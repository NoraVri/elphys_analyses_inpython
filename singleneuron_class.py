# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:14:57 2020

@author: neert
"""
# %% imports
import os
from neo import io
import matplotlib.pyplot as plt

#imports of functions I wrote
import singleneuron_plotting_functions as plots
import singleneuron_analyses_functions as snafs
# %%
class SingleNeuron:
     # init
    def __init__(self, singleneuron_name, path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):
    # path should be to a folder that contains data and results beloning to SingleNeuron's project.
    # path gets updated to absolute path of the folder/file containing the raw data recorded for singleneuron
        self.name = singleneuron_name
        self.path = path #folder containing folders with data and folder with 'myResults'
        self.rawdata_path = []
        self.rawdata_recordingtype = None #raw data file(s) type; gets updated once data files are found
        self.rawdata_blocks = [] #all recorded raw data, as a list of neo block objects (one block per file)

        self.depolarizing_events = {}
        self.subthreshold_oscillations = []
        self.input_resistance = []

        self.get_singleneuron_storeddata()

    def get_singleneuron_storeddata(self):
        """ This function determines whether a file carrying singleneuron_name
        is present in a folder with 'myResults';
        if yes, it will populate the class instance with results found in the file (if such results are present).
        """
        results_file_path = self.get_results_file_path()
        if results_file_path:
            data = {} #TODO: put code here that actually reads a file
            print('no actual results file opened')
            # if data.get('rawdata_reading_notes'):
            #     rawdata_reading_notes = data['rawdata_reading_notes']#or whichever other way this will be accessed
            #     #reading_notes will be a list of file_origin / nonrecording channel pairs
            #     #self.get_rawdata_withadjustments(self.name,rawdata_reading_notes)
            # else:
            #     #self.get_singleneuron_rawdata()
            # if data.get('depolarizing_events'):
            #     self.depolarizing_events = data['depolarizing_events']
            # if data.get('subthreshold_oscillations'):
            #     self.subthreshold_oscillations = data['subthreshold_oscillations']
            # if data.get('input_resistance'):
            #     self.input_resistance = data['input_resistance']
        else:
            self.get_singleneuron_rawdata()

    def get_results_file_path(self):
        results_file_path = None
        for folder in os.listdir(self.path):
            if folder.startswith('myResults'):
                for file in os.listdir(self.path+'\\'+folder):
                    if self.name in file:
                        results_file_path = self.path+'\\'+folder+'\\'+file
        return results_file_path

    def write_results_file(self):
        print('code under construction')

# %% functions for reading raw data into the class instance (actual read functions further below)
    def get_singleneuron_rawdata(self):
    # this function uses neuron_name to find a path to the raw data file(s) recorded for that neuron;
    # once the right path(s) are found, it calls on files_reader to read the data in as Neo blocks.
    # !! it currently only works for single-cell recordings in abf format !!
        for folder_name in os.listdir(self.path):
            subdirectory_path = self.path + '\\' + folder_name
            if self.name in os.listdir(subdirectory_path):
                self.rawdata_recordingtype = 'abf'
                self.rawdata_path = subdirectory_path+'\\'+self.name
                self.files_reader_abf()

            elif (self.name + '.pxp') in os.listdir(subdirectory_path):
                self.rawdata_recordingtype = 'pxp'
                self.rawdata_path = subdirectory_path
                self.files_reader_pxp()
            else:
                continue
            break
        if not self.rawdata_path:
            print('files matching neuron name exactly were not found')

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
                #code that saves changes made goes here

    def get_rawdata_withadjustments(self, rawdata_reading_notes):
        all_raw_data = self.get_singleneuron_rawdata(self.name)
        for item in rawdata_reading_notes:
            all_raw_data = self.remove_nonrecordingchannel(all_raw_data,item[0],item[1])
        return all_raw_data

# %% functions for plotting the raw data:
    def plot_allrawdata(self):
        """plots all blocks of raw traces imported for singleneuron;
        one figure per block, separate subplots for each channel_index.
        """
        for block in self.rawdata_blocks:
            plots.plot_block(block)
            plt.suptitle(self.name+' raw data file '+block.file_origin)

    def plot_block_byname(self, block_file_origin):
        """takes the name of the file from which the rawdata_block was created
        and plots only that block (separate subplots for each channel_index).
        """
        for block in self.rawdata_blocks:
            if block.file_origin == block_file_origin:
                plots.plot_block(block)
                plt.suptitle(self.name+' raw data file '+block.file_origin)


# %% functions for analyzing raw data:
# %% depolarizing events
    def get_depolarizingevents_fromRawData(self,
                                           min_event_amplitude = 0.5,
                                           peak_height = 0.15,
                                           plot='off'):
        """This function takes the raw data belonging to SingleNeuron (in the form of a SingleNeuron_RawData class instance)
        and peakfinding parameters (minimal amplitude and 'peak height').

        It outputs a dictionary containing the idcs of depolarizingevents_peaks by block&trace no,
        as well as the corresponding depolarizingevents_measures (amplitude, baseline_v, ...)
        """
        dictionary = {}
        for block in self.rawdata_blocks:
            for i, segment in enumerate(block.segments):
                depolarizingevents_peaksidcs = snafs.singlevoltagetrace_find_depolarizingevents_peaksidcs(
                                                segment,
                                                min_event_amplitude = min_event_amplitude,
                                                peakheight = peak_height,
                                                plotting = plot)
                depolarizingevents_peaksidcs_withmeasures = snafs.singlevoltagetrace_get_depolarizingevents_measures(
                                                            segment,
                                                            depolarizingevents_peaksidcs)

                dictionary.update(
                    {f'file {segment.file_origin} trace {str(i)}' :
                     {'peaks_indices' : depolarizingevents_peaksidcs_withmeasures,
                      'param_mineventamp' : min_event_amplitude,
                      'param_peakheight' : peak_height}
                     })

        self.depolarizing_events = dictionary
        #TODO: write code that returns this in a Pandas dataframe instead
        #use the dataframe to make nice plots of things, starting with events baselined
        #use Pandas to save the results in json format.

# %% the actual reading in of raw data from files
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
        os.chdir(self.rawdata_path)
        for file in os.listdir():
            if file.endswith(".abf"):
                print(self.rawdata_path+'file'+file)
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
        os.chdir(self.rawdata_path)
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