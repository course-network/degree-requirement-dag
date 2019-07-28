import json

obj = json.load(open('../mock_data.json'))
nodes = list(filter(lambda x: 'CS ' in x['id'], obj['nodes']))
classes = list(map(lambda x: x['id'], nodes))

links = list(filter(
    lambda x: x['target'] in classes,
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
new_classes = list(new_sources.union(new_targets))

nodes = list(filter(lambda x: x['id'] in new_classes, obj['nodes']))

# Sort nodes by 'id' and links by 'source' and 'target'
nodes.sort(key=lambda x: x['id'])
links.sort(key=lambda x: f"{x['source']}|{x['target']}")

filtered = {'links': links, 'nodes': nodes}

output_path = './mock_data_filtered.json'
with open(output_path, 'w') as f:
    f.write(json.dumps(filtered, sort_keys=True, indent=4))

print(
    f"result: {len(filtered['nodes'])} nodes, {len(filtered['links'])} edges"
)
print(f'wrote file to {output_path}')
