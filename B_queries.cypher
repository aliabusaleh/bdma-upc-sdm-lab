//B1:
// Top 3 most cited articles per conference
MATCH (c:Conference)<-[:of]-(:Proceedings)<-[:publishedIn]-(p:Paper)<-[:cites*0..1]-(q:Paper)
WITH c.name as conference, p.title as article, COUNT(*)-1 as citations
WITH conference, article, citations ORDER BY citations DESC
RETURN conference, article[0..3] as MostCitedArticles
ORDER BY conference

// Ali Version
MATCH (c:conference)<-[:of]-(:proceeding)<-[:PublishedInProceeding]-(p:Paper)<-[:cites*1..]-(q:Paper)
WITH c.name as conference, p.title as article, COUNT(*) as citations
WITH conference, article, citations ORDER BY citations DESC
where citations > 0
RETURN conference, article[0..3] as MostCitedArticles, citations
ORDER BY conference, citations desc



//B2:
// For each conference find authors that have published in at least 4 different editions of the conference
MATCH (c:Conference)<-[:of]-(pr:Proceedings)<-[:publishedIn]-(:Paper)-[:writtenBy]->(a:Author)
WITH c.name AS conference, a.name AS author, COUNT(pr) as nParticipations
WHERE nParticipations >= 4
RETURN conference, author, nParticipations


// Ali version
MATCH (c:conference)<-[*]-(p:Paper)-[:writtenBy]->(a:author)
WITH c.name AS conference, a.name AS author, COUNT(*) as nParticipations
RETURN conference, collect(author) as Authorslist, nParticipations
order by conference, nParticipations desc


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




