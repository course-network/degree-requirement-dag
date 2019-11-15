import json
import pickle
import re
from sys import argv


if __name__ == '__main__':
    if len(argv) < 2:
        exit("Usage: 'python3 pickle_to_csv.py [name of object]'")
    pickle_obj = argv[1]

    courses_file = open(f'../course_data/{pickle_obj}_courses.obj', 'rb')
    courses = pickle.load(courses_file)
    json_object = {
        'nodes': [],
        'links': []
    }

    for course, data in courses.items():
        json_object['nodes'].append({
            'id': course,
            'in_degree': data['or_magnitude'],
            'size': 1
        })
        for prereq in data['prereqs']:
            json_object['links'].append({'source': prereq, 'target': course})

    with open(f'../course_data/json/{pickle_obj}_courses.json', 'w') as outfile:
        json.dump(json_object, outfile)
