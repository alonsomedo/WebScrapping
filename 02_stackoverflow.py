import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url = 'https://stackoverflow.com/questions'

response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.text)

container_of_questions = soup.find(id="questions")
list_of_questions = container_of_questions.find_all('div', class_="question-summary")

for question in list_of_questions:
    title_element = question.find('h3')
    title = title_element.text

    # 1era forma
    #description = question.find(class_='excerpt').text

    # 2da forma:
    description = title_element.find_next_sibling('div').text


    description = description.replace("\n",'').replace("\r",'').strip()
    print(title)
    print(description, "\n")


