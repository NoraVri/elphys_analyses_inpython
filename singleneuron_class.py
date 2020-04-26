# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:14:57 2020

@author: neert
"""
# %% imports
import os
import re
import json
from igor import packed
from neo import io
from neo.core import Block, Segment, ChannelIndex
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# imports of functions I wrote
import singleneuron_plotting_functions as plots
import singleneuron_analyses_functions as snafs
# %%


class SingleNeuron:
    # init
    def __init__(self, singleneuron_name,
                 path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):

        self.name = singleneuron_name       # a unique name, that appears literally on all raw data files recorded for this singleneuron
        self.path = path                    # folder containing: 1. folder(s) with raw data and 2. 'myResults' folder where analyses notes/results are stored.
        self.rawdata_path = []              # gets updated with the exact filepath leading to singleneuron's raw data files once they are found.
        self.rawdata_recordingtype = None   # raw data file(s) type; gets updated once data files are found.
        self.rawdata_blocks = []            # all recorded raw data, as a list of Neo block objects
                                            # the readingnotes-dictionary contains all default kwargs settings, for each of the singleneuron analyses class-methods.
        self.rawdata_readingnotes = {
            'getdepolarizingevents_settings': {
                'min_depolspeed': 0.1,
                'min_depolamp': 0.2,
                'peakwindow': 5,
                'eventdecaywindow': 40,
                'noisefilter_hpfreq': 3000,
                'oscfilter_lpfreq': 20,
                'plot': 'off'
            }
        }                                   # notes are updated with non-default kwargs needed to exactly recreate analyses results inside each method.
                                            # the objects containing analyses results are updated
                                            # inside the method that gets them, or from stored results.
        self.depolarizing_events = pd.DataFrame()
        self.action_potentials = pd.DataFrame()
        self.subthreshold_oscillations = []
        self.input_resistance = []
        self.passive_decay = []
        self.get_singleneuron_rawdata()
        self.get_singleneuron_storedresults()



    def write_results(self):
        """
        this function saves all analysis results belonging to the singleneuron instance
        to a folder on path labeled 'myResults'.
        Each results-table is stored in a separate .csv file, and the parameter values
        used to get them (stored in self.rawdata_readingnotes) are stored as a .json.
        """
        results_folder = [folder for folder in os.listdir(self.path)
                          if folder.startswith('myResults')]

        if results_folder:
            results_path = self.path + '\\' + results_folder[0]
            os.chdir(results_path)

            if len(self.rawdata_readingnotes) > 0:
                with open(results_path + '\\' + self.name +
                          '_rawdata_readingnotes', 'w') as file:
                    file.write(json.dumps(self.rawdata_readingnotes))

            if len(self.depolarizing_events) > 0:
                self.depolarizing_events.to_csv(self.name + '_depolarizing_events.csv')

            if len(self.action_potentials) > 0:
                self.action_potentials.to_csv(self.name + '_action_potentials.csv')

            print('results have been saved.')

        else:
            print('no results folder found')



    def get_singleneuron_rawdata(self):
        """ This function uses singleneuron_name and path to find the
        raw data file(s) recorded from singleneuron.
        Once the right path is found, it calls on the relevant files_reader (defined further below)
        to import the raw data in my standardized format using the Python/Neo framework.

        This function currently works for .abf-files (one folder per singleneuron)
        and pxp-files (one file per singleneuron; each file has an internal folder-structure).
        """
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
                print('this code is under construction')

            else:
                continue

            break

        if not self.rawdata_path:
            print('files matching neuron name exactly were not found')



    def rawdata_remove_nonrecordingchannel(self, file_origin, non_recording_channel):
        """ This function takes the name of a file/block and the number of the recording channel-set (voltage and current)
        on which singleneuron is not recorded.
        It returns self.rawdata_blocks with the superfluous traces removed from the relevant file,
        and updates rawdata_readingnotes accordingly.
        """
        if not self.rawdata_readingnotes.get('nonrecordingchannels'):
            self.rawdata_readingnotes['nonrecordingchannels'] = {}

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
                else: print('input valid channel-set number: 1 or 2')

                if file_origin not in self.rawdata_readingnotes['nonrecordingchannels'].keys():
                    self.rawdata_readingnotes['nonrecordingchannels'].update({
                        file_origin: non_recording_channel
                    })



    def rawdata_remove_nonrecordingblock(self, file_origin):
        """ This function takes the name of a recording file/block as input,
        and returns self.rawdata_blocks without the recording by that name.
        rawdata_readingnotes get updated with the names of the blocks that are removed.
        """
        if not self.rawdata_readingnotes.get('nonrecordingblocks'):
            self.rawdata_readingnotes['nonrecordingblocks'] = []

        for i, block in enumerate(self.rawdata_blocks):
            if block.file_origin == file_origin:
                self.rawdata_blocks.__delitem__(i)
                if file_origin not in self.rawdata_readingnotes['nonrecordingblocks']:
                    self.rawdata_readingnotes['nonrecordingblocks'].append(file_origin)



    def get_singleneuron_storedresults(self):
        """ This function finds any files in the 'myResults' folder bearing singleneuron's name,
        and adds their contents to the relevant containers on this instance of singleneuron.
        """
        resultsfilespaths_list = []  # getting a list of paths to each of the relevant results files
        for folder in os.listdir(self.path):
            if folder.startswith('myResults'):
                resultsfolder_path = self.path + '\\' + folder

                for path in os.listdir(resultsfolder_path):
                    if self.name in path:
                        resultsfilespaths_list.append(
                            resultsfolder_path + '\\' + path)

        if resultsfilespaths_list:
            for path in resultsfilespaths_list:

                if 'rawdata_readingnotes' in path:
                    with open(path, 'r') as file:
                        self.rawdata_readingnotes = json.loads(file.read())

                if 'depolarizing_events' in path:
                    self.depolarizing_events = pd.read_csv(path)

                if 'action_potentials' in path:
                    self.action_potentials = pd.read_csv(path)

                if 'subthreshold_oscillations' in path:
                    self.subthreshold_oscillations = {}

                if 'input_resistance' in path:
                    self.input_resistance = {}

                if 'passive_decay' in path:
                    self.passive_decay = {}

        if self.rawdata_readingnotes.get('nonrecordingchannels'):
            for filename, channelno in \
                    self.rawdata_readingnotes['nonrecordingchannels'].items():
                self.rawdata_remove_nonrecordingchannel(filename, channelno)

        if self.rawdata_readingnotes.get('nonrecordingblocks'):
            for filename in self.rawdata_readingnotes['nonrecordingblocks']:
                self.rawdata_remove_nonrecordingblock(filename)



# %% functions for quickly seeing things about the raw data

    def get_blocknames(self, printing='on'):
        """ returns the (file)names of all the blocks of singleneuron as a list, and prints them.
        """
        blocks_list = [block.file_origin for block in self.rawdata_blocks]

        if printing == 'on':
            print(blocks_list)
        return blocks_list



    def plot_allrawdata(self):
        """plots all blocks of raw traces imported for singleneuron;
        one figure per block, separate subplots for each channel_index (voltage/current/aux).
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



# %% functions for analyzing raw data

# %% depolarizing events
    def get_depolarizingevents_fromRawData(self, **kwargs):
        """This function goes over all voltage-traces in all raw-data blocks, and returns
        two Pandas dataframes: one for action potentials, and one for subthreshold depolarizing events.
        Each dataframe contains a set of standard measures taken from each event, as well as
        all information needed to recover the location of the event in the original data trace.
        Default values for function parameters are read in from rawdata_readingnotes, and are
        updated there if non-default kwargs are used.
        """
        for key, value in kwargs.items():
            if key in self.rawdata_readingnotes['getdepolarizingevents_settings'].keys():
                self.rawdata_readingnotes['getdepolarizingevents_settings'][key] = value

        # initializing empty measures-dictionaries
        all_actionpotentials, all_depolarizations = snafs.make_depolarizingevents_measures_dictionaries()
        # getting all events: looping over each block, and each trace within each block
        for block in self.rawdata_blocks:
            for i, segment in enumerate(block.segments):
                (segment_actionpotentials,
                 segment_subthresholddepolarizations) = snafs.get_depolarizingevents(
                                                            segment,
                                                            **self.rawdata_readingnotes['getdepolarizingevents_settings'])

                trace_origin = [block.file_origin]
                segment_idx = [i]
                segment_actionpotentials['file_origin'] = \
                    trace_origin * len(segment_actionpotentials['peakv'])
                segment_actionpotentials['segment_idx'] = \
                    segment_idx * len(segment_actionpotentials['peakv'])
                segment_subthresholddepolarizations['file_origin'] = \
                    trace_origin * len(segment_subthresholddepolarizations['peakv'])
                segment_subthresholddepolarizations['segment_idx'] = \
                    segment_idx * len(segment_subthresholddepolarizations['peakv'])

                # updating the measures-dictionaries with the results from a single trace
                for key in all_actionpotentials:
                    all_actionpotentials[key] += segment_actionpotentials[key]
                for key in all_depolarizations:
                    all_depolarizations[key] += segment_subthresholddepolarizations[key]

        self.depolarizing_events = pd.DataFrame(all_depolarizations).round(decimals=2)
        self.action_potentials = pd.DataFrame(all_actionpotentials).round(decimals=2)



# %% functions for plotting analysis results
    def plot_depolevents_overlayed(self, condition_series,
                                   plotwindow_start = -20, plotwindow_inms = 80,
                                   time_align_to = 'peakv_idx',
                                   do_baselining = False, do_normalizing = False):

        events_forplotting = self.depolarizing_events.loc[condition_series]
        uniqueblocks_nameslist = list(set(events_forplotting['file_origin']))
        allblocks_nameslist = self.get_blocknames(printing='off')

        figure, axis = plt.subplots(1,1, squeeze=True)
        plt.suptitle(self.name + 'depolarizing events')
        axis.set_title('raw voltage')

        for block_name in uniqueblocks_nameslist:

            rawdata_block = self.rawdata_blocks[allblocks_nameslist.index(block_name)]
            block_events = events_forplotting.loc[
                events_forplotting['file_origin'] == block_name
                ]

            unique_vtraces = list(set(block_events['segment_idx']))


            for vtrace_idx in unique_vtraces:

                trace_events = block_events.loc[block_events['segment_idx'] == vtrace_idx]
                vtrace = rawdata_block.segments[vtrace_idx].analogsignals[0]
                sampling_period_inms = float(vtrace.sampling_period) * 1000
                vtrace = np.squeeze(np.array(vtrace))

                for event_idx, eventmeasures in trace_events.iterrows():
                    plot_startidx = eventmeasures[time_align_to] + int((plotwindow_start / sampling_period_inms))
                    plots.plot_single_event(vtrace,sampling_period_inms,axis,
                                            plot_startidx,
                                            plotwindow_inms,
                                            linecolor = 'blue', label = None,
                                            eventmeasures_series = eventmeasures,
                                            do_baselining=do_baselining,
                                            do_normalizing=do_normalizing)
                    print('event no.' + str(event_idx) + ' plotted')





    def plot_individualdepolevents_withmeasures(self, condition_series,
                                                plotwindow_inms = 40,
                                                baselinewindow_inms = 5):
        """ This function takes a Pandas true/false series of the same length as self.depolarizing_events,
        and plots the subset of events for which the condition is True.
        Each event is plotted in a separate figure, with one subplot showing the
        raw voltage trace and one showing the event-detect trace (from which filtered data are substracted).
        In each subplot, the relevant measures taken from that event are marked.
        By default, events are plotted in a window of 40 ms, starting from 5ms before baselinev_idx.
        """
        events_forplotting = self.depolarizing_events.loc[condition_series]
        uniqueblocks_nameslist = list(set(events_forplotting['file_origin']))
        allblocks_nameslist = self.get_blocknames(printing = 'off')

        for block_name in uniqueblocks_nameslist:
            rawdata_block = self.rawdata_blocks[allblocks_nameslist.index(block_name)]
            block_events = events_forplotting.loc[
                events_forplotting['file_origin'] == block_name]
            unique_vtraces = list(set(block_events['segment_idx']))

            for vtrace_idx in unique_vtraces:
                plots.plot_singlesegment_individualdepolevents_withmeasures(
                        rawdata_block,
                        block_events,
                        vtrace_idx,
                        self.rawdata_readingnotes['getdepolarizingevents_settings'],
                        plotwindow_inms, baselinewindow_inms)



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