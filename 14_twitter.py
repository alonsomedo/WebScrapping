from optparse import Option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
from time import sleep


credentials = open('credentials.txt').readline().strip().split(',')
user = credentials[0]
password = credentials[1]

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)

driver = webdriver.Chrome()

driver.get('https://twitter.com/i/flow/login')

driver.refresh()

sleep(random.uniform(2,3))

input_user = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]'))
)

input_user.send_keys(user)

sleep(random.uniform(2,3))

next_button = driver.find_element(By.XPATH, '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]')
next_button.click()


########### Temporal #################
input_user = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]'))
)

input_user.send_keys("941851494")

next_button = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-peo1c r-1ps3wis r-1ny4l3l r-1guathk r-o7ynqc r-6416eg r-lrvibr"]'))
)
next_button.click()


########### Temporal #################

sleep(random.uniform(2,3))
password_user = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]'))
)

password_user.send_keys(password)

sleep(random.uniform(2,3))
next_button = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]'))
)
next_button.click()


tweets = WebDriverWait(driver, 10).until(
  EC.presence_of_all_elements_located((By.XPATH, '//section//article//div[@dir="auto"]'))
)

for tweet in tweets:
    print(tweet.text)





