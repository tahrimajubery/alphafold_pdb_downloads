import json
from pathlib import Path
from urllib.parse import urlparse

reference_file = "uniprot_download.json"

set_of_primary_accession = set()

with open(reference_file) as f:
    ref_data = json.load(f)
    for raw_url in ref_data['results']:
        set_of_primary_accession.add(raw_url['primaryAccession'])

source_file = 'cafeteria_pdb_urls.txt'

with open(source_file, 'r') as f:
    data = f.read().splitlines()

urls_to_keep = []

for raw_url in data:
    url_obj = urlparse(raw_url)

    pth = Path(url_obj.path)

    # get the 2nd item so from AF-A0A5A8DWL2-F1-model_v4.pdb -> A0A5A8DWL2
    id = pth.stem.split('-')[1]

    if id in set_of_primary_accession:
        urls_to_keep += [raw_url]

out_file = 'filtered_cafeteria_pdb_urls.json'
with open(out_file, 'w') as f:
    json.dump(urls_to_keep, f, indent=2)


print(f"Saved {len(urls_to_keep)} urls to {out_file}. Enjoy PB!")

# print(len(set_of_primary_accession))
# print(data)
#
# read from nand_pdb_urls.json
