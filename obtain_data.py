import requests
import json
import time

# Replace this with your API key
api_key = "1WBrQVQGeo6ZZI2eJmWMk2eFnmgl8W1T7VEDvRyQ"

# Define the keywords you want to search for
keywords = ['data science', 'big data', 'databases']

# URL for the API endpoint that searches for papers
url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=data science+big data+databases&year=2023&limit=15&fields=title,externalIds,year,journal,venue,authors,abstract,s2FieldsOfStudy'

# Set the headers to include your API key
headers = {'x-api-key': api_key}

# Send a GET request to the API endpoint with the query parameters and headers
response = requests.get(url, headers=headers)

# If response is not 200, print the error message and exit
if response.status_code != 200:
    print(response.json().get('message'))
    exit()

papers = response.json().get('data', [])

# Map paper ID to CorpusID
paper_ids_cid = {}
for paper in papers:
    paper_ids_cid[paper['paperId']] = paper['externalIds']['CorpusId']
    # Append the paper to the json file of papers
    with open('semantic_sch_data/papers.json', 'a') as f:
        f.write(json.dumps(paper)+'\n')

def getReferences(paperID):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paperID}/references"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.json().get('message'))
        return []
    return response.json().get('data', [])

def getPaper(paperID):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paperID}?fields=title,externalIds,year,journal,venue,authors,abstract,s2FieldsOfStudy"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.json().get('message'))
        return []
    return response.json()

def getPapersRecursive(paperID, corpusID, depth, visited_papers):
    if depth == 0:
        return []
    print(f'Processing paper {paperID}')
    references = getReferences(paperID)
    for reference in references:
        if reference['citedPaper']['paperId'] is None:
            continue
        paper = getPaper(reference['citedPaper']['paperId'])
        if paper is None:
            continue
        with open('semantic_sch_data/citations.json', 'a') as f:
            f.write(f"{{\"citingCorpusId\":\"{corpusID}\", \"citedCorpusId\":\"{paper['externalIds']['CorpusId']}\"}}\n")
        if paper['paperId'] in visited_papers:
            continue
        with open('semantic_sch_data/papers.json', 'a') as f:
            f.write(json.dumps(paper)+'\n')
        visited_papers.append(paper['paperId'])
        getPapersRecursive(paper['paperId'],paper['externalIds']['CorpusId'], depth-1, visited_papers)

depth = 3
visited_papers = []
request_count = 0

# For each paperID in the map
for paperID in paper_ids_cid:
    # Get the corpusID for the paperID
    corpusID = paper_ids_cid[paperID]
    # Get the papers recursively
    getPapersRecursive(paperID, corpusID, depth, visited_papers)