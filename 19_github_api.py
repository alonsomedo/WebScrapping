import requests
from lxml import html
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

endpoint = 'https://api.github.com/user/repos?page=1'

credentials = open('./credentials.txt').readline().split(',')

username = credentials[0]
token = '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'

response = requests.get(endpoint, headers=headers, auth=(username, token))

data = response.json()

for repo in data:
    print(repo["name"])