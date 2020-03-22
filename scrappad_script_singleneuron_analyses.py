# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert
"""
import os
os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from raw_data_reading import SingleNeuron_RawData
# %%
emptycell_RawData = SingleNeuron_RawData("20190814")
cell20190814A_RawData = SingleNeuron_RawData("20190814A")
cell20191119A_RawData = SingleNeuron_RawData("20191119A")
# %% plotting raw data
#this throws up a plot for each block that is read in
cell20190814A_RawData.allrawdata_plotter()
# %%
cell20200310F_RawData = SingleNeuron_RawData("20200310F")
