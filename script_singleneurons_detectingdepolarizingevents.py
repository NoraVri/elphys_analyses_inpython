import os
import json
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

# currently working on a dataset of neurons with >10min. of recording and some manipulation of inputs to IO neurons
# (evoked by activating axons arriving to the olive, or pharmacologically blocked).
# recordings that are listed here but do not fit the criteria are marked with '###'

# %% running get_depolarizingevents function on a batch of neurons
# resultsfolderpath = "D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me\\myResults"
# storedparams_jsonfiles = [file for file in os.listdir(resultsfolderpath) if file.endswith('json')]
# depolevents_tables = [file for file in os.listdir(resultsfolderpath) if 'depolarizing_events' in file]
#
# for storedparamsfile in storedparams_jsonfiles:
#     cell_name = storedparamsfile[0:10]
#     cell_name = cell_name.split('_')[0]
#     cell_depolevents = [file for file in depolevents_tables if cell_name in file]
#     if not cell_depolevents:
#         resultsfilepath = resultsfolderpath + '\\' + storedparamsfile
#         with open(resultsfilepath, 'r') as file:
#             storedresultsfile = json.loads(file.read())
#         if 'getdepolarizingevents_settings' in storedresultsfile.keys():
#             print(cell_name)
#             singleneuron_data = SingleNeuron(cell_name)
#             singleneuron_data.get_depolarizingevents_fromrawdata()
#             singleneuron_data.write_results()
#             del singleneuron_data



# %% plotting the raw data

singleneuron_data.plot_rawdatablocks(time_axis_unit='s')
singleneuron_data.get_blocknames()
# %% setting parameters for get_depolarizingevents for each neuron
# neuron20190527A: used block no.12 to find good parameter settings
# neuron20190527B: used block no.2 to find good parameter settings


# neuron20200708G: used block no.3 to find good parameter settings

# neuron20200818C: used block no.0 to find good parameter settings

# neuron20201116B: used blocks 0, 1 and 3

block_no = 3
segment_no = 3
# time_slice = [100, 250]

(eventmeasures_dict,
 depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
                                                                                      return_dicts=True,
                                                                                      # time_slice=time_slice,
                                    min_depolspeed=0.3,
                                    # min_depolamp=0.3,
                                    # depol_to_peak_window=5,
                                    # event_width_window=40,
                                    # ahp_width_window=10,
                                    noisefilter_hpfreq=2500,
                                    oscfilter_lpfreq=10,
                                    ttleffect_window=2500,
)

# %% when satisfied with settings, adding them onto singleneuron_data instance
singleneuron_data.rawdata_readingnotes['getdepolarizingevents_settings'] = depolevents_readingnotes_dict
singleneuron_data.write_results()


