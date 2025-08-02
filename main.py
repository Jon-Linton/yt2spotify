from utils import convert_yt_to_mp3, delete_files_with_substring

yt_url_file = "./io_files/youtube_urls.txt"
past_downloads_file = "./io_files/past_downloads.txt"
target_directory = "./mp3_downloads"  # Replace with your directory path
search_string = "_final"
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
    target_directory = "./mp3_downloads"  # Replace with your directory path
    search_string = "_final"
    try:
        print("Searching for mp3 files to clean up...")
        delete_status_msg = delete_files_with_substring(target_directory, search_string)
        print(delete_status_msg or "No delete status available")
    except FileNotFoundError:
        print(f"Error: directory '{target_directory}' not found.")
    except OSError as e:
        print(f"Error deleting file '{target_directory}': {e}")


except FileNotFoundError:
    print(f"File not found: {yt_url_file}")
except Exception as e:
    print(f"An error occurred: {e}")
