from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def human_scroll(driver: WebDriver, element: WebElement = None, step=200, delay=0.1):
  if element:  # Scroll em um elemento específico
    last_height = driver.execute_script("return arguments[0].scrollHeight;", element)
    current_position = 0
    while current_position < last_height:
      current_position += step
      driver.execute_script("arguments[0].scrollTop = arguments[1];", element, current_position)
      sleep(delay)
  else:  # Scroll na página principal
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = driver.execute_script("return window.pageYOffset")
    while current_position < last_height:
      current_position += step
      driver.execute_script("window.scrollTo(0, arguments[0]);", current_position)
      sleep(delay)
