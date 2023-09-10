import time
import pandas as pd
import numpy as np
import argparse
import datetime
import pickle
import requests
from bs4 import BeautifulSoup
import time
import json

parser = argparse.ArgumentParser(description='')
parser.add_argument('--ranking',help='Select ranking types from competitions or datasets or notebooks or discussion',
                    default=['competitions','datasets','notebooks','discussion'])
args = parser.parse_args()

if type(args.ranking)==list:
    ranking_ls=args.ranking
else:
    ranking_ls=[args.ranking]

for ranking_type in ranking_ls:
    country_ls=[]
    region_ls=[]
    city_ls=[]
    occupation_ls=[]
    organization_ls=[]

    with open(f'data_ranking_{ranking_type}.pkl', 'rb') as handle:
        dic = pickle.load(handle)

    for i, link in enumerate(dic['url']):
        cnt=0
        for j in range(5):  # Try maximum 5 times
            print(i, link)
            try:
                time.sleep(7) # 7秒待機
                if cnt:
                    print('response')

                response = requests.get(link)
                #print(f"!!!response!!!{response}")
                if cnt:
                    print('soup')
                soup = BeautifulSoup(response.text, 'html.parser')
                #print(f"!!!soup!!!{soup}")
                #print(soup.select('#site-body > script.kaggle-component')[0].contents[0][77:7000])
                if cnt:
                    print('json_data')
                    print(soup.select('#site-body > div > script.kaggle-component')[0].contents[0])

                json_data = json.loads(soup.select('#site-body > script.kaggle-component')[0].contents[0][77:].split('"userLastActive":',1)[0][:-1]+'}')
                #2023, February
                #json_data = json.loads(soup.select('#site-body > div > script.kaggle-component')[0].contents[0][77:].split('"userLastActive":',1)[0][:-1]+'}')
                #print(json_data)
                try:
                    country_ls.append(json_data['country'])
                except KeyError:
                    country_ls.append(np.nan)
                try:
                    region_ls.append(json_data['region'])
                except KeyError:
                    region_ls.append(np.nan)
                try:
                    city_ls.append(json_data['city'])
                except KeyError:
                    city_ls.append(np.nan)
                try:
                    occupation_ls.append(json_data['occupation'])
                except KeyError:
                    occupation_ls.append(np.nan)
                try:
                    organization_ls.append(json_data['organization'])
                except KeyError:
                    organization_ls.append(np.nan)
                break
            except Exception as e:
                print(f'Try {j+1}')
                print(e)
                cnt=1
                time.sleep(100)
        else:
            break

    dic['country']=country_ls
    dic['region']=region_ls
    dic['city']=city_ls
    dic['occupation']=occupation_ls
    dic['organization']=organization_ls

    print('saving pickle start')
    with open(f'data_ranking_{ranking_type}_final.pkl','wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('saving pickle end')

    print('saving csv start')
    dt_now=datetime.datetime.now()
    df=pd.DataFrame(dic).replace({np.nan: 'UNKOWN'})
    # df.to_csv(f'results/{ranking_type}/top_1000_{ranking_type}_{dt_now.year}_{dt_now.month}.csv',index=False)
    df.to_csv(f'results/top_1000_{ranking_type}_{dt_now.year}_{dt_now.month}.csv',index=False)
    print('saving csv end')
