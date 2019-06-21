import csv
import pickle
import re

courses = {}

courses_file = open('../catalog_data_acquisition/courses.obj', 'rb')
courses = pickle.load(courses_file)

edges_csv = open('edges.csv', 'w')
nodes_csv = open('nodes.csv', 'w')

edges_writer = csv.DictWriter(edges_csv, fieldnames=['source', 'dest'])
nodes_writer = csv.DictWriter(nodes_csv, fieldnames=['node'])

for course, prereqs in courses.items():
    nodes_writer.writerow({'node': course})
    for prereq in re.findall(r'[^[( ]+[\dH]+', prereqs):
        edges_writer.writerow({'source': course, 'dest': prereq})

nodes_csv.close()
edges_csv.close()
