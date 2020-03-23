# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert
"""
import os
import matplotlib.pyplot as plt
os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from raw_data_reading import SingleNeuron_RawData
# %% abf files
emptycell_RawData = SingleNeuron_RawData("20190814")
cell20190814A_RawData = SingleNeuron_RawData("20190814A")
#cell20191119A_RawData = SingleNeuron_RawData("20191119A")
# %% plotting raw data
#this throws up a plot for each block that is read in
cell20190814A_RawData.plot_allrawdata()
# %%
file_toexcept = cell20190814A_RawData.rawdata_blocks[0].file_origin
cell20190814A_RawData.rawdata_remove_nonrecordingchannel(file_toexcept,2)

cell20190814A_RawData.plot_block_byname(file_toexcept)







# %% pxp files
cell20200310F_RawData = SingleNeuron_RawData("20200310F")
os.chdir(cell20200310F_RawData.file_path)
# %%
from neo import io
import igor
file_name = cell20200310F_RawData.file_path+'\\'+cell20200310F_RawData.name+'.pxp'
reader = io.IgorIO(filename=file_name)