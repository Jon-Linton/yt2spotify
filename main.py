from utils import convert_yt_to_mp3, delete_files_with_substring
import os

yt_url_file = "youtube_urls.txt"
target_directory = "./mp3_downloads"  # Replace with your directory path
search_string = "_final"
try:
    with open(yt_url_file, "r") as file:
        for line in file:
            convert_yt_to_mp3(line)

    # Cleans up non-final mp3 files (the ones without the jpeg cover art)
    target_directory = "./mp3_downloads"  # Replace with your directory path
    search_string = "_final"
    try:
        print("Attempting to clean up mp3 files")
        delete_files_with_substring(target_directory, search_string)
        print("Files cleaned up successfully")
    except FileNotFoundError:
        print(f"Error: directory '{target_directory}' not found.")
    except OSError as e:
        print(f"Error deleting file '{target_directory}': {e}")


except FileNotFoundError:
    print(f"File not found: {yt_url_file}")
except Exception as e:
    print(f"An error occurred: {e}")
