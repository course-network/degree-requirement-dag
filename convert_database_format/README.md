# Convert pickle to JSON
```bash
python3 ./pickle_to_json <name of pickle>
```
example:
```bash
python3 ./pickle_to_json cs_courses
```
This generates cs_courses.json in [course_data/json](../course_data/json)

# Convert pickle to csv
```bash
python3 ./pickle_to_csv <name of pickle>
```
example:
```bash
python3 ./pickle_to_csv cs_courses
```
This generates cs_courses_nodes.csv and cs_courses_edges.csv in [course_data/csv](../course_data/csv)

# nodes.csv format
Course title, or degree

Or degree is the amount of prerequisites necessary to satisfy the or condition. Normal courses have or degree 0. All catalog or requirements have degree 1 (1 class of prerequisites to this node needed). As we add degree requirements, we will see nodes of higher or degree (such as 'take 4 of these courses').

# edges.csv format
prerequisite, course
