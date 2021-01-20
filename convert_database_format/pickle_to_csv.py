import csv
import pickle
from sys import argv

if __name__ == '__main__':
    if len(argv) < 2:
        exit("Usage: 'python3 pickle_to_csv.py [name of object]'")
    pickle_obj = argv[1]

    courses_file = open(f'../course_data/{pickle_obj}.obj', 'rb')
    courses = pickle.load(courses_file)

    edges_csv = open(f'../course_data/csv/{pickle_obj}_edges.csv', 'w')
    nodes_csv = open(f'../course_data/csv/{pickle_obj}_nodes.csv', 'w')

    edges_writer = csv.DictWriter(edges_csv, fieldnames=['source', 'dest'])
    nodes_writer = csv.DictWriter(nodes_csv,
                                  fieldnames=['node', 'or_magnitude'])

    for course, data in courses.items():
        nodes_writer.writerow(
            {'node': course, 'or_magnitude': data['or_magnitude']})
        for prereq in data['prereqs']:
            edges_writer.writerow({'source': prereq, 'dest': course})

    nodes_csv.close()
    edges_csv.close()
