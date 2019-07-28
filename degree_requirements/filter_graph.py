import json

obj = json.load(open('./mock_data_pretty.json'))

nodes = list(filter(lambda x: 'CS ' in x['id'], obj['nodes']))
print(nodes)

classes = list(map(lambda x: x['id'], nodes))

links = list(filter(
    lambda x: x['target'] in classes,
    obj['links']
))
print(links)

# links = []
while True:
    print('\niterating')
    sources = set(map(lambda x: x['source'], links))
    new_links = list(filter(
        lambda x: x['target'] in sources,
        obj['links']
    ))
    diff = [i for i in new_links if i not in links]
    print(diff)
    if not diff:
        break
    # if new_links == links:
    #     break
    links.extend(diff)
    # for i in [diff for diff in new_links if diff not in links]:
    #     links.append(i)
    #     print(i)

new_sources = set(map(lambda x: x['source'], links))
new_targets = set(map(lambda x: x['target'], links))
new_classes = list(new_sources.union(new_targets))

nodes = list(filter(lambda x: x['id'] in new_classes, obj['nodes']))

filtered = {'links': links, 'nodes': nodes}
# print(filtered)
print(f"{len(filtered['nodes'])} nodes, {len(filtered['links'])} edges")

with open('./mock_data_filtered.json', 'w') as f:
    f.write(json.dumps(filtered))

# filtered = filter(lambda x: x[0] == 'nodes', obj.items())

# print(dict(filtered))
