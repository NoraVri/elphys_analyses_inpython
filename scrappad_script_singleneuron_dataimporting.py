# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:24:39 2020

@author: neert
"""
# %% imports
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgnl
import quantities as pq
from neo import io
from neo.core import Block, ChannelIndex, Segment

os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from singleneuron_class import SingleNeuron
# %%
#exampleData_pClamp = SingleNeuron("20190729A")



exampleData_SutterPatch = SingleNeuron("20200308D")
cell20200310C = SingleNeuron("20200310C")
#cell20200310G = SingleNeuron("20200310G") this one bugs out for some reason
cell20200312F = SingleNeuron("20200312F")

# %%
os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\\myData_nRiMLabRig")
reader = io.IgorIO(filename="20200308D.pxp")

signals = reader.read_analogsignal(path='root:SutterPatch:Data:R1_S1_spontactivity_CCmode')
