from selenium import webdriver
from selenium.webdriver.common.by import By
print("starting webdriver")
driver = webdriver.Firefox()
print("getting webpage")
driver.get("https://www.allareacodes.com/")
result = driver.find_elements(By.XPATH, "//select[@style='width: 100%; margin-right: 2px']")
area_code_and_place = result.text.split("\n")

