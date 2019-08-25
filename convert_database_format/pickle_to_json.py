import json
import pickle

courses_file = open('../parse_course_requirements/courses_parsed.obj', 'rb')
courses = pickle.load(courses_file)

json_object = {
    'nodes': [],
    'links': []
}

for course, data in courses.items():
    json_object['nodes'].append({
        'id': course,
        'group': data['or_magnitude'],
        'size': 1
    })
    for prereq in data['prereqs']:
        json_object['links'].append({'source': prereq, 'target': course})


with open('catalog.json', 'w') as outfile:
    json.dump(json_object, outfile)
