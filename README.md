# Rules for network visualization

### 1. No class is drawn more than once
This rule ensures that the network is a true graph.

### 2. OR conditions are represented by a single node, with connections to each option
OR conditions allow the user to "trim" the network. By choosing the course that fulfills that requirement, they remove branches that no longer exist because of that choice.

### 3. If a node's only connection is to a condition node that has selected a different node, it is removed
Once the decision has been made, these optional nodes are clutter. They can be revisualized if the user changes the condition back to unselected.

### 4. Tree redraws itself upon selection in condition
With each decision, the network must reevaluate which branches exist given the remaining nodes.

### 5. Conditions begin unselected
The network displays all possible outcomes, which the user narrows down until they have their specific degree plan.
