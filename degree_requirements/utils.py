import json


def filter_data(courses):
    obj = json.load(open('../mock_data.json'))
    links = list(filter(
        lambda x: x['target'] in courses,
        obj['links']
    ))

    # Add prerequisite links
    while True:
        sources = set(map(lambda x: x['source'], links))
        new_links = list(filter(
            lambda x: x['target'] in sources,
            obj['links']
        ))
        diff = [i for i in new_links if i not in links]
        if not diff:
            break
        links.extend(diff)

    new_sources = set(map(lambda x: x['source'], links))
    new_targets = set(map(lambda x: x['target'], links))
    new_courses = list(new_sources.union(new_targets))

    nodes = list(filter(lambda x: x['id'] in new_courses, obj['nodes']))

    # Sort nodes by 'id' and links by 'source' and 'target'
    nodes.sort(key=lambda x: x['id'])
    links.sort(key=lambda x: f"{x['source']}|{x['target']}")

    return {'links': links, 'nodes': nodes}
