Semantic Scholar Academic Graph Datasets

These datasets provide a variety of information about research papers taken from a snapshot in time of the Semantic Scholar corpus.

This site is provided by The Allen Institute for Artificial Intelligence (“AI2”) as a service to the
research community. The site is covered by AI2 Terms of Use and Privacy Policy. AI2 does not claim
ownership of any materials on this site unless specifically identified. AI2 does not exercise editorial
control over the contents of this site. AI2 respects the intellectual property rights of others. If
you believe your copyright or trademark is being infringed by something on this site, please follow
the "DMCA Notice" process set out in the Terms of Use (https://allenai.org/terms).

SAMPLE DATA ACCESS
Sample data files can be downloaded with the following UNIX command:

for f in $(curl https://s3-us-west-2.amazonaws.com/ai2-s2ag/samples/MANIFEST.txt)
  do curl --create-dirs "https://s3-us-west-2.amazonaws.com/ai2-s2ag/$f" -o $f
done

See the "s2ag.py" file for Python code that downloads and parses the data.

FULL DATA ACCESS
Downloading the full data requires an API key, which can be obtained at https://www.semanticscholar.org/product/api#Partner-Form
For access to the full datasets, see https://api.semanticscholar.org/api-docs/datasets.

LICENSE and ATTRIBUTION

See the README files for each dataset for information about licensing and attribution.