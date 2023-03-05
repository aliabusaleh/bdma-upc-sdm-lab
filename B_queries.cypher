//B1:
// Top 3 most cited articles per conference
MATCH (c:Conference)<-[:of]-(:Proceedings)<-[:publishedIn]-(p:Paper)<-[:cites*0..1]-(q:Paper)
WITH c.name as conference, p.title as article, COUNT(*)-1 as citations
WITH conference, article, citations ORDER BY citations DESC
RETURN conference, article[0..3] as MostCitedArticles
ORDER BY conference

// Ali Version
MATCH (c:Conference)<-[:of]-(p:Proceeding)<-[:PublishedInProceeding]-(pa:Paper)<-[cite:Cites]-(pb:Paper)
WHERE pa <> pb
WITH c.name AS ConferenceName, pa.title AS PaperTitle, COUNT(cite) AS NumCitations
ORDER BY ConferenceName, NumCitations DESC
WITH ConferenceName, COLLECT({title: PaperTitle, citations: NumCitations}) AS papers
RETURN ConferenceName, papers[0..3] AS TopPapers




//B2:
// For each conference find authors that have published in at least 4 different editions of the conference
MATCH (c:Conference)<-[:of]-(pr:Proceedings)<-[:publishedIn]-(:Paper)-[:writtenBy]->(a:Author)
WITH c.name AS conference, a.name AS author, COUNT(pr) as nParticipations
WHERE nParticipations >= 4
RETURN conference, author, nParticipations



//B3:
// Compute the impact factor of each journal
// (Unfinished, but the idea is there)
MATCH (j:Journal)<-[:publishedIn]-(v:Volume)
WITH j.name AS journal, date.truncate('year', date.realtime()).year AS year
MATCH (q:Paper)-[:cites*0..1]->(p:Paper)-[:isIn]->(v)-[:inYear]->(:year {y:year})
WITH journal, year, COUNT(q) as citations_y
MATCH (p:Paper)-[:isIn*0..1]->(v)-[:inYear]->(:year {y:year-1})
WITH journal, year, citations_y, COUNT(p) AS publications_y1
MATCH (p:Paper)-[:isIn*0..1]->(v)-[:inYear]->(:year {y:year-2})
WITH journal, citations_y, publications_y1, COUNT(p) AS publications_y2
RETURN journal, citations_y/(publications_y1 + publications_y2) AS impactFactor


//B4:
// Find the H-index of the authors in the graph
MATCH (a:Author)<-[:WrittenBy]-(p:Paper)<-[c:Cites]-(otherPaper:Paper)
WITH a, p, COUNT(c) AS citations
ORDER BY citations DESC
WITH a, COLLECT(citations) AS citationCounts
WITH a, REDUCE(hIndex = 0, i IN RANGE(0, SIZE(citationCounts)-1) |
  CASE WHEN citationCounts[i] >= i+1 AND citationCounts[i+1] <= i+1
    THEN i+1
    ELSE hIndex END
) AS hIndex
RETURN a.name AS authorName, hIndex
ORDER BY hIndex DESC
