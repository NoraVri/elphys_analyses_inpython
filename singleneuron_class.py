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
from neo.core import Block, Segment, ChannelIndex, AnalogSignal
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import quantities as pq
import pandas as pd

# imports of functions I wrote
import singleneuron_plotting_functions as plots
import singleneuron_analyses_functions as snafs
# %%


class SingleNeuron:
    # initializing the class instance
    def __init__(self,
                 singleneuron_name,
                 path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive"):
        """
        singleneuron_name should be a unique identifier for the recording, with a date (YYYYMMDD) and letter (uppercase)
            that also appear on the raw data folder/file belonging to singleneuron.
        path should be to a folder containing:
            1. folder(s) containing folder(s) and/or file(s) of raw data
            2. a 'myResults' folder where analyses notes/results are stored and read from
            3. the 'myData_experiments_metadata' file.

        All raw data belonging to singleneuron are returned as a list of neo block objects.
        If files with singleneuron_name are found in the 'myResults' folder,
        raw data adjustments are applied based on notes found in rawdata_readingnotes,
        and objects containing analyses results are added to the class instance.

        Manipulations to the class instance can be saved (to be recreated on the next instance call)
        by calling the write_results()-method.
        """
        self.name = singleneuron_name
        self.path = path
        self.rawdata_path = ''  # gets updated with the exact filepath leading to singleneuron's raw data files.
        self.rawdata_recordingtype = None
        self.blocks = []

        self.experiment_metadata = pd.Series()
        self.rawdata_readingnotes = {}
        # Notes are updated with non-default kwargs needed to exactly recreate analyses results
        # inside the class method.

        self.depolarizing_events = pd.DataFrame()
        self.action_potentials = pd.DataFrame()
        self.subthreshold_oscillations = []
        self.input_resistance = []
        self.passive_decay = []
        self.get_singleneuron_rawdata()
        self.get_singleneuron_storedresults()

    # save all results currently present on the singleneuron instance
    def write_results(self):

        """
        this function saves all analysis results belonging to the singleneuron instance
        to a folder on path labeled 'myResults'.
        !! There should be only one folder with a name starting with 'myResults' on the path.
        Each results-table is stored in a separate .csv file, and the parameter values
        used to get them (as well as all other notes needed to exactly recreate the class instance
        stored in self.rawdata_readingnotes) are saved as a .json.
        """
        results_folder = [folder for folder in os.listdir(self.path)
                          if folder.startswith('myResults')]

        if results_folder:
            results_path = self.path + '\\' + results_folder[0]
            os.chdir(results_path)

            if len(self.rawdata_readingnotes) > 0:
                with open(results_path + '\\' + self.name +
                          '_rawdata_readingnotes.json', 'w') as file:
                    file.write(json.dumps(self.rawdata_readingnotes))

            if len(self.depolarizing_events) > 0:
                self.depolarizing_events.to_csv(self.name + '_depolarizing_events.csv')

            if len(self.action_potentials) > 0:
                self.action_potentials.to_csv(self.name + '_action_potentials.csv')

            print('results have been saved.')

        else:
            print('no results folder found')

    # get all raw electrophysiology recordings associated with singleneuron
    def get_singleneuron_rawdata(self):

        """ This function uses singleneuron_name and path to find the
        raw data file(s) recorded from singleneuron.
        Once the right path is found, it calls on the relevant files_reader (defined further below)
        to import the raw data in my standardized format using the Python/Neo framework.

        This function currently works for .abf-files (one folder per singleneuron)
        and pxp-files (one file per singleneuron; each file has an internal folder-structure).
        """
        neuronnamesplit = re.split("(\D)", self.name)
        experiment_date = int(neuronnamesplit[0])
        search_name = neuronnamesplit[0] + neuronnamesplit[1]
        experiments_metadata = pd.read_csv(self.path + '\\myData_experiments_metadata.csv')
        self.experiment_metadata = experiments_metadata.loc[
                                    experiments_metadata.date == experiment_date]

        for name in os.listdir(self.path):
            if len(name.split('.')) > 1:  # it's a file name
                continue

            else:
                subdirectory_path = self.path + '\\' + name
                searchitems_list = [item for item in os.listdir(subdirectory_path)
                                    if search_name in item]
                if len(searchitems_list) > 0:
                    for item in searchitems_list:

                        if len(item.split('.')) == 2 and item.split('.')[1] == 'pxp':
                            self.rawdata_recordingtype = 'pxp'
                            self.rawdata_path = subdirectory_path

                        elif len(item.split('.')) == 1:
                            subdirectory_path = subdirectory_path + '\\' + item
                            recording_files = [file for file in os.listdir(subdirectory_path)
                                               if file.endswith(('.ibw', '.abf', '.txt'))]
                            if len(recording_files) > 0:
                                file_type = recording_files[0].split(sep='.')[1]
                                self.rawdata_path = subdirectory_path
                                self.rawdata_recordingtype = file_type
                else:
                    continue

        if not self.rawdata_path:
            print('no files matching neuron name were found')

        elif self.rawdata_recordingtype == 'abf':
            self.files_reader_abf()

        elif self.rawdata_recordingtype == 'pxp':
            self.files_reader_pxp()

        elif self.rawdata_recordingtype == 'ibw':
            self.files_reader_ibw()

        elif self.rawdata_recordingtype == 'txt':
            self.files_reader_txt()

    # apply all 'cleaning notes' and get any stored analysis results for singleneuron
    def get_singleneuron_storedresults(self):
        """ This function finds any files in the 'myResults' folder bearing singleneuron's name,
        and adds their contents to the relevant containers on this instance of singleneuron.
        Also, any manipulations to clean the raw data are applied again based on the data
        stored in rawdata_readingnotes.
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
                    self.depolarizing_events = pd.read_csv(path, index_col=0)

                if 'action_potentials' in path:
                    self.action_potentials = pd.read_csv(path, index_col=0)

                if 'subthreshold_oscillations' in path:
                    self.subthreshold_oscillations = {}

                if 'input_resistance' in path:
                    self.input_resistance = {}

                if 'passive_decay' in path:
                    self.passive_decay = {}

        if self.rawdata_readingnotes.get('nonrecordingchannels'):
            for filename, dictionary in \
                    self.rawdata_readingnotes['nonrecordingchannels'].items():
                self.rawdata_remove_nonrecordingchannel(filename,
                                                        dictionary['nonrecordingchannel'],
                                                        dictionary['is_pairedrecording'])

        if self.rawdata_readingnotes.get('nonrecordingblocks'):
            for filename in self.rawdata_readingnotes['nonrecordingblocks']:
                self.rawdata_remove_nonrecordingblock(filename)

        if self.rawdata_readingnotes.get('nonrecordingtimeslices'):
            for filename, dictionary in \
                    self.rawdata_readingnotes['nonrecordingtimeslices'].items():
                self.rawdata_remove_nonrecordingsection(filename,
                                                        trace_start_t=dictionary['t_start'],
                                                        trace_end_t=dictionary['t_end'],
                                                        segment_idx=dictionary['segment_idx'])

    # remove a block that does not contain any actual data for singleneuron
    def rawdata_remove_nonrecordingblock(self, file_origin):
        """ This function takes the name of a recording file/block as input,
        and returns self.rawdata_blocks without the recording by that name.
        rawdata_readingnotes get updated with the names of the blocks that are removed.
        """
        if not self.rawdata_readingnotes.get('nonrecordingblocks'):
            nonrecordingblocks_list = []
            self.rawdata_readingnotes['nonrecordingblocks'] = nonrecordingblocks_list
        else:
            nonrecordingblocks_list = self.rawdata_readingnotes['nonrecordingblocks']

        for i, block in enumerate(self.blocks):
            if block.file_origin == file_origin:
                self.blocks.__delitem__(i)
                if file_origin not in nonrecordingblocks_list:
                    nonrecordingblocks_list.append(file_origin)
        self.rawdata_readingnotes['nonrecordingblocks'] = nonrecordingblocks_list

    # remove channels on which singleneuron is not recorded from a rawdata_block
    def rawdata_remove_nonrecordingchannel(self, file_origin,
                                           non_recording_channel,
                                           pairedrecording=False):
        """ This function takes the name of a file/block and
        the number of the recording channel-set (voltage and current)
        on which singleneuron is not recorded.
        It returns self.rawdata_blocks with the superfluous traces
        removed from the relevant file,
        and updates rawdata_readingnotes accordingly.
        """
        if not self.rawdata_readingnotes.get('nonrecordingchannels'):
            self.rawdata_readingnotes['nonrecordingchannels'] = {}

        for block in self.blocks:
            if block.file_origin == file_origin:
                if non_recording_channel == 1:
                    block.channel_indexes[0:2] = []
                    for segment in block.segments:
                        segment.analogsignals[0:2] = []
                elif non_recording_channel == 2:
                    block.channel_indexes[2:4] = []
                    for segment in block.segments:
                        segment.analogsignals[2:4] = []
                else:
                    print('input valid channel-set number: 1 or 2')

                if pairedrecording:
                    block.annotate(is_paired=True)

                if file_origin not in self.rawdata_readingnotes['nonrecordingchannels'].keys():
                    self.rawdata_readingnotes['nonrecordingchannels'].update({
                        file_origin: {'nonrecordingchannel': non_recording_channel,
                                      'is_pairedrecording': pairedrecording}
                    })

    # remove parts of individual traces where singleneuron is not yet/no longer being recorded
    def rawdata_remove_nonrecordingsection(self, file_origin,
                                           trace_start_t=None,
                                           trace_end_t=None,
                                           segment_idx=None):
        """ This function takes the name of the file/block from which a section is to be removed.
        If a start and/or end time (in s) are provided (one or the other has to be),
        segment_idx is assumed to be 0 (the single segment on blocks that have just one long trace)
        and the segment is adjusted to start and/or end at the new time(s).
        If a segment_idx is provided, this segment will be removed from the block.
        It returns self.rawdata_blocks with the superfluous data removed,
        and updates rawdata_readingnotes accordingly.
        """
        if not self.rawdata_readingnotes.get('nonrecordingtimeslices'):
            self.rawdata_readingnotes['nonrecordingtimeslices'] = {}

        if not isinstance(segment_idx, int):
            if trace_start_t:
                start_t = trace_start_t * pq.s
            if trace_end_t:
                end_t = trace_end_t * pq.s

            block_idx = self.get_blocknames(printing='off').index(file_origin)
            block = self.blocks[block_idx]

            if trace_start_t and not trace_end_t:
                segmentslice_tokeep = block.segments[0].time_slice(
                                        t_start=start_t)
            elif trace_end_t and not trace_start_t:
                segmentslice_tokeep = block.segments[0].time_slice(
                                        t_start=block.segments[0].t_start,
                                        t_stop=end_t)
            else:
                segmentslice_tokeep = block.segments[0].time_slice(
                                        t_start=start_t,
                                        t_stop=end_t)
            self.blocks[block_idx].segments[0] = segmentslice_tokeep
            for i, _ in enumerate(self.blocks[block_idx].channel_indexes):
                self.blocks[block_idx].channel_indexes[i].analogsignals[0] = segmentslice_tokeep.analogsignals[i]

        else:
            for block in self.blocks:
                if block.file_origin == file_origin:
                    block_idx = self.blocks.index(block)
                    self.blocks[block_idx].segments.remove(
                        self.blocks[block_idx].segments[segment_idx])
                    chidxs = self.blocks[block_idx].channel_indexes
                    for i, chidx in enumerate(chidxs):
                        analogsignals = chidx.analogsignals
                        del analogsignals[segment_idx]
                        chidx.analogsignals = analogsignals
                        self.blocks[block_idx].channel_indexes[i] = chidx

        if file_origin not in self.rawdata_readingnotes['nonrecordingtimeslices'].keys():
            self.rawdata_readingnotes['nonrecordingtimeslices'].update({
                file_origin: {'t_start': trace_start_t,
                              't_end': trace_end_t,
                              'segment_idx': segment_idx}
            })

    # note which blocks have special chemicals applied
    def rawdata_note_chemicalinbath(self, *block_identifiers):
        """
        """
        # checking that information on chemicals applied is present in the experimentday metadata
        if self.experiment_metadata.empty or self.experiment_metadata.specialchemicals_type.empty:
            print('no notes on chemicals applied have been found.')
        else:
            # adding 'chemicals applied' to the rawdata reading notes
            if self.rawdata_readingnotes.get('chemicalsapplied_blocks'):
                blockswithchemicals_list = self.rawdata_readingnotes['chemicalsapplied_blocks']
            else:
                blockswithchemicals_list = []
                self.rawdata_readingnotes['chemicalsapplied_blocks'] = blockswithchemicals_list
            # adding any blocks containing the identifier(s) to the list of blocks with chemicals applied
            blocknames_list = self.get_blocknames(printing='off')
            for identifier in block_identifiers:
                chemicalsapplied_blocks = [block for block in blocknames_list
                                           if identifier in block]
                for block in chemicalsapplied_blocks:
                    if block not in blockswithchemicals_list:
                        blockswithchemicals_list.append(block)
            self.rawdata_readingnotes['chemicalsapplied_blocks'] = blockswithchemicals_list

# %% functions for plotting/seeing stuff

    # getting a list of all block names
    def get_blocknames(self, get_subset=False, printing='on'):
        """ returns the (file)names of all the blocks of singleneuron as a list, and prints them."""
        if get_subset is not False \
                and ('no' in get_subset or 'without' in get_subset):
            allblocks_list = [block.file_origin for block in self.blocks]
            if 'chemicalsapplied_blocks' in self.rawdata_readingnotes.keys():
                blocks_list = [block for block in allblocks_list
                               if block not in self.rawdata_readingnotes['chemicalsapplied_blocks']]
            else:
                blocks_list = allblocks_list
                print('no notes on chemicals applied were found; returning a list of all block names.')
        elif get_subset is not False \
                and 'chemicals' in get_subset:
            if 'chemicalsapplied_blocks' in self.rawdata_readingnotes.keys():
                blocks_list = self.rawdata_readingnotes['chemicalsapplied_blocks']
            else:
                blocks_list = []
                print('no notes on chemicals applied were found; returning an empty list.')
        else:
            blocks_list = [block.file_origin for block in self.blocks]

        if printing == 'on':
            print(blocks_list)
        return blocks_list

    # plotting all raw data, as recorded
    def plot_allrawdata(self, **kwargs):
        """plots all blocks of raw traces imported for singleneuron;
        one figure per block, separate subplots for each channel_index (voltage/current/aux).
        optional kwargs:
        events_to_mark='none', time_axis_unit='ms', segments_overlayed=True
        """
        for block in self.blocks:
            plots.plot_block(block, **kwargs)
            plt.suptitle(self.name + ' raw data file ' + block.file_origin)

    # plotting specific blocks, optionally with action potentials or depolarizing events marked
    def plot_blocks_byname(self, *block_file_origin, **kwargs):
        """takes the name(s) of the file from which the rawdata_block was created
        and plots only that/those block(s) (separate subplots for each channel_index).
        optional kwargs:
        events_to_mark='none', time_axis_unit='ms', segments_overlayed=True
        """
        blocknames_list = self.get_blocknames(printing='off')
        for block_name in block_file_origin:
            block = self.blocks[blocknames_list.index(block_name)]
            plots.plot_block(block, **kwargs)
            plt.suptitle(self.name + ' raw data file ' + block.file_origin)

    # plotting (subsets of) action potentials or depolarizing events, overlayed
    def plot_depolevents_overlayed(self, condition_series=pd.Series(),
                                   get_subthreshold_events=True,
                                   newplot_per_block=False, blocknames_list=None,
                                   colorby_measure='', color_lims=[],
                                   plt_title='',
                                   **kwargs):
        """ This function plots overlays of depolarizing events, either all in one plot
        or as one plot per rawdata_block present on the singleneuron class instance.
        By default, all detected events are plotted in a single plot; all blue lines
        representing the original raw recorded events.

        Optional inputs:
        condition_series: a Pandas True/False series (same length as depolarizingevents)
            marking a subset of events for plotting.
        newplot_per_block: if True, a new figure will be drawn for each rawdata_block.
        [blocknames_list]: a list of block names (== block.file_origin) marking a subset of blocks for event-plotting.
        'colorby_measure': key of a depolarizingevents_measure to color-code the lines by.
        [color_lims]: [minvalue, maxvalue] of the colorbar. If not provided, min and max will be inferred from the data.
        'plt_title': default='', string giving the title of the plot(s).
        'timealignto_measure': default='peakv_idx', but can be changed to any key representing a time measurement.
        prealignpoint_window_inms: default=10, length of the timewindow for plotting before the align-point.
        total_plotwindow_inms: default=50, total length of the window for plotting the events.
        get_measures_type: default='raw', if it's something else the event-detect trace will be recreated and used.
        do_baselining: if True, baselinev is subtracted from the event-trace.
        do_normalizing: if True, the event-trace is divided by amplitude.
        """
        # selecting the (subset of) events for plotting:
        if get_subthreshold_events and not condition_series.empty:
            events_for_plotting = self.depolarizing_events.loc[condition_series]
        elif not condition_series.empty:
            events_for_plotting = self.action_potentials.loc[condition_series]
        elif get_subthreshold_events:
            events_for_plotting = self.depolarizing_events
        else:
            events_for_plotting = self.action_potentials
        # if required, set colorbar limits
        # (if newplot_per_block, figure colorbar is handled inside plot_singleblock_events function)
        if colorby_measure and len(color_lims) == 0 and not newplot_per_block:
            color_lims = [events_for_plotting[colorby_measure].min(),
                          events_for_plotting[colorby_measure].max()]
        if colorby_measure and len(color_lims) == 2 and not newplot_per_block:
            colormap, cm_normalizer = plots.get_colors_forlineplots(colorby_measure,
                                                                    color_lims)
        # get the (subset of) blocks for which events are to be plotted:
        unique_blocks_forplotting = set(events_for_plotting['file_origin'])
        if blocknames_list:
            unique_blocks_forplotting = unique_blocks_forplotting.intersection(set(blocknames_list))
        unique_blocks_forplotting = list(unique_blocks_forplotting)
        allblocks_nameslist = self.get_blocknames(printing='off')

        # plotting events:
        if newplot_per_block:
            for block_name in unique_blocks_forplotting:
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]
                # making a new plot for each block, getting the figure and axis handles out
                figure, axis = plots.plot_singleblock_events(
                    rawdata_block,
                    block_events,
                    self.rawdata_readingnotes['getdepolarizingevents_settings'],
                    colorby_measure=colorby_measure,
                    color_lims=color_lims,
                    **kwargs)
                # setting axis properties and figure title
                axis_title = 'voltage'
                if 'get_measures_type' in kwargs.keys() and not kwargs['get_measures_type'] == 'raw':
                    axis_title += ' event-detect trace, '
                if 'do_baselining' in kwargs.keys() and kwargs['do_baselining']:
                    axis_title += ' baselined'
                if 'do_normalizing' in kwargs.keys() and kwargs['do_normalizing']:
                    axis_title += ' normalized'
                axis.set_title(axis_title)
                figure.suptitle(self.name + block_name + plt_title)

        else:
            # initializing the figure:
            figure, axis = plt.subplots(1, 1, squeeze=True)
            plt.suptitle(self.name + plt_title)
            for block_name in unique_blocks_forplotting:
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]

                plots.plot_singleblock_events(rawdata_block, block_events,
                                              self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                              axis_object=axis,
                                              colorby_measure=colorby_measure,
                                              color_lims=color_lims,
                                              **kwargs)
            # setting axis properties and figure title
            axis_title = 'voltage'
            if 'get_measures_type' in kwargs.keys() and not kwargs['get_measures_type'] == 'raw':
                axis_title += ' event-detect trace '
            if 'do_baselining' in kwargs.keys() and kwargs['do_baselining']:
                axis_title += ' baselined'
            if 'do_normalizing' in kwargs.keys() and kwargs['do_normalizing']:
                axis_title += ' normalized'
            axis.set_title(axis_title)
            if colorby_measure:
                figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer,cmap=colormap),
                                label=colorby_measure)

    # plotting (subsets of) action potentials or depolarizing events, individually with measures marked
    def plot_individualdepolevents_withmeasures(self, condition_series=pd.Series(),
                                                get_subthreshold_events=True,
                                                plotwindow_inms=40,
                                                prebaselinewindow_inms=5):
        """ This function plots the subset of events for which the condition is True,
        each a separate figure. By default, subthreshold events are plotted,
        with one subplot showing the raw voltage trace and one showing the
        event-detect trace (with oscillations and noise substracted).
        If get_subthreshold_events is False, action potentials are plotted.
        In each subplot, the relevant measures taken from that event are marked.

        Optional inputs:
        condition_series: a Pandas True/False series (same length as depolarizingevents)
                          marking a subset of events for plotting.
        plotwindow_inms: default=40, the total length of the plot window.
        baselinewindow_inms: default=5, the length of the plot window before baselinev_idx.
        """
        if get_subthreshold_events and not condition_series.empty:
            events_forplotting = self.depolarizing_events.loc[condition_series]
        elif not condition_series.empty:
            events_forplotting = self.action_potentials.loc[condition_series]
        elif get_subthreshold_events:
            events_forplotting = self.depolarizing_events
        else:
            events_forplotting = self.action_potentials
        uniqueblocks_nameslist = list(set(events_forplotting['file_origin']))
        allblocks_nameslist = self.get_blocknames(printing='off')

        for block_name in uniqueblocks_nameslist:
            rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
            block_events = events_forplotting.loc[
                events_forplotting['file_origin'] == block_name]
            unique_vtraces = list(set(block_events['segment_idx']))

            for vtrace_idx in unique_vtraces:
                plots.plot_singlesegment_events_individually_withmeasures(
                        get_subthreshold_events,
                        rawdata_block,
                        block_events,
                        vtrace_idx,
                        self.rawdata_readingnotes['getdepolarizingevents_settings'],
                        plotwindow_inms, prebaselinewindow_inms)

    def plot_eventdetecttraces_forsegment(self, block_idx, segment_idx,
                                          return_dicts=False,
                                          **kwargs):
        segment = self.blocks[block_idx].segments[segment_idx]

        if not self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            self.rawdata_readingnotes['getdepolarizingevents_settings'] = {
                                                            'min_depolspeed': 0.1,
                                                            'min_depolamp': 0.2,
                                                            'peakwindow': 5,
                                                            'spikewindow': 40,
                                                            'spikeahpwindow': 150,
                                                            'noisefilter_hpfreq': 3000,
                                                            'oscfilter_lpfreq': 20,
                                                            'ttleffect_windowinms': None,
                                                            'plot': 'off'}

        stored_kwargs = self.rawdata_readingnotes['getdepolarizingevents_settings']

        for key, value in kwargs.items():
            if key in stored_kwargs.keys():
                stored_kwargs[key] = value

        stored_kwargs['plot'] = 'on'
        apsdict, depolsdict = snafs.get_depolarizingevents(
            segment,
            **stored_kwargs)
        stored_kwargs['plot'] = 'off'

        if return_dicts:
            return apsdict, depolsdict

# %% functions for analyzing raw data

# %% depolarizing events (subthreshold ones and action potentials)

    # getting the action_potentials and depolarizing_events DataFames
    def get_depolarizingevents_fromrawdata(self, **kwargs):
        """This function goes over all voltage-traces in all raw-data blocks, and returns
        two Pandas dataframes: one for action potentials, and one for subthreshold depolarizing events.
        Each dataframe contains a set of standard measures taken from each event, as well as
        all information needed to recover the location of the event in the original data trace.
        Default values for function parameters are read in from rawdata_readingnotes, and are
        updated there if non-default kwargs are used.

        Inputs (all optional):
        'min_depolspeed': minimal speed of increase (mV/ms) for detecting depolarizations.
        'min_depolamp': minimal amplitude from baseline to a possible event peak.
        'peakwindow': maximal time between a detected depolarization and an event peak (in ms),
          and time after peak within which voltage should not get higher, and decay again to <80% of its amplitude.
        'spikewindow': time after peak within which half-width, threshold and whole-width are expected to occur.
        'spikeahpwindow': time after threshold-width end within which AHP end is expected to occur.
        'noisefilter_hpfreq': cutoff frequency for high-pass filter applied to reduce noise.
        'oscfilter_lpfreq': cutoff frequency for low-pass filter applied to get sub-treshold STOs only.
        'ttleffect_windowinms': time after TTL pulse turns off but still has effects working through.
        ('plot': if 'on', will plot each voltage trace, with scatters for baselinevs and peakvs.)

        !! This function can take quite a long time to run for neuron recordings longer than just a few minutes.
        The recommended workflow is to use plot_eventdetecttraces_forsegment() on a (time_slice of a)
        single, representative segment first to find good settings for kwargs.
        !! Once satisfied with the results, run self.write_results() to save the data !!
        """
        if not self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            self.rawdata_readingnotes['getdepolarizingevents_settings'] = {
                                                            'min_depolspeed': 0.1,
                                                            'min_depolamp': 0.2,
                                                            'peakwindow': 5,
                                                            'spikewindow': 40,
                                                            'spikeahpwindow': 150,
                                                            'noisefilter_hpfreq': 3000,
                                                            'oscfilter_lpfreq': 20,
                                                            'ttleffect_windowinms': None,
                                                            'plot': 'off'}

        for key, value in kwargs.items():
            if key in self.rawdata_readingnotes['getdepolarizingevents_settings'].keys():
                self.rawdata_readingnotes['getdepolarizingevents_settings'][key] = value

        # initializing empty measures-dictionaries
        all_actionpotentials, all_depolarizations = snafs.make_depolarizingevents_measures_dictionaries()
        # getting all events: looping over each block, and each trace within each block
        for block in self.blocks:
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

# %% the actual reading in of raw data from files

    # reading .abf files
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
                reader = io.AxonIO(filename=file)
                # for abf's, the general read function returns one block per file
                # with segments/channel_indexes assigned automatically and units scaled to mV/pA where relevant.
                block = reader.read()[0]
                epoch_infos = reader._axon_info['dictEpochInfoPerDAC'] #returns some more metadata on stimulus waveforms
                block.annotate(epoch_infos=epoch_infos)

                self.blocks.append(block)

    # reading .pxp files
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
        # getting the names of the subderictories that contain recorded data
        subdirectories_list = []
        for key, value in filesystem['root'][b'SutterPatch'][b'Data'].items():
            key_converted = key.decode("utf-8")
            result = re.search(r'R([0-9]*)_S([0-9]*)_', key_converted)
            if result:
                subdirectories_list.append(key_converted)
        # get the number of unique runs, and import data as one block per run
        runs_list = [item[0:3] for item in subdirectories_list]
        unique_runs = list(set(runs_list))
        unique_runs.sort()
        # getting one block per run
        for run in unique_runs:
            block = self.get_bwgroup_as_block(run, subdirectories_list, reader=reader)
            self.blocks.append(block)

    # reading .ibw files
    def files_reader_ibw(self):
        # go to the folder containing the raw data and get a list of ibw files
        os.chdir(self.rawdata_path)
        ibwfiles_list = [filename for filename in os.listdir() if filename.endswith('.ibw')]
        # get a list of unique runs (each run should have multiple files that together will be one block)
        runs_list = [filename[0:3] for filename in ibwfiles_list]
        unique_runs = list(set(runs_list))
        unique_runs.sort()
        for run in unique_runs:
            # get the names of all the files associated with this run
            run_traces = [filename for filename in ibwfiles_list if filename.startswith(run)]
            vtrace_name = [name for name in run_traces if 'S1' in name][0]
            itrace_name = [name for name in run_traces if 'S2' in name][0]
            if len (run_traces) == 3:
                auxtrace_name = [name for name in run_traces if 'S3' in name][0]
                auxsignals_reader = io.IgorIO(filename=auxtrace_name)
                auxsignals = auxsignals_reader.read_analogsignal()
            vtrace_reader = io.IgorIO(filename=vtrace_name)
            vsignals = vtrace_reader.read_analogsignal()
            itrace_reader = io.IgorIO(filename=itrace_name)
            isignals = itrace_reader.read_analogsignal()

            # setting up an empty block with the right number of channel_indexes:
            block = Block()
            for i in range(len(run_traces)):
                chidx = ChannelIndex(index=i, channel_names=['Channel ' + str(i)])
                block.channel_indexes.append(chidx)

            # setting up the block with right number of segments
            block.file_origin = vtrace_name[0:3] + vtrace_name[6:]
            if 'spontactivity' in block.file_origin:  # by my conventions, spontactivity protocols are the only ones using 'continuous mode', and these never have a third recording channel.
                no_of_segments = 1
                vsignals = np.transpose(vsignals).reshape(-1, 1)
                isignals = np.transpose(isignals).reshape(-1, 1)
            else:
                no_of_segments = len(vsignals[1, :])

            for i in range(no_of_segments):
                segment = Segment(name=block.file_origin + str(i))
                block.segments.append(segment)

            # adding the raw data
            for idx, segment in enumerate(block.segments):
                single_v_analogsignal = vsignals[:, idx].rescale('mV')
                single_v_analogsignal.file_origin = block.file_origin
                segment.analogsignals.append(single_v_analogsignal)
                single_v_analogsignal.channel_index = block.channel_indexes[0]
                block.channel_indexes[0].analogsignals.append(single_v_analogsignal)

                single_i_analogsignal = isignals[:, idx].rescale('pA')
                single_i_analogsignal.file_origin = block.file_origin
                segment.analogsignals.append(single_i_analogsignal)
                single_i_analogsignal.channel_index = block.channel_indexes[1]
                block.channel_indexes[1].analogsignals.append(single_i_analogsignal)

                if len(run_traces) == 3:
                    single_aux_analogsignal = auxsignals[:, idx]
                    single_aux_analogsignal.file_origin = block.file_origin
                    segment.analogsignals.append(single_aux_analogsignal)
                    single_aux_analogsignal.channel_index = block.channel_indexes[2]
                    block.channel_indexes[2].analogsignals.append(single_aux_analogsignal)

            self.blocks.append(block)

    def files_reader_txt(self):
        os.chdir(self.rawdata_path)
        txtfiles_list = [filename for filename in os.listdir() if filename.endswith('.txt')]

        for datafile in txtfiles_list:
            print('currently processing file: ')
            # in my .txt-file data there are always just two recording channels: V and I
            # getting one block per file, with all the channel_indexes/segments/analogsignals
            block = Block()
            for i in range(2):
                chidx = ChannelIndex(index=i)
                block.channel_indexes.append(chidx)

            voltagesignals_list = []
            currentsignals_list = []
            with open(datafile, 'r') as file:
                firstline = file.readline()
                # in Dumper files, the first line gives the channels; in TrigIn files, it's the time axis
                if len(firstline) > 100:
                    file_data = pd.read_table(datafile, header=None)
                    sampling_interval = file_data.iloc[0,1] * pq.s
                    for i in range(1, len(file_data), 4):
                        current_analogsignal = AnalogSignal(file_data.iloc[i, :],
                                                            units=pq.nA,
                                                            sampling_period=sampling_interval)
                        current_analogsignal = current_analogsignal.rescale('pA')
                        current_analogsignal.file_origin = datafile
                        voltage_analogsignal = AnalogSignal(file_data.iloc[i + 1, :],
                                                            units=pq.mV,
                                                            sampling_period=sampling_interval)
                        voltage_analogsignal.file_origin = datafile

                        currentsignals_list.append(current_analogsignal)
                        voltagesignals_list.append(voltage_analogsignal)
                else:
                    file_data = pd.read_table(datafile, header=None, skiprows=2)
                    sampling_interval_str = file.readline()
                    sampling_interval = float(
                        re.split('\t', sampling_interval_str)[0]) * pq.ms
                    voltage_analogsignal = AnalogSignal(file_data.iloc[:, 0],
                                                        units=pq.mV,
                                                        sampling_period=sampling_interval)
                    voltage_analogsignal.file_origin = datafile
                    current_analogsignal = AnalogSignal(file_data.iloc[:, 1],
                                                        units=pq.pA,
                                                        sampling_period=sampling_interval)
                    current_analogsignal.file_origin = datafile

                    voltagesignals_list.append(voltage_analogsignal)
                    currentsignals_list.append(current_analogsignal)

            block.file_origin = datafile
            no_of_segments = len(voltagesignals_list)
            for i in range(no_of_segments):
                segment = Segment(name=datafile+str(i))
                block.segments.append(segment)

            for idx, segment in enumerate(block.segments):
                voltage_signal = voltagesignals_list[idx]
                voltage_signal.channel_index = block.channel_indexes[0]
                segment.analogsignals.append(voltage_signal)
                block.channel_indexes[0].analogsignals.append(voltage_signal)

                current_signal = currentsignals_list[idx]
                current_signal.channel_index = block.channel_indexes[1]
                segment.analogsignals.append(current_signal)
                block.channel_indexes[1].analogsignals.append(current_signal)

            self.blocks.append(block)

    @staticmethod
    # helper function to files_reader_pxp
    def get_bwgroup_as_block(run, subdirectories_list, reader):
        # getting the traces belonging to this run
        traces_names = [item for item in subdirectories_list if item.startswith(run)]
        # setting up an empty block with the right number of channel_indexes:
        block = Block()
        for i in range(len(traces_names)):
            chidx = ChannelIndex(index=i, channel_names=['Channel '+str(i)])
            block.channel_indexes.append(chidx)

        # importing the raw analogsignals for each channel - two or three signal groups per file
        sg1_name = [name for name in traces_names if 'S1' in name][0]
        sg2_name = [name for name in traces_names if 'S2' in name][0]
        if len(traces_names) == 3:
            sg3_name = [name for name in traces_names if 'S3' in name][0]
            sg3_signals = reader.read_analogsignal(path='root:SutterPatch:Data:'+sg3_name)
        sg1_signals = reader.read_analogsignal(path='root:SutterPatch:Data:'+sg1_name)
        sg2_signals = reader.read_analogsignal(path='root:SutterPatch:Data:'+sg2_name)
        if len(traces_names) > 3:
            print('too many traces to import:')
            print(traces_names)
            return []

        # setting up the block with right number of segments
        block.file_origin = sg1_name[0:3] + sg1_name[6:]
        if 'spontactivity' in block.file_origin:
            # refactoring segments into single long trace;
            # by my conventions, spontactivity protocols are the only ones using 'continuous mode',
            # and these never have a third recording channel.
            no_of_segments = 1
            sg1_signals = np.transpose(sg1_signals).reshape(-1,1)
            sg2_signals = np.transpose(sg2_signals).reshape(-1,1)
        else:
            no_of_segments = len(sg1_signals[1,:])
        for i in range(no_of_segments):
            segment = Segment(name=block.file_origin+str(i))
            block.segments.append(segment)

        # adding the raw data to the block's channel_indexes/segments, in the correct order and units of measurement
        if 'V' in str(sg1_signals[:,0].units):
            voltage_signals = sg1_signals
            current_signals = sg2_signals
        elif 'A' in str(sg1_signals[:,0].units):
            voltage_signals = sg2_signals
            current_signals = sg1_signals
        else:
            print('could not import file: ' + block.file_origin)
            return []
        for idx, segment in enumerate(block.segments):
            single_v_analogsignal = voltage_signals[:,idx].rescale('mV')
            single_v_analogsignal.file_origin = block.file_origin
            segment.analogsignals.append(single_v_analogsignal)
            single_v_analogsignal.channel_index = block.channel_indexes[0]
            block.channel_indexes[0].analogsignals.append(single_v_analogsignal)

            single_i_analogsignal = current_signals[:,idx].rescale('pA')
            single_i_analogsignal.file_origin = block.file_origin
            segment.analogsignals.append(single_i_analogsignal)
            single_i_analogsignal.channel_index = block.channel_indexes[1]
            block.channel_indexes[1].analogsignals.append(single_i_analogsignal)

            if len(traces_names) == 3:
                single_aux_analogsignal = sg3_signals[:,idx]
                single_aux_analogsignal.file_origin = block.file_origin
                segment.analogsignals.append(single_aux_analogsignal)
                single_aux_analogsignal.channel_index = block.channel_indexes[2]
                block.channel_indexes[2].analogsignals.append(single_aux_analogsignal)

        print(block.file_origin + ' raw data imported')
        return block
