# yt2spotify

Converts YouTube videos to MP3 to be added to Spotify.

# Getting started

## 1. Download FFmpeg

Download ffmpeg from a reliable source:

- Windows: https://www.gyan.dev/ffmpeg/builds/

Add the `bin` folder (containing `ffmpeg.exe` and `ffprobe.exe`) to your PATH variable.

Confirm it's configured correctly by running `ffmpeg -version` and `ffprobe -version` in the terminal you'll use to run this script — both must succeed.

> **Note:** Even if `ffmpeg -version` works in your terminal, some environments (IDEs, task runners, certain venv setups) launch Python with a different PATH than your shell, and won't find ffmpeg. If you hit an error like `ffprobe and ffmpeg not found`, skip PATH entirely and set `FFMPEG_PATH` in your `.env` file instead (see below) — it points directly at the ffmpeg `bin` folder as a reliable fallback.

## 2. Set up `.venv` (or don't, your call)

Create the `.venv` with:

```
python -m venv .venv
```

Activate it:

```
.venv\Scripts\Activate.ps1
```

Install dependencies:

```
pip install -r requirements.txt
```

## 3. Configure your `.env`

Copy `.env.example` to `.env` and fill in the values (see below for what each one does).

## 4. Run it

```
python main.py
```

# How it works

Create a text file and paste in the YouTube video URLs you want converted to MP3, one URL per line.

Name the file `input.txt` and place it in the same directory as `main.py` — the script resolves this path relative to its own location, so it works regardless of the directory you run it from. (This is set by the `pending_urls_path` variable in `main.py` if you need to change it.)

Running the script will:

1. Read the URLs from `input.txt`
2. Download and convert each video to MP3, storing it in a `mp3_downloads` folder created in the project directory
3. Embed the video thumbnail as cover art on the final MP3
4. Archive the processed URLs to `downloaded.txt` and clear `input.txt`

# Environment variables

- `YT_URL_INPUT_FILE`: Path to the file that gets cleared out after a successful run (typically your `input.txt`)
- `CLEAN_SEARCH_STR`: Substring used to identify which MP3s to _keep_ during cleanup (files without it get deleted — e.g. non-final files missing embedded cover art)
- `FFMPEG_PATH`: Optional fallback path to your ffmpeg `bin` folder (or the `ffmpeg` binary itself), used only if ffmpeg isn't found on this process's PATH
