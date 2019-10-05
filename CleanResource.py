# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 01:07:18 2019

@author: 19799
"""


import pandas as pd
import numpy as np
import os
os.chdir('E:\\606 adv db\\io')
resources = pd.read_csv('Resources.csv')
finalop_split=np.array_split(resources,5)
finalop_split[0].to_csv('PipedResources1.csv',sep='|',index=False)
finalop_split[1].to_csv('PipedResources2.csv',sep='|',index=False)
finalop_split[2].to_csv('PipedResources3.csv',sep='|',index=False)
finalop_split[3].to_csv('PipedResources4.csv',sep='|',index=False)
finalop_split[4].to_csv('PipedResources4.csv',sep='|',index=False)