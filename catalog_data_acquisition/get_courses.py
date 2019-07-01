from bs4 import BeautifulSoup
import pickle
import requests
import unicodedata

courses = {}

urls_file = open('department_urls.obj', 'rb')
urls = pickle.load(urls_file)

for url in urls:
    courses_html = requests.get(url).text
    soup = BeautifulSoup(courses_html, 'html.parser')
    for course in soup.find_all(class_='courseblock'):
        title = course.find(class_='courseblocktitle').get_text().split('.')[0]
        title = unicodedata.normalize('NFKD', title)
        print(title)
        for block in course.find_all(class_='courseblockextra'):
            if block is not None:
                for strong_tag in block.find_all('strong'):
                    if strong_tag.get_text() == 'Prerequisites:':
                        prereqs = block.get_text().replace('Prerequisites: ', '')
                        prereqs = unicodedata.normalize('NFKD', prereqs)
                        courses[title] = prereqs

courses_file = open('courses.obj', 'wb')
pickle.dump(courses, courses_file)
