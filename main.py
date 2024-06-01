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
    name=driver.find_element(By.CSS_SELECTOR,"h1>a").text
    jigyo=driver.find_element(By.XPATH,"//th[contains(text(), '事業内容')]/following-sibling::td[1]").text
    year=driver.find_element(By.XPATH,"//th[contains(text(), '設立')]/following-sibling::td[1]").text
    shihon=driver.find_element(By.XPATH,"//th[contains(text(), '資本金')]/following-sibling::td[1]").text
    uriage=driver.find_element(By.XPATH,"//th[contains(text(), '売上高')]/following-sibling::td[1]").text
    ceo=driver.find_element(By.XPATH,"//th[contains(text(), '代表者')]/following-sibling::td[1]").text
    ceo=ceo.replace('\u3000', ' ')
    address=driver.find_element(By.XPATH,"//th[contains(text(), '事業所')]/following-sibling::td[1]").text
    address=address.replace('\n', ' ')
    homepage=driver.find_element(By.XPATH,"//th[contains(text(), 'ホームページ')]/following-sibling::td[1]").text

    dict_detail={"会社名":name,"事業内容":jigyo,"設立":year,"資本金":shihon,"売上高":uriage,"代表者":ceo,"住所":address,"ホームページ":homepage}
    detail_list.append(dict_detail)




driver.get("https://job.rikunabi.com/2026/company/")
time.sleep(3)

driver.find_element(By.CSS_SELECTOR,"div.mp_company_various_cont > div:nth-child(1) > div > label").click()
time.sleep(1)

driver.find_element(By.CSS_SELECTOR,"div.mp_company_various_cs>div>p>a").click()
time.sleep(2)

company_elems=driver.find_elements(By.CSS_SELECTOR,"h2>a")

for company_elm in company_elems:
    company_href=company_elm.get_attribute("href")
    company_href_list.append(company_href)

driver.get(company_href_list[0])
time.sleep(2)

get_detail()
time.sleep(3)

print(detail_list)

time.sleep(3)
driver.quit()