import requests
from bs4 import BeautifulSoup
import mimetypes

url = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/"

response = requests.get(url)
soup = BeautifulSoup(response.text)

urls = []

downloads = soup.find_all('a', class_="download-button")
for link in downloads:
    urls.append(link["href"])

i = 0
for url in urls: 
    r = requests.get(url, allow_redirects=True)
    content_type = r.headers['content-type']
    extension = mimetypes.guess_extension(content_type)

    file_name = './files_downloaded/excel-file-' + str(i) + extension
    output = open(file_name, 'wb')
    output.write(r.content) 
    output.close()
    i += 1

