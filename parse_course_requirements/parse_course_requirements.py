import pickle
import pyparsing
import re

courses_file = open('../catalog_data_acquisition/courses.obj', 'rb')
courses = pickle.load(courses_file)

courses_parsed = {}
or_id = 0


def parse_prereqs(parent, prereqs):
    for prereq in prereqs:
        if isinstance(prereq, list):
            if any(isinstance(p, str) and len(re.findall(r'[^[( a-z]+ [\dH]+',
                                              p)) > 0 for p in prereq):
                global or_id
                parse_prereqs(f'OR {or_id}', prereq)
                prereqs.append(f'OR {or_id}')
                or_id += 1
        else:
            prereq = re.findall(r'[^[( a-z]+ [\dH]+', prereq)
            or_magnitude = 1 if parent.startswith('OR ') else 0
            if parent in courses_parsed:
                or_magnitude += courses_parsed[parent]['or_magnitude']
                prereq.extend(courses_parsed[parent]['prereqs'])
            courses_parsed[parent] = {
                'or_magnitude': or_magnitude,
                'prereqs': prereq
            }


for course, prereq_str in courses.items():
    if course in ['HORT 360', 'NSE 311']:
        prereq_str = prereq_str + ')'
    print(course)
    parser = pyparsing.nestedExpr(content=pyparsing.CharsNotIn('()'))
    nested_prereqs = parser.parseString(f'({prereq_str})').asList()[0]
    for prereqs in nested_prereqs:
        if isinstance(prereqs, str):
            prereq_count = len(re.findall(r'[^[( a-z]+ [\dH]+', prereqs))
            if prereq_count > 1 and 'and' not in prereqs:
                prereqs = [f'({prereqs})']
        parse_prereqs(course, [prereqs])

courses_file = open('./courses_parsed.obj', 'wb')
courses = pickle.dump(courses_parsed, courses_file)
