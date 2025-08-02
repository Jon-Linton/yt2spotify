from utils import convert_yt_to_mp3, delete_files_with_substring
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
yt_url_file = os.getenv("YT_URL_INPUT_FILE")
past_downloads_file = os.getenv("YT_URL_OUTPUT_FILE")
clean_target_dir = os.getenv("MP3_CLEAN_TARGET_DIR")
file_str_to_skip_del = os.getenv("CLEAN_SEARCH_STR")

try:
    with open(yt_url_file, "r") as file:
        lines = file.readlines()
        for line in file:
            convert_yt_to_mp3(line)

    # Write downloaded urls to an archival file
    with open("downloaded.txt", "w") as file:
        for line in lines:
            file.write(line)

    # Clean up URL input file
    with open(yt_url_file, "w") as file:
        file.write("")

    # Cleans up non-final mp3 files (the ones without the jpeg cover art)
    mp3_clean_target_dir = "./mp3_downloads"  # Replace with your directory path
    file_str_to_skip_del = "_final"
    print("Searching for mp3 files to clean up...")
    delete_status_msg = delete_files_with_substring(
        mp3_clean_target_dir, file_str_to_skip_del
    )
    print(delete_status_msg or "No delete status available")


except FileNotFoundError:
    print(f"File not found: {yt_url_file}")
except Exception as e:
    print(f"An error occurred: {e}")
