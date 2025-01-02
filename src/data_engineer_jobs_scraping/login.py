from os import getenv
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

load_dotenv()

def linkedin_login():
    driver = webdriver.Chrome()

    url = "https://www.linkedin.com/login/pt"
    driver.get(url)

    sleep(1)

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    LINKEDIN_EMAIL = getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = getenv('LINKEDIN_PASSWORD')

    username_field.send_keys(LINKEDIN_EMAIL)
    password_field.send_keys(LINKEDIN_PASSWORD)

    login_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[@data-litms-control-urn='login-submit']"))
    )
    login_button.click()

    return driver
