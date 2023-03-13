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

    def find_louvain_communities(self, min_community_size=50):
        if not self._check_if_graph_exits('cited_authors'):
            self._project_authors()
        query = f'CALL gds.louvain.stream(\'cited_authors\')\
            YIELD nodeId, communityId\
            WITH communityId, COLLECT(gds.util.asNode(nodeId).name) as community\
            WHERE size(community) > {min_community_size}\
            RETURN communityId, size(community) as nMembers, community'
        return self.query(query)

    def _project_authors(self):
        # Delete projected graph if exits before
        query = '''
        CALL gds.graph.drop('cited_authors', false);
        '''
        self.query(query)

        # Project the new graph
        query = '''
            CALL gds.graph.project.cypher(
                'cited_authors',
                'MATCH (a:Author) RETURN id(a) as id', 
                'MATCH (citing:Author)<-[:WrittenBy]-(:Paper)-[:Cites]->(:Paper)-[:WrittenBy]->(cited:Author)
                    RETURN id(citing) AS source, id(cited) AS target',
                    { validateRelationships: false }
                    ) YIELD
                        graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;
        '''
        return self.query(query)

    def _project_biggest_louvain_community(self):
        if not self._check_if_graph_exits('cited_authors'):
            self._project_authors()
        query = '''
        CALL gds.graph.project.cypher(
            "biggest_community",
            'CALL gds.louvain.stream("cited_authors")
            YIELD nodeId, communityId
            WITH communityId, COLLECT(gds.util.asNode(nodeId)) AS authors
            WITH communityId, authors, size(authors) AS nAuthors
            ORDER BY nAuthors DESC LIMIT 1
            UNWIND authors AS author
            RETURN communityId, ID(author) AS id',
            'MATCH (citing:Author)<-[:WrittenBy]-(:Paper)-[:Cites]->(:Paper)-[:WrittenBy]->(cited:Author)
                RETURN id(citing) AS source, id(cited) AS target',
            { validateRelationships: false }
            ) YIELD
                graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels;
        '''
        return self.query(query)

    def find_top_authors_biggest_com(self, num=10):
        if not self._check_if_graph_exits('biggest_community'):
            self._project_biggest_louvain_community()
        query = f'CALL gds.pageRank.stream(\'biggest_community\')\
            YIELD nodeId, score\
            WITH nodeId as nodeIdBC, score as scoreBC\
            CALL gds.pageRank.stream(\'cited_authors\')\
            YIELD nodeId, score\
            WHERE nodeId = nodeIdBC\
            RETURN gds.util.asNode(nodeId).name AS author, score as fullScore, scoreBC as communityScore\
            ORDER BY communityScore DESC, author ASC\
            LIMIT {num}'
        return self.query(query)
    
    def find_top_authors_all(self, num=10):
        if not self._check_if_graph_exits('cited_authors'):
            self._project_authors()
        query = f'CALL gds.pageRank.stream(\'cited_authors\')\
            YIELD nodeId, score\
            RETURN gds.util.asNode(nodeId).name AS author, score\
            ORDER BY score DESC, author ASC\
            LIMIT {num}'
        return self.query(query)

    def _check_if_graph_exits(self, graph_name):
        query = f'''
        RETURN gds.graph.exists('{graph_name}') AS personsExists
        '''
        return self.query(query)[0][0]

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
    menu_message = "Please choose the task to perform \n (1) Compute the page rank of all authors in the database." + \
                   "\n (2) Compute the louvain communities bigger than a given value.\n" + \
                   " (3) Get the pagerank of the authors of the biggest community, compared to their pagerank in the whole graph." + \
                   "\n (4) exit \n Input: "
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
            print("How many authors do you want to see? (default 10)")
            num = input()
            if num == "":
                num = 10
            print(graph_handler.find_top_authors_all(num))
        elif mode == 2:
            print("What is the minimum community size? (default 50)")
            min_community_size = input()
            if min_community_size == "":
                min_community_size = 50
            print(graph_handler.find_louvain_communities(min_community_size))
        elif mode == 3:
            print("How many authors do you want to see? (default 10)")
            num = input()
            if num == "":
                num = 10
            print(graph_handler.find_top_authors_biggest_com(num))
        elif mode == 4:
            exit(1)
        mode = print_menu()
