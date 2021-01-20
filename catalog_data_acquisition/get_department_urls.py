from bs4 import BeautifulSoup
import pickle
import requests

urls = []

courses_url = 'https://catalog.oregonstate.edu/courses/'
course_description_html = requests.get(courses_url).text

soup = BeautifulSoup(course_description_html, 'html.parser')
soup.find('div', class_="azMenu").decompose()
for link in soup.find(class_='az_sitemap').find_all('a'):
    url = link.get('href')
    if url is not None:
        urls.append(f'https://catalog.oregonstate.edu{url}')

urls_file = open('../course_data/department_urls.obj', 'wb')
pickle.dump(urls, urls_file)
urls_file.close()
