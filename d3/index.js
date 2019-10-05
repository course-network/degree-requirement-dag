d3.json('treeData.json', function(treeData) {

    // set the dimensions and margins of the diagram
    const top = 40;
    const right = 90;
    const bottom = 50;
    const left= 90;
    const width = 660 - left - right;
    const height = 500 - top - bottom;

    // declares a tree layout and assigns the size
    const treeMap = d3.tree()
                    .size([width, height]);

    // assigns the data to a hierarchy using parent-child relationships
    // maps the node data to the tree layout
    const nodes = treeMap(d3.hierarchy(treeData));

    // append the svg object to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    const svg = d3.select('body')
                .append('svg')
                .attr('width', width + left + right)
                .attr('height', height + top + bottom),
    g = svg.append('g')
           .attr('transform', `translate(${left},${top})`);

    // adds the links between the nodes
    const link = g.selectAll('.link')
                .data(nodes.descendants().slice(1))
                .enter().append('path')
                .attr('class', 'link')
                .attr('d', ({x, y, parent}) => {
                    const yLink = (y + parent.y) / 2;
                    return `M${x},${y}C${x},${yLink} ${parent.x},${yLink} ${parent.x},${parent.y}`
                });

    // adds each node as a group
    const node = g.selectAll('.node')
                .data(nodes.descendants())
                .enter()
                .append('g')
                .attr('class', ({children}) => `node${(children ? ' node--internal' : ' node--leaf')}`)
                .attr('transform', ({x, y}) => `translate(${x},${y})`);

    // adds the circle to the node
    node.append('circle')
        .attr('r', 10);

    // adds the text to the node
    node.append('text')
        .attr('dy', '.35em')
        .attr('y', ({children}) => children ? -20 : 20)
        .style('text-anchor', 'middle')
        .text(({data}) => data.name);
});
