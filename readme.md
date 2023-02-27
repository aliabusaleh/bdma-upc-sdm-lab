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
* Load the [Data](https://www.kaggle.com/datasets/Cornell-University/arxiv)  into neo4j.
  * The data is taken from Kaggle.
* Discuss improvements we can do to improve the design in step 1.

## Prerequisites
 * All prerequisites libraries, versions, ...etc are mentioned in [here](requirements.txt) 
### Designing the Graph 

[//]: # (% plesae add the schema and description) 

### Preprocessing the data
* Extract the keywords from the abstract 
  * The Dataset on Kaggle has no keywords, so we needed to extract it, we used library <b>[yake](https://pypi.org/project/yake/)</b> for 
  that, which is "Unsupervised Approach for Automatic Keyword Extraction using Text Features."
  * Python [script](keywork_extraction.py) was written for that.
  * Usage
  * ``
  ./keywork_extraction data_source_path data_source_destination 
  ``
* Generate affiliation for each paper
  * We also need to generate affiliation for each paper, for that we used dataset of 
  world universities that's available [here](https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json)
  * Python [script](affiliation_assignment.py) used for that purpose 
### Load data into neo4j 
*  
