# Catalog Data Acquisition

## Prerequisites
Requires Python3 and BeautifulSoup4:

`pip3 install -r requirements.txt`

## Getting Department Urls
The [course description page](https://catalog.oregonstate.edu/courses/) gives a list of departments urls.

`python3 get_department_urls.py`
should be run first to generate department_urls.obj.

## Getting Courses / Prereqs
`python3 get_courses.py` generates courses.obj. This object lists courses in the format

    { "ME 250", "ENGR 248 with C or better and (PH 211 [C] or PH 211H [C])" }

Prerequisite strings still need to be parsed.
