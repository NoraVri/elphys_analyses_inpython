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

    ## init
    def __init__(self, singleneuron_name,
                 path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):
                    # path should be to a folder that contains data and results beloning to SingleNeuron's project.
        self.name = singleneuron_name
        self.path = path #folder containing: 1. folder(s) with raw data and 2. 'myResults' folder where analyses notes/results are stored.
        self.rawdata_path = []
        self.rawdata_recordingtype = None #raw data file(s) type; gets updated once data files are found
        self.rawdata_blocks = [] #all recorded raw data, as a list of neo block objects (one block per file)
        self.rawdata_readingnotes = {} #notes needed to exactly recreate all stored results

        self.depolarizing_events = pd.DataFrame()
        self.action_potentials = pd.DataFrame()
        self.subthreshold_oscillations = []
        self.input_resistance = []
        self.passive_decay = []

        self.get_singleneuron_rawdata()
        self.get_singleneuron_storedresults()


    def write_results(self):

        results_folder = [folder for folder in os.listdir(self.path) \
                          if folder.startswith('myResults')]

        if results_folder:

            results_path = self.path + '\\' + results_folder[0]
            os.chdir(results_path)

            if len(self.rawdata_readingnotes) > 0:
                with open(results_path +'\\' + self.name + \
                          '_rawdata_readingnotes', 'w') as file:
                    file.write(json.dumps(self.rawdata_readingnotes))

            if len(self.depolarizing_events) > 0:
                self.depolarizing_events.to_csv(self.name + '_depolarizing_events.csv')

            if len(self.action_potentials) > 0:
                self.action_potentials.to_csv(self.name + '_action_potentials.csv')

        else:

            print('no results folder found')



    def get_singleneuron_rawdata(self):
        """ This function uses singleneuron_name and path to find the
        raw data file(s) recorded from singleneuron.
        Once the right path(s) are found, it calls on the relevant files_reader (defined further below)
        to import the raw data in my standardized format using the Python/Neo framework.

        This function currently works for .abf-files (one folder per singleneuron)
        and pxp-files (one file per singleneuron).
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

            else:
                continue

            break

        if not self.rawdata_path:

            print('files matching neuron name exactly were not found')



    def rawdata_remove_nonrecordingchannel(self, file_origin, non_recording_channel):
    #this function takes a file name and the number of the channel
    #that singleneuron is not recorded on (1 or 2, following my home rig conventions),
    #and removes superfluous traces from the corresponding block's channel_indexes and segments
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

                if file_origin not in self.rawdata_readingnotes['nonrecordingchannels'].keys():
                    self.rawdata_readingnotes['nonrecordingchannels'].update({
                        file_origin: non_recording_channel
                    })



    def rawdata_remove_nonrecordingblock(self, file_origin):
        if not self.rawdata_readingnotes.get('nonrecordingblocks'):
            self.rawdata_readingnotes['nonrecordingblocks'] = []

        for i, block in enumerate(self.rawdata_blocks):
            if block.file_origin == file_origin:
                self.rawdata_blocks.__delitem__(i)
                if file_origin not in self.rawdata_readingnotes['nonrecordingblocks']:
                    self.rawdata_readingnotes['nonrecordingblocks'].append(file_origin)



    def get_singleneuron_storedresults(self):

        resultsfilespaths_list = []

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


        if self.rawdata_readingnotes:

            if self.rawdata_readingnotes.get('nonrecordingchannels'):

                for filename, channelno in \
                        self.rawdata_readingnotes['nonrecordingchannels'].items():

                    self.rawdata_remove_nonrecordingchannel(filename, channelno)

            if self.rawdata_readingnotes.get('nonrecordingblocks'):

                for filename in self.rawdata_readingnotes['nonrecordingblocks']:

                    self.rawdata_remove_nonrecordingblock(filename)



    # %% functions for quickly seeing things about the raw data:
    def get_blocknames(self,printing = 'on'):
        "returns the (file)names of all the blocks of singleneuron, and returns them as a list."
        blocks_list = [block.file_origin for block in self.rawdata_blocks]

        if printing == 'on':

            print(blocks_list)

        return blocks_list



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
    def get_depolarizingevents_fromRawData(self, **kwargs):
        self.rawdata_readingnotes['getdepolarizingevents_settings'] = kwargs

        all_actionpotentials, all_depolarizations = snafs.make_depolarizingevents_measures_dictionaries()
        for block in self.rawdata_blocks:
            for i, segment in enumerate(block.segments):
                (segment_actionpotentials,
                 segment_subthresholddepolarizations) = snafs.get_depolarizingevents(
                                                            segment,
                                                            **kwargs)

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

                for key in all_actionpotentials:
                    all_actionpotentials[key] += segment_actionpotentials[key]
                for key in all_depolarizations:
                    all_depolarizations[key] += segment_subthresholddepolarizations[key]

        self.depolarizing_events = pd.DataFrame(all_depolarizations)
        self.action_potentials = pd.DataFrame(all_actionpotentials)



# %% functions for plotting analysis results
    def plot_singledepolevents_withmeasures(self, conditions_series):

        events_forplotting = self.depolarizing_events.loc[conditions_series]

        uniqueblocks_nameslist = list(set(events_forplotting['file_origin']))

        allblocks_nameslist = self.get_blocknames(printing = 'off')


        for block_name in uniqueblocks_nameslist:

            rawdata_block = self.rawdata_blocks[allblocks_nameslist.index(block_name)]
            block_events = events_forplotting.loc[
                events_forplotting['file_origin'] == block_name
                ]

            unique_vtraces = list(set(block_events['segment_idx']))


            for vtrace_idx in unique_vtraces:

                trace_events = block_events.loc[
                    block_events['segment_idx'] == vtrace_idx
                    ]

                vtrace = rawdata_block.segments[vtrace_idx].analogsignals[0]

                sampling_frequency = float(vtrace.sampling_rate)

                sampling_period_inms = float(vtrace.sampling_period) * 1000

                vtrace = np.squeeze(np.array(vtrace))

                edtrace, _, _ = snafs.apply_filters_torawdata(vtrace,
                                                        oscfilter_lpfreq=20,
                                                        noisefilter_hpfreq=3000,
                                                        sampling_frequency=sampling_frequency,
                                                        plot='off')


                for event_idx, event_measures in trace_events.iterrows():

                    plot_startidx = event_measures['baselinev_idx'] - int(5/sampling_period_inms)

                    figure, axes = plt.subplots(1,2,sharex='all', num=event_idx)
                    plt.suptitle(block_name + ' segment' + str(vtrace_idx))

                    plots.plot_single_event(vtrace, sampling_period_inms, axes[0],
                      plot_startidx, plotwindow_inms = 40,
                      linecolor = 'blue',
                      label = 'raw V',
                      measures_dict = plots.make_measuresdict_for_subthresholdevent(
                                                        event_measures,'raw')
                                            )
                    axes[0].set_ylabel('voltage (mV)')

                    plots.plot_single_event(edtrace, sampling_period_inms, axes[1],
                                            plot_startidx, plotwindow_inms=40,
                                            linecolor='black',
                                            label='event-detect trace',
                                            measures_dict=plots.make_measuresdict_for_subthresholdevent(
                                                        event_measures, 'edtrace')
                                            )




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