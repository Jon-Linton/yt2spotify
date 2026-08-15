import shutil
import yt_dlp
import glob
import subprocess
from PIL import Image
import os


def _require_ffmpeg():
    """Locate ffmpeg/ffprobe or raise a clear, early error instead of letting
    yt-dlp fail later with a vague 'not found' message.

    Resolution order:
    1. shutil.which() — works if this process's PATH includes ffmpeg
    2. FFMPEG_PATH env var (e.g. set in .env) — explicit override/fallback
    """
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")

    if not ffmpeg_path or not ffprobe_path:
        env_path = os.getenv(
            "FFMPEG_PATH"
        )  # accepts either a bin dir or the ffmpeg binary itself
        if env_path:
            exe_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
            probe_name = "ffprobe.exe" if os.name == "nt" else "ffprobe"

            if os.path.isdir(env_path):
                candidate_ffmpeg = os.path.join(env_path, exe_name)
                candidate_dir = env_path
            else:
                candidate_ffmpeg = env_path
                candidate_dir = os.path.dirname(env_path)

            candidate_probe = os.path.join(candidate_dir, probe_name)

            if os.path.isfile(candidate_ffmpeg) and os.path.isfile(candidate_probe):
                return candidate_ffmpeg, candidate_dir

        raise RuntimeError(
            "ffmpeg and/or ffprobe not found on PATH for this Python process, "
            f"and FFMPEG_PATH ({env_path!r}) did not resolve to a valid ffmpeg "
            "+ ffprobe pair. Set FFMPEG_PATH to either the bin directory "
            "containing both binaries, or the full path to the ffmpeg binary."
        )

    return ffmpeg_path, os.path.dirname(ffmpeg_path)


def convert_yt_to_mp3(youtube_url, output_dir="./mp3_downloads", ffmpeg_path=None):

    os.makedirs(output_dir, exist_ok=True)

    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
    else:
        ffmpeg_path, ffmpeg_dir = _require_ffmpeg()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "noplaylist": True,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "ffmpeg_location": ffmpeg_dir,
        "quiet": False,
        "verbose": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {
                "key": "FFmpegMetadata",
            },
        ],
    }

    # Download MP3 and thumbnail (unconverted)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Locate most recent mp3 and thumbnail (webp or png)
    mp3_files = sorted(
        glob.glob(f"{output_dir}/*.mp3"), key=os.path.getmtime, reverse=True
    )
    thumb_files = sorted(
        glob.glob(f"{output_dir}/*.webp") + glob.glob(f"{output_dir}/*.png"),
        key=os.path.getmtime,
        reverse=True,
    )

    if not mp3_files or not thumb_files:
        print("Could not find MP3 or thumbnail to process.")
        return

    mp3_path = mp3_files[0]
    thumb_path = thumb_files[0]
    jpg_path = thumb_path.rsplit(".", 1)[0] + ".jpg"
    final_path = mp3_path.rsplit(".", 1)[0] + "_final.mp3"

    # Convert thumbnail to JPEG
    try:
        with Image.open(thumb_path) as im:
            rgb = im.convert("RGB")
            rgb.save(jpg_path, "JPEG")
        print(f"Converted {thumb_path} to {jpg_path}")
    except Exception as e:
        print(f"Failed to convert thumbnail: {e}")
        return

    # Embed JPEG into MP3 using ffmpeg
    subprocess.run(
        [
            ffmpeg_path,
            "-i",
            mp3_path,
            "-i",
            jpg_path,
            "-map",
            "0",
            "-map",
            "1",
            "-c",
            "copy",
            "-id3v2_version",
            "3",
            "-metadata:s:v",
            "title=Album cover",
            "-metadata:s:v",
            "comment=Cover (front)",
            final_path,
        ],
        check=True,
    )
    print(f"Embedded JPEG into: {final_path}")

    # Clean up intermediate files
    os.remove(thumb_path)
    os.remove(jpg_path)


def delete_files_with_substring(directory, substring):
    deleted_filenames = []
    for filename in os.listdir(directory):
        if substring not in filename:
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            deleted_filenames.append(filename)
            print("File deleted:", filename)

    if not deleted_filenames:
        return "No files found to delete"

    return "Files deleted: " + ", ".join(deleted_filenames)
