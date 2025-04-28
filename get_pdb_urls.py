import requests
import time

def fetch_chunk(start, chunk_size):
    url = f"https://alphafold.ebi.ac.uk/api/search?q=organismScientificName%3ACafeteria%5C%20roenbergensis&type=main&start={start}&rows={chunk_size}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching chunk starting at {start}: {response.status_code}")
        print(response.text)
        return None

def main():
    chunk_size = 2000
    max_records = 32000
    filename = "cafeteria_pdb_urls.txt"
    
    # Open file in append mode
    with open(filename, "a") as file:
        for start in range(0, max_records, chunk_size):
            print(f"Fetching records {start} to {start + chunk_size}...")
            
            data = fetch_chunk(start, chunk_size)
            if not data:
                break
                
            docs = data.get("docs", [])
            if not docs:
                print(f"No more records found after {start}")
                break
                
            for doc in docs:
                entryId = doc.get("entryId")
                if entryId:
                    pdb_url = f"https://alphafold.ebi.ac.uk/files/{entryId}-model_v4.pdb"
                    file.write(pdb_url + "\n")
            
            # Add a small delay between requests to be nice to the server
            time.sleep(1)
            
            print(f"Processed {len(docs)} records")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)