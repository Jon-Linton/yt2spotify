from utils import convert_yt_to_mp3, delete_files_with_substring
from dotenv import load_dotenv
import os

# Force Python to find everything relative to this script's location,
# regardless of what directory the script is invoked from.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file (also anchored to script dir)
load_dotenv(os.path.join(script_dir, ".env"))

url_input_env_path = os.getenv("YT_URL_INPUT_FILE")
mp3_keep_substring = os.getenv("CLEAN_SEARCH_STR")

# Resolve the one env-provided path we actually use against script_dir too
if url_input_env_path and not os.path.isabs(url_input_env_path):
    url_input_env_path = os.path.join(script_dir, url_input_env_path)

pending_urls_path = os.path.join(script_dir, "input.txt")
downloaded_urls_path = os.path.join(script_dir, "downloaded.txt")
mp3_clean_dir = os.path.join(script_dir, "mp3_downloads")

try:
    with open(pending_urls_path, "r") as pending_urls_file:
        pending_urls = pending_urls_file.readlines()
        for url in pending_urls:
            print(url)
            convert_yt_to_mp3(url)

    # Write downloaded urls to an archival file
    with open(downloaded_urls_path, "w") as downloaded_urls_file:
        for url in pending_urls:
            downloaded_urls_file.write(url)

    # Clean up URL input file
    with open(url_input_env_path, "w") as url_input_file:
        url_input_file.write("")

    # Cleans up non-final mp3 files (the ones without the jpeg cover art)
    print("Searching for mp3 files to clean up...")
    delete_status_msg = delete_files_with_substring(mp3_clean_dir, mp3_keep_substring)
    print(delete_status_msg or "No delete status available")

except FileNotFoundError:
    print(f"File not found: {url_input_env_path}")
except Exception as e:
    print(f"An error occurred: {e}")
