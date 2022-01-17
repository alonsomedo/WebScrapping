import requests
import pandas as pd

headers = {
    "referer": "https://www.udemy.com/courses/search/?q=python&skip_price=false"
}

course_data = []
for i in range(1,4):
    url_api = f'https://www.udemy.com/api-2.0/search-courses/?p={i}&q=python&skip_price=false'

    response = requests.get(url_api, headers = headers)

    data = response.json()
    courses = data['courses']

    for course in courses:
        course_data.append( {
            'title': course['title'],
            'num_reviews': course['num_reviews'],
            'page': i
        })
           
df = pd.DataFrame(course_data)
print(df[:15])