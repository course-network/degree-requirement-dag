import csv
import pickle

courses_file = open('../parse_course_requirements/courses_parsed.obj', 'rb')
courses = pickle.load(courses_file)

edges_csv = open('edges.csv', 'w')
nodes_csv = open('nodes.csv', 'w')

edges_writer = csv.DictWriter(edges_csv, fieldnames=['source', 'dest'])
nodes_writer = csv.DictWriter(nodes_csv, fieldnames=['node', 'or_magnitude'])

for course, data in courses.items():
    nodes_writer.writerow(
        {'node': course, 'or_magnitude': data['or_magnitude']})
    for prereq in data['prereqs']:
        edges_writer.writerow({'source': prereq, 'dest': course})

nodes_csv.close()
edges_csv.close()
