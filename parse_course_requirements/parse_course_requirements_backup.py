import pickle
import pyparsing
import re

courses_file = open('../catalog_data_acquisition/courses.obj', 'rb')
courses = pickle.load(courses_file)

courses_parsed = {}
or_id = 0


# def flatten(l, output):
#     for i in l:
#         if type(i) == list:
#             flatten(i, output)
#         else:
#             output.append(i)
#     return output
#
#
# def parse_prereqs_old(parent, prereqs):
#     for prereq in prereqs:
#         if isinstance(prereq, list):
#             if any(isinstance(p, str) and len(re.findall(r'[^[( a-z]+ [\dH]+',
#                                               p)) > 0 for p in flatten(prereq, [])):
#                 global or_id
#                 print('orid: ', or_id)
#                 print('prereqs: ', prereq)
#                 parse_prereqs(f'OR {or_id}', prereq)
#                 prereqs.append(f'OR {or_id}')
#                 or_id += 1
#         else:
#             prereq = re.findall(r'[^[( a-z]+ [\dH]+', prereq)
#             or_magnitude = 1 if parent.startswith('OR ') else 0
#             if parent in courses_parsed:
#                 prereq.extend(courses_parsed[parent]['prereqs'])
#             courses_parsed[parent] = {
#                 'or_magnitude': or_magnitude,
#                 'prereqs': prereq
#             }


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


def determine_or_magnitude(course, or_prereqs):
    or_magnitude = 0 if course not in courses_parsed else courses_parsed[course]['or_magnitude']
    existing_prereqs = [] if course not in courses_parsed else courses_parsed[course]['prereqs']
    for or_prereq in or_prereqs:
        if or_prereq not in existing_prereqs:
            or_magnitude += 1
    if any('or' in prereq for prereq in or_prereqs) or any('or' in prereq for prereq in existing_prereqs):
        or_magnitude = 1
    return or_magnitude


def update_node(course, prereqs, or_magnitude):
    existing_prereqs = [] if course not in courses_parsed else courses_parsed[course]['prereqs']
    for prereq in prereqs:
        if not existing_prereqs or prereq not in existing_prereqs:
            existing_prereqs.append(prereq)
    courses_parsed[course] = {'prereqs': existing_prereqs, 'or_magnitude': or_magnitude}


def generate_course_object(course, regexed_prereqs):
    global or_id
    print(regexed_prereqs)
    print(' ')
    for key in set([i[0] for i in regexed_prereqs]):
        prereq_keys = [i for i in regexed_prereqs if i[0] == key]
        if any([len(prereq_key) > 1 for prereq_key in prereq_keys]):
            if any(['OR' in regexed_prereqs[prereq_key] for prereq_key in prereq_keys]):
                or_id += 1
                or_prereqs = {}
                for prereq_key in [i for i in prereq_keys if 'OR' not in regexed_prereqs[i]]:
                    or_prereqs[prereq_key[1:]] = regexed_prereqs[prereq_key]
                update_node(course, [f'OR {or_id}'], determine_or_magnitude(course, or_prereqs))
                generate_course_object(f'OR {or_id}', or_prereqs)
            else:
                or_id += 1
                or_prereqs = {}
                for prereq_key in prereq_keys:
                    or_prereqs[prereq_key[1:]] = regexed_prereqs[prereq_key]
                    update_node(course, [f'OR {or_id}'], determine_or_magnitude(course, or_prereqs))
                    generate_course_object(f'OR {or_id}', or_prereqs)
        else:
            for prereq_key in prereq_keys:
                update_node(course, regexed_prereqs[prereq_key], determine_or_magnitude(course, regexed_prereqs[prereq_key]))
                # print(course, prereq_key, regexed_prereqs[prereq_key])
        # for idx, prereq_key in enumerate(prereq_keys):
        #     print(idx, prereq_key, regexed_prereqs[prereq_key])
            # if len(prereq_key) > 1:
            #     or_prereqs = {}
            #     if isinstance(regexed_prereqs[prereq_key], str):
            #         regexed_prereqs[prereq_key] = [regexed_prereqs[prereq_key]]
            #     for or_idx, or_prereq in enumerate(regexed_prereqs[prereq_key]):
            #         or_prereqs[tuple([or_idx])] = or_prereq
            #     or_id += 1
            #     generate_course_object(f'OR{or_id}', or_prereqs)
            # else:
            #     print(course, prereq_key, regexed_prereqs[prereq_key])

for course, prereq_str in [('BB 314', ' ((BI 211 with C- or better or BI 211H with C- or better) and (BI 212 [C-] or BI 212H [C-]) and (BI 213 [C-] or BI 213H [C-])) and (CH 231 or CH 232)')]:  #courses.items()
    # Fix errors in catalog
    if course in ['HORT 360', 'NSE 311']:
            prereq_str = prereq_str + ')'

    # Create nested lists delimited by parantheses
    parser = pyparsing.nestedExpr(content=pyparsing.CharsNotIn('()'))
    nested_prereqs = parser.parseString(f'({prereq_str})').asList()[0]

    # Traverse list, converting strings to regex matches
    nested_prereqs_regexed = {}
    apply_regex(nested_prereqs, [], nested_prereqs_regexed)


    # Traverse regexed object, adding OR nodes
    generate_course_object(course, nested_prereqs_regexed)
    print(courses_parsed)
    #
    # print('course', course)
    # print('object', nested_prereqs)
    # print('regexed', nested_prereqs_regexed)
    #
    #





















# for prereq_str in ['(((BI 211 with C- or better or BI 211H with C- or better) and (BI 212 [C-] or BI 212H [C-]) and (BI 213 [C-] or BI 213H [C-])) or (BI 204 [C-] and BI 205 [C-] and BI 206 [C-]))']:
#     course = 'BB 314H'
#     if course in ['HORT 360', 'NSE 311']:
#         prereq_str = prereq_str + ')'
#
#     print(course)
#
#     parser = pyparsing.nestedExpr(content=pyparsing.CharsNotIn('()'))
#     nested_prereqs = parser.parseString(f'({prereq_str})').asList()[0]
#     for prereqs in nested_prereqs:
#         if isinstance(prereqs, str):
#             prereq_count = len(re.findall(r'[^[( a-z]+ [\dH]+', prereqs))
#             if prereq_count > 1 and 'and' not in prereqs:
#                 prereqs = [f'({prereqs})']
#         parse_prereqs(course, [prereqs])
#
# print(courses_parsed)
# courses_file = open('./courses_parsed.obj', 'wb')
# pickle.dump(courses_parsed, courses_file)
