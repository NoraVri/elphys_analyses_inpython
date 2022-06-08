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
import seaborn as sns

# imports of functions I wrote
import singleneuron_plotting_functions as plots
import singleneuron_analyses_functions as snafs
# %%
rawdata_path = "D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"


class SingleNeuron:
    # initializing the class instance
    def __init__(self, singleneuron_name, path=rawdata_path):
        """
        singleneuron_name should be a unique identifier for the recording: in my conventions each neuron is named
            by the date (YYYYMMDD) and letter (uppercase), and occasionally also a number (reflecting the
            recording channel, in cases where a double patch was performed/attempted).
        singleneuron_name should match the name of the raw data folder/file belonging to singleneuron.
        path should be to a folder containing:
            1. folder(s) containing the actual raw data recorded for (pairs of) neurons (in my conventions,
                one folder per rig used, containing one folder or file per recorded neuron (pair))
            2. a 'myResults' folder where analyses notes/results are stored and read from
            3. the 'myData_experiments_metadata' and 'myData_recordings_metadata' csv tables.

        All recorded raw data belonging to singleneuron are imported as a list of neo block objects.
        If files with singleneuron_name are found in the 'myResults' folder,
        raw data adjustments are applied based on notes found in rawdata_readingnotes,
        and the relevant empty objects are updated with ones containing analyses results.

        Manipulations to the class instance can be saved (to be recreated on the next instance call)
        by calling the write_results()-method.
        """
        self.name = singleneuron_name
        self.path = path
        self.rawdata_path = ''  # gets updated with the exact filepath leading to singleneuron's raw data files.
        self.rawdata_recordingtype = None
        self.blocks = []

        self.experiment_metadata = pd.Series()
        self.recording_metadata = pd.Series()
        self.rawdata_readingnotes = {}

        self.depolarizing_events = pd.DataFrame()
        self.recordingblocks_index = pd.DataFrame()
        self.ttlon_measures = pd.DataFrame()
        self.subthreshold_oscillations = []
        self.longpulse_measures = []
        self.passive_decay = []
        self.get_singleneuron_rawdata()
        self.get_singleneuron_storedresults()

    # save all results currently present on the singleneuron instance
    def write_results(self):
        """
        this function saves all analysis results belonging to the singleneuron instance
        to a folder on path labeled 'myResults'.
        It also updates the 'total_t_recorded'-column in the recordings_metadata table, based on the blocks that are on the singleneuron instance at the time of calling this function.
        !! There should be only one folder with a name starting with 'myResults' on the path !!
        Each results-table is stored in a separate .csv file, and the parameter values
        used to get them (as well as all other notes needed to exactly recreate the class instance
        stored in self.rawdata_readingnotes) are saved as a .json.
        """
        # saving total time recorded to recordings_metadata:
        recordings_metadata = pd.read_csv(self.path + '\\myData_recordings_metadata.csv')
        self.recording_metadata = recordings_metadata.loc[recordings_metadata.name == self.name]
        if self.recording_metadata.empty:
            print('no metadata for the recording were found; table not updated.')
        else:
            time_recorded_ins = float(self.get_timespentrecording(unit='second'))
            recordings_metadata.loc[recordings_metadata.name == self.name, 'total_t_recorded_in_s'] = time_recorded_ins
            os.chdir(self.path)
            recordings_metadata.to_csv('myData_recordings_metadata.csv', index=False)
            print(self.name + ' total t recorded updated')


        # saving to myResults folder
        results_folder = [folder for folder in os.listdir(self.path)
                          if folder.startswith('myResults')]
        if results_folder:
            results_path = self.path + '\\' + results_folder[0]
            os.chdir(results_path)
            # saving raw data readingnotes:
            if len(self.rawdata_readingnotes) > 0:
                with open(results_path + '\\' + self.name +
                          '_rawdata_readingnotes.json', 'w') as file:
                    file.write(json.dumps(self.rawdata_readingnotes))
            # saving depolarizingevents table:
            if len(self.depolarizing_events) > 0:
                self.depolarizing_events.to_csv(self.name + '_depolarizing_events.csv')
            # saving recordingblocks index:
            if len(self.recordingblocks_index) > 0:
                self.recordingblocks_index.to_csv(self.name + '_recordingblocks_index.csv')
            else:
                self.get_recordingblocks_index()
                self.recordingblocks_index.to_csv(self.name + '_recordingblocks_index.csv')
            # saving ttlon-measures:
            if len(self.ttlon_measures) > 0:
                self.ttlon_measures.to_csv(self.name + '_ttlon_measures.csv')

            print(self.name + ' results have been saved.')

        else:
            print('no results folder found; results not saved')

    # get all raw electrophysiology recordings associated with singleneuron
    def get_singleneuron_rawdata(self):
        """ This function uses singleneuron_name and path to find the
        raw data file(s) recorded from singleneuron.
        Once the right path is found, it calls on the relevant files_reader (defined further below)
        to import the raw data in my standardized format using the Python/Neo framework.
        This function also imports any metadata found for singleneuron (in experiments_ and recordings_metadata tables)
        and attaches these to the class instance.

        This function currently works for:
        - abf-files (one folder per singleneuron(/pair))
        - pxp-files (one file per singleneuron; each file has an internal folder-structure)
        - ibw-files (one folder per singleneuron)
        - txt-files (one folder per singleneuron)
        """
        neuronnamesplit = re.split("(\D)", self.name)
        experiment_date = int(neuronnamesplit[0])
        search_name = neuronnamesplit[0] + neuronnamesplit[1]  # the recording date and the letter of the neuron(s)

        for name in os.listdir(self.path):  # searching through the root folder's files/subdirectories
            if len(name.split('.')) == 1:  # that means it's a folder name (not a file)
                subdirectory_path = self.path + '\\' + name
                searchitems_list = [item for item in os.listdir(subdirectory_path)
                                    if search_name in item]

                if len(searchitems_list) > 0:  # a file/folder with singleneuron_name has been found in the subdirectory
                    for item in searchitems_list:  # find out what type of recording file it is
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

        # getting metadata for the singleneuron experiment day & recording:
        experiments_metadata = pd.read_csv(self.path + '\\myData_experimentDays_metadata.csv')
        self.experiment_metadata = experiments_metadata.loc[
                                    experiments_metadata.date == experiment_date]
        if self.experiment_metadata.empty:
            print('no metadata for the experiment day were found.')

        recordings_metadata = pd.read_csv(self.path + '\\myData_recordings_metadata.csv')
        self.recording_metadata = recordings_metadata.loc[recordings_metadata.name == self.name]
        if self.recording_metadata.empty:
            print('no metadata for the recording were found.')

        # getting the raw data for the singleneuron:
        if not self.rawdata_path:
            print('no files matching neuron name were found.')
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

        # adding the contents of results files to the singleneuron class instance
        if resultsfilespaths_list:
            for path in resultsfilespaths_list:
                if 'rawdata_readingnotes' in path:
                    with open(path, 'r') as file:
                        self.rawdata_readingnotes = json.loads(file.read())

                if 'depolarizing_events' in path:
                    self.depolarizing_events = pd.read_csv(path, index_col=0)
                    dtypes_dict = {}
                    for key in self.depolarizing_events.keys():  # converting columns containing idcs and missing values
                        if 'idx' in key:                         # to bypass their being cast to float
                            dtypes_dict[key] = 'Int64'
                    self.depolarizing_events = self.depolarizing_events.astype(dtypes_dict)

                if 'recordingblocks_index' in path:
                    self.recordingblocks_index = pd.read_csv(path, index_col=0)

                if 'ttlon_measures' in path:
                    self.ttlon_measures = pd.read_csv(path, index_col=0)

        # applying raw data cleanup
        if self.rawdata_readingnotes.get('nonrecordingchannels'):
            for filename, dictionary in self.rawdata_readingnotes['nonrecordingchannels'].items():
                self.rawdata_remove_nonrecordingchannel(filename,
                                                        dictionary['nonrecordingchannel'],
                                                        dictionary['is_pairedrecording'])

        if self.rawdata_readingnotes.get('nonrecordingblocks'):
            for filename in self.rawdata_readingnotes['nonrecordingblocks']:
                self.rawdata_remove_nonrecordingblock(filename)

        if self.rawdata_readingnotes.get('nonrecordingtimeslices'):
            for filename, dictionary in self.rawdata_readingnotes['nonrecordingtimeslices'].items():
                self.rawdata_remove_nonrecordingsection(filename,
                                                        trace_start_t=dictionary['t_start'],
                                                        trace_end_t=dictionary['t_end'],
                                                        remove_segments=dictionary['segment_idx'])

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
                                           remove_segments=None):
        """ This function takes the name of the file/block from which a section is to be removed.
        If a start and/or end time (in s) are provided (one or the other has to be),
        segment_idx is assumed to be 0 (the single segment on blocks that have just one long trace)
        and the segment is adjusted to start and/or end at the new time(s).
        If a single int is passed for remove_segments, this segment will be removed from the block.
        If a list list of ints is provided, each of these will be removed from the block.
        !!Note: this function will fail if anything besides a (list of) int is passed through for remove_segments,
        and care should be taken to remove all relevant segments in one go (or things will bug out when the neuron is called next).

        The function returns self.rawdata_blocks with the superfluous data removed,
        and updates rawdata_readingnotes accordingly.
        """
        if not self.rawdata_readingnotes.get('nonrecordingtimeslices'):
            self.rawdata_readingnotes['nonrecordingtimeslices'] = {}

        block_idx = self.get_blocknames(printing='off').index(file_origin)

        # removing a time-slice from segments[0] of a block
        if (trace_start_t is not None) or (trace_end_t is not None):
            block = self.blocks[block_idx]

            if trace_start_t:
                start_t = trace_start_t * pq.s
                block.segments[0] = block.segments[0].time_slice(t_start=start_t)
            if trace_end_t:
                end_t = trace_end_t * pq.s
                block.segments[0] = block.segments[0].time_slice(t_start=block.segments[0].t_start,
                                                                 t_stop=end_t)
            # updating the block as attached to the class instance:
            self.blocks[block_idx] = block
            for i, _ in enumerate(self.blocks[block_idx].channel_indexes):
                self.blocks[block_idx].channel_indexes[i].analogsignals[0] = block.segments[0].analogsignals[i]

        # removing a single segment from a block
        elif isinstance(remove_segments, int):
            self.blocks[block_idx].segments.remove(self.blocks[block_idx].segments[remove_segments])
            chidxs = self.blocks[block_idx].channel_indexes
            for i, chidx in enumerate(chidxs):
                analogsignals = chidx.analogsignals
                del analogsignals[remove_segments]
                chidx.analogsignals = analogsignals
                self.blocks[block_idx].channel_indexes[i] = chidx

        # removing multiple segments from a block
        elif isinstance(remove_segments, list):
            remove_segments.sort(reverse=True)
            for idx in remove_segments:
                self.blocks[block_idx].segments.remove(self.blocks[block_idx].segments[idx])
                chidxs = self.blocks[block_idx].channel_indexes
                for i, chidx in enumerate(chidxs):
                    analogsignals = chidx.analogsignals
                    del analogsignals[idx]
                    chidx.analogsignals = analogsignals
                    self.blocks[block_idx].channel_indexes[i] = chidx

        # updating reading-notes dictionary:
        if file_origin not in self.rawdata_readingnotes['nonrecordingtimeslices'].keys():
            self.rawdata_readingnotes['nonrecordingtimeslices'].update({
                file_origin: {'t_start': trace_start_t,
                              't_end': trace_end_t,
                              'segment_idx': remove_segments}
            })
        # else:
        #     removedsegs_idcs = self.rawdata_readingnotes['nonrecordingtimeslices'][file_origin]['segment_idx']
        #     if isinstance(removedsegs_idcs, int):
        #         if isinstance(remove_segments, int):
        #             removedsegs_idcs = [removedsegs_idcs, remove_segments]
        #         elif isinstance(remove_segments, list):
        #             removedsegs_idcs = [removedsegs_idcs, *remove_segments]
        #     elif isinstance(removedsegs_idcs, list):
        #         if isinstance(remove_segments, int):
        #             removedsegs_idcs = [*removedsegs_idcs, remove_segments]
        #         elif isinstance(remove_segments, list):
        #             removedsegs_idcs = [*removedsegs_idcs, *remove_segments]
        #
        #     self.rawdata_readingnotes['nonrecordingtimeslices'][file_origin]['segment_idx'] = list(set(removedsegs_idcs))

    # note which blocks have special chemicals applied
    def rawdata_note_chemicalinbath(self, *block_identifiers):
        """ This function checks that information about applied chemicals is available,
        and if so, adds any blocksnames corresponding to (any of the) block_identifiers
        to the list of blocks with chemicals applied.
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


    def get_recordingblocks_index(self):
        all_blocks_infos_dict = snafs.make_recordings_index_dictionary()
        for block in self.blocks:
            block_infos_dict = snafs.fill_singleneuron_recordings_index_dictionary(block)
            for key in all_blocks_infos_dict:
                all_blocks_infos_dict[key] += block_infos_dict[key]
        self.recordingblocks_index = pd.DataFrame(all_blocks_infos_dict).round(decimals=2)

    # getting a list of all block names
    def get_blocknames(self, printing='on'):
        """ returns the (file)names of all the blocks of singleneuron as a list, and prints them."""
        blocks_list = [block.file_origin for block in self.blocks]
        if printing == 'on':
            for idx, block in enumerate(blocks_list):
                print(block + ' , idx=' + str(idx))
            # return blocks_list
        else:
            return blocks_list

    # get the total length (in s) of recordings for the singleneuron, optinally for a subset of blocks
    def get_timespentrecording(self, *block_identifiers, unit='minute',
                               make_baselinev_hist=False, axis=None):
        blocknames_list = self.get_blocknames(printing='off')
        time_count = 0 * pq.s
        # if a histogram of baselinev is to be made and no axis is passed, create a figure:
        if make_baselinev_hist:
            baselinevs_array = np.empty((1,1))
            ax = axis
            if axis is None:
                figure, ax = plt.subplots()

        # getting the list of block names for which to count the time recorded
        if not block_identifiers:
            identified_blocks = blocknames_list
        else:
            identified_blocks = []
            for identifier in block_identifiers:
                blocknames = [block for block in blocknames_list if identifier in block]
                identified_blocks = [*identified_blocks, *blocknames]
        # counting time recorded
        for blockname in identified_blocks:
            block_idx = blocknames_list.index(blockname)
            for segment in self.blocks[block_idx].segments:
                time_count += (segment.t_stop - segment.t_start)
                # if a histogram of baselinev is to be made, collect them all into an array
                if make_baselinev_hist:
                    vtrace = segment.analogsignals[0]
                    baselinevs_array = np.concatenate((baselinevs_array, vtrace))
        # plot the baselinev histogram, if required
        if make_baselinev_hist:
            nbins = int((np.max(baselinevs_array) - np.min(baselinevs_array)) * 10)
            ax.hist(baselinevs_array, bins=nbins)
        return time_count.rescale(unit)

    # plotting raw data blocks, optionally with (a subset of) depolarizing events marked
    def plot_rawdatablocks(self, *block_identifiers, **kwargs):
        """Plots raw data by block, separate subplots for each channel_index.
        If block_identifiers are passed, only blocks with those strings in block.file_origin will be plotted.
        additional kwargs:
        events_to_mark='none', can be changed to a pd.Series of booleans marking the locations of events to be marked
        time_axis_unit='ms',     # has to be ms if events_to_mark are passed down (or they'll end up in the wrong place)
        segments_overlayed=True  # works only for data recorded as abf at the moment
        """
        allblocknames_list = self.get_blocknames(printing='off')
        if not block_identifiers:
            blocknames_list = allblocknames_list
        else:
            blocknames_list = []
            for identifier in block_identifiers:
                blocks = [blockname for blockname in allblocknames_list if identifier in blockname]
                for block in blocks:
                    blocknames_list.append(block)

        for blockname in blocknames_list:
            block = self.blocks[allblocknames_list.index(blockname)]
            figure, axes = plots.plot_block(block, self.depolarizing_events, **kwargs)
            plt.suptitle(self.name + ' raw data file ' + block.file_origin)
        if len(blocknames_list) == 1:
            return figure, axes

    def plot_rawdatatraces_ttlaligned(self, *block_identifiers,
                                      newplot_per_block=False,
                                      newplot_per_ttlduration=False,
                                      newplot_per_ttlintensity=False,
                                      plt_title='',
                                      noisefilter_hpfreq='default',
                                      **kwargs):

        """
        This function plots raw data aligned to ttl onset, baselined to V in the ms before,
        color-coded by baseline V.
        kwargs:
        - prettl_t_inms, postttl_t_inms: time before and after ttl-onset-time to be plotted.
            default: 2, 30
        - do_baselining: default True, plots traces zeroed in V to baselinev (meanV in ms before ttl on)
        - plotdvdt: default True, plots dVdt vs V in a second subplot.
        - colorby_measure: default 'baselinev', values to use for distributing line colors.
        - color_lims: [min max] of colorbar/traces to be plotted (traces falling outside are omitted).
            default: None - uses min and max baselinev values for colorbar
        - plotlims: [minv maxv mindvdt maxdvdt] values for axes limits settings.
            default: None - default axes limits of matplotlib are used.
        - skip_vtraces_idcs: can be a list of ints - segments with those indices will be skipped.
            default: None - all traces of the block are plotted.
        - skip_vtraces_block: can be a list of block identifiers - if skip_vtraces is a list of ints, traces will be skipped only in the identified blocks.
        - noisefilter_hpfreq: int - high-pass value for the filter getting the noise off the raw vtrace.
            default: 3000 Hz
        """
        if not hasattr(self, 'ttlon_measures'):
            self.get_ttlonmeasures_fromrawdata()
        if self.ttlon_measures.empty:
            return
        # updating noisefilter_hpfreq if set to 'default' but value for get_depolarizingevents is different from standard default
        if noisefilter_hpfreq == 'default' and\
                self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            noisefilter_hpfreq = self.rawdata_readingnotes['getdepolarizingevents_settings']['noisefilter_hpfreq']
        elif not isinstance(noisefilter_hpfreq, int):
            noisefilter_hpfreq = 3000

        # getting the list of blocks to plot
        allblocksnames_list = self.get_blocknames(printing='off')
        ttlblocksnames_list = self.ttlon_measures['file_origin'].unique()
        blocks_list = []
        if not block_identifiers:
            for blockname in ttlblocksnames_list:
                blocks_list.append(self.blocks[allblocksnames_list.index(blockname)])
        else:
            for identifier in block_identifiers:
                blocknames = [block for block in ttlblocksnames_list if identifier in block]
                for blockname in blocknames:
                    blocks_list.append(self.blocks[allblocksnames_list.index(blockname)])

        # plotting
        if newplot_per_block:
            for block in blocks_list:
                figure, _ = plots.plot_ttlaligned([block], self.ttlon_measures, noisefilter_hpfreq=noisefilter_hpfreq, **kwargs)
                figure.suptitle(self.name + ' block ' + block.file_origin)
        if newplot_per_ttlduration:
            ttldurations = self.ttlon_measures.ttlon_duration_inms.unique()
            for duration in ttldurations:
                identicaldurationblocks_names = self.ttlon_measures[
                    (self.ttlon_measures.ttlon_duration_inms == duration)].file_origin.unique()
                identicalduration_blocks = [block for block in blocks_list
                                            if block.file_origin in identicaldurationblocks_names]
                figure, axes = plots.plot_ttlaligned(identicalduration_blocks, self.ttlon_measures, noisefilter_hpfreq=noisefilter_hpfreq, **kwargs)
                figure.suptitle(str(len(identicalduration_blocks)) + ' blocks with identical ttl-on time, cell ' + self.name)
                print(identicaldurationblocks_names)
                print('ttl on duration: ' + str(duration) + ' ms')
        else:
            figure, axes = plots.plot_ttlaligned(blocks_list, self.ttlon_measures, noisefilter_hpfreq=noisefilter_hpfreq, **kwargs)
            figure.suptitle(plt_title + '; ' + str(len(blocks_list)) + ' blocks plotted together, cell ' + self.name)
            return figure, axes

    # plotting (subsets of) action potentials or depolarizing events, overlayed
    def plot_depolevents(self, events_to_plot=pd.Series(), blocknames_list=None,
                         newplot_per_block=False, newplot_per_event=False,
                         colorby_measure='', color_lims=None, colormap='viridis',
                         plt_title='',
                         plot_dvdt=True, plot_ddvdt=False,
                         **kwargs):
        """ This function plots overlays of depolarizing events, either all in one plot
        or as one plot per rawdata_block present on the singleneuron class instance.
        By default, all detected events are plotted in a single plot; all blue lines
        representing the original raw recorded events.

        Optional inputs:
        events_to_plot: a Pandas True/False series (same length as depolarizingevents)
            marking a subset of events for plotting.
        [blocknames_list]: a list of block names (== block.file_origin) marking a subset of blocks for event-plotting.
        newplot_per_block: if True, a new figure will be drawn for each rawdata_block.
        newplot_per_event: if True, a new figure will be drawn for each individual event (as well).
        'colorby_measure': key of a depolarizingevents-measure to color-code the lines by.
        colormap: viridis by default, changes to cividis if something else is put there
        [color_lims]: [minvalue, maxvalue] of the colorbar. If not provided, min and max will be inferred from the data.
        'plt_title': default='', string giving the title of the plot(s).
        Other kwargs (passed through to plots.plot_single_event):
        'timealignto_measure': default='peakv_idx', but can be changed to any key representing a time measurement.
        prealignpoint_window_inms: default=5, length of the timewindow for plotting before the align-point.
        plotwindow_inms: default=50, total length of the window for plotting the events.
        get_measures_type: default='raw', if it's something else the event-detect trace will be recreated and used.
        do_baselining: if True, baselinev is subtracted from the event-trace.
        do_normalizing: if True, the event-trace is divided by amplitude.
        display_measures: if True, onset and duration of measures for each event will be displayed in the plot(s).
        """
        # getting the (subset of) events for plotting:
        if not events_to_plot.empty:
            events_for_plotting = self.depolarizing_events.loc[events_to_plot]
        else:
            events_for_plotting = self.depolarizing_events
        # getting the (subset of) blocks for plotting:
        allblocks_nameslist = self.get_blocknames(printing='off')
        blocks_for_plotting = set(events_for_plotting['file_origin'])
        if blocknames_list is not None:
            blocks_for_plotting = list(blocks_for_plotting.intersection(set(blocknames_list)))

        # setting the figure title:
        axis_title = 'voltage (mV)'
        if 'get_measures_type' in kwargs.keys() and not kwargs['get_measures_type'] == 'raw':
            axis_title += ' event-detect trace, '
        if 'do_baselining' in kwargs.keys() and kwargs['do_baselining']:
            axis_title += ' baselined'
        if 'do_normalizing' in kwargs.keys() and kwargs['do_normalizing']:
            axis_title += ' normalized'

        if newplot_per_event:
            for block_name in blocks_for_plotting:
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]
                plots.plot_singleblock_events(rawdata_block, block_events,
                                              self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                              newplot_per_event=newplot_per_event,
                                              plot_dvdt=plot_dvdt,
                                              plot_ddvdt=plot_ddvdt,
                                              **kwargs)
            if 'display_measures' in kwargs.keys() and kwargs['display_measures']:
                kwargs['display_measures'] = False  # turning it off for the overlayed-lines plot(s) that are made next

        if newplot_per_block:
            for block_name in blocks_for_plotting:
                if plot_dvdt and plot_ddvdt:
                    figure, axes = plt.subplots(1, 3, squeeze=True)
                    axis = axes[0]
                    dvdt_axis = axes[1]
                    ddvdt_axis = axes[2]
                elif plot_dvdt:
                    figure, axes = plt.subplots(1, 2, squeeze=True)
                    axis = axes[0]
                    dvdt_axis = axes[1]
                    ddvdt_axis = None
                else:
                    figure, axis = plt.subplots(1, 1, squeeze=True)
                    dvdt_axis = None
                    ddvdt_axis = None
                figure.suptitle(self.name + block_name + plt_title)
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]
                plots.plot_singleblock_events(
                    rawdata_block,
                    block_events,
                    self.rawdata_readingnotes['getdepolarizingevents_settings'],
                    colorby_measure=colorby_measure,
                    color_lims=color_lims,
                    colormap=colormap,
                    axis_object=axis,
                    dvdt_axis_object=dvdt_axis,
                    ddvdt_axis_object=ddvdt_axis,
                    **kwargs)
                axis.set_title(axis_title)
        else:
            if plot_dvdt and plot_ddvdt:
                figure, axes = plt.subplots(1, 3, squeeze=True)
                axis = axes[0]
                dvdt_axis = axes[1]
                ddvdt_axis = axes[2]
            elif plot_dvdt:
                figure, axes = plt.subplots(1, 2, squeeze=True)
                axis = axes[0]
                dvdt_axis = axes[1]
                ddvdt_axis = None
            else:
                figure, axis = plt.subplots(1, 1, squeeze=True)
                dvdt_axis = None
                ddvdt_axis = None
            plt.suptitle(self.name + plt_title)
            # (optional) setting color limits for the figure
            if colorby_measure:
                if color_lims is None:
                    color_lims = [events_for_plotting[colorby_measure].min(),
                                  events_for_plotting[colorby_measure].max()]
                elif not len(color_lims) == 2:
                    print('please input valid colorbar limits')
                    return
                color_map, cm_normalizer = plots.get_colors_forlineplots(colorby_measure,
                                                                         color_lims,
                                                                         colormap=colormap)
                figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=color_map),
                                label=colorby_measure)
            # plotting
            for block_name in blocks_for_plotting:
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]
                plots.plot_singleblock_events(rawdata_block, block_events,
                                              self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                              axis_object=axis,
                                              dvdt_axis_object=dvdt_axis,
                                              ddvdt_axis_object=ddvdt_axis,
                                              colorby_measure=colorby_measure,
                                              color_lims=color_lims,
                                              colormap=colormap,
                                              **kwargs)
            axis.set_title(axis_title)
            if dvdt_axis and ddvdt_axis:
                return axis, dvdt_axis, ddvdt_axis
            elif dvdt_axis:
                return  axis, dvdt_axis
            else:
                return axis

    # plotting groups of depolarizing events overlayed, one color per group
    def plot_depoleventsgroups_overlayed(self, *events_groups, group_labels=None,
                                         blocknames_list=None, plt_title='',
                                         **kwargs):
        """
        This function plots groups of events overlayed, one color per group.
        events_groups_series should be pd.Series of booleans, marking the positions
            of the events to be plotted on the relevant pd.DataFrame (depolarizations or action potentials).
        If get_subthreshold_events is not True, action potentials will be plotted.
        If a blocknames_list is passed, events will be plotted only for those blocks.
        If plt_title is passed, it is passed straight through to the figure's suptitle.
        Other optional kwargs that can be passed through to plot_singleblock_events:
        - timealignto_measure = 'peakv_idx' - by default, traces are aligned to event peaks; any
            time-based event-measures are acceptable.
        - prealignpoint_window_inms = 5 - startpoint of the displayed trace, in ms before the alignment-point.
        - plotwindow_inms = 50 - the total length of traces to display.
        - axis_object = None - by default, all events will be plotted in a single new plot; if
            an axis object is passed, traces are plotted onto it and no new figure is created.
        - get_measures_type = 'raw' - otherwise, the event-detect traces will be displayed instead of raw v.
        - do_baselining and do_normalizing - if True, uses baselinev and amplitude (raw or event-detect,
            depending on get_measures_type) values to do baselining and/or normalizing, respectively.
        - plot_dvdt - if True, will make a dVdt/V plot as well.
        """
        color_lims = [0, len(events_groups) - 1]
        colormap, cm_normalizer = plots.get_colors_forlineplots([], color_lims)

        allblocks_nameslist = self.get_blocknames(printing='off')
        if blocknames_list is not None:
            blocks_forplotting = blocknames_list
        else:
            blocks_forplotting = allblocks_nameslist

        if 'plot_dvdt' in kwargs.keys() and kwargs['plot_dvdt']:
            figure, axes = plt.subplots(1, 2, squeeze=True)
            axis = axes[0]
            dvdt_axis = axes[1]
        else:
            figure, axis = plt.subplots(1, 1, squeeze=True)
            dvdt_axis = None

        for i, events_group in enumerate(events_groups):
            events_for_plotting = self.depolarizing_events[events_group]
            for block_name in blocks_forplotting:
                rawdata_block = self.blocks[allblocks_nameslist.index(block_name)]
                block_events = events_for_plotting.loc[events_for_plotting['file_origin'] == block_name]
                if len(block_events) > 0:
                    plots.plot_singleblock_events(rawdata_block, block_events,
                                                  self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                                  axis_object=axis,
                                                  dvdt_axis_object=dvdt_axis,
                                                  linecolor=colormap(cm_normalizer(i)),
                                                  label=('event group ' + str(i)),
                                                  **kwargs)
        colorbar = figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap),
                                   ticks=list(range(len(events_groups)))
                                   )
        if group_labels is not None and (len(group_labels) == len(events_groups)):
            colorbar.ax.set_yticklabels(group_labels)
        plt.suptitle(plt_title)

    # plotting depolarizing events group averages
    def plot_depoleventsgroups_averages(self, *events_groups, group_labels=None, plt_title='group averages',
                                        plot_dvdt=True,
                                        subtract_traces=False, add_traces=False, delta_t=0,
                                        **kwargs):
        """
        This function plots averages (mean +/- std) of selected groups of events; optionally, the first two groups'
        averages can be added together or subtracted from each other (with a specified delta-t between the traces).
        optional kwargs that are passed on to get_events_average:
        timealignto_measure='peakv_idx',
        prealignpoint_window_inms=5,
        plotwindow_inms=40,
        do_normalizing=False,
        get_measures_type='raw',
        """
        # getting colors to plot with
        if (subtract_traces or add_traces):
            color_lims = [0, len(events_groups)]
        else:
            color_lims = [0, len(events_groups) - 1]
        colormap, cm_normalizer = plots.get_colors_forlineplots([], color_lims)
        # setting up figure axes
        if plot_dvdt:
            figure, axes = plt.subplots(1, 2, squeeze=True)
            axis = axes[0]
            dvdt_axis = axes[1]
        else:
            figure, axis = plt.subplots(1, 1, squeeze=True)
            dvdt_axis = None
        # initializing variables, in case added/subtracted traces are to be plotted
        group1average=None
        group2average=None
        time_axis=None

        # getting events group averages and plotting them
        for i, events_group in enumerate(events_groups):
            linecolor = colormap(cm_normalizer(i))
            events_group_avg, events_group_std, time_axis = snafs.get_events_average(self.blocks, self.depolarizing_events,
                                                        self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                                        events_group, **kwargs)
            axis.plot(time_axis, events_group_avg,
                      color=linecolor, linewidth=2.5)
            axis.plot(time_axis, (events_group_avg - events_group_std),
                      '--',
                      color=linecolor)
            axis.plot(time_axis, (events_group_avg + events_group_std),
                      '--',
                      color=linecolor)
            axis.set_xlabel('time (ms)')
            if dvdt_axis is not None:
                diff_events_avg = np.diff(events_group_avg)
                dvdt_axis.plot(events_group_avg[:-1:], diff_events_avg, color=linecolor)
                dvdt_axis.set_xlabel('V')
                dvdt_axis.set_ylabel('dV/dt')
        # also plotting traces subtracted or added, if so required
            if (subtract_traces or add_traces) and (i == 0):
                group1average = events_group_avg
            if (subtract_traces or add_traces) and (i == 1):
                group2average = events_group_avg
        if (group2average is not None):
            if delta_t != 0:  # taking samples off the start/end of averaged traces to get the right time difference
                sampling_period_inms = float(self.blocks[0].segments[0].analogsignals[0].sampling_period) * 1000
                nsamples_tocull = int(abs(delta_t) / sampling_period_inms)
                time_axis = time_axis[:-nsamples_tocull:]
                if delta_t < 0:  # moving the second trace up in time relative to the first one
                    group2average = group2average[nsamples_tocull::]
                    group1average = group1average[:-nsamples_tocull:]
                elif delta_t > 0:  # moving the first trace up in time relative to the second one
                    group1average = group1average[nsamples_tocull::]
                    group2average = group2average[:-nsamples_tocull:]
            if subtract_traces:
                mathd_trace = group1average - group2average
            elif add_traces:
                mathd_trace = group1average + group2average
            else:
                mathd_trace = None
        else:
            mathd_trace = None

        if mathd_trace is not None:
            axis.plot(time_axis, mathd_trace,
                      color=colormap(cm_normalizer(len(events_groups))))
            if dvdt_axis is not None:
                diff_mathdevents_avg = np.diff(mathd_trace)
                dvdt_axis.plot(mathd_trace[:-1:], diff_mathdevents_avg, color=colormap(cm_normalizer(len(events_groups))))
                dvdt_axis.set_xlabel('V')
                dvdt_axis.set_ylabel('dV/dt')
        # add colorbar and tick labels
        if group_labels is not None and (len(group_labels) == len(events_groups)):
            if subtract_traces:
                group_labels.append('subtracted')
            if add_traces:
                group_labels.append('added')
            if delta_t != 0:
                group_labels[-1] = group_labels[-1] + ' with dt = ' + str(delta_t) + ' ms'
                group_labels.append('re-timed trace')
                if delta_t < 0:
                    axis.plot(time_axis, group2average, '--')
                elif delta_t > 0:
                    axis.plot(time_axis, group1average, '--')

        if group_labels is not None:
            colorbar = figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap),
                                       ticks=list(range(len(group_labels)))
                                       )
            colorbar.ax.set_yticklabels(group_labels)
        plt.suptitle(plt_title)
        return axis, dvdt_axis

    # plotting the event-detect trace that was used to find depolarizing events
    def plot_eventdetecttraces_forsegment(self, block_idx, segment_idx,
                                          return_dicts=False,
                                          time_slice=None,
                                          **kwargs):
        """ This function reproduces the results of get_depolarizing_events on a single trace,
        showing all the figures in between.
        If a segment is very long, this can cause plotting to be very slow or even crash; this can be prevented
        by instead plotting a time-slice of the segment (by setting time_slice=[t_start, t_stop] (in s)).

        If depolarizing-events detection has already been performed (and saved) for the singleneuron instance,
        this function will use those parameter settings to reproduce plots; otherwise, default parameters will be used.
        Adding kwargs will update those parameters for plotting the trace (without overwriting parameters stored on singleneuron).
        For the list of kwargs, see get_depolarizing_events_fromrawdata.
        """
        segment = self.blocks[block_idx].segments[segment_idx]
        if time_slice:
            t_start = time_slice[0] * pq.s
            t_stop = time_slice[1] * pq.s
            segment = segment.time_slice(t_start, t_stop)
        # if there are no saved values, set getdepolarizingevents-parameters to defaults; otherwise, use saved values
        stored_kwargs = {}
        if not self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            stored_kwargs = {
                            'min_depolspeed': 0.1,
                            'min_depolamp': 0.2,
                            'depol_to_peak_window': 5,
                            'event_width_window': 40,
                            'ahp_width_window': 150,
                            'noisefilter_hpfreq': 3000,
                            'oscfilter_lpfreq': 20,
                            'ttleffect_window': None,
                            'plot': 'on'}
        else:
            stored_kwargs.update(self.rawdata_readingnotes['getdepolarizingevents_settings'])
            stored_kwargs['plot'] = 'on'

        # update parameter values that have been passed as kwargs
        for key, value in kwargs.items():
            if key in stored_kwargs.keys():
                stored_kwargs[key] = value
        # plot event-detect results figures
        eventmeasures_dictionary = snafs.get_depolarizingevents(
            self.blocks[block_idx].file_origin, segment_idx,
            segment,
            **stored_kwargs)

        if return_dicts:
            stored_kwargs['plot'] = 'off'
            return eventmeasures_dictionary, stored_kwargs

    # scattering measured events parameters, one subplot per (named) group of events
    def scatter_depolarizingevents_measures(self, xmeasure, ymeasure,
                                            cmeasure=None,
                                            plot_fit=False,
                                            **events_groups):
        """
        This function creates an overview of scatterplots:
        xmeasure vs ymeasure (optionally) colored by cmeasure,
        in a separate subplot for each event-group.
        events_groups should be a named pd.Series() of booleans marking the location
            of events to be included in the scatter.
        """
        if len(events_groups) > 1:
            figure, axes = plt.subplots(nrows=len(events_groups), ncols=1,
                                        # sharex='all', # it's buggy, have to find a work-around
                                        sharey='all')
            for axis, eventgroupname, eventgroup in zip(axes,
                                                        events_groups.keys(),
                                                        events_groups.values()):
                eventsgroup_measures = self.depolarizing_events[eventgroup]
                eventsgroup_measures.plot.scatter(x=xmeasure,
                                                  y=ymeasure,
                                                  c=cmeasure,
                                                  colormap='cividis',
                                                  ax=axis)
                axis.set_title(eventgroupname)
                if plot_fit:
                    sns.regplot(x=xmeasure, y=ymeasure, data=eventsgroup_measures, ax=axis, scatter=False)

        elif len(events_groups) == 1:
            figure, axis = plt.subplots(1, 1)
            eventgroupname = list(events_groups.keys())[0]
            eventgroup = list(events_groups.values())[0]
            eventsgroup_measures = self.depolarizing_events[eventgroup]
            eventsgroup_measures.plot.scatter(x=xmeasure,
                                              y=ymeasure,
                                              c=cmeasure,
                                              colormap='cividis',
                                              ax=axis)
            axis.set_title(eventgroupname)
            if plot_fit:
                sns.regplot(x=xmeasure, y=ymeasure, data=eventsgroup_measures, ax=axis, scatter=False,)

        else:
            figure, axis = plt.subplots(1, 1)
            self.depolarizing_events.plot.scatter(x=xmeasure,
                                                    y=ymeasure,
                                                    c=cmeasure,
                                                    colormap='cividis',
                                                    ax=axis)
            if plot_fit:
                sns.regplot(x=xmeasure, y=ymeasure, data=self.depolarizing_events, ax=axis, scatter=False)
            axis.set_title('all events')

    # scattering measured events parameters overlayed, one color per group
    #TODO replace with nice plots with fits and such using seaborn's lmplot
    def scatter_depoleventsgroups_overlayed(self, xmeasure, ymeasure, plt_title='',
                                            **events_groups):
        color_lims = [0, len(events_groups) - 1]
        colormap, cm_normalizer = plots.get_colors_forlineplots([], color_lims)

        figure, axis = plt.subplots()
        eventsgroups_labels = events_groups.keys()
        colorbar = figure.colorbar(mpl.cm.ScalarMappable(norm=cm_normalizer, cmap=colormap),
                                   ticks=list(range(len(events_groups)))
                                   )
        colorbar.ax.set_yticklabels(eventsgroups_labels)

        for i, eventgroup in enumerate(events_groups.values()):
            eventsgroup_measures = self.depolarizing_events[eventgroup]
            eventsgroup_measures.plot.scatter(x=xmeasure,
                                              y=ymeasure,
                                              c=colormap(cm_normalizer(i)),
                                              ax=axis)
        plt.suptitle(plt_title)

# %% functions for analyzing raw data


    # getting the depolarizing_events DataFrame
    def get_depolarizingevents_fromrawdata(self, **kwargs):
        """This function goes over all voltage-traces in all raw-data blocks, and returns
        a Pandas dataframe containing action potentials and subthreshold depolarizing events.
        The dataframe contains a set of standard measures taken from each event, as well as
        all information needed to recover the location of the event in the original data trace.
        Default values for function parameters are read in from rawdata_readingnotes, and are
        updated there if non-default kwargs are used.

        Inputs (all optional):
        'min_depolspeed': minimal speed of increase (mV/ms) for detecting depolarizations.
        'min_depolamp': minimal amplitude from baseline to a possible event peak.
        'depol_to_peak_window': maximal time between a detected depolarization and an event peak (in ms),
          and time after peak within which voltage should decay again to <80% of its amplitude.
        'event_width_window': time after peak within which half-width, threshold and whole-width are measured
            (if a measurement cannot be taken within the window, a NaN value is filled in instead).
        'ahp_width_window': time after baseline-re-reached within which AHP end is measured.
        'noisefilter_hpfreq': cutoff frequency for high-pass filter applied to reduce noise.
        'oscfilter_lpfreq': cutoff frequency for low-pass filter applied to get sub-treshold STOs only.
        'ttleffect_window': time after TTL pulse turns off but still has effects working through.
        ('plot': if 'on', will plot each voltage trace, with scatters for baselinevs and peakvs.)
        !! Any time this function runs, reading-notes are updated with any kwargs that are passed through.

        !! This function can take quite a long time to run for neuron recordings longer than just a few minutes.
        The recommended workflow is to use plot_eventdetecttraces_forsegment() on a (time_slice of a)
        single, representative segment first to find good settings for kwargs.
        !! Once satisfied with the results, run self.write_results() to save the data !!
        """
        if not self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            self.rawdata_readingnotes['getdepolarizingevents_settings'] = {
                                                            'min_depolspeed': 0.1,
                                                            'min_depolamp': 0.2,
                                                            'depol_to_peak_window': 5,
                                                            'event_width_window': 40,
                                                            'ahp_width_window': 150,
                                                            'noisefilter_hpfreq': 3000,
                                                            'oscfilter_lpfreq': 20,
                                                            'ttleffect_window': None,
                                                            'plot': 'off'}
        # updating reading-notes with new parameter settings if relevant kwargs are passed
        for key, value in kwargs.items():
            if key in self.rawdata_readingnotes['getdepolarizingevents_settings'].keys():
                self.rawdata_readingnotes['getdepolarizingevents_settings'][key] = value

        # initializing empty measures-dictionaries
        all_eventsmeasures_dictionary = snafs.make_eventsmeasures_dictionary()
        # getting all events: looping over each block, and each trace within each block
        for block in self.blocks:
            if ('Vclamp' or 'vclamp') in block.file_origin:
                continue  # skip blocks recorded in Vclamp mode

            for i, segment in enumerate(block.segments):
                segment_eventmeasuresdict = snafs.get_depolarizingevents(
                    block.file_origin, i, segment,
                    **self.rawdata_readingnotes['getdepolarizingevents_settings'])
                # updating the measures-dictionaries with the results from a single trace
                for key in all_eventsmeasures_dictionary:
                    all_eventsmeasures_dictionary[key] += segment_eventmeasuresdict[key]

        # converting the results to a DataFrame and attaching to the class instance
        self.depolarizing_events = pd.DataFrame(all_eventsmeasures_dictionary).round(decimals=2)
        dtypes_dict = {}
        for key in self.depolarizing_events.keys():  # converting columns containing idcs and missing values
            if 'idx' in key:                         # to bypass their being cast to float
                dtypes_dict[key] = 'Int64'
        self.depolarizing_events.astype(dtypes_dict)

    # getting prepotentials for APs
    def get_ap_prepotentials(self, aps_series, tracesnippet_length_inms=5, baselinewindow_length_inms=2):

        new_depolarizingevents_df = snafs.get_ap_prepotentials(self.blocks,
                                                               self.get_blocknames(printing='off'),
                                                               self.depolarizing_events,
                                                               self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                                               aps_series=aps_series,
                                                               tracesnippet_length_inms=tracesnippet_length_inms,
                                                               baselinewindow_length_inms=baselinewindow_length_inms)
        self.depolarizing_events = new_depolarizingevents_df

    def get_eventsgroups_averages(self, *events_groups, **kwargs):
        """
        This function gets averages (mean +/- std) of selected groups of events (as indexed into the
        depolarizingevents-dataframe through Series of booleans).
        optional kwargs that are passed on to get_events_average:
        timealignto_measure='peakv_idx',
        prealignpoint_window_inms=5,
        plotwindow_inms=40,
        do_normalizing=False,
        get_measures_type='raw',
        """
        averages = []
        averages_stds = []
        for i, events_group in enumerate(events_groups):
            events_group_avg, events_group_std, time_axis = snafs.get_events_average(self.blocks, self.depolarizing_events,
                                                        self.rawdata_readingnotes['getdepolarizingevents_settings'],
                                                        events_group, **kwargs)

    def get_ttlonmeasures_fromrawdata(self, **kwargs):
        # kwargs:
        # ttlhigh_value=1; sets the binary cutoff value for measuring ttl low/high
        # response_window_inms=30; time window since ttl on in which response max amp is calculated
        if self.rawdata_readingnotes.get('getdepolarizingevents_settings'):
            noisefilter_hpfreq = self.rawdata_readingnotes['getdepolarizingevents_settings']['noisefilter_hpfreq']
        else:
            noisefilter_hpfreq = 3000
        all_ttlonmeasures_dictionary = snafs.make_ttlonmeasures_dictionary()
        for block in self.blocks:
            ttlon_measures_dictionary = snafs.get_ttlresponse_measures(block, noisefilter_hpfreq, **kwargs)
            if ttlon_measures_dictionary is not None:
                for key in all_ttlonmeasures_dictionary.keys():
                    all_ttlonmeasures_dictionary[key] += ttlon_measures_dictionary[key]
        # converting the results to a DataFrame and attaching to the class instance
        ttlon_measures = pd.DataFrame(all_ttlonmeasures_dictionary).round(decimals=2)
        dtypes_dict = {}
        for key in ttlon_measures.keys():  # converting columns containing idcs & missing values
            if 'idx' in key:                         # to bypass their being cast to float
                dtypes_dict[key] = 'Int64'
        self.ttlon_measures = ttlon_measures.astype(dtypes_dict)

    # getting long-pulse measures (unfinished)
    def get_longpulsemeasures_fromrawdata(self, longpulses_blocks, **kwargs):
        all_longpulsesmeasures = snafs.make_longpulsesmeasures_dictionary()

        all_blocks = self.get_blocknames(printing='off')
        for block in longpulses_blocks:
            for i, segment in enumerate(self.blocks[all_blocks.index(block)]):
                segment_longpulsesmeasures = snafs.get_longpulsemeasures(
                    block, i, segment,
                    **kwargs
                )
                for key in all_longpulsesmeasures:
                    all_longpulsesmeasures[key] += segment_longpulsesmeasures[key]

        self.longpulse_measures = pd.DataFrame(all_longpulsesmeasures).round(decimals=2)

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
            print('currently processing file: ' + datafile)
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
                if len(firstline) > 100:  #TrigIn file
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
                else:  #Dumper file
                    file_data = pd.read_table(datafile, header=None, skiprows=2)
                    sampling_interval_str = file.readline()
                    sampling_interval = float(
                        re.split('\t', sampling_interval_str)[0]) * pq.ms
                    sampling_interval = sampling_interval.rescale('s')
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
