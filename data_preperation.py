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
for paper in papers:
    if not paper.get('journal'):
        conidx = int(random.randint(0, 12))
        paper['venue'] = conf[conidx]['title']
        paper['edition'] = int(random.randint(0, 20)) # very stupid way to format it !
    else:
        paper['journal']['name'] = list(journals.values())[int(random.randint(0, 71))]
        # if no volume - fake it!
        if not paper['journal']['volume']:
            paper['journal']['volume'] = random.randint(1, 99)

# save paper changes
with open('./preprocessed_data/papers_json.json', 'w') as fout:
    json.dump(papers, fout)

# save citation as json
with open('preprocessed_data/citation_json.json', 'w') as fout:
    json.dump(citations, fout)

# for a in annotations['paragraph'][:10]: print(a)
# for a in annotations['bibref'][:10]: print(a)
# for a in annotations['bibentry'][:10]: print(a)
#
#
# def text_of(type):
#     return [text[a['start']:a['end']] for a in annotations[type]]
#
#
# text_of('abstract')
#
# print('\n\n'.join(text_of('paragraph')[:3]))
#
# print('\n'.join(text_of('bibref')[:10]))
