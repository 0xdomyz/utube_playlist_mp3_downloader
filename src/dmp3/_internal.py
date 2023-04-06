import re
from pathlib import Path
from typing import List

import pytube
import yt_dlp

HEADERS = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "age_limit": 18,
}


# def fetch_items_from_list(
#     webpath: str, start: int = None, end: int = None
# ) -> List[str]:
#     headers = {
#         "flat_playlist": True,
#         "age_limit": 18,
#     }
#     if start is not None:
#         headers["playliststart"] = start
#     if end is not None:
#         headers["playlistend"] = end
#     with yt_dlp.YoutubeDL(headers) as ydl:
#         playlist = ydl.extract_info(webpath, download=False)
#         return [video["webpage_url"] for video in playlist["entries"]]


def fetch_items_from_list(
    playlist_url: str, start: int = None, end: int = None
) -> List[str]:
    playlist = pytube.Playlist(playlist_url)
    res = playlist.video_urls
    if start is not None and end is not None:
        res = res[start:end]
    elif start is not None:
        res = res[start:]
    elif end is not None:
        res = res[:end]
    return res


def already_downloaded_ids(folder: Path) -> List[str]:
    # already downloaded files
    files = [i.stem for i in folder.iterdir() if i.suffix == ".mp3"]
    existing_ids = [re.findall(r"-([^-]*)$", file)[0] for file in files]
    return existing_ids


def ids_from_list(target_urls: List[str]) -> List[str]:
    # fetch chars after ?v=, and up to end of string
    target_ids = [re.findall(r"\?v=([^=]*)$", url)[0] for url in target_urls]
    return target_ids


SAVE_FILE_FORMAT = "%(title)s-%(id)s.%(ext)s"


def download_ids_and_convert_to_mp3(ids: List[str], folder: Path):
    headers = dict(HEADERS, outtmpl=f"{folder}/{SAVE_FILE_FORMAT}")
    with yt_dlp.YoutubeDL(headers) as ydl:
        for id in ids:
            ydl.download([f"https://www.youtube.com/watch?v={id}"])


def download_list_subset_and_convert_to_mp3(
    webpath: str, folder: Path, start: int = None, end: int = None
):
    headers = dict(HEADERS, outtmpl=f"{folder}/{SAVE_FILE_FORMAT}")
    if start is not None:
        headers["playliststart"] = start
    if end is not None:
        headers["playlistend"] = end

    with yt_dlp.YoutubeDL(headers) as ydl:
        ydl.download([webpath])
