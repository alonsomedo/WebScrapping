import requests
from lxml import html


"""
- Cuando hacemos requerimientos hay informacion adicional que viene, los ENCABEZADOS.
- Estos encabezados tienen informacion adicional, entre estos hay una variable llamada USER-AGENT
- Esta variable le dice al servidor de que navegador se hace el request y cual es el sistema operativo 
- Por defecto esta variable user-agent va identificarlo como ROBOT, por lo mismo tenemos que sobreescribirla
"""

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url = "https://www.wikipedia.org/"

response = requests.get(url, headers=headers)

parser = html.fromstring(response.text)

english = parser.get_element_by_id("js-link-box-en")

english = parser.xpath("//a[@id='js-link-box-en']/strong/text()")

languages = parser.xpath("//a[contains(@id, 'js-link-box')]/strong/text()")

#for language in languages:
#    print(language)

languages_2 = parser.find_class('central-featured-lang')

for language in languages_2:
    print(language.text_content())