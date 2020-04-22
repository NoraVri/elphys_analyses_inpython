# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:14:57 2020

@author: neert
"""
# %% imports
import os
import re
from igor import packed
from neo import io
from neo.core import Block, Segment, ChannelIndex, AnalogSignal
import matplotlib.pyplot as plt
import numpy as np

#imports of functions I wrote
import singleneuron_plotting_functions as plots
import singleneuron_analyses_functions as snafs
# %%
class SingleNeuron:
    ## init
    def __init__(self, singleneuron_name,
                 path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):
    # path should be to a folder that contains data and results beloning to SingleNeuron's project.
    # path gets updated to absolute path of the folder/file containing the raw data recorded for singleneuron
        self.name = singleneuron_name
        self.path = path #folder containing folders with data and folder with 'myResults'
        self.rawdata_path = []
        self.rawdata_recordingtype = None #raw data file(s) type; gets updated once data files are found
        self.rawdata_blocks = [] #all recorded raw data, as a list of neo block objects (one block per file)

        self.depolarizing_events = {}
        self.action_potentials = {}
        self.subthreshold_oscillations = []
        self.input_resistance = []

        self.get_singleneuron_storeddata()

    ## other class-technical functions related to getting data
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
            elif (self.name + '_asibws') in os.listdir(subdirectory_path):
                self.rawdata_recordingtype = 'ibw'
                self.rawdata_path = subdirectory_path+'\\'+self.name+'_asibws'
                self.files_reader_ibw()
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

    def rawdata_remove_nonrecordingblock(self, file_origin):
        for i, block in enumerate(self.rawdata_blocks):
            if block.file_origin == file_origin:
                self.rawdata_blocks.__delitem__(i)
                #code that saves changes made goes here

    def get_rawdata_withadjustments(self, rawdata_reading_notes):
        all_raw_data = self.get_singleneuron_rawdata(self.name)
        for item in rawdata_reading_notes:
            all_raw_data = self.remove_nonrecordingchannel(all_raw_data,item[0],item[1])
        return all_raw_data

# %% functions for quickly seeing things about the raw data:
    def print_blocknames(self):
        "prints the (file)names of all the blocks of singleneuron."
        for block in self.rawdata_blocks:
             print(block.file_origin)

    def plot_allrawdata(self):
        """plots all blocks of raw traces imported for singleneuron;
        one figure per block, separate subplots for each channel_index.
        """
        for block in self.rawdata_blocks:
            plots.plot_block(block)
            plt.suptitle(self.name + ' raw data file ' + block.file_origin)

    def plot_block_byname(self, block_file_origin):
        """takes the name of the file from which the rawdata_block was created
        and plots only that block (separate subplots for each channel_index).
        """
        for block in self.rawdata_blocks:
            if block.file_origin == block_file_origin:
                plots.plot_block(block)
                plt.suptitle(self.name + ' raw data file ' + block.file_origin)


# %% functions for analyzing raw data:
# %% depolarizing events
    def get_depolarizingevents_fromRawData(self, plotting='off'):
        #TODO
        #write this whole thing up so that function defaults can be changed easily

        all_actionpotentials, all_depolarizations = snafs.make_depolarizingevents_measures_dictionaries()
        for block in self.rawdata_blocks:
            for i, segment in enumerate(block.segments):
                segment_actionpotentials, segment_subthresholddepolarizations = snafs.make_depolarizingevents_measures_dictionaries()
                (segment_actionpotentials,
                segment_subthresholddepolarizations) = snafs.get_depolarizingevents(
                                                            segment,
                                                            segment_actionpotentials,
                                                            segment_subthresholddepolarizations,
                                                            plot=plotting)

                trace_origin = block.file_origin + 'segment' + str(i)
                segment_actionpotentials['origin'] = \
                    [trace_origin] * len(segment_actionpotentials['peakv'])
                segment_subthresholddepolarizations['origin'] = \
                    [trace_origin] * len(segment_subthresholddepolarizations['peakv'])

                for key in all_actionpotentials:
                    all_actionpotentials[key] += segment_actionpotentials[key]
                for key in all_depolarizations:
                    all_depolarizations[key] += segment_subthresholddepolarizations[key]

        self.depolarizing_events = all_depolarizations
        self.action_potentials = all_actionpotentials

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

        By my conventions, all raw data recorded from a neuron is stored together
        in one pxp-file named SingleNeuron_name,
        and are recorded with 'consecutive-mode' either on or off. (Consecutive-mode 'on' corresponds to gap-free mode in pClamp, 'off' to fixed-length mode.)

        By the IgorPro and Neo/IgorIO conventions, one pxp-file contains subdirectories,
        where each subdirectory is read as analogsignals and contains traces from a single recording channel only.
        Correspondences between channel_indexes and segments are reconstructed from
            the subdirectory names, and are set up here so that the resulting rawdata_blocks list
            matches those obtained for pClamp data.
        """
        os.chdir(self.rawdata_path)
        file_name = self.rawdata_path+'\\'+self.name+'.pxp'
        reader = io.IgorIO(filename=file_name)
        _, filesystem = packed.load(file_name)
        #getting the names of the subderictories that contain recorded data
        subdirectories_list = []
        for key, value in filesystem['root'][b'SutterPatch'][b'Data'].items():
            key_converted = key.decode("utf-8")
            result = re.search(r'R([0-9]*)_S([0-9]*)_', key_converted)
            if result:
                subdirectories_list.append(key_converted)
        #get the number of unique runs, and import data as one block per run
        runs_list = [item[0:3] for item in subdirectories_list]
        unique_runs = list(set(runs_list))
        unique_runs.sort()
        #getting one block per run
        for run in unique_runs:
            block = self.get_bwgroup_as_block(run, subdirectories_list, reader=reader)
            self.rawdata_blocks.append(block)
            #segments and channel_indexes - indexes and units (on analogsignals)
            #block.file_origin as a unique pointer to the original raw data files

    def files_reader_ibw(self):
        print('function under construction')


    @staticmethod
    def get_bwgroup_as_block(run, subdirectories_list, reader):
        #getting the traces belonging to this run
        traces_names = [item for item in subdirectories_list if item.startswith(run)]
        #setting up an empty block with the right number of channel_indexes:
        block = Block()
        for i in range(len(traces_names)):
            chidx = ChannelIndex(index=i,channel_names=['Channel Group '+str(i)])
            block.channel_indexes.append(chidx)

        #importing the raw analogsignals for each channel
        vtrace_name = [name for name in traces_names if 'S1' in name][0]
        itrace_name = [name for name in traces_names if 'S2' in name][0]
        if len(traces_names) == 3:
            auxtrace_name = [name for name in traces_names if 'S3' in name][0]
            auxsignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+auxtrace_name)
        vsignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+vtrace_name)
        isignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+itrace_name)

        #setting up the block with right number of segments
        block.file_origin = vtrace_name[0:3] + vtrace_name[6:]
        if 'spontactivity' in block.file_origin: #by my conventions, spontactivity protocols are the only ones using 'continuous mode', and these never have a third recording channel.
            no_of_segments = 1
            vsignals = np.transpose(vsignals).reshape(-1,1)
            isignals = np.transpose(isignals).reshape(-1,1)
        else:
            no_of_segments = len(vsignals[1,:])

        for i in range(no_of_segments):
            segment = Segment(name=block.file_origin+str(i))
            block.segments.append(segment)

        #adding the raw data to the block's channel_indexes/segments
        for idx, segment in enumerate(block.segments):
            single_v_analogsignal = vsignals[:,idx].rescale('mV')
            segment.analogsignals.append(single_v_analogsignal)
            single_v_analogsignal.channel_index = block.channel_indexes[0]
            block.channel_indexes[0].analogsignals.append(single_v_analogsignal)

            single_i_analogsignal = isignals[:,idx].rescale('pA')
            segment.analogsignals.append(single_i_analogsignal)
            single_i_analogsignal.channel_index = block.channel_indexes[1]
            block.channel_indexes[1].analogsignals.append(single_i_analogsignal)

            if len(traces_names) == 3:
                single_aux_analogsignal = auxsignals[:,idx]
                segment.analogsignals.append(single_aux_analogsignal)
                single_aux_analogsignal.channel_index = block.channel_indexes[2]
                block.channel_indexes[2].analogsignals.append(single_aux_analogsignal)

        return block