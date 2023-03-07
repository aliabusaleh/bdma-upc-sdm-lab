import requests
import json

# Replace this with your API key
api_key = "1WBrQVQGeo6ZZI2eJmWMk2eFnmgl8W1T7VEDvRyQ"

# Define the keywords you want to search for
keywords = ['data science', 'big data', 'databases']

# URL for the API endpoint that searches for papers
url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=data science+big data+databases&year=2023&limit=8&fields=title,externalIds,year,journal,venue,authors,abstract,s2FieldsOfStudy'

# Set the headers to include your API key
headers = {'x-api-key': api_key}

# Send a GET request to the API endpoint with the query parameters and headers
response = requests.get(url, headers=headers)

# If response is not 200, print the error message and exit
if response.status_code != 200:
    print(response.json().get('message'))
    exit()

papers = response.json().get('data', [])



depth = 2
paper_ids = []
for i in range(depth):
    print(f"Depth {i}")
    for paper in papers:
        # Append the paper to the json file of papers
        with open('semantic_sch_data/papers.json', 'a') as f:
            f.write(json.dumps(paper)+'\n')
        # Get the referenced papers through the endpoint /paper/{paperId}/references
        # Only if the paper has a paperId, it is not None and the paperId is not already in the list
        if paper['paperId'] is None or paper['paperId'] in paper_ids:
            continue
        paper_ids.append(paper['paperId']) # Mark the paper as visited
        url2 = f"https://api.semanticscholar.org/graph/v1/paper/{paper['paperId']}/references"
        response2 = requests.get(url2, headers=headers)
        references = response2.json().get('data', []) # Get the references
        papers2 = []
        for reference in references:
            # Only processed the references that have a paperId not None
            if reference['citedPaper']['paperId'] is None:
                continue
            # Get the paper data through the endpoint /paper/{paperId}
            url3 = f"https://api.semanticscholar.org/graph/v1/paper/{reference['citedPaper']['paperId']}?fields=title,externalIds,year,journal,venue,authors,abstract,s2FieldsOfStudy"
            paper2 = requests.get(url3, headers=headers).json()
            papers2.append(paper2) # Append the paper to the list of papers
            # Append the reference to the json file of references: [{"citingCorpusId":"paper", "citedCorpusId":"reference"}]
            with open('semantic_sch_data/citations.json', 'a') as f:
                f.write(f"{{\"citingCorpusId\":\"{paper['externalIds']['CorpusId']}\", \"citedCorpusId\":\"{paper2['externalIds']['CorpusId']}\"}}\n")
        print(f"Retrieved {len(papers2)} references for paper {paper['title']}")
    # Add the papers to the list of papers to be processed in the next iteration
    papers = papers2
