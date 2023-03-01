// 1-create papers
CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
CREATE (p:Paper {doi: paper.externalids.DOI, CorpusId: paper.externalids.CorpusId , title: paper.title, abstract: "this is nice paper!"})
WITH p,paper,  paper.authors AS authors
UNWIND authors AS author
CREATE (a:author {name: author.name, authorId: author.authorId})
CREATE (p)-[w:writtenBy]->(a)
SET w.mainAuthor = CASE when author = head(authors) then 1 END

// 2- create journals
CALL apoc.load.json("file://papers_json.json") YIELD value
match (p:Paper{CorpusId: value.externalids.CorpusId})
WITH value  where value.journal is not null
CREATE (j:journal {name: value.journal.name})
CREATE (v:volume {number: value.volume})
create (v)-[:publishedInVolume]->(j)
CREATE (p:Paper{CorpusId: value.CorpusId})-[:isIn]->(v)
create (y:Year {year: p.year})
create (v)-[:inYear]->(y)

//3- create conf

CALL apoc.load.json("file://papers_json.json") YIELD value as paper
match (p:Paper{CorpusId: paper.externalids.CorpusId})
with p, paper, paper.venue as ven where paper.venue is not null
create (pro:proceeding {Edition: p.edition})
create (c:conference {name: ven})
create (p)-[:PublishedInProceeding]->(pro)
create (y:Year {year: p.year})
create (pro)-[:inYear]->(y)
create (pro)-[:of]->(c)
create (ci:City {name: paper.city})
create (co:Country{name: paper.country})
create (pro)-[:heldin]->(ci)
create (ci)-[:belongsTo]->(co)


//4- create citation

call apoc.load.json("file://citation_json.json") yield value as info
match (src:Paper {CorpusId: info.citingcorpusid})
match (dst:Paper {CorpusId: info.citedcorpusid})
create (src)-[:cites]->(dst)




//5- create reviewers

CALL apoc.load.json("file://papers_json.json") YIELD value
match (p:Paper{CorpusId: value.externalids.CorpusId})
WITH p, value.reviewers as reviewers
unwind reviewers as reviewer
match (a:author{authorId: reviewer.authorId})
create (p)-[:reviwedBy]->(a)


//6- remove duplicate edges between nodes caused by randomization ( 2 parts)

CALL apoc.periodic.iterate(
  "MATCH (a)-[r]->(b)
   WHERE id(a) < id(b)
   RETURN a, b, type(r) as type, collect(r) as rels",
  "FOREACH(rel in tail(rels) | DELETE rel)"
  , {batchSize:1000, parallel:false}
);

CALL apoc.periodic.iterate(
  "MATCH (a)-[r]->(b)
   WHERE id(a) > id(b)
   RETURN a, b, type(r) as type, collect(r) as rels",
  "FOREACH(rel in tail(rels) | DELETE rel)"
  , {batchSize:1000, parallel:false}
);

