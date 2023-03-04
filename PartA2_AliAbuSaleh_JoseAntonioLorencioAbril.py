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

    def __init__(self, uri, user, password):
        # in case you have auth username/password, please modify it  auth=(user, password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password) if (user and password) else None)

    def load_data(self):
        return self.__clean_previous_data(), \
               self._create_main_nodes(), \
               self._create_journal_nodes(), \
               self._create_conference_nodes(), \
               self._create_citation_nodes(), \
               self._create_reviewers_edges(), \
               self._clean_edges()

    def _create_main_nodes(self):
        # create paper nodes
        query = '''
                CALL apoc.load.json("file://papers_json.json") YIELD value AS paper
                CREATE (p:Paper {DOI: paper.externalids.DOI, CorpusId: paper.externalids.CorpusId , title: paper.title,
                abstract: "this is nice paper!"})
                WITH p,paper,  paper.authors AS authors
                UNWIND authors AS author
                CREATE (a:Author {name: author.name, authorId: author.authorId})
                CREATE (p)-[w:WrittenBy]->(a)
                SET w.mainAuthor = CASE when author = head(authors) then 1 END
                '''
        return self.query(query)

    def _create_journal_nodes(self):
        # create journal nodes
        query = '''
                CALL apoc.load.json("file://papers_json.json") YIELD value
                match (p:Paper{CorpusId: value.externalids.CorpusId})
                WITH value  where value.journal is not null
                CREATE (j:Journal {name: value.journal.name})
                CREATE (v:Volume {number: value.volume})
                create (v)-[:PublishedInVolume]->(j)
                CREATE (p)-[:IsIn]->(v)
                create (y:Year {year: p.year})
                create (v)-[:InYear]->(y)
                '''
        return self.query(query)

    def _create_conference_nodes(self):
        # create conference nodes
        query = '''
                CALL apoc.load.json("file://papers_json.json") YIELD value as paper
                match (p:Paper{CorpusId: paper.externalids.CorpusId})
                with p, paper, paper.venue as ven where paper.venue is not null
                create (pro:Proceeding {edition: p.edition})
                create (c:Conference {name: ven})
                create (p)-[:PublishedInProceeding]->(pro)
                create (y:Year {year: p.year})
                create (pro)-[:InYear]->(y)
                create (pro)-[:of]->(c)
                create (ci:City {name: paper.city})
                create (co:Country{name: paper.country})
                create (pro)-[:Heldin]->(ci)
                create (ci)-[:BelongsTo]->(co)
                  '''
        return self.query(query)

    def _create_citation_nodes(self):
        # create citation nodes
        query = '''
            call apoc.load.json("file://citation_json.json") yield value as info
            match (src:Paper {CorpusId: info.citingcorpusid})
            match (dst:Paper {CorpusId: info.citedcorpusid})
            create (src)-[:Cites]->(dst)
                  '''
        return self.query(query)

    def _create_reviewers_edges(self):
        # create reviewers edges
        query = '''
            CALL apoc.load.json("file://papers_json.json") YIELD value
            match (p:Paper{CorpusId: value.externalids.CorpusId})
            WITH p, value.reviewers as reviewers
            unwind reviewers as reviewer
            match (a:Author{authorId: reviewer.authorId})
                create (p)-[:ReviewedBy ]->(a)
                  '''
        return self.query(query)

    def _clean_edges(self):
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
            query = '''
                    MATCH (n)
                    DETACH DELETE n
                    '''
            return self.query(query)


if __name__ == '__main__':
    graph_handler = PropertyGraphLab("bolt://localhost:7687", "neo4j", "password")
    print(color.GREEN)
    print("hello, world! Cypher is speaking! connection established \n ")
    print(color.BLUE)
    graph_handler.load_data()
    print(color.GREEN + 'Database initiated and loaded, see you!')











