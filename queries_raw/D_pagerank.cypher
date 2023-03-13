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

// Now with CLOSENESS
// 1- The projection
CALL gds.graph.project.cypher(
    'cited_authors',
    'MATCH (a:Author) RETURN id(a) as id', 
    'MATCH (citing:Author)<-[:WrittenBy]-(:Paper)-[:Cites]->(:Paper)-[:WrittenBy]->(cited:Author)
        RETURN id(citing) AS source, id(cited) AS target',
        { validateRelationships: false }
        ) YIELD
               graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;

// 2- The computation
CALL gds.beta.closeness.stream('cited_authors')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS author, score
ORDER BY score DESC

// Compute the Louvain communities
CALL gds.louvain.stream('cited_authors')
YIELD nodeId, communityId
WITH communityId, COLLECT(gds.util.asNode(nodeId).name) as community
WHERE size(community) > 50
RETURN communityId, size(community) as nMembers, community

// We can create the biggest community as a subgraph
CALL gds.graph.project.cypher(
    "biggest_community",
    'CALL gds.louvain.stream("cited_authors")
    YIELD nodeId, communityId
    WITH communityId, COLLECT(gds.util.asNode(nodeId)) AS authors
    WITH communityId, authors, size(authors) AS nAuthors
    ORDER BY nAuthors DESC LIMIT 1
    UNWIND authors AS author
    RETURN communityId, ID(author) AS id',
    'MATCH (citing:Author)<-[:WrittenBy]-(:Paper)-[:Cites]->(:Paper)-[:WrittenBy]->(cited:Author)
        RETURN id(citing) AS source, id(cited) AS target',
        { validateRelationships: false }
        ) YIELD
               graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;

// Now we can compute the pagerank for the biggest community
CALL gds.pageRank.stream('biggest_community')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS author, score
ORDER BY score DESC, author ASC

// This way we get the most important authors in the biggest community

// We can also compute the pagerank for the whole graph, and compare the results
CALL gds.pageRank.stream('biggest_community')
YIELD nodeId, score
WITH nodeId as nodeIdBC, score as scoreBC
CALL gds.pageRank.stream('cited_authors')
YIELD nodeId, score
WHERE nodeId = nodeIdBC
RETURN gds.util.asNode(nodeId).name AS author, score as fullScore, scoreBC as communityScore
ORDER BY communityScore DESC, author ASC

// Using this, we can see which authors are heavily cited in the biggest community, but not in the whole graph
