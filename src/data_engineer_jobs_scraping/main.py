from re import compile, IGNORECASE
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

from src.data_engineer_jobs_scraping.helpers import human_scroll
from src.data_engineer_jobs_scraping.login import linkedin_login

driver = linkedin_login()

sleep(10)

print("Página atual:", driver.title)

driver.get("https://www.linkedin.com/jobs/search/?keywords=dados")

sleep(5)
scrollable_element = driver.find_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div")

human_scroll(driver, scrollable_element)

element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')
html_trecho = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_trecho, 'html.parser')

li_items = soup.find_all('li', id=compile('^ember'))
print(len(li_items))

# Extrair o texto de cada título de vaga
for job in li_items:
  try:
    title = job.find('span', {'aria-hidden': 'true'}).find('strong')
    if title:
      print(title.get_text(strip=True))
  except Exception as e:
    continue

sleep(90)
