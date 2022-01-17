import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec/autos_c378')

# Forcing a sleep
sleep(3)

# We refresh the page to solve a bug
driver.refresh()

# Forcing a sleep
sleep(5)

button = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')

for i in range(3):
    try:
        button.click()
        sleep(random.uniform(3.0, 7.0))
        button = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        print("Something Happens")
        break

# All the elements of a list
cars = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for c in cars:
    price = c.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
    description = c.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text
    print(price)
    print(description)



