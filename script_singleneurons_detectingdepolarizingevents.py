import os
import json
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

# %% list of neurons with light-evoked responses recordings
## experiment: activation of inputs to IO neurons by ChR activation in Thy1 mouse (experiment days 20190527, 20190529, 20200630 and 20200701)
# singleneuron_data = SingleNeuron('20190527A')

# cell20190527B = SingleNeuron('20190527B')
#
# singleneuron_data = SingleNeuron('20190527C')
#
# singleneuron_data = SingleNeuron('20190529A1')

# cell20190529A2 = SingleNeuron('20190529A2')
#
# singleneuron_data = SingleNeuron('20190529B')
#
# singleneuron_data = SingleNeuron('20190529C')
#
# singleneuron_data = SingleNeuron('20190529D')
#
# singleneuron_data = SingleNeuron('20190529E')
#

## experiment: pharmacological blockage of inputs to IO neurons
singleneuron_data = SingleNeuron('20190814A')

## experiment: activation of inputs to IO neurons by ChR activation in Thy1 mouse
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


## experiment: activation of inputs to IO neurons by rubiGlu-uncaging (experiment days 20200306, 20200308, 20200310 and 20200312)
#
# singleneuron_data = SingleNeuron('20200306C')
#
# singleneuron_data = SingleNeuron('20200308B')
#
# singleneuron_data = SingleNeuron('20200308C')
#
# singleneuron_data = SingleNeuron('20200308D')
#
# singleneuron_data = SingleNeuron('20200308E')
#
# singleneuron_data = SingleNeuron('20200310G')
#
# singleneuron_data = SingleNeuron('20200312C')
#
# singleneuron_data = SingleNeuron('20200312G')


## experiment:
# singleneuron_data = SingleNeuron('20200708F')



# singleneuron_data.plot_rawdatablocks()
# singleneuron_data.get_blocknames()
# %% setting parameters for get_depolarizingevents for each neuron
# neuron20190527A: used block no.12 to find good parameter settings
# neuron20190527B: used block no.2 to find good parameter settings
# neuron20190529A1: used block no.2  to find good parameter settings
# neuron20190529B: used block no.14 to find good parameter settings
# neuron20190529C: used block no.3 to find good parameter settings
# neuron20190529D: used block no.2 to find good parameter settings
# neuron20190529E: used block no.2 to find good parameter settings

# neuron20190814A: used block no.0 to find good parameter settings

# neuron20200708G: used block no.3 to find good parameter settings


block_no = 4
segment_no = 0

(eventmeasures_dict,
 depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
                                                                                      return_dicts=True,
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
# %% running get_depolarizingevents function on a batch of neurons

resultsfolderpath = "D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me\\myResults"
storedparams_jsonfiles = [file for file in os.listdir(resultsfolderpath) if file.endswith('json')]
depolevents_tables = [file for file in os.listdir(resultsfolderpath) if 'depolarizing_events' in file]

for storedparamsfile in storedparams_jsonfiles:
    cell_name = storedparamsfile[0:10]
    cell_name = cell_name.split('_')[0]
    cell_depolevents = [file for file in depolevents_tables if cell_name in file]
    if not cell_depolevents:
        resultsfilepath = resultsfolderpath + '\\' + storedparamsfile
        with open(resultsfilepath, 'r') as file:
            storedresultsfile = json.loads(file.read())
        if 'getdepolarizingevents_settings' in storedresultsfile.keys():
            print(cell_name)
            singleneuron_data = SingleNeuron(cell_name)
            singleneuron_data.get_depolarizingevents_fromrawdata()
            singleneuron_data.write_results()
