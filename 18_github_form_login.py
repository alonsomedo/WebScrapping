import requests
from lxml import html


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


login_url = 'https://github.com/login'

session = requests.Session()

login_response = requests.get(login_url, headers = headers)

parser = html.fromstring(login_response.text)

token = parser.xpath('//input[@name="authenticity_token"]/@value')

session_url = 'https://github.com/session'

login_data = {
  "login": open('./credentials.txt').readline().split(',')[0],
  "password": open('./credentials.txt').readline().split(',')[1],
  "commit": "Sign in", 
  "authenticity_token":  token
}

session.post(
    session_url,
    data = login_data,
    headers = headers
)

data_url = 'https://github.com/alonsomedo?tab=repositories'
response_data = session.get(data_url, headers = headers)
data_parser = html.fromstring(response_data.text)

repositories = data_parser.xpath('//h3[@class="wb-break-all"]/a/text()')

for r in repositories:
    print(r)



