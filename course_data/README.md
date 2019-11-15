# Pickle Objects
The data from parsing the course catalog is stored in courses_parsed.obj

# Subsetting courses
In [degreee_requirements](degree_requirements), links to degree course listings are specified in [degree_requirement_urls.json](degree_requirements/degree_requirement_urls.json). Add the page for the degree you are interested in and give it a name.

Then run
```bash
python3 ./subset_courses.py <degree name>
```

example:
```bash
python3 ./subset_courses.py cs
```

This generates a pickle 'cs_courses.obj' in the course_data directory.


# Converting to JSON or CSV
See the [README](../convert_database_format/pickle_to_csv.py) in [convert_database_format](../convert_database_format)
