import os
from datetime import date
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
from utils import chrome
from selenium.webdriver.support.select import Select
from utils import envio_correo

from glob import glob
import os


#ruta_descarga=chrome.ruta_descargas()
driver = chrome.opciones_chrome()

driver.get('https://selenium.dev/selenium/web/formPage.html')
select_element = driver.find_element(By.NAME, 'selectomatic')
select = Select(select_element)


two_element = driver.find_element(By.CSS_SELECTOR, 'option[value=two]')
four_element = driver.find_element(By.CSS_SELECTOR, 'option[value=four]')
count_element = driver.find_element(By.CSS_SELECTOR, "option[value='still learning how to count, apparently']")
select.select_by_visible_text('Four')
assert four_element.is_selected()