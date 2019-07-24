import pickle
import pyparsing
import re

courses_file = open('../catalog_data_acquisition/courses.obj', 'rb')
courses = pickle.load(courses_file)

courses_parsed = {}
or_id = 0


def apply_regex(prereqs, indices, output):
    if isinstance(prereqs, list):
        for idx, prereq in enumerate(prereqs):
            # True if trailing or
            if apply_regex(prereq, indices + [idx], output):
                prereqs[idx + 1].insert(0, 'OR')
    else:
        regex_match = re.findall(r'[^[( ]+ ?[^[( a-z]+ [\dH]+', prereqs)
        if regex_match:
            output[tuple(indices)] = regex_match
        # Handle trailing or
        if prereqs is 'OR':
            output[tuple(indices)] = prereqs
        return prereqs.endswith('or ')


def update_node(course, prereqs):
    existing_prereqs = [] if course not in courses_parsed else courses_parsed[
      course]['prereqs']
    for prereq in prereqs:
        if not existing_prereqs or prereq not in existing_prereqs:
            existing_prereqs.append(prereq)
    # if OR present, it is an OR-1 node, default is AND
    or_magnitude = len(existing_prereqs)
    if any(i is 'OR' for i in existing_prereqs):
        or_magnitude = 1
    courses_parsed[course] = {'prereqs': existing_prereqs,
                              'or_magnitude': or_magnitude}


def generate_course_object(course, regexed_prereqs):
    global or_id
    # Loop through top level
    for key in set([i[0] for i in regexed_prereqs]):
        # Get all keys in belonging to top level iteration
        sub_keys = [i for i in regexed_prereqs if i[0] == key]
        # If there are multiple subkeys, create or node and make recursive call
        if len(sub_keys) > 1:
            or_id += 1
            or_prereqs = {}
            for idx, sub_key in enumerate(sub_keys):
                or_prereqs[sub_key[1:]] = regexed_prereqs[sub_key]
            update_node(course, [f'OR {or_id}'])
            generate_course_object(f'OR {or_id}', or_prereqs)
        # If only one subkey, add prereq to parsed_courses
        else:
            if len(sub_keys[0]) == 1:
                # Handle trailing OR
                if any(i is 'O' or 'or' for i in regexed_prereqs[sub_keys[0]]):
                    for key in courses_parsed:
                        if course in courses_parsed[key]['prereqs']:
                            update_node(key, ['OR'])
                update_node(course, [i for i in regexed_prereqs[
                  sub_keys[0]] if i != 'O' and i != 'R'])
            # reformat list of strings as nested object to generate OR-1 node
            else:
                prereqs = {}
                prereqs[(0, 0)] = ['OR']
                for idx, prereq in enumerate(regexed_prereqs[sub_keys[0]]):
                    prereqs[(0, idx + 1)] = [prereq]
                generate_course_object(course, prereqs)


def clean_parsed_courses(courses):
    for key in courses:
        courses[key]['prereqs'] = re.findall(r'[^[( a-z]+ [\dH]+',
                                             ' '.join(courses[key]['prereqs']))


def create_missing_nodes(courses):
    for key in set(courses.keys()):
        for prereq in courses[key]['prereqs']:
            if prereq not in courses:
                courses_parsed[prereq] = {'prereqs': [],
                                          'or_magnitude': 1}


for course, prereq_str in courses.items():
    # Fix errors in catalog
    if course in ['HORT 360', 'NSE 311']:
        prereq_str = prereq_str + ')'
    if course in ['ALS 161' or 'ALS 162']:
        preq_str = 'ALS 150 and ALS 151'

    # Create nested lists delimited by parantheses
    parser = pyparsing.nestedExpr(content=pyparsing.CharsNotIn('()'))
    nested_prereqs = parser.parseString(f'({prereq_str})').asList()[0]

    # Traverse list, converting strings to regex matches
    nested_prereqs_regexed = {}
    apply_regex(nested_prereqs, [], nested_prereqs_regexed)

    # Traverse regexed object, adding OR nodes
    generate_course_object(course, nested_prereqs_regexed)

# Clean courses_parsed for OR, and, or by matching course number regex
clean_parsed_courses(courses_parsed)

# Create nodes for courses no longer offered, but still satisfy prereqs
create_missing_nodes(courses_parsed)

# Save parsed courses
courses_parsed_file = open('courses_parsed.obj', 'wb')
pickle.dump(courses_parsed, courses_parsed_file)
