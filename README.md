# Degree Directed Acyclic Graph
The idea of [this project](https://github.com/course-network/degree-requirement-dag/) is to visualize the course requirements of a college degree program as a force directed graph. A single top level node will represent the degree, and the course requirements will branch down from it.

The idea is that this might serve as an advising tool for students planning their schedule or choosing a major. It would visually display the progression of courses and decisions. Displaying two degrees at once would show the student which courses are shared and which are not.

We start with the ecological engineering degree from Oregon State as an example. [Catalog data acquisition](catalog_data_acquisition) scrapes course prerequisites from OSU's catalog. [Degree requirements](degree_requirements) scrapes degree requirements from OSU's catalog. [Parse course requirements](parse_course_requirements) processes more complicated requirements. [d3](d3) visualizes this data.

## Proposed method for implementing uncertainty in a DAG
Degree requirements at OSU are generally expressed as a list of OR conditions. For example, an ecological engineering student must take "Ethics" or "The Responsible Engineer".

Sometimes, these conditions require a variable amount of courses from a variable amount of options. For example, a computational physics student must take two of three available senior capstone courses.

These conditions introduce uncertainty in the DAG. We suggest using an "OR node" to account for this.

![OR node example](or_example.png)
```
graph BT;
    A[PHL 205]-->B[OR];
    C[IE 380]-->B;
    B-->D[Degree];
```

We also define the "order" of the node as the amount of prerequisite nodes it requires to be satisfied. In the ethics requirement example, only one course is required so the OR node order is 1.

The goal of this project is to visualize all possible paths through a degree program by displaying all courses and OR nodes for a degree program. One idea to increase its utility is to allow the student to make decisions about which courses they take (either completed or planned), trimming the network to eliminate OR nodes.

## Hierarchical ordering
Ideally, the courses would be ordered so that the earliest courses the student takes are at the bottom. As you move up the y-axis, you move later in the degree program until reaching the degree node at the top.

The challenge with this is our data is not a tree (some nodes have multiple parents). So, we cannot take advantage of d3's built-in hierarchical layouts. Instead, we use the many-body force layout and add a strong y-position force. This force makes a node's y-position proportional to its max depth to the root node.

[This does achieve the desired result](https://course-network.github.io/degree-requirement-dag/), but it also shows the infeasibility of this project. A degree is simply too complicated to meaningfully represent in this way - there are far too many OR nodes and courses cluttering the graph. This may be resolved by hiding the OR nodes, but this raises further issues of positioning and accurate representation.
