from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import argparse
import pickle
import time
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description='')
parser.add_argument('--ranking',help='Select ranking types from competitions or datasets or notebooks or discussion',
                    default=['competitions','datasets','notebooks','discussion'])
args = parser.parse_args()

rank_lowest_num = 1000 #スクレイピングするランキングの下限順位

if type(args.ranking)==list:
    ranking_ls=args.ranking
else:
    ranking_ls=[args.ranking]

for ranking_type in ranking_ls:
    options = Options()
    #JavaScriptが組み込まれたので、ヘッドレスは無効にする
    # options.add_argument('--headless')
    browser = webdriver.Chrome('/Users/tropicbird/Dropbox/chromedriver/chromedriver-mac-arm64/chromedriver', options=options)
    print(f'ranking_type: {ranking_type}')

    browser.get(f'https://www.kaggle.com/rankings?group={ranking_type}')
    print(browser)

    #August 2023
    scroll_container=browser.find_element_by_xpath("/html/body/main/div[1]/div/div[6]/div[2]/div/div[4]/div/div/div[2]")
    # スクロール対象の要素の現在のスクロールの高さを取得
    current_scroll_position = browser.execute_script("return arguments[0].scrollTop", scroll_container)

    # スクロール対象の要素の全体の高さを取得
    total_height = browser.execute_script("return arguments[0].scrollHeight", scroll_container)

    length=0
    current_height=0
    cnt=0

    data = []
    rank_ls=[]
    tier_ls=[]
    name_ls=[]
    url_ls=[]
    gold_ls=[]
    silver_ls=[]
    bronze_ls=[]
    points_ls=[]

    print('Scrolling Sarted')
    while len(data) < rank_lowest_num:
        # 現在のテーブルデータを取得
        rows = browser.find_elements(By.CSS_SELECTOR, "div.MuiDataGrid-row[role='row']")
        for row in rows:
            link_element = row.find_element(By.CSS_SELECTOR, "a.sc-eIrltS.eRdaFm")
            href_value = link_element.get_attribute("href")
            # print(href_value)
            img_element = row.find_element(By.CSS_SELECTOR, "img[alt]")
            alt_value = img_element.get_attribute("alt")
            # print(alt_value)
            # print(row.text)
            row_data=[cell.replace(",","") for cell in row.text.split("\n")]
            row_data.append(href_value)
            row_data.append(alt_value)

            # cells = row.find_elements(By.TAG_NAME, "td")
            # row_data = [cell.text for cell in cells]
            if row_data not in data:
                print(row_data)
                data.append(row_data)
                rank_ls.append(row_data[0])
                name_ls.append(row_data[1])
                gold_ls.append(row_data[2])
                silver_ls.append(row_data[3])
                bronze_ls.append(row_data[4])
                points_ls.append(row_data[5])
                tier_ls.append(alt_value)
                url_ls.append(href_value)

        # スクロールダウン
        browser.execute_script("arguments[0].scrollTop += 500;", scroll_container)

        # スクロール後の読み込みを待つ
        time.sleep(2)


    print('Scrolling Ended')

    # 1000行を超えたデータをトリミング
    rank_ls=rank_ls[:rank_lowest_num]
    tier_ls=tier_ls[:rank_lowest_num]
    name_ls=name_ls[:rank_lowest_num]
    url_ls=url_ls[:rank_lowest_num]
    gold_ls=gold_ls[:rank_lowest_num]
    silver_ls=silver_ls[:rank_lowest_num]
    bronze_ls=bronze_ls[:rank_lowest_num]
    points_ls=points_ls[:rank_lowest_num]

    dic_names=['rank','tier','name','url','gold','silver','bronze','points']
    data_ls=[rank_ls,tier_ls,name_ls,url_ls,gold_ls,silver_ls,bronze_ls,points_ls]
    dic=dict(zip(dic_names,data_ls))

    browser.quit()

    with open(f'data_ranking_{ranking_type}.pkl','wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)