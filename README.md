# yt2spotify

Converts Youtube Videos to MP3 to be added to Spotify

yt2spotify/
├── README.md
├── requirements.txt
├── .env.example
├── main.py
├── yt2spotify/
│ ├── **init**.py
│ ├── downloader.py # Handles YouTube video downloading & MP3 conversion
│ ├── metadata.py # Parses/handles song metadata (title, artist, etc.)
│ ├── spotify_uploader.py # Handles Spotify API integration and uploading
│ └── utils.py # Miscellaneous helper functions
├── tests/
│ ├── **init**.py
│ ├── test_downloader.py
│ ├── test_metadata.py
│ └── test_spotify_uploader.py
└── .gitignore
