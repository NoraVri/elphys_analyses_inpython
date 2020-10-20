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

# %% recorded neurons, ordered by date
## experiment: activation of inputs to IO neurons by ChR activation in Thy1 mouse
# (experiment days 20190527, 20190529, 20200630, 20200701, 20200706, 20200707, 20200708)
# singleneuron_data = SingleNeuron('20190527A')
#
### cell20190527B = SingleNeuron('20190527B')
#
### singleneuron_data = SingleNeuron('20190527C')
#
# singleneuron_data = SingleNeuron('20190529A1')
#
### cell20190529A2 = SingleNeuron('20190529A2')
#
# singleneuron_data = SingleNeuron('20190529B')
#
# singleneuron_data = SingleNeuron('20190529C')
#
# singleneuron_data = SingleNeuron('20190529D')
#
# singleneuron_data = SingleNeuron('20190529E')

## experiment: pharmacological blockage of inputs to IO neurons
# singleneuron_data = SingleNeuron('20190729A')

singleneuron_data = SingleNeuron('20190804A')

# singleneuron_data = SingleNeuron('20190804B')

# singleneuron_data = SingleNeuron('20190805A2')

# singleneuron_data = SingleNeuron('20190805B1')

# singleneuron_data = SingleNeuron('20190805B2')

# singleneuron_data = SingleNeuron('20190812A')

# singleneuron_data = SingleNeuron('20190812B')

# singleneuron_data = SingleNeuron('20190814A')

# singleneuron_data = SingleNeuron('20190815D1')

# singleneuron_data = SingleNeuron('20191105A1')

# singleneuron_data = SingleNeuron('20191105A2')

# singleneuron_data = SingleNeuron('20191105C')

# singleneuron_data = SingleNeuron('20191106A1')

# singleneuron_data = SingleNeuron('20191106A2')

# singleneuron_data = SingleNeuron('20191119A')

# singleneuron_data = SingleNeuron('20191119B')

# singleneuron_data = SingleNeuron('20191120A')

# singleneuron_data = SingleNeuron('20191120B1')

# singleneuron_data = SingleNeuron('20191120B2')

## experiment: activation of inputs to IO neurons by rubiGlu-uncaging
# (experiment days 20200306, 20200308, 20200310 and 20200312)
### singleneuron_data = SingleNeuron('20200306C')
#
### singleneuron_data = SingleNeuron('20200308B')
#
### singleneuron_data = SingleNeuron('20200308C')
#
### singleneuron_data = SingleNeuron('20200308D')
#
### singleneuron_data = SingleNeuron('20200308E')
#
### singleneuron_data = SingleNeuron('20200310G')
#
### singleneuron_data = SingleNeuron('20200312C')
#
### singleneuron_data = SingleNeuron('20200312G')

## experiment: activation of inputs to IO neurons by ChR activation in Thy1 mouse
# (experiment days 20190527, 20190529, 20200630, 20200701, 20200706, 20200707, 20200708)
# singleneuron_data = SingleNeuron('20200630A')
#
# singleneuron_data = SingleNeuron('20200630B1')
#
# singleneuron_data = SingleNeuron('20200630B2')
#
# singleneuron_data = SingleNeuron('20200630C')
#
# singleneuron_data = SingleNeuron('20200630D')
#
# singleneuron_data = SingleNeuron('20200701A')

# singleneuron_data = SingleNeuron('20200701B')

# singleneuron_data = SingleNeuron('20200701D')

# singleneuron_data = SingleNeuron('20200706B')

# singleneuron_data = SingleNeuron('20200706D')

# singleneuron_data = SingleNeuron('20200706E')

# singleneuron_data = SingleNeuron('20200708C')

# singleneuron_data = SingleNeuron('20200708D')

# singleneuron_data = SingleNeuron('20200708F')

### singleneuron_data = SingleNeuron('20200708G')

## experiment: activation of inputs to IO neurons by ChR activation in RBP mouse
# (experiment days 20200805, 20200818, 20200819)
# singleneuron_data = SingleNeuron('20200818B')

# singleneuron_data = SingleNeuron('20200818C')


# %% plotting data

singleneuron_data.plot_rawdatablocks(time_axis_unit='s')
singleneuron_data.get_blocknames()
# %% setting parameters for get_depolarizingevents for each neuron
# neuron20190527A: used block no.12 to find good parameter settings
# neuron20190527B: used block no.2 to find good parameter settings
# neuron20190529A1: used block no.2  to find good parameter settings
# neuron20190529B: used block no.14 to find good parameter settings
# neuron20190529C: used block no.3 to find good parameter settings
# neuron20190529D: used block no.2 to find good parameter settings
# neuron20190529E: used block no.2 to find good parameter settings
# neuron20190729A: used block no.1 to find good parameter settings, time-sliced 180-280

# neuron20190814A: used block no.0 to find good parameter settings

# neuron20200708G: used block no.3 to find good parameter settings


block_no = 1
segment_no = 0
time_slice = [180, 280]

(eventmeasures_dict,
 depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
                                                                                      return_dicts=True,
                                                                                      time_slice=time_slice,
                                    # min_depolspeed=0.1,
                                    # min_depolamp=0.2,
                                    # depol_to_peak_window=5,
                                    # event_width_window=40,
                                    ahp_width_window=200,
                                    # noisefilter_hpfreq=3000,
                                    # oscfilter_lpfreq=20,
                                    # ttleffect_window=None,
)

# %% when satisfied with settings, adding them onto singleneuron_data instance
singleneuron_data.rawdata_readingnotes['getdepolarizingevents_settings'] = depolevents_readingnotes_dict
singleneuron_data.write_results()
