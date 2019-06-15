from bs4 import BeautifulSoup
import pickle

urls = []

html_file = open('course_descriptions.html', 'r')
data = html_file.read()
html_file.close()

soup = BeautifulSoup(data, 'html.parser')
soup.find('div', class_="azMenu").decompose()
for link in soup.find(class_='az_sitemap').find_all('a'):
    url = link.get('href')
    if url is not None:
        urls.append(url)

urls_file = open('department_urls.obj', 'wb')
pickle.dump(urls, urls_file)
urls_file.close()
