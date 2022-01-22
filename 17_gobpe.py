import requests
from lxml import html
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

response = requests.get('https://www.gob.pe/busquedas?reason=sheet&sheet=')
response.enconding = 'UTF-8'
parser = html.fromstring(response.text)

data = parser.xpath('//script[contains(text(), "window.initialData")]')[0].text_content()
index = data.find('{')
data = data[index:]

obj_data = json.loads(data)

results = obj_data['data']['attributes']['results']

for r in results:
    print(r['content'])

