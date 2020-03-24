# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert
"""
import os
import matplotlib.pyplot as plt
os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from raw_data_reading import SingleNeuron_RawData
from single_neuron_analyses import SingleNeuron_Analyses
# %% abf files
#emptycell_RawData = SingleNeuron_RawData("20190814")
cell20190814A_RawData = SingleNeuron_RawData("20190814A")
#cell20191119A_RawData = SingleNeuron_RawData("20191119A")
# %% plotting raw data
#this throws up a plot for each block that is read in
cell20190814A_RawData.plot_allrawdata()
# %% cleanup
file_toexcept = cell20190814A_RawData.rawdata_blocks[0].file_origin #in this block, there are 2 recording channels active but only Ch1 is actually recording from a neuron
cell20190814A_RawData.rawdata_remove_nonrecordingchannel(file_toexcept,2)
#cell20190814A_RawData.plot_block_byname(file_toexcept)

# %% fast-events analyses
cell20190814A_Analyses = SingleNeuron_Analyses(cell20190814A_RawData.name)
#workflow:
#use staticmethod SingleNeuron_Analyses.singlevoltagetrace_find_depolarizingevents_peaksidcs
#on a single, representative segment for that neuron/block and play with parameters (min_event_amplitude and peak_height)
#until the results look good (plotting of detected peaks is built in.)
#Repeat for other data blocks to see consistency.
#SingleNeuron_Analyses.singlevoltagetrace_find_depolarizingevents_peaksidcs(cell20190814A_RawData.rawdata_blocks[0].segments[0])

#then, call SingleNeuronName_Analyses.get_depolarizingevents_fromRawData()
cell20190814A_Analyses.get_depolarizingevents_fromRawData(cell20190814A_RawData,min_event_amplitude=0.2)




# %% pxp files
cell20200310F_RawData = SingleNeuron_RawData("20200310F")
os.chdir(cell20200310F_RawData.file_path)
# %%
from neo import io
import igor
file_name = cell20200310F_RawData.file_path+'\\'+cell20200310F_RawData.name+'.pxp'
reader = io.IgorIO(filename=file_name)