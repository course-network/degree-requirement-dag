import pickle


def filter_data(courses):
    obj = pickle.load(open('../parse_course_requirements/courses_parsed.obj',
                           'rb'))

    # Add prerequisite courses
    sources = set([course for course in obj if course in courses])
    new_sources = sources.copy()
    while True:
        for course in sources:
            new_sources.update(set(obj[course]['prereqs']))
        diff = set([i for i in new_sources if i not in sources])
        if not diff:
            break
        sources.update(diff)

    courses = {}
    for course in sources:
        courses[course] = obj[course]

    return courses
