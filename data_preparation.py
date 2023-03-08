import json
import random

## Papers
papers = [json.loads(l) for l in open("semantic_sch_data/papers.json", "r", encoding="utf8").readlines()]

# If an author of a paper has authorId null, we delete it
for paper in papers:
    paper['authors'] = [a for a in paper['authors'] if a['authorId'] is not None]

# If the year of a paper is null, we change it to 2000
for paper in papers:
    if paper['year'] is None:
        paper['year'] = 2000

## Citations
citations = [json.loads(l) for l in
             open("semantic_sch_data/citations.json", "r", encoding="utf8").readlines()]
# Transform the CorpusId into integers
for citation in citations:
    citation['citingCorpusId'] = int(citation['citingCorpusId'])
    citation['citedCorpusId'] = int(citation['citedCorpusId'])

## Embeddings
#embeddings = [json.loads(l) for l in
#              open("samples/embeddings/embeddings-sample.jsonl", "r", encoding="utf8").readlines()]

# ## Authors
# authors = [json.loads(l) for l in open("samples/authors/authors-sample.jsonl", "r", encoding="utf8").readlines()]

## S2ORC
#docs = [json.loads(l) for l in open("samples/s2orc/s2orc-sample.jsonl", "r", encoding="utf8").readlines()]
#text = docs[0]['content']['text']
#annotations = {k: json.loads(v) for k, v in docs[0]['content']['annotations'].items() if v}

# random journal
journals = {
    "aacr": "American Association for Cancer Research (AACR)",
    "acm": "Association for Computing Machinery (ACM)",
    "acs": "American Chemical Society (ACS)",
    "afs": "American Fisheries Society (AFS)",
    "agu": "American Geophysical Union (AGU)",
    "aiaa": "American Institute of Aeronautics and Astronautics (AIAA)",
    "aip": "American Institute of Physics (AIP)",
    "aims": "AIMS Journals",
    "american-physical-society": "American Physical Society (APS)",
    "ams": "American Meteorological Society (AMS)",
    "amstat": "American Statistical Association",
    "annual-reviews": "Annual Reviews",
    "aosis": "AOSIS",
    "apa": "American Psychological Association (APA)",
    "aps": "American Physiological Society (APS)",
    "asa": "American Sociological Association (ASA)",
    "asce": "American Society of Civil Engineers (ASCE)",
    "asm": "American Society for Microbiology (ASM)",
    "asme": "American Society of Mechanical Engineers (ASME)",
    "aspet": "American Society for Pharmacology and Experimental Therapeutics (ASPET)",
    "baishideng": "Baishideng Publishing Group",
    "begell-house": "Begell House",
    "bes": "British Ecological Society",
    "biologists": "The Company of Biologists",
    "bmj": "BMJ",
    "cell-press-research": "Cell Press - Research Journals",
    "cell-press-trends": "Cell Press - Trends Journals",
    "copernicus": "Copernicus",
    "csiro": "Commonwealth Scientific and Industrial Research Organisation",
    "current-opinion": "Elsevier Current Opinion",
    "elsevier": "Elsevier",
    "elsevier-es": "Elsevier España",
    "expert-reviews": "Expert Review journal series",
    "endocrine-press": "Endocrine Society",
    "fems": "Federation of European Microbiological Societies (FEMS)",
    "frontiers": "Frontiers",
    "future-science-group": "Future Science Group",
    "healio": "Healio",
    "ieee": "Institute of Electrical and Electronics Engineers (IEEE)",
    "iet": "The Institution of Engineering and Technology (IET)",
    "ima": "Institute of Mathematics and its Applications",
    "ims": "Institute of Mathematical Statistics",
    "informs": "Institute for Operations Research and the Management Sciences (INFORMS)",
    "int-res": "Inter-Research Science Center",
    "integrated-science-publishing": "Integrated Science Publishing",
    "iop": "IOP Publishing",
    "iucr": "International Union of Crystallography (IUCr)",
    "karger": "Karger",
    "landes-bioscience": "Landes Bioscience",
    "mal": "Mary Ann Liebert, Inc. (MAL)",
    "mdpi": "Multidisciplinary Digital Publishing Institute (MDPI)",
    "mhra": "Modern Humanities Research Association (MHRA)",
    "microbiology-society": "Microbiology Society",
    "mnhn": "Muséum national d'Histoire naturelle",
    "mp": "Medicine Publishing",
    "nihr": "National Institute of Health Research",
    "nrc": "NRC Research Press",
    "npg": "Nature Publishing Group",
    "oikos": "Oikos Editorial Office",
    "osa": "The Optical Society (OSA)",
    "pensoft": "Pensoft Publishers",
    "plos": "Public Library Of Science (PLOS)",
    "royal-society": "The Royal Society",
    "rsc": "Royal Society of Chemistry (RSC)",
    "slas": "Society for Laboratory Automation and Screening (SLAS)",
    "spandidos": "Spandidos Publications",
    "spie": "SPIE",
    "springer": "Springer",
    "springer-fachzeitschriften-medizin": "Springer Fachzeitschriften Medizin",
    "taylor-and-francis": "Taylor & Francis",
    "the-geological-society": "The Geological Society of London",
    "thieme": "Thieme Fachzeitschriften",
    "tr-law-australia": "Thomson Reuters Legal, Tax and Accounting Australia"
}
# random conf
conf = [
  {
    "title": "Agent Conf",
    "url": "http://www.agent.sh/",
    "where": "Dornbirn, Austria",
    "when": "January 20-21, 2017",
    "month": "January",
    "submissionDeadline": ""
  },
  {
    "title": "O'Reilly Velocity Conference",
    "url": "http://conferences.oreilly.com/velocity/vl-ca",
    "where": "San Jose, CA",
    "when": "January 19-22, 2017",
    "month": "January",
    "submissionDeadline": ""
  },
  {
    "title": "Script17",
    "url": "https://scriptconf.org/",
    "where": "Linz, Austria",
    "when": "January 27, 2017",
    "month": "January",
    "submissionDeadline": ""
  },
  {
    "title": "Agile Content Conf",
    "url": "https://2017.agilecontentconf.com/",
    "where": "London, UK",
    "when": "January 30-31, 2017",
    "month": "January",
    "submissionDeadline": ""
  },
  {
    "title": "Jfokus",
    "url": "http://www.jfokus.se/jfokus/",
    "where": "Stockholm, Sweden",
    "when": "February 6-8, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "Webstock",
    "url": "http://www.webstock.org.nz/17/",
    "where": "Wellington, New Zealand",
    "when": "February 13-17, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "Sustainable UX",
    "url": "http://sustainableux.com/",
    "where": "Online",
    "when": "February 16, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "The Rolling Scopes Conference",
    "url": "https://2017.conf.rollingscopes.com/",
    "where": "Minsk, Belarus",
    "when": "February 18-19, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "The Lead Developer New York",
    "url": "http://2017.theleaddeveloper-ny.com/",
    "where": "New York City, US",
    "when": "February 21, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "Voxxed Days - Zurich",
    "url": "https://voxxeddays.com/zurich/",
    "where": "Zurich, Switzerland",
    "when": "February 23, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "UX Riga",
    "url": "http://www.uxriga.lv/",
    "where": "Riga, Latvia",
    "when": "February 23, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "Typography Day 2017",
    "url": "http://www.typoday.in/",
    "where": "Moratuwa, Sri Lanka",
    "when": "February 23, 2017",
    "month": "February",
    "submissionDeadline": ""
  },
  {
    "title": "Voxxed Days - Cern",
    "url": "https://voxxeddays.com/cern/",
    "where": "Geneva, Switzerland",
    "when": "February 25, 2017",
    "month": "February",
    "submissionDeadline": ""
  }]

# random country
countries = [
    {
  "name": "Belgium",
  "city": "Brussels"
}, {
  "name": "Italy",
  "city": "Rome"
}, {
  "name": "Germany",
  "city": "Berlin"
}, {
  "name": "Spain",
  "city": "Barcelona"
}, {
  "name": "France",
  "city": "Paris"
}, {
  "name": "United Kingdom",
  "city": "London"
}]

# random affiliation

affiliations = [
    {
        "name": "ULB",
        "country":  "Belgium",
        "city": "Brussels"
     },
    {
        "name": "UPC",
        "country":"Spain",
        "city": "Barcelona"
     },
    {
        "name": "UniPd",
        "country": "Italy",
        "city": "Rome"
    },
    {
        "name": "CS",
        "country": "France",
        "city": "Paris"
    },
    {
        "name": "Humboldt University of Berlin",
        "country": "Germany",
        "city": "Berlin"
    }
]

# build map to paper - authors
paper_authors = {}
for paper in papers:
    paper_authors[paper['externalIds']['CorpusId']] = [author['authorId'] for author in paper['authors'] if author['authorId'] is not None]

paper_ids = list(set([paper["externalIds"]["CorpusId"] for paper in papers]))

authors_ids = []
for paper in papers:
    authors_ids.extend([author['authorId'] for author in paper['authors'] if author['authorId'] is not None and author['authorId'] not in authors_ids]) 
    conidx_cty = int(random.randint(0, 5))
    paper['country'] = countries[conidx_cty]['name']
    paper['city'] = countries[conidx_cty]['city']
    if paper['abstract'] is None:
        paper['abstract'] = "No abstract available"
    # As there are few conferences, we fake one with probability 1/3
    if not paper.get('journal') or random.randint(0, 2) == 0:
        conidx = int(random.randint(0, 12))
        paper['venue'] = conf[conidx]['title']
        paper['edition'] = int(random.randint(0, 3)) # simple way to fake edition
        paper['journal'] = None
    else:
        if not paper['journal'].get('name'):
          paper['journal']['name'] = list(journals.values())[int(random.randint(0, 10))]
        paper['venue'] = None
        # if no volume - fake it!
        if not paper['journal'].get('volume'):
            paper['journal']['volume'] = int(random.randint(0, 10))

for paper in papers:
    # assign reviewers: a reviewer is an author different from the paper's authors
    howmany = random.randint(1, 4)
    paper['reviewers'] = []
    while howmany > 0:
        selected = int(random.randint(0, len(authors_ids)-1))
        possible_reviewer = authors_ids[selected]
        if possible_reviewer not in paper_authors[paper['externalIds']['CorpusId']]:
            paper['reviewers'].append(authors_ids[selected])
            howmany -= 1

# randomize the affiliations
authors = []
for author_id in authors_ids:
    uni_rand = random.randint(0,4)
    authors.append({'author_id': author_id,
                   'affiliations': affiliations[uni_rand]['name'],
                    'country': affiliations[uni_rand]['country'],
                    'city': affiliations[uni_rand]['city']
                    })

# save paper changes
with open('./preprocessed_data/papers_json.json', 'w') as fout:
    json.dump(papers, fout)

# save citation as json
with open('preprocessed_data/citation_json.json', 'w') as fout:
    json.dump(citations, fout)

# save authors as json
with open('preprocessed_data/authors_json.json', 'w') as fout:
    json.dump(authors, fout)

# save paper_ids as json
with open('preprocessed_data/paper_ids_json.json', 'w') as fout:
    json.dump(paper_ids, fout)


