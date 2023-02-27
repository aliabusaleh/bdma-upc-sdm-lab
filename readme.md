# Property Graph Lab 1
This repository is for Lab#1 for *Semantic Data Management* (SDM), 
the main objective for it is to explore and work with property graphs,
starting from designing the graph "schema", loading the data, and then querying the graph.

Authors:

[Abusaleh, Ali](github.com/aliabusaleh)

[Lorencio Abril, Jose Antonio](github.com/lorenc1o)

## Week 1
In first week, we are required to :
* Design the graph in terms of nodes and edges.
* Load the [Data](https://blog.allenai.org/new-academic-graph-datasets-released-from-semantic-scholar-18b6b3b3140e)  into neo4j.
  * The data is taken from [Semantic Scholar](https://www.semanticscholar.org/).
* Discuss improvements we can do to improve the design in step 1.

## Prerequisites
 * Neo4j version [neo4j-community-4.4.18](https://neo4j.com/download-center/#community)
 * Java JDK version [11](https://www.oracle.com/es/java/technologies/javase/jdk11-archive-downloads.html)
 * other python libraries mentioned [here](requirements.txt)

## Set up the system 
* install the prerequisites
* install the sample data using the following <b>UNIX</b> command <br>
``
for f in $(curl https://s3-us-west-2.amazonaws.com/ai2-s2ag/samples/MANIFEST.txt)
  do curl --create-dirs "https://s3-us-west-2.amazonaws.com/ai2-s2ag/$f" -o $f
done
`` <br>
* Copy <b>apoc-4.4.0.14-core.jar</b> into ``./path/neo4j-community-4.4.18/plugins``
  * Path is your path for the neo4j
* edit ``./path/neo4j-community-4.4.18/conf/neo4j.conf``
  * Create Database ``dbms.default_database=GraphLab``
  * add ``apoc.import.file.enabled=true`` to enable APOC plugin
  * disable authorization ``dbms.security.auth_enabled=false``

### Designing the Graph 

[//]: # (% plesae add the schema and description) 

### Preprocessing the data
* Extract the keywords from the abstract
  * ...
  
[//]: # (  * I will add this later )

* unzip the files in <br> ``./Samples/papers`` <br> ``./samples/citations``<br> ``./samples/embeddings`` <br>
* run the [script](data_preperation.py)
  * This script change <b>JSONL</b> into <b>JSON</b>
  * randomize the journals.
  * randomize the volumes.
  * randomize the proceedings.
  * randomize the conferences.
  * Save the data into the folder [preprocessed_data](./preprocessed_data/)
### Load data into neo4j 
*  cypher queries 
  * creating the main Nodes (Paper,Journal, Author ... etc) <br>
```
CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
CREATE (p:paper {doi: paper.externalids.DOI, CorpusId: paper.externalids.CorpusId , title: paper.title, abstract: "this is nice paper!"})
WITH p,paper,  paper.authors AS authors 
UNWIND authors AS author
CREATE (a:author {name: author.name, authorId: author.authorId})
CREATE (p)-[:writtenBy]->(a)
WITH p, paper, p.journal AS journal
CREATE (j:journal {name: journal.name})
WITH p, j,paper,  journal.volume AS volume
CREATE (v:volume {number: volume})
create (v)-[:publishedIn]->(j)
CREATE (p)-[:isIn]->(v)
create (y:Year {year: p.year})
create (v)-[:inYear]->(y)
with p, paper, paper.s2fieldsofstudy as s2fields where paper.s2fieldsofstudy is not null
UNWIND s2fields AS s2f
CREATE (t:topics {name: s2f.category})
create (t)<-[:relatedTo]-(p)
with p, paper.venue as ven where paper.venue is not null 
create (pro:proceeding {Edition: p.edition})
create (c:conference {name: ven})
create (p)-[:PublishedIn]->(pro)
create (pro)-[:of]->(c)
```
* creating citation 

[//]: # (* TO BE ADD LATER )

