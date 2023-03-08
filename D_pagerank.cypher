// To be able to apply the algorithms from the data science library, we need to first obtain an appropriate
//      projected graph.

// Let's do an example for pagerank

// Say we want to compute the pagerank for the papers in the graph, so that we can rank them by importance.
// Step 1: project the graph
//  For this, we only need the papers and the citations between them:
call gds.graph.project(
    'PapersGraph', // Name of the projected graph
    'Paper', // Nodes to project
    'Cites') // Relationships to project

// Step 2: compute the pagerank
CALL gds.pageRank.stream('PapersGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).title AS title, score
ORDER BY score DESC, title ASC