import json
import pickle
import re
from sys import argv


def determine_highest_prereq(course):
    if course.startswith('OR'):
        highest_prereqs = []
        for prereq in courses[course]['prereqs']:
            highest_prereqs.append(determine_highest_prereq(prereq))
        return max(highest_prereqs)
    else:
        return int(re.findall('[\d]+', course)[0])


if __name__ == '__main__':
    if len(argv) < 2:
        exit("Usage: 'python3 pickle_to_csv.py [name of object]'")
    pickle_obj = argv[1]

    courses_file = open(f'../course_data/{pickle_obj}.obj', 'rb')
    courses = pickle.load(courses_file)

    json_object = {
        'nodes': [],
        'links': []
    }

    for course, data in courses.items():
        if course.startswith('OR'):
            fy = 2.5*(800 - (determine_highest_prereq(course) + 20))
        else:
            fy = 2.5*(800 - int(re.findall('[\d]+', course)[0]))
        json_object['nodes'].append({
            'id': course,
            'group': data['or_magnitude'],
            'size': 1,
            'fy': fy
        })
        for prereq in data['prereqs']:
            json_object['links'].append({'source': prereq, 'target': course})

    with open(f'../course_data/d3/{pickle_obj}.json', 'w') as outfile:
        json.dump(json_object, outfile)
