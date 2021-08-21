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

    # Assign a level to each node indicating max depth to root node
    def traverse_to_root(node_id, current_depth = 1, max_depth = 1):
        links = [link for link in json_object['links'] if link['source'] is node_id]
        for link in links:
            if link['target'] != pickle_obj:
                current_depth = traverse_to_root(link['target'], current_depth + 1, max_depth)
            if current_depth > max_depth:
                max_depth = current_depth
        return max_depth

    for node in json_object['nodes']:
        if node['id'].startswith('OR'):
            node['level'] = 0
        else:
            node['level'] = traverse_to_root(node['id'])


    with open(f'../course_data/json/{pickle_obj}_courses.json', 'w') as outfile:
        json.dump(json_object, outfile)
