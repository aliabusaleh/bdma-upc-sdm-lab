# Property Graph Lab 1
This repository is for Lab#1 for *Semantic Data Management* (SDM), 
the main objective for it is to explore and work with property graphs,
starting from designing the graph "schema", loading the data, and then querying the graph.

Authors:

[Abusaleh, Ali](github.com/aliabusaleh)

[Lorencio Abril, Jose Antonio](github.com/lorenc1o)

## Week 1
In the first week, we are required to:
* Design the graph in terms of nodes and edges.
* Load the [Data](https://blog.allenai.org/new-academic-graph-datasets-released-from-semantic-scholar-18b6b3b3140e)  into neo4j.
  * The data is taken from [Semantic Scholar](https://www.semanticscholar.org/).
* Discuss improvements we can do to the design in step 1.

## Prerequisites
 * Neo4j version [neo4j-community-4.4.18](https://neo4j.com/download-center/#community)
 * Neo4j APOC library version [apoc-4.4.0.14-core.jar](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases)
 * Neo4j Graph Data science library [neo4j-graph-data-science-2.3.1.jar](https://github.com/neo4j/graph-data-science/releases)
 * Java JDK version [11](https://www.oracle.com/es/java/technologies/javase/jdk11-archive-downloads.html)
 * Other python libraries mentioned [here](requirements.txt)

## Set up the system 
* Install the prerequisites
* Install the sample data using the following <b>UNIX</b> command <br>
``
for f in $(curl https://s3-us-west-2.amazonaws.com/ai2-s2ag/samples/MANIFEST.txt)
  do curl --create-dirs "https://s3-us-west-2.amazonaws.com/ai2-s2ag/$f" -o $f
done
`` <br>
* Copy <br> <b>apoc-4.4.0.14-core.jar <br> </b> and <b> <br> neo4j-graph-data-science-2.3.1.jar</b> <br> into <br> ``./path/neo4j-community-4.4.18/plugins``
  * Path is your path for the neo4j
* Edit ``./path/neo4j-community-4.4.18/conf/neo4j.conf``
  * Create Database ``dbms.default_database=GraphLab``
  * Add ``apoc.import.file.enabled=true`` to enable APOC plugin
  * Disable authorization ``dbms.security.auth_enabled=false``
  * Enable APOC, GDS, ALGO ``dbms.security.procedures.unrestricted=apoc.*, algo.*, gds.*``
* Save the changes, and restart neo4j server.

### Designing the Graph 

[//]: # (% plesae add the schema and description) 

### Preprocessing the data
* Extract the keywords from the abstract
  * ...
  
[//]: # (  * I will add this later )

* Unzip the files in <br> ``./Samples/papers`` <br> ``./samples/citations``<br> ``./samples/embeddings`` <br>
* Run the [script](data_preperation.py)
  * This script change <b>JSONL</b> into <b>JSON</b>
  * Randomize the journals.
  * Randomize the volumes.
  * Randomize the proceedings.
  * Randomize the conferences.
  * Randomize the citation.
  * Randomize the city.
  * Randomize the country.
  * Save the data into the folder [preprocessed_data](./preprocessed_data/)
### Load data into neo4j 
#### Before executing the following queries, make sure to <br> copy the files in <br> `./preprocessed_data` <br> into <br> `/path/neo4j-community-4.4.18/import`
#####  Cypher queries
  * Clean the database <br>
    ```
    MATCH (n)
    DETACH DELETE n
    ```
  * Creating the main Nodes and their relation (Paper And Author) <br>
    ```
    CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
    CREATE (p:Paper {DOI: paper.externalIds.DOI, CorpusId: paper.externalIds.CorpusId , title: paper.title, abstract: paper.abstract})
    WITH p, paper.authors AS authors
    UNWIND authors AS author
    MERGE (a:Author {name: author.name, authorId: author.authorId})
    CREATE (p)-[w:WrittenBy]->(a)
    SET w.mainAuthor = CASE when author = head(authors) then 1 END
    ```
  * Create Topic-related nodes and relations  <br>
    ```
    CALL apoc.load.json("file://papers_json.json") YIELD value
    MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
    WITH  p, value.s2FieldsOfStudy as s2fields
    UNWIND s2fields AS s2f
    MERGE (kw:Keyword {name: s2f.category})
    MERGE (t:Topic {name: s2f.category})
    CREATE (t)<-[:RelatedTo]-(kw)<-[:ContainsKeyWord]-(p)
    ``` 
  * Create Journal-related nodes and relations <br>
    ```
    CALL apoc.load.json("file://papers_json.json") YIELD value
    MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
    WITH p, value WHERE value.journal IS NOT null
    MERGE (j:Journal {name: value.journal.name})
    MERGE (v:Volume {number: value.journal.volume})
    MERGE (v)-[:InJournal]->(j)
    CREATE (p)-[:PublishedInVolume]->(v)
    MERGE (y:Year {year: value.year})
    MERGE (v)-[:InYear]->(y)
    ```
    * Create Conference-related nodes and relations <br>
      ```
      CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
      MATCH (p:Paper{CorpusId: paper.externalIds.CorpusId})
      WITH p, paper, paper.venue AS ven WHERE paper.venue IS NOT null
      MERGE (pro:Proceeding {name: ven, edition: paper.edition})
      MERGE (c:Conference {name: ven})
      CREATE (p)-[:PublishedInProceeding]->(pro)
      MERGE (y:Year {year: paper.year})
      CREATE (pro)-[:InYear]->(y)
      CREATE (pro)-[:ofConference]->(c)
      MERGE (ci:City {name: paper.city})
      MERGE (co:Country{name: paper.country})
      CREATE (pro)-[:Heldin]->(ci)
      CREATE (ci)-[:BelongsTo]->(co)
      ```
  * Create citations' relationships <br>
    ```
    CALL apoc.load.json("file://citation_json.json") YIELD value AS info
    MATCH (src:Paper {CorpusId: info.citingCorpusId})
    MATCH (dst:Paper {CorpusId: info.citedCorpusId})
    CREATE (src)-[:Cites]->(dst)
    ```
  * Create reviewers edges <br>
    ```
    CALL apoc.load.json("file://papers_json.json") YIELD value
    MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
    WITH p, value.reviewers AS reviewers
    UNWIND reviewers AS reviewer
    MATCH (a:Author{authorId: reviewer})
    CREATE (p)-[:ReviewedBy]->(a)
    ```
  * Change data to have database-related papers
    ```
    // Remove old topics
    MATCH (t:Topic)
    WHERE t.name IN ["Data Modeling", "Indexing", "Big Data", "Data Querying"]
    DETACH DELETE t;
    // impute the topic
    match(k:Keyword)
    where k.name in ["Data Modeling", "Indexing", "Big Data", "Data Querying"]
    MERGE (t:Topic{name: "Database"})
    MERGE (t)<-[:RelatedTo]-(k) 

    ```
  * Clean duplicate edges (which might happen due to randomization)  <br>
    ```
    CALL apoc.periodic.iterate(
        "MATCH (a)-[r]->(b)
         WHERE id(a) < id(b)
         RETURN a, b, type(r) as type, collect(r) as rels",
        "FOREACH(rel in tail(rels) | DELETE rel)"
        , {batchSize:1000, parallel:false}
      );
    ```

### Extend the Graph in neo4j  
<b> This is part A.3 in the lab, it needs to be executed after Loading the data </b> <br>

##### Cypher queries

* Create Affiliation and related nodes/edges <br>
  ```
  CALL apoc.load.json("file://authors_json.json") YIELD value AS author_data
  match (a:Author {authorId: author_data.author_id})
  MERGE (aff:Institution{name:author_data.affiliations})
  create (a)-[:AffiliatedTo]->(aff)
  with aff, author_data 
  match (c:Country{name:author_data.country}) 
  create (aff)-[:IsInCountry]->(c)
  ```
* add Reviews attribute (static text for all relations for simplicity) <br>
  ```
  MATCH (n:Paper)-[r:ReviewedBy]->(a:Author)
  SET r.details = "es bien!"
  ```

## Week 2
All information can be found here [Part B](PartB_AliAbuSaleh_JoseAntonioLorencioAbril.py), [Part C](PartC_AliAbuSaleh_JoseAntonioLorencioAbril.py)

## Week 3
All information can be found here [Part D](PartD_AliAbuSaleh_JoseAntonioLorencioAbril.py)


