# yt2spotify

Converts Youtube Videos to MP3 to be added to Spotify

# Project Structure

```text
yt2spotify/ ├── README.md ├── requirements.txt ├── .env ├── main.py ├── tests/ └── .gitignore

# Getting started

# Download FFMPEG

Download ffmpeg from a reliable source
Windows: https://www.gyan.dev/ffmpeg/builds/
Add the exe path to your PATH variable
Confirm that it's configured correctly by running ffmpeg -version in terminal

# Setup .venv (or don't your call)

Create .venv with the command "python -m venv"
Activate the .venv with the command ".venv venv\Scripts\Activate.ps1"

Run "pip install -r requirements.txt" to install all necessary modules

Run python main.py

# How it works

Create a text file and paste in the Youtube video URLs you want to be converted to MP3.
The expected format is one URL per line separated by a newline.
Name the file 'youtube_urls.txt', just be sure to update the file_path variable in main.py if you do change it.
Running the script will take the URLs, convert the videos to MP3, and create a folder in your project directory called "mp3_downloads" to store the MP3 files under.
```
