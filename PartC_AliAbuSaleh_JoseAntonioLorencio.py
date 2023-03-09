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


def print_database_keywords():
    database_keywords = ["Data Modeling", "Indexing", "Big Data", "Data Querying"]
    return_keywords = f"Database community keywords are: {[kw for kw in database_keywords]}"
    return return_keywords


class PropertyGraphLab:

    def __init__(self, uri, user, password):
        # in case you have auth username/password, please modify it  auth=(user, password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password) if (user and password) else None)

    def find_database_community(self):
        query = '''
        MATCH (p:Paper)-[:ContainsKeyWord]->(:Keyword)-[:RelatedTo]->(t:Topic)
        OPTIONAL match (p)-[:PublishedInVolume]->(:Volume)-[:InJournal]->(j:Journal)
        OPTIONAL match (p)-[:PublishedInProceeding]->(:Proceeding)-[:ofConference]->(c:Conference)
    
        WITH p, j, c,
             COUNT(CASE WHEN t.name = "Database" THEN 1 END) AS database_topics_count,
             COUNT(*) AS total_topics_count,
             CASE WHEN j.name IS NULL THEN 'Journal' ELSE 'CONFERENCE' END as source
        WITH p, j, c, source, total_topics_count as TotalPublications, database_topics_count as DatabasePublications, (toFloat(database_topics_count) / total_topics_count * 100) as Percentage
        WHERE Percentage >=90
        RETURN COALESCE(j.name, c.name) as Name, source as TypeOfInstitution,  TotalPublications, DatabasePublications, Percentage
        ORDER BY Percentage DESC
        '''
        return self.query(query)

    def _project_database_community_graph(self):
        # Delete projected graph if exits before
        query = '''
        CALL gds.graph.drop('papers', false);
        '''
        self.query(query)

        # Project the new graph
        query = '''
        // project the papers for the database community 
        CALL gds.graph.project.cypher(
          'papers',
          'MATCH (p:Paper)-[:ContainsKeyWord]->(:Keyword)-[:RelatedTo]->(t:Topic)
           OPTIONAL MATCH (p)-[:PublishedInVolume]->(:Volume)-[:InJournal]->(j:Journal)
           OPTIONAL MATCH (p)-[:PublishedInProceeding]->(:Proceeding)-[:ofConference]->(c:Conference)
           WITH p, j, c,
                COUNT(CASE WHEN t.name = "Database" THEN 1 END) AS database_topics_count,
                COUNT(*) AS total_topics_count,
                CASE WHEN j.name IS NULL THEN "Journal" ELSE "CONFERENCE" END as source
           WITH p, j, c, source, total_topics_count as TotalPublications, database_topics_count as DatabasePublications, (toFloat(database_topics_count) / total_topics_count * 100) as Percentage
           WHERE Percentage >=90
           RETURN id(p) as id',
           'MATCH (p:Paper)-[:Cites]-(q:Paper)
           RETURN id(p) AS source, id(q) AS target',
           { validateRelationships: false }
        ) YIELD
           graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;
        '''
        return self.query(query)

    def _project_top_100(self):
        # use graph generated in C.2
        if not self._check_if_graph_exits('papers'):
            self._project_database_community_graph()
        query = '''
        CALL gds.graph.project.cypher('top100Papers', '
        CALL gds.pageRank.stream("papers")
        YIELD nodeId, score
        WITH gds.util.asNode(nodeId) as paper, score, nodeId
        WHERE score > 0     
        WITH paper, score, nodeId
        MATCH (paper)-[:Cites]->(citedPaper)
        WITH paper, COUNT(DISTINCT citedPaper) AS numCitations, score, nodeId
        RETURN nodeId as id
        ORDER BY score DESC
        LIMIT 100',
        'MATCH (p:Paper)-[:WrittenBy]-(q:Author)
        RETURN id(p) AS source, id(q) AS target',
        { validateRelationships: false }
        ) YIELD
               graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;
        '''
        return self.query(query)

    def find_top_papers_pagerank(self):
        # use graph generated in C.2
        if not self._check_if_graph_exits('papers'):
            self._project_database_community_graph()
        query = '''
            // Use projected Papers
            CALL gds.pageRank.stream('papers')
            YIELD nodeId, score
            WITH gds.util.asNode(nodeId) as paper, score
            WHERE score > 0
        
            // Find the top papers based on incoming page rank and the number of citations from the same community
            RETURN DISTINCT paper.title AS PaperTitle, score AS PageRank
            ORDER BY score DESC
            LIMIT 100
        '''
        return self.query(query)

    def _check_if_graph_exits(self, graph_name):
        query = f'''
        RETURN gds.graph.exists('{graph_name}') AS personsExists
        '''
        return self.query(query)[0][0]

    def find_gurus(self):
        # Use graph generated in C.3
        if not self._check_if_graph_exits('top100Papers'):
            self._project_top_100()
        query = '''
              MATCH (paper)-[:Cites]->(m)
              WHERE gds.alpha.linkprediction.commonNeighbors(paper, m, { graph: 'top100Papers' }) > 2
              WITH paper
              MATCH (paper)-[:WrittenBy]->(author:Author)
              WITH author.name as guruName, collect(paper) AS papers, count(paper) AS paperCount
              WHERE paperCount >= 2
              RETURN  guruName as AuthorName, paperCount as NumberOfPapers
              ORDER BY paperCount DESC limit 10
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


def print_menu():
    print(color.GREEN)
    menu_message = "Please choose the task to perform \n (1) C.1 (Print the database-community keywords)" + \
                   "\n (2) C.2 (Find database community)\n" + \
                   " (3) C.3 (Find top 100 papers based on PageRank for database-community Journals/Conferences) " + \
                   "\n (4) C.4 (Find Gurus for Papers in Part C.3). \n (5) exit \n Input: "
    mode_ = input(menu_message)
    mode_ = int(mode_)
    print(color.CYAN)
    while int(mode_) not in [1, 2, 3, 4, 5]:
        print(color.RED + "Error input, please read the instructions carefully" + color.GREEN)
        mode_ = input(menu_message)
    else:
        return mode_


if __name__ == '__main__':
    graph_handler = PropertyGraphLab("bolt://localhost:7687", "neo4j", "password")
    print(color.GREEN)
    print("Main Program Part (C) Menu, Please follow the instructions! \n ")
    print(color.BLUE)
    mode = print_menu()

    while mode:
        if mode == 1:
            print(print_database_keywords())
        elif mode == 2:
            print(graph_handler.find_database_community())
        elif mode == 3:
            print(graph_handler.find_top_papers_pagerank())
        elif mode == 4:
            print(graph_handler.find_gurus())
        elif mode == 5:
            exit(1)
        mode = print_menu()
