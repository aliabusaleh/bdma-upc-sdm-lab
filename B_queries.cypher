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


// Best version
MATCH (c:Conference)<-[:ofConference]-(:Proceeding)<-[:PublishedInProceeding]-(p:Paper)<-[cite:Cites]-(q:Paper)
WITH c.name AS conference, p.title AS article, COUNT(cite) as citations
WITH conference, article, citations ORDER BY citations DESC
WITH conference, COLLECT(article) AS articles, COLLECT(citations) AS citations
WITH conference, [i IN range(0,size(articles)-1) | [articles[i], citations[i]]] AS ArtCit
RETURN conference, ArtCit[0..3] AS Citations
ORDER BY conference


//B2:
// For each conference find authors that have published in at least 4 different editions of the conference
MATCH (c:Conference)<-[:of]-(pr:Proceedings)<-[:publishedIn]-(:Paper)-[:writtenBy]->(a:Author)
WITH c.name AS conference, a.name AS author, COUNT(pr) as nParticipations
WHERE nParticipations >= 4
RETURN conference, author, nParticipations


<<<<<<< HEAD
=======
// Ali version
MATCH (c:conference)<-[*]-(p:Paper)-[:writtenBy]->(a:author)
WITH c.name AS conference, a.name AS author, COUNT(*) as nParticipations
RETURN conference, collect(author) as Authorslist, nParticipations
order by conference, nParticipations desc

// Best version
MATCH (c:Conference)<-[:ofConference]-(pr:Proceeding)<-[:PublishedInProceeding]-(:Paper)-[:WrittenBy]->(a:Author)
WITH c.name AS conference, a.name AS author, COUNT(pr) as nParticipations
WHERE nParticipations >= 4
WITH conference, COLLECT(author) as authors, COLLECT(nParticipations) as nParticipations
WITH conference, [i IN range(0, size(authors)-1) | [authors[i],nParticipations[i]]] as authors_participations
RETURN conference, authors_participations

>>>>>>> obtain_data

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

// Best version
WITH date.truncate('year', date.realtime()).year AS year
MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year-2}), (v)<-[:PublishedInVolume]-(p:Paper)
WITH j, year, COUNT(p) AS publications_y2
MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year-1}), (v)<-[:PublishedInVolume]-(p:Paper)
WITH j, year, publications_y2, COUNT(p) AS publications_y1
MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year}), (v)<-[:PublishedInVolume]-(:Paper)<-[citation:Cites]-(:Paper)
WITH j, publications_y2, publications_y1, COUNT(citation) AS citations_y
RETURN j.name, toFloat(citations_y) / (publications_y1 + publications_y2) AS ImpactFactor


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
