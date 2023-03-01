import json
import random

## Papers
papers = [json.loads(l) for l in open("samples/papers/papers-sample.jsonl", "r", encoding="utf8").readlines()]

## Citations
citations = [json.loads(l) for l in
             open("samples/citations/citations-sample.jsonl", "r", encoding="utf8").readlines()]

## Embeddings
embeddings = [json.loads(l) for l in
              open("samples/embeddings/embeddings-sample.jsonl", "r", encoding="utf8").readlines()]

##

## S2ORC
docs = [json.loads(l) for l in open("samples/s2orc/s2orc-sample.jsonl", "r", encoding="utf8").readlines()]
text = docs[0]['content']['text']
annotations = {k: json.loads(v) for k, v in docs[0]['content']['annotations'].items() if v}

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
  "name": "Andorra",
  "city": "Andorra la Vella"
}, {
  "name": "Albania",
  "city": "Tirana"
}, {
  "name": "Austria",
  "city": "Vienna"
}, {
  "name": "Åland Islands",
  "city": "Mariehamn"
}, {
  "name": "Bosnia and Herzegovina",
  "city": "Sarajevo"
}, {
  "name": "Belgium",
  "city": "Brussels"
}, {
  "name": "Bulgaria",
  "city": "Sofia"
}, {
  "name": "Belarus",
  "city": "Minsk"
}, {
  "name": "Switzerland",
  "city": "Bern"
}, {
  "name": "Cyprus",
  "city": "Nicosia"
}, {
  "name": "Czech Republic",
  "city": "Prague"
}, {
  "name": "Germany",
  "city": "Berlin"
}, {
  "name": "Denmark",
  "city": "Copenhagen"
}, {
  "name": "Estonia",
  "city": "Tallinn"
}, {
  "name": "Spain",
  "city": "Madrid"
}, {
  "name": "Finland",
  "city": "Helsinki"
}, {
  "name": "Faroe Islands",
  "city": "Tórshavn"
}, {
  "name": "France",
  "city": "Paris"
}, {
  "name": "United Kingdom",
  "city": "London"
}, {
  "name": "Guernsey",
  "city": "Saint Peter Port"
}, {
  "name": "Greece",
  "city": "Athens"
}, {
  "name": "Croatia",
  "city": "Zagreb"
}, {
  "name": "Hungary",
  "city": "Budapest"
}, {
  "name": "Ireland",
  "city": "Dublin"
}]

# build map to paper - authors
paper_map = [{paper["externalids"]["CorpusId"]: paper['authors']} for paper in papers]

paper_ids = list(set([paper['corpusid'] for paper in papers]))

for paper in papers:
    conidx_cty = int(random.randint(0, 10))
    paper['country'] = countries[conidx_cty]['name']
    paper['city'] = countries[conidx_cty]['city']
    if not paper.get('journal'):
        conidx = int(random.randint(0, 3))
        paper['venue'] = conf[conidx]['title']
        paper['edition'] = int(random.randint(0, 20)) # very stupid way to format it !
        paper['journal'] = None
    else:
        paper['journal']['name'] = list(journals.values())[int(random.randint(0, 10))]
        paper['venue'] = None
        # if no volume - fake it!
        if not paper['journal']['volume']:
            paper['journal']['volume'] = random.randint(1, 99)
    # assign reviewers
    review_rand = int(random.randint(0, 98))
    paper['reviewers'] = list(paper_map[review_rand].values())[0] \
        if str(paper['corpusid']) != list(paper_map[review_rand +1].keys())[0] else list(paper_map[review_rand+1].values())[0]

# save paper changes
with open('./preprocessed_data/papers_json.json', 'w') as fout:
    json.dump(papers, fout)


# randomize the citation
for cite in citations:
    rand_id = random.randint(0, 50)
    cite['citingcorpusid'] = str(paper_ids[rand_id])
    cite['citedcorpusid'] = str(paper_ids[rand_id+1])

# save citation as json
with open('preprocessed_data/citation_json.json', 'w') as fout:
    json.dump(citations, fout)

# save paper_ids as json
with open('preprocessed_data/paper_ids_json.json', 'w') as fout:
    json.dump(paper_ids, fout)


