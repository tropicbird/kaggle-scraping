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
    # options.add_argument('--headless')
    # browser = webdriver.Chrome('/home/tropicbird/kaggle-scraping/chromedriver',options=options)
    browser = webdriver.Chrome('/Users/tropicbird/Dropbox/chromedriver/chromedriver-mac-arm64/chromedriver', options=options)
    # browser = webdriver.Chrome(service=Service('/Users/tropicbird/Dropbox/chromedriver/chromedriver_mac_arm64/chromedriver'), options=options)
    # service = webdriver.ChromeService(executable_path='/Users/tropicbird/Dropbox/chromedriver/chromedriver_mac_arm64/chromedriver')
    # browser = webdriver.Chrome(service=service, options=options)

    print(f'ranking_type: {ranking_type}')

    browser.get(f'https://www.kaggle.com/rankings?group={ranking_type}')
    print(browser)

    #In October 2021
    #element=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[5]/div[3]")

    #In November 2021
    #element=browser.find_element_by_xpath("/html/body/main/div[1]/div[1]/div[4]/div[3]")

    #September 2022
    #element=browser.find_element_by_xpath("/html/body/main/div[1]/div[1]/div[5]/div[2]")

    #November 2022
    #element=browser.find_element_by_xpath("/html/body/main/div[1]/div[1]/div[6]/div[2]")

    #December 2022
    # element1=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[6]/div[2]")
    # element2=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[6]")

    #August 2023
    # scroll_container=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[6]/div[2]/div/div[4]")
    scroll_container=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[6]/div[2]/div/div[4]/div/div/div[2]")
    # スクロール対象の要素の現在のスクロールの高さを取得
    current_scroll_position = browser.execute_script("return arguments[0].scrollTop", scroll_container)

    # スクロール対象の要素の全体の高さを取得
    total_height = browser.execute_script("return arguments[0].scrollHeight", scroll_container)

    length=0
    current_height=0
    cnt=0

    print('Scrolling Sarted')
    while length<800:
    # while length<500:
        tmp=length
        browser.execute_script("arguments[0].scrollTop += 100;", scroll_container)
        time.sleep(3)
        # スクロールの位置を更新
        # current_scroll_position += 500
        time.sleep(3)
        current_height=browser.execute_script("return arguments[0].scrollHeight", scroll_container)
        print(current_height)
        length=current_height
        if length==tmp:
            cnt+=1
        else:
            cnt=0
        if cnt==5:
            break
    print('Scrolling Ended')

    #In October 2021
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[5]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #In November 2021
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div[1]/div[4]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #September 2022
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div[1]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #November 2022
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div[1]/div[6]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #Dec 2022
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div[1]/div[6]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]')[0]
    #base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[6]/div[1]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #March 2023
    # base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[6]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]

    #August 2023
    base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[6]/div[2]/div/div[4]/div/div/div[2]/div/div')[0]

    rank_ls=[]
    tier_ls=[]
    name_ls=[]
    url_ls=[]
    gold_ls=[]
    silver_ls=[]
    bronze_ls=[]
    points_ls=[]

    print('Scraping from the ranking started')
    #for i in tqdm(range(1000)):
    for i in range(100):
        #userdata = base.find_element_by_xpath(f'div[{i+2}]/div/div')
        try:
            userdata = base.find_element_by_xpath(f'div[{i+1}]')
            #print(userdata)
            #/div[1]/p
            rank=userdata.find_element_by_xpath('div[1]').text
            #/div[2]/img
            tier=userdata.find_element_by_xpath('div[2]/img').get_attribute('alt')
            #/div[3]/div/div/a[2]
            name=userdata.find_element_by_xpath('div[3]/div/div/a[2]').text
            #/div[3]/div/div/a[1]
            url=userdata.find_element_by_xpath('div[3]/div/div/a[1]').get_attribute('href')
            #/div[3]/span[1]/text()
            gold=userdata.find_element_by_xpath('div[4]/span[1]').text

            #/div[3]/span[2]/text()
            silver=userdata.find_element_by_xpath('div[4]/span[2]').text

            #/div[3]/span[2]/text()
            bronze=userdata.find_element_by_xpath('div[4]/span[2]').text

            #/div[4]/p
            points=userdata.find_element_by_xpath('div[5]').text
            points=points.replace(',','')

            rank_ls.append(rank)
            tier_ls.append(tier)
            name_ls.append(name)
            url_ls.append(url)
            gold_ls.append(gold)
            silver_ls.append(silver)
            bronze_ls.append(bronze)
            points_ls.append(points)
        except Exception as e:
            print(e)
            print(f'Number of users: {i}')
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
        cnt=0
        for j in range(5):  # Try maximum 5 times
            print(i, link)
            try:
                time.sleep(7)
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
    with open('data_ranking_final.pkl','wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('saving pickle end')


    print('saving csv start')
    dt_now=datetime.datetime.now()
    df=pd.DataFrame(dic).replace({np.nan: 'UNKOWN'})
    # df.to_csv(f'results/{ranking_type}/top_1000_{ranking_type}_{dt_now.year}_{dt_now.month}.csv',index=False)
    df.to_csv(f'results/top_1000_{ranking_type}_{dt_now.year}_{dt_now.month}.csv',index=False)
    print('saving csv end')
