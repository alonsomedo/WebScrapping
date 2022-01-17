import requests

headers = {
    "referer": "https://www.udemy.com/courses/search/?q=python&skip_price=false"
}

for i in range(1,4):
    url_api = f'https://www.udemy.com/api-2.0/search-courses/?p={i}&q=python&skip_price=false'

    response = requests.get(url_api, headers = headers)

    data = response.json()
    courses = data['courses']

    for course in courses:
        title = course['title']
        num_reviews = course['num_reviews']
        print(i, ' - ', num_reviews, ' - ', title)