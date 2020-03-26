# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert
"""
import os
import matplotlib.pyplot as plt
os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from singleneuron_class import SingleNeuron
# %% abf files
#emptycell_RawData = SingleNeuron("20190814")
rawdata_20190814A = SingleNeuron("20190814A")
#cell20191119A_RawData = SingleNeuron("20191119A")
# %% plotting raw data
#this throws up a plot for each block that is read in
rawdata_20190814A.plot_allrawdata()
# %% cleanup
file_toexcept = rawdata_20190814A.rawdata_blocks[0].file_origin #in this block, there are 2 recording channels active but only Ch1 is actually recording from a neuron
rawdata_20190814A.rawdata_remove_nonrecordingchannel(file_toexcept,2)
rawdata_20190814A.plot_block_byname(file_toexcept)
#TODO: adjust code to record which files are getting excepted, and save this information

# %% fast-events analyses
rawdata_20190814A.get_depolarizingevents_fromRawData()



# %% pxp files
cell20200310F_RawData = SingleNeuron_RawData("20200310F")
os.chdir(cell20200310F_RawData.file_path)
# %%
from neo import io
import igor
file_name = cell20200310F_RawData.file_path+'\\'+cell20200310F_RawData.name+'.pxp'
reader = io.IgorIO(filename=file_name)