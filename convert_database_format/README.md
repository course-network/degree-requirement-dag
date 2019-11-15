# Convert pickle to JSON
```bash
python3 ./pickle_to_json <name of pickle>
```
example:
```bash
python3 ./pickle_to_json cs_courses
```


# Convert pickle to csv
'''bash
python3 ./pickle_to_csv <name of pickle>
'''
example:
'''bash
python3 ./pickle_to_csv cs_courses
'''

# nodes.csv format
Course title, or degree

Or degree is the amount of prerequisites necessary to satisfy the or condition. Normal courses have or degree 0. All catalog or requirements have degree 1 (1 class of prerequisites to this node needed). As we add degree requirements, we will see nodes of higher or degree (such as 'take 4 of these courses').

# edges.csv format
prerequisite, course
