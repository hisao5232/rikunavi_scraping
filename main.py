from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

detail_list=[]
company_href_list=[]

def get_detail():
    #企業情報取得
    name=driver.find_element(By.CSS_SELECTOR,"h1>a").text
    jigyo=driver.find_element(By.XPATH,"//th[contains(text(), '事業内容')]/following-sibling::td[1]").text
    year=driver.find_element(By.XPATH,"//th[contains(text(), '設立')]/following-sibling::td[1]").text
    shihon=driver.find_element(By.XPATH,"//th[contains(text(), '資本金')]/following-sibling::td[1]").text
    uriage=driver.find_element(By.XPATH,"//th[contains(text(), '売上高')]/following-sibling::td[1]").text
    ceo=driver.find_element(By.XPATH,"//th[contains(text(), '代表者')]/following-sibling::td[1]").text
    ceo=ceo.replace('\u3000', ' ')
    address=driver.find_element(By.XPATH,"//th[contains(text(), '事業所')]/following-sibling::td[1]").text
    address=address.replace('\n', ' ')
    try:
        homepage=driver.find_element(By.XPATH,"//th[contains(text(), 'ホームページ')]/following-sibling::td[1]").text
    except:
        homepage="なし"
        
    dict_detail={"会社名":name,"事業内容":jigyo,"設立":year,"資本金":shihon,"売上高":uriage,"代表者":ceo,"住所":address,"ホームページ":homepage}
    print(dict_detail)
    detail_list.append(dict_detail)

def get_company_href():
    #各企業のトップページの要素取得
    company_elems=driver.find_elements(By.CSS_SELECTOR,"h2>a")

    #それぞれのhrefをリストの格納
    for company_elm in company_elems:
        company_href=company_elm.get_attribute("href")
        company_href_list.append(company_href)

def access_company_top():
    #企業トップページアクセス
    for company_top in company_href_list:
        driver.get(company_top)
        time.sleep(2)
        #企業情報取得
        get_detail()
        time.sleep(2)

#リクナビトップページにアクセス
driver.get("https://job.rikunabi.com/2026/company/")
time.sleep(3)

#業種からメーカーすべてをチェック
driver.find_element(By.CSS_SELECTOR,"div.mp_company_various_cont > div:nth-child(1) > div > label").click()
time.sleep(1)

#検索ボタンクリック
driver.find_element(By.CSS_SELECTOR,"div.mp_company_various_cs>div>p>a").click()
time.sleep(2)

#企業トップページhref取得
get_company_href()

#各企業のトップページにアクセス
access_company_top()

while True:
    try:
        #ページ送り出来るなら
        driver.find_element(By.CSS_SELECTOR,"a.ts-p-search-pager01-list-item_next").click()
        time.sleep(2)
        get_company_href()
        time.sleep(2)
        access_company_top()
        time.sleep(2)
    
    except:
        break
    
driver.quit()