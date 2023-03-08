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

    def find_top_3_papers(self):
        query = '''  
        MATCH (c:Conference)<-[:ofConference]-(:Proceeding)<-[:PublishedInProceeding]-(p:Paper)<-[cite:Cites]-(q:Paper)
        WITH c.name AS conference, p.title AS article, COUNT(cite) as citations
        WITH conference, article, citations ORDER BY citations DESC
        WITH conference, COLLECT(article) AS articles, COLLECT(citations) AS citations
        WITH conference, [i IN range(0,size(articles)-1) | [articles[i], citations[i]]] AS ArtCit
        RETURN conference, ArtCit[0..3] AS Citations
        ORDER BY conference
        '''
        return self.query(query)

    def find_conference_community(self):
        query = '''
        MATCH (c:Conference)<-[:ofConference]-(pr:Proceeding)<-[:PublishedInProceeding]-(:Paper)-[:WrittenBy]->(a:Author)
        WITH c.name AS conference, a.name AS author, COUNT(pr) as nParticipations
        WHERE nParticipations >= 4
        WITH conference, COLLECT(author) as authors, COLLECT(nParticipations) as nParticipations
        WITH conference, [i IN range(0, size(authors)-1) | [authors[i],nParticipations[i]]] as authors_participations
        RETURN conference, authors_participations
        '''
        return self.query(query)

    def find_impact_factor(self):
        query = '''
        WITH date.truncate('year', date.realtime()).year AS year
        MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year-2}), (v)<-[:PublishedInVolume]-(p:Paper)
        WITH j, year, COUNT(p) AS publications_y2
        MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year-1}), (v)<-[:PublishedInVolume]-(p:Paper)
        WITH j, year, publications_y2, COUNT(p) AS publications_y1
        MATCH (j:Journal)<-[:InJournal]-(v:Volume)-[:InYear]->(y:Year {year:year}), (v)<-[:PublishedInVolume]-(:Paper)<-[citation:Cites]-(:Paper)
        WITH j, publications_y2, publications_y1, COUNT(citation) AS citations_y
        RETURN j.name, toFloat(citations_y) / (publications_y1 + publications_y2) AS ImpactFactor
        '''
        return self.query(query)

    def find_h_index(self):
        query = '''
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
    menu_message = "Please choose the task to perform \n (1) B.1 (Find the first Top 3 cited papers of each " \
                   "conference) " + \
                   "\n (2) B.2 (For each conference find its community)\n" + \
                   " (3) B.3 (Find the impact factor of the journals in the graph) " + \
                   "\n (4) B.4 (Find the H-index of the authors in the graph). \n (5) exit \n Input: "
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
    print("Main Program Part (B) Menu, Please follow the instructions! \n ")
    print(color.BLUE)
    mode = print_menu()

    while mode:
        if mode == 1:
            print(graph_handler.find_top_3_papers())
        elif mode == 2:
            print(graph_handler.find_conference_community())
        elif mode == 3:
            print(graph_handler.find_impact_factor())
        elif mode == 4:
            print(graph_handler.find_h_index())
        elif mode == 5:
            exit(1)
        mode = print_menu()


