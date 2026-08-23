import re
from pathlib import Path
from typing import List

import yaml
import yt_dlp


def read_saved_info(path: Path):
    with open(path, "r") as f:
        info = yaml.safe_load(f)
    return info


def save_info(info, path: Path):
    with open(path, "w") as f:
        yaml.safe_dump(info, f)


def fetch_items_from_channel(
    webpath: str, start: int = None, end: int = None
) -> List[str]:
    headers = {
        "flat_playlist": True,
        # "age_limit": 18,
        "ignoreerrors": True,
    }
    if start is not None:
        headers["playliststart"] = start
    if end is not None:
        headers["playlistend"] = end
    with yt_dlp.YoutubeDL(headers) as ydl:
        playlist = ydl.extract_info(webpath, download=False)
        return [video["webpage_url"] for video in playlist["entries"]]


def fetch_items_from_list(
    playlist_url: str, start: int = None, end: int = None
) -> List[str]:
    ydl_opts = {
        "extract_flat": True,
        "ignoreerrors": True,
    }
    if start is not None:
        ydl_opts["playliststart"] = start
    if end is not None:
        ydl_opts["playlistend"] = end

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist = ydl.extract_info(playlist_url, download=False)

    if not playlist:
        return []

    entries = playlist.get("entries") or []
    return [
        video.get("webpage_url")
        or video.get("url")
        or f"https://www.youtube.com/watch?v={video.get('id')}"
        for video in entries
        if video
    ]


def already_downloaded_ids(folder: Path) -> List[str]:
    # already downloaded files
    files = [i.stem for i in folder.iterdir() if i.suffix == ".mp3"]
    # the final 11 chars are the id
    existing_ids = [file[-11:] for file in files]
    return existing_ids


def ids_from_list(target_urls: List[str]) -> List[str]:
    # fetch chars after ?v=, and up to end of string
    target_ids = [re.findall(r"\?v=([^=]*)$", url)[0] for url in target_urls]
    return target_ids


def id_from_video_webpath(webpath: str) -> str:
    # fetch 11 chars after ?v=
    target_id = re.findall(r"\?v=([^=]{11})", webpath)[0]
    return target_id


def parse_webpath(webpath: str) -> str:
    """
    Parse webpath archetype:

    video:
    https://www.youtube.com/watch?v=mD4GbGmvNRc&list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy&index=2&ab_channel=Katrulzin
    https://www.youtube.com/watch?v=zAS8KivZX5s&ab_channel=nudl3r

    playlist:
    https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy

    channel's video list:
    https://www.youtube.com/@Diablo/videos
    """
    if webpath is None:
        raise ValueError("webpath cannot be None")

    if "https://www.youtube.com/" not in webpath:
        raise ValueError(f"https://www.youtube.com/ not in: {webpath}")

    if "watch?v=" in webpath:
        webpath_type = "video"
    elif "playlist?list=" in webpath:
        webpath_type = "playlist"
    elif "/@" in webpath and "/videos" in webpath:
        webpath_type = "channel"
    else:
        raise ValueError(f"Unrecognized webpath: {webpath}")

    return webpath_type


SAVE_FILE_FORMAT = "%(title)s-%(id)s.%(ext)s"


def yt_dlp_download(webpath: str, headers: dict):
    try:
        with yt_dlp.YoutubeDL(headers) as ydl:
            ydl.download([webpath])
    except Exception as e:
        print(e)


HEADERS = {
    "format": "bestaudio/best",
    # "age_limit": 18,
    "ignoreerrors": True,
}

# load cookies from home directory if exists
COOKIE_FILE = Path.home() / ".youtube-cookies.txt"
if COOKIE_FILE.exists():
    HEADERS["cookiefile"] = str(COOKIE_FILE)


def make_download_headers(
    folder: Path, mp3: bool = True, start: int = None, end: int = None
):
    headers = HEADERS.copy()
    headers["outtmpl"] = f"{folder}/{SAVE_FILE_FORMAT}"

    if mp3:
        headers["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
    else:
        # Download full video when not converting to MP3
        headers["format"] = "bestvideo+bestaudio/best"

    if start is not None:
        headers["playliststart"] = start
    if end is not None:
        headers["playlistend"] = end
    return headers


def download_ids_and_convert_to_mp3(ids: List[str], folder: Path, mp3: bool = True):
    headers = make_download_headers(folder, mp3)
    for id in ids:
        yt_dlp_download(
            webpath=f"https://www.youtube.com/watch?v={id}", headers=headers
        )


def download_list_subset_and_convert_to_mp3(
    webpath: str, folder: Path, start: int = None, end: int = None, mp3: bool = True
):
    headers = make_download_headers(folder, mp3, start, end)
    yt_dlp_download(webpath=webpath, headers=headers)
