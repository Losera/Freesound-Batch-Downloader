import sys
import os
import freesound  # Import the freesound library
import argparse

# Add the path to the freesound-python directory
sys.path.append('/Users/jnaran/Desktop/Intelligent-Production-Assistant/freesound-python')

# Set up authentication
from dotenv import load_dotenv  # Optional, if using .env
load_dotenv()

client = freesound.FreesoundClient()
api_key = os.getenv("FREESOUND_API_KEY")
client.set_token(api_key)

#Identify for Authentication
print("Authentication successful!")


#Function to query files on freesound.org
def query_search_download(query,page_size,download_folder):

    result = client.text_search(query=query,page_size=page_size,fields='id,name,previews')
    sounds = []

    if result.count == 0:
        print(f"No results found for query: '{query}'")
        return []
        
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    for sound in result:
        print(f"Sound Name: {sound.name}, ID: {sound.id}")
        sounds.append(sound)
    
    if not sounds:
        print("No results found")
    else:
        for sound in sounds:
             
             #Clean file name
             cleaned_name = "".join(c for c in sound.name if c.isalnum() or c in (' ', '_', '-')).rstrip()
             download_path = os.path.join(download_folder,f'{cleaned_name}.wav')

             try:
                 # Open the file in write-binary mode and download the sound
                    with open(download_path, 'wb') as f:
                        sound.retrieve_preview(download_path)
                    print(f"Downloaded: {download_path}")
           
             except Exception as e:
                    print(f"Failed to download {sound.name}: {e}")

    return sounds


def main():
    parser = argparse.ArgumentParser(description="Parse queries for freesound.org")

    parser.add_argument('query', type=str, help="A string for intiating search query in freesound.org")
    parser.add_argument('page_size', type=int, help="Amount of pages to be searched for query")
    parser.add_argument('download_folder', type=str, help="Destination folder for query download")
     
    args = parser.parse_args()
    result = query_search_download(args.query,args.page_size,args.download_folder)
    
    print(f"Result of query: {result}")


if __name__ == "__main__":
    main()