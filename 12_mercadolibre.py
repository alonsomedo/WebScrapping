from optparse import Option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

driver.get('https://listado.mercadolibre.com.pe/repuestos-autos-camionetas-bujia#D[A:repuestos%20autos%20camionetas%20bujia]')

driver.refresh()

while True:
    product_links = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element ui-search-link"]')
    page_links = []

    for link in product_links:
        page_links.append(link.get_attribute('href'))

    for link in page_links:
        try:
            driver.get(link)
            title = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]').text
            price = driver.find_element(By.XPATH, "//div[@class='ui-pdp-price__second-line']//span[@class='price-tag-fraction']").text 
            print('Producto: ', title)
            print('Precio: ', price.replace('\n', '').replace('\t', ''))
            print('********************************************************')
            # Return the the before page
            driver.back()

        except Exception as e:
            driver.back()
            print(e)

    try:
        next_button = driver.find_element(By.XPATH,'//span[text()="Siguiente"]')
        next_button.click()
    except Exception as e:
        break # When the next_button doesnt exist we stop the program
     
