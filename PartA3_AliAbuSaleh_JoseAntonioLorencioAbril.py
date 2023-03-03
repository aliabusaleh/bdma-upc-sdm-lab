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

    def extend_graph(self):
        return self._create_affiliations(), self._add_review_attributes()

    def _create_affiliations(self):
        query = '''  
        CALL apoc.load.json("file://authors_json.json") YIELD value AS author_data
        match (a:Author {authorId: author_data.author_id})
        MERGE (aff:Institution{name:author_data.affiliations})
        create (a)-[:AffiliatedTo]->(aff)
        with aff, author_data 
        match (c:Country{name:author_data.country}) 
        create (aff)-[:IsInCountry]->(c)
        '''
        return self.query(query)

    def _add_review_attributes(self):
        query = '''
        MATCH (n:Paper)-[r:ReviewedBy]->(a:Author)
        SET r.details = "es bien!"
        '''

        return self.query(query)

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


if __name__ == '__main__':
    graph_handler = PropertyGraphLab("bolt://localhost:7687", "neo4j", "password")
    print(color.GREEN)
    print("hello, world! Cypher is speaking! connection established \n ")
    print(color.BLUE)
    graph_handler.extend_graph()
    print(color.GREEN + 'Database extended')

