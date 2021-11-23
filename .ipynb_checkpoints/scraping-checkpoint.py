from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
import argparse
import datetime
import gc
from tqdm import tqdm
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
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome('/home/tropicbird/kaggle-scraping/chromedriver',options=options)
    #browser = webdriver.Chrome('C:/Users/hdais/Dropbox/github/kaggle-ranking/driver/chromedriver_win32' + '/chromedriver',options=options)
    
    print(f'ranking_type: {ranking_type}')

    browser.get(f'https://www.kaggle.com/rankings?group={ranking_type}')
    print(browser)
    
    #In October 2021
    #element=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[5]/div[3]")
    
    #In November 2021
    element=browser.find_element_by_xpath("/html/body/main/div[1]/div[1]/div[4]/div[3]")
    length=0

    print('Scrolling Sarted')
    # while length<60000:
    while length<500:
        tmp=length
        browser.execute_script("return arguments[0].scrollIntoView(false);", element)
        length=browser.execute_script("return arguments[0].scrollHeight", element)
        time.sleep(3)
        print(length)
        if tmp==length:
            break    
    print('Scrolling Ended')
    
    #In October 2021
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[5]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]
    
    #In November 2021
    base=browser.find_elements_by_xpath('/html/body/main/div[1]/div[1]/div[4]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]
    rank_ls=[]
    tier_ls=[]
    name_ls=[]
    url_ls=[]
    gold_ls=[]
    silver_ls=[]
    bronze_ls=[]
    points_ls=[]

    print('Scraping from the ranking started')
    for i in tqdm(range(1000)):
        try:
            userdata = base.find_element_by_xpath(f'div[{i+2}]/div/div')  
            rank=userdata.find_element_by_xpath('div[1]').text
            tier=userdata.find_element_by_xpath('div[2]/img').get_attribute('title')
            name=userdata.find_element_by_xpath('div[4]/p[1]/a').text
            url=userdata.find_element_by_xpath('div[4]/p[1]/a').get_attribute('href')
            gold=userdata.find_element_by_xpath('div[5]/div[1]/div[2]').text
            silver=userdata.find_element_by_xpath('div[5]/div[2]/div[2]').text
            bronze=userdata.find_element_by_xpath('div[5]/div[3]/div[2]').text
            points=userdata.find_element_by_xpath('div[6]').text
            points=points.replace(',','')
            
            rank_ls.append(rank)
            tier_ls.append(tier)
            name_ls.append(name)
            url_ls.append(url)
            gold_ls.append(gold)
            silver_ls.append(silver)
            bronze_ls.append(bronze)
            points_ls.append(points)
        except:
            print(f'Number of users: {i+1}')
            break
        
    print('Scraping from the ranking ended')

    dic_names=['rank','tier','name','url','gold','silver','bronze','points']
    data_ls=[rank_ls,tier_ls,name_ls,url_ls,gold_ls,silver_ls,bronze_ls,points_ls]
    dic=dict(zip(dic_names,data_ls))

    browser.quit()
    
    with open('data_ranking.pkl','wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

    
    country_ls=[]
    region_ls=[]
    city_ls=[]
    occupation_ls=[]
    organization_ls=[]

    with open('data_ranking.pkl', 'rb') as handle:
        dic = pickle.load(handle)

    for i, link in enumerate(dic['url']):
        for j in range(3):  # Try maximum 3 times
            try:
                time.sleep(5)
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                json_data = json.loads(soup.select('#site-body > script.kaggle-component')[0].contents[0][77:700].split('"bio":',1)[0][:-1]+'}')
                country_ls.append(json_data['country'])
                region_ls.append(json_data['region'])
                city_ls.append(json_data['city'])
                occupation_ls.append(json_data['occupation'])
                organization_ls.append(json_data['organization'])
                print(i, link)
                break
            except:
                print(f'Try {j+1}')
                print('error')
                print(i, link)
                time.sleep(10)
        else:
            break        
        
    dic['country']=country_ls
    dic['region']=region_ls
    dic['city']=city_ls
    dic['occupation']=occupation_ls
    dic['organization']=organization_ls

    print('saving pickle start')
    with open('data_ranking_final.pkl','wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('saving pickle end')


    print('saving csv start')
    dt_now=datetime.datetime.now()
    df=pd.DataFrame(dic).replace({np.nan: 'UNKOWN'})
    df.to_csv(f'/home/tropicbird/ranking_dataset/top_1000_{ranking_type}_{dt_now.year}_{dt_now.month}.csv',index=False)
    print('saving csv end')