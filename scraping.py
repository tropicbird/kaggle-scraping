from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
 


# driver = webdriver.Chrome('C:/Users/hdais/Dropbox/github/kaggle-ranking/driver/chromedriver_win32' + '/chromedriver')
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome('C:/Users/hdais/Dropbox/github/kaggle-ranking/driver/chromedriver_win32' + '/chromedriver',options=options)

#browser.get('https://www.kaggle.com/rankings?group=competitions')
browser.get('https://www.kaggle.com/rankings?group=datasets')
browser.get('https://www.kaggle.com/rankings?group=notebooks')
browser.get('https://www.kaggle.com/rankings?group=discussion')
element=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[5]/div[3]")
length=0

print('Scrolling Sarted')
while length<60000:
#while length<5000:
    tmp=length
    browser.execute_script("return arguments[0].scrollIntoView(false);", element)
    length=browser.execute_script("return arguments[0].scrollHeight", element)
    time.sleep(3)
    print(length)
    if tmp==length:
        break    
print('Scrolling Ended')

# from tqdm.notebook import tqdm
from tqdm import tqdm
import pickle
base=browser.find_elements_by_xpath('/html/body/main/div[1]/div/div[5]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div')[0]
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
#for i in tqdm(range(50)):
    try:
        userdata = base.find_element_by_xpath(f'div[{i+2}]/div/div')  
        rank=userdata.find_element_by_xpath('div[1]') .text
        tier=userdata.find_element_by_xpath('div[2]/img') .get_attribute('title')
        name=userdata.find_element_by_xpath('div[4]/p[1]/a') .text
        url=userdata.find_element_by_xpath('div[4]/p[1]/a') .get_attribute('href')
        gold=userdata.find_element_by_xpath('div[5]/div[1]/div[2]') .text
        silver=userdata.find_element_by_xpath('div[5]/div[2]/div[2]') .text
        bronze=userdata.find_element_by_xpath('div[5]/div[3]/div[2]') .text
        points=userdata.find_element_by_xpath('div[6]') .text
        points=points.replace(',','')
        
        rank_ls.append(rank)
        tier_ls.append(tier)
        name_ls.append(name)
        url_ls.append(url)
        gold_ls.append(gold)
        silver_ls.append(silver)
        bronze_ls.append(bronze)
        points_ls.append(points)
        #if i%100==0:
        #    print(i)
    except:
        print(f'Number of users: {i+1}')
        break
        
print('Scraping from the ranking ended')

dic_names=['rank','tier','name','url','gold','silver','bronze','points']
data_ls=[rank_ls,tier_ls,name_ls,url_ls,gold_ls,silver_ls,bronze_ls,points_ls]
dic=dict(zip(dic_names,data_ls))

with open('data_ranking.pkl','wb') as handle:
    pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('data_ranking.pkl', 'rb') as handle:
    dic = pickle.load(handle)
    
import requests
from bs4 import BeautifulSoup
import time
import json
country_ls=[]
region_ls=[]
city_ls=[]
occupation_ls=[]
organization_ls=[]

# import pickle5 as pickle
#with open('data_ranking.pkl', 'rb') as handle:
#    dic = pickle.load(handle)

with open('data_ranking.pkl', 'rb') as handle:
    dic = pickle.load(handle)

for i, link in enumerate(dic['url']):
    for j in range(3):  # 最大3回実行
        try:
            time.sleep(4)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            json_data = json.loads(soup.select('#site-body > script.kaggle-component')[0].contents[0][77:700].split('"bio":',1)[0][:-1]+'}')
            # print(json_data)
            country_ls.append(json_data['country'])
            region_ls.append(json_data['region'])
            city_ls.append(json_data['city'])
            occupation_ls.append(json_data['occupation'])
            organization_ls.append(json_data['organization'])
        #     break
        #    if i%50==0:
            print(i, link)
            break
        except:
            print(f'Try {j+1}')
            print('error')
            print(i, link)
    else:
        break        
        
dic['country']=country_ls
dic['region']=region_ls
dic['city']=city_ls
dic['occupation']=occupation_ls
dic['organization']=organization_ls

#print(dic)

print('saving pickle start')
with open('data_ranking_final.pkl','wb') as handle:
    pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('saving pickle end')

# !pip install pickle5
# import pickle5 as pickle
# with open('../input/top1000data/top_1000_comp_data.pkl', 'rb') as handle:
#     dic = pickle.load(handle)

print('saving csv start')
df=pd.DataFrame(dic).replace({np.nan: 'UNKOWN'})
#df.to_csv('top_1000_comp_data.csv',index=False)
df.to_csv('top_1000_dataset_data.csv',index=False)
print('saving csv end')