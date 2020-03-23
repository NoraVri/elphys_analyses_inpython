# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:33:29 2020

@author: neert

This file defines a class for working with depolarizing events.
"""
# %% imports
import os
import json
# %%
class SingleNeuron_analyses:

    def __init__(self, singleneuron_name, path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\\elphysData_recordedByMe"):
        self.name = singleneuron_name
        self.depolarizing_events = []

    def getstoredresults(self):
        for folder_name in os.listdir(self.path):
            if folder_name.startswith('myResults'):
                os.chdir(self.path+folder_name)

                for file in os.listdir():
                    if self.name in file:
                        with open(f'{self.name}.json','r') as file:
                            data = json.load(file)
                            if data.get('depolarizing_events'):
                                self.depolarizing_events = data['depolarizing_events']


