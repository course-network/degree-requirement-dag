from bs4 import BeautifulSoup
import pickle
import requests

courses = {}

urls_file = open('department_urls.obj', 'rb')
urls = pickle.load(urls_file)

for url in urls:
    courses_html = requests.get(url).text
    soup = BeautifulSoup(courses_html, 'html.parser')
    for course in soup.find_all(class_='courseblock'):
        title = course.find(class_='courseblocktitle').get_text().split('.')[0]
        print(title)
        block = course.find(class_='courseblockextra')
        prereqs = ''
        if block is not None:
            if block.find('strong') is not None:
                if block.find('strong').get_text() == 'Prerequisites:':
                    prereqs = block.get_text().replace('Prerequisites: ', '')
        courses[title] = prereqs

courses_file = open('courses.obj', 'wb')
pickle.dump(courses, courses_file)
