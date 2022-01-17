from optparse import Option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
from time import sleep

# Vertical scroling
# We get element on index 0
# It will do scroling until it reaches the pixel 20k.
scrolling_script = """
    document.getElementsByClassName("siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc")[0].scroll(0, 20000);
"""

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)

driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://www.google.com/maps/place/Amazonian+Restaurant/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423715!4d-3.6850997!9m1!1b1')

sleep(random.uniform(3,7))

SCROLLS = 0

while(SCROLLS != 3):
    driver.execute_script(scrolling_script)
    sleep(random.uniform(4,6))
    SCROLLS += 1

reviews = driver.find_elements(By.XPATH, '//div[@class="ODSEW-ShBeI NIyLF-haAclf gm2-body-2"]')

for review in reviews:
    userLink = review.find_element(By.XPATH, './/div[@class="ODSEW-ShBeI-tXxcle ODSEW-ShBeI-tXxcle-SfQLQb-menu"]')

    try:
        userLink.click() # We navigate to the new url.
        
        driver.switch_to.window(driver.window_handles[1]) # Index start in 0 , we need 1 to be in the profile of the user.

        # We navigate to the review tab and make a click on it.
        #review_tab = WebDriverWait(driver, 4).until(
        #    EC.presence_of_all_elements_located((By.XPATH, 'button[@data-tab-index="0"]'))
        #)
        #review_tab.click()

        # After clicking on REVIEWS TAB, We wait for all the comments to be loaded.
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc"]'))
        )

        USER_SCROLLS = 0

        while(USER_SCROLLS != 3):
            driver.execute_script(scrolling_script)
            sleep(random.uniform(4,6))
            USER_SCROLLS += 1

        user_reviews = driver.find_elements(By.XPATH, '//div[@class="ODSEW-ShBeI NIyLF-haAclf gm2-body-2 ODSEW-ShBeI-d6wfac ODSEW-ShBeI-SfQLQb-QFlW2 ODSEW-ShBeI-De8GHd-KE6vqe-purZT"]')

        for review in user_reviews:
            print(review)
            name_hotel = review.find_element(By.XPATH, './/div[@class="ODSEW-ShBeI-title ODSEW-ShBeI-title-juPPCf-SfQLQb-ShBeI-text"]/span').text
            comment = review.find_element(By.XPATH, './/div[@class="ODSEW-ShBeI-ShBeI-content"]/span[@jstcache="154"]').text
            score = review.find_element(By.XPATH, './/span[@jstcache="149"]').get_attribute('aria-label')

            print('HOTEL: ', name_hotel)
            print('SCORE: ', score)
            print('REVIEW: ', comment)
            print('****************************************************')

        driver.close()
        driver.switch_to.window(driver.window_handles[0]) # We need to return to index [0]

    except Exception as e:
        print('ERROR', e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])