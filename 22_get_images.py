import requests
from PIL import Image
import io
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec/autos_c378')

# We refresh the page to solve a bug
driver.refresh()

for i in range(2):
    try:
        # We wait until the Load Button is loaded.
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

        button.click()

        # We wait until of the elements of the DOM get a value.
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
    except:
        print("Something Happens")
        break


driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
# Para asegurarme que todas las imagenes han sido cargadas, hago un scrolling hasta 
# bien abajo en la pagina (20mil pixeles, podria necesitar mas pixeles eventualmente)
driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)

# All the elements of a list
cars = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')
i = 0 

for c in cars:
    price = c.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
    description = c.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text
    print(price)
    print(description)
    
    try:
        url = c.find_element(By.XPATH, './/img').get_attribute('src')
        img_content = requests.get(url).content
        img_file = io.BytesIO(img_content)
        img = Image.open(img_file).convert('RGB')

        path = './images/' + str(i) + '.jpg'
        with open(path, 'wb') as f:
            img.save(f, "JPEG", quality=85)

    except:
        None

    i += 1

