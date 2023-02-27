# Python script to extract keywords from json attribute
import yake
import json
from tqdm import tqdm

import sys

file_path = sys.argv.get(0) or "./../Data//arxiv-metadata-oai-snapshot.json"

output_path = sys.argv.get(0) or './../Data/keyword_added.json'

# top is the number of keywords we want to extract from the text
kw_extractor = yake.KeywordExtractor(top=3, stopwords=None)

# prepare output file
with open(output_path, mode='w', encoding='utf-8') as f:
    json.dump("[", f)

# read the papers one by one, since it's different objects structures.
with open(file_path) as user_file:
    for line in tqdm(user_file.readlines()):
        # read a paper
        paper = json.loads(line)
        # extract the abstract
        abstract = paper.get('abstract', None)
        if abstract:
            keywords = kw_extractor.extract_keywords(abstract)
            paper['keywords'] = [v[0] for v in keywords]
        else:
            paper['keywords'] = []
        with open(output_path, mode='a', encoding='utf-8') as feedsjson:
            json.dump(paper, feedsjson, indent=2)

with open(output_path, mode='a', encoding='utf-8') as f:
    json.dump("]", f)

# Iterating through the json
print("finish!")
