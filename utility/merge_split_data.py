from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('ranking',help='Select ranking types from competitions or datasets or notebooks or discussion')
args = parser.parse_args() 
ranking_type=args.ranking
print(f'ranking_type: {ranking_type}')


# from tqdm.notebook import tqdm
from tqdm import tqdm
import pickle

import requests
from bs4 import BeautifulSoup
import time
import json

# !pip install pickle5
# import pickle5 as pickle
with open('keep0_989/data_ranking_final.pkl', 'rb') as handle:
    dic1 = pickle.load(handle)
with open('keep990_999/data_ranking_final.pkl', 'rb') as handle:
    dic2 = pickle.load(handle)

l1=dic1['country']+dic2['country']
l2=dic1['region']+dic2['region']
l3=dic1['city']+dic2['city']
l4=dic1['occupation']+dic2['occupation']
l5=dic1['organization']+dic2['organization']

#l1=l1+dic3['country']
#l2=l2+dic3['region']
#l3=l3+dic3['city']
#l4=l4+dic3['occupation']
#l5=l5+dic3['organization'] 

#dic4['country']=l1+dic4['country']
#dic4['region']=l2+dic4['region']
#dic4['city']=l3+dic4['city']
#dic4['occupation']=l4+dic4['occupation']
#dic4['organization']=l5+dic4['organization']

dic2['country']=l1
dic2['region']=l2
dic2['city']=l3
dic2['occupation']=l4
dic2['organization']=l5

print('saving csv start')
df=pd.DataFrame(dic2).replace({np.nan: 'UNKOWN'})
#df.to_csv('top_1000_comp_data.csv',index=False)
#df.to_csv('top_1000_dataset_data.csv',index=False)
df.to_csv(f'top_1000_{ranking_type}_data.csv',index=False)
print('saving csv end')