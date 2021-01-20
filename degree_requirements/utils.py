import pickle


def filter_data(courses, degree):
    obj = pickle.load(open('../course_data/courses_parsed.obj',
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

    courses[degree] = {
            'prereqs': list(courses.keys()),
            'or_magnitude': len(courses.keys())
    }
    return courses
