#!/usr/bin/env python3
from tqdm import tqdm
import json
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial

os.makedirs("Cafeteria_pdb_files", exist_ok=True)

def download_single(url):
    try:
        out_file = url.split("/")[-1]
        filename = f"Cafeteria_pdb_files/{out_file}"
        if os.path.exists(filename):
            return
        resp = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(resp.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

with open("filtered_cafeteria_pdb_urls.json", 'r') as f:
    pdb_urls = json.load(f)

with ThreadPoolExecutor(max_workers=2) as executor:
    list(tqdm(executor.map(download_single, pdb_urls), total=len(pdb_urls)))
