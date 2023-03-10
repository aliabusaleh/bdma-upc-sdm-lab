import os
from neo4j import GraphDatabase


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class PropertyGraphLab:

    """
    Function init: connect to the database
    - uri: the uri of the database
    - user: the username of the database
    - password: the password of the database

    In case you have auth username/password, please modify the code accordingly
    """
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password) if (user and password) else None)

    """
    Function load_data: load the data from the json files into the database
    """
    def load_data(self):
        return self.__clean_previous_data(), \
               self._create_main_nodes(), \
               self._create_topics_nodes(), \
               self._create_journal_nodes(), \
               self._create_conference_nodes(), \
               self._create_citation_nodes(), \
               self._create_reviewers_edges(), \
               self._fix_database_relation(), \
               self._clean_edges()

    """
    Function _CREATE_main_nodes: CREATE the main nodes of the graph, i.e., Paper, Author, and the edges between them

    Assumptions:
    - The json file is in the import folder of neo4j
    - The json file is called papers_json.json
    - The main author is the first author in the list of authors
    """
    def _create_main_nodes(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating papers and authors..." + color.END)
        # CREATE paper nodes
        query = '''
                CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
                CREATE (p:Paper {DOI: paper.externalIds.DOI, CorpusId: paper.externalIds.CorpusId , title: paper.title, abstract: paper.abstract})
                WITH p, paper.authors AS authors
                UNWIND authors AS author
                MERGE (a:Author {name: author.name, authorId: author.authorId})
                CREATE (p)-[w:WrittenBy]->(a)
                SET w.mainAuthor = CASE when author = head(authors) then 1 END
                '''
        return self.query(query)
    
    def _create_topics_nodes(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating topics and keywords..." + color.END)
        query = '''
            CALL apoc.load.json("file://papers_json.json") YIELD value
            MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
            WITH  p, value.s2FieldsOfStudy as s2fields
            UNWIND s2fields AS s2f
            MERGE (kw:Keyword {name: s2f.category})
            MERGE (t:Topic {name: s2f.category})
            CREATE (t)<-[:RelatedTo]-(kw)<-[:ContainsKeyWord]-(p)
            '''
        return self.query(query)

    def _create_journal_nodes(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating journals and volumes..." + color.END)
        # CREATE journal nodes
        query = '''
                CALL apoc.load.json("file://papers_json.json") YIELD value
                MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
                WITH p, value WHERE value.journal IS NOT null
                MERGE (j:Journal {name: value.journal.name})
                MERGE (v:Volume {number: value.journal.volume})
                MERGE (v)-[:InJournal]->(j)
                CREATE (p)-[:PublishedInVolume]->(v)
                MERGE (y:Year {year: value.year})
                MERGE (v)-[:InYear]->(y)
                '''
        return self.query(query)

    def _create_conference_nodes(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating conferences, proceedings, and cities..." + color.END)
        # CREATE conference nodes
        query = '''
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
                  '''
        return self.query(query)

    def _create_citation_nodes(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating citations..." + color.END)
        # CREATE citation nodes
        query = '''
            CALL apoc.load.json("file://citation_json.json") YIELD value AS info
            MATCH (src:Paper {CorpusId: info.citingCorpusId})
            MATCH (dst:Paper {CorpusId: info.citedCorpusId})
            CREATE (src)-[:Cites]->(dst)
                  '''
        return self.query(query)

    def _create_reviewers_edges(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Creating reviewers..." + color.END)
        # CREATE reviewers edges
        query = '''
            CALL apoc.load.json("file://papers_json.json") YIELD value
            MATCH (p:Paper{CorpusId: value.externalIds.CorpusId})
            WITH p, value.reviewers AS reviewers
            UNWIND reviewers AS reviewer
            MATCH (a:Author{authorId: reviewer})
            CREATE (p)-[:ReviewedBy]->(a)
                  '''
        return self.query(query)

    def _fix_database_relation(self):
        query = '''
        MATCH (t:Topic)
        WHERE t.name IN ["Data Modeling", "Indexing", "Big Data", "Data Querying", "Computer Science", "Education",
         "Database", "Psychology", "Political Science", "Business"]
        DETACH DELETE t
        '''
        self.query(query)
        query = '''
        match(k:Keyword)
        where k.name in ["Data Modeling", "Indexing", "Big Data", "Data Querying", "Computer Science", "Education",
         "Database", "Psychology", "Political Science", "Business"]
        MERGE (t:Topic{name: "Database"})
        MERGE (t)<-[:RelatedTo]-(k) 
        '''
        return self.query(query)
    def _clean_edges(self):
        print(color.BOLD + color.UNDERLINE + color.GREEN + "Cleaning edges..." + color.END)
        query = '''
        CALL apoc.periodic.iterate(
          "MATCH (a)-[r]->(b)
           WHERE id(a) < id(b)
           RETURN a, b, type(r) as type, collect(r) as rels",
          "FOREACH(rel in tail(rels) | DELETE rel)"
          , {batchSize:1000, parallel:false}
        );
                          '''
        self.query(query)
        query_v2 = '''
         CALL apoc.periodic.iterate(
          "MATCH (a)-[r]->(b)
           WHERE id(a) > id(b)
           RETURN a, b, type(r) as type, collect(r) as rels",
          "FOREACH(rel in tail(rels) | DELETE rel)"
          , {batchSize:1000, parallel:false}
        );
        '''
        return self.query(query_v2)

    def close(self):
        self.driver.close()

    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

    def __clean_previous_data(self):
        print(color.DARKCYAN + 'Please make sure you did \n 1- executed the data_preparation.py \n '
                               '2- copied the files in ./preprocessed_data/ to neo4j/import dicrectory')
        inp = input(color.CYAN + "All data in the current " + color.RED + "*ACTIVE* Database will be " +
                    color.BOLD + "erased! continue? Y/N \t ")
        while inp not in ['Y', 'N']:
            inp = input("All data in the current Database will be erased! continue? Y/N \t ")
        if inp == 'N':
            exit(-1)
        else:
            print(color.DARKCYAN + 'Deleting all nodes and edges... \n')
            query = '''
                    MATCH (n)
                    DETACH DELETE n
                    '''
            return self.query(query)


if __name__ == '__main__':
    graph_handler = PropertyGraphLab("bolt://localhost:7687", "neo4j", "password")
    print(color.GREEN)
    print("Hello, world! Cypher is speaking! Connection established. \n ")
    print(color.BLUE)
    graph_handler.load_data()
    print(color.GREEN + 'Database initiated and loaded, see you!')












