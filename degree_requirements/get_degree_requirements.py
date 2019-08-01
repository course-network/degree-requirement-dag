import json
from sys import argv
import unicodedata

from bs4 import BeautifulSoup
import requests

from utils import filter_data

if __name__ == '__main__':
    if len(argv) < 2:
        exit("Usage: 'python3 get_degree_requirments.py [degree]'")
    degree = argv[1]

    urls = json.load(open('./degree_requirement_urls.json'))
    if degree not in urls:
        exit(f'Invalid degree. Valid choices are {list(urls.keys())}')

    url = urls[degree]

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    courses = list(map(
        lambda x: unicodedata.normalize('NFKD', x['title']),
        soup.select('a.code.bubblelink')
    ))

    filtered_data = filter_data(courses)

    output_path = f'./mock_data_{degree}.json'
    with open(output_path, 'w') as f:
        f.write(json.dumps(filtered_data, sort_keys=True, indent=4))

    print(
        f"result: {len(filtered_data['nodes'])} nodes, "
        f"{len(filtered_data['links'])} edges")
    print(f'wrote file to {output_path}')
