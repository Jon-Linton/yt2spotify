import shutil
import yt_dlp
import glob
import subprocess
from PIL import Image
import os


def convert_yt_to_mp3(youtube_url, output_dir="./mp3_downloads"):

    # Create directory and set ffmpeg path
    os.makedirs(output_dir, exist_ok=True)

    ffmpeg_path = shutil.which("ffmpeg")
    ffmpeg_dir = os.path.dirname(ffmpeg_path) if ffmpeg_path else None

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
    final_path = mp3_path.replace(".mp3", "_final.mp3")

    # Step 3: Convert thumbnail to JPEG
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

    # Optional: Clean up
    os.remove(thumb_path)
    os.remove(jpg_path)


def delete_files_with_substring(directory, substring):
    delete_status_msg = "Files deleted: "
    names_of_deleted_files = ""
    for filename in os.listdir(directory):
        if substring not in filename:
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            names_of_deleted_files += "{filename}, "
            print("File deleted:", filename)

    if len(names_of_deleted_files) < 1:
        delete_status_msg = "No files found to delete"

    return delete_status_msg
