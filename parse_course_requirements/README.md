# Parse Course Requirements

## Parsing the prerequisite string to introduce OR nodes

The catalog gives prerequisite strings following a consistent format.

For example, the prereq string for BEE 472 is

    'MTH 112 with C- or better and (MTH 227 [C-] or MTH 251 [C-] or MTH 251H [C-]) and PH 201 [C-]'

The parse_course_requirements script interprets nested parantheses, 'and' and 'or' to create a Python object in the following format:

```python
{
   'BEE 472': {
       'prereqs': ['MTH 112', 'OR 1', 'PH 201'],
       'or_magnitude': 3
   },
   'OR 1': {
       'prereqs': ['MTH 227', 'MTH 251', 'MTH 251H'],
       'or_magnitude': 1
   }
}
```

## OR magnitude
OR magnitude is just the amount of prerequisite edges required to satisfy that node. For example, `OR 1` requires only one course from the prereqs list, while `BEE 427` requires everything in the prereq list.

In the global catalog preqrequisites, or magnitude can only be 1 or the total amount of prerequisites. Degree requirements will have OR nodes with magnitudes in between these limits.
