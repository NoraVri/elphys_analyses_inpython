# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import singleneuron_plotting_functions as plots

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

results_path = path + '\\myResults'
resultsfiles_all = os.listdir(results_path)
resultsfiles_ttl = [filename for filename in resultsfiles_all if 'ttl' in filename]
resultsfiles_des = [filename for filename in resultsfiles_all if 'depolarizing_events' in filename]


for filename in resultsfiles_ttl:
    cell_name = re.split('_', filename)[0]
    ttlonmeasures_filepath = results_path + '\\' + filename
    cell_ttlonmeasures = pd.read_csv(ttlonmeasures_filepath)
    des_df_filepath = results_path + '\\' + [filename for filename in resultsfiles_des if filename.startswith(cell_name)][0]
    cell_des_df = pd.read_csv(des_df_filepath)
    has_neatevents = ('neat_event' in cell_des_df.columns)
    if has_neatevents:
        neat_blocks_fileorigins = cell_des_df.file_origin[cell_des_df.neat_event].unique()
        ttlon_blocks_fileorigins = cell_ttlonmeasures.file_origin
        neat_ttlonblocks_fileorigins = cell_ttlonmeasures.file_origin.isin(neat_blocks_fileorigins)
        if sum(neat_ttlonblocks_fileorigins) > 0:
            neat_ttlon_measures = cell_ttlonmeasures[neat_ttlonblocks_fileorigins]
            neat_ttlon_measures.plot.scatter('baselinev', 'response_maxdvdt')
            plt.title(cell_name + ' neat files only')

            neuron_data = SingleNeuron(cell_name)
            neuron_data.plot_rawdatatraces_ttlaligned(*neat_ttlon_measures.file_origin.unique())

# criteria I made up for fastevent detection in the evoked response, based on seeing them in these 'neat' responses:
# at baselineV > -65mV, 0.4 < response_maxdVdt < 2 means a fastevent was included.
# response_maxdvdt > 8 definitely indicates AP; and I'm not sure what's up with responses with 2 < maxdvdt < 8 (they tend to happen in the less nice recordings).
# %% plot: maxdVdt of subthreshold response (at baselineV > -65mV)
# twice: for neurons with and without at least one evokedAP

i = 0
j = 0
figure1, axes = plt.subplots(1,2,squeeze=True, sharex='row', sharey='row')
axis1 = axes[0]
axis2 = axes[1]

for filename in resultsfiles_ttl:
    ttlonmeasures_filepath = results_path + '\\' + filename
    cell_ttlonmeasures = pd.read_csv(ttlonmeasures_filepath)
    cell_name = re.split('_t', filename)[0]
    baselinevrange_ttlonmeasures = cell_ttlonmeasures[
        ((cell_ttlonmeasures.baselinev > -65) & (cell_ttlonmeasures.baselinev < -30))]
    evoked_aps = (baselinevrange_ttlonmeasures.response_maxdvdt >= 8)
    subthreshold_events = baselinevrange_ttlonmeasures[(baselinevrange_ttlonmeasures.response_maxdvdt < 2)]
    if sum(evoked_aps) > 0:
        i += 1
        subthresholdevents_maxdvdt = subthreshold_events.response_maxdvdt
        jitter = np.random.uniform(-0.2, 0.2, size=len(subthresholdevents_maxdvdt))
        scatter_is = np.ones([len(subthresholdevents_maxdvdt)]) * i + jitter
        axis1.scatter(scatter_is, subthresholdevents_maxdvdt, label=cell_name)
    else:
        j += 1
        subthresholdevents_maxdvdt = subthreshold_events.response_maxdvdt
        jitter = np.random.uniform(-0.2, 0.2, size=len(subthresholdevents_maxdvdt))
        scatter_js = np.ones([len(subthresholdevents_maxdvdt)]) * j + jitter
        axis2.scatter(scatter_js, subthresholdevents_maxdvdt, label=cell_name)
axis1.set_title('at least one AP evoked')
axis1.set_xlabel('neuron #')
axis1.set_ylabel('lightresponse maxdvdt')
axis1.legend(bbox_to_anchor=(1.04, 1))
axis2.set_title('no APs evoked')
axis2.set_xlabel('neuron #')
axis2.set_ylabel('lightresponse maxdvdt')
axis2.legend(bbox_to_anchor=(1.04, 1), loc='upper left')