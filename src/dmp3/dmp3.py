from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path

from dmp3._internal import *

argparser = ArgumentParser(formatter_class=RawTextHelpFormatter)

argparser.add_argument(
    "folder",
    type=Path,
    help="Folder to store mp3 files",
)
argparser.add_argument(
    "-w",
    "--webpath",
    type=str,
    help="Webpath to download from, creates a .dmp3 file insdie folder to store webpath",
    default=None,
)
argparser.add_argument(
    "-s", "--start", type=int, help="Start index of the playlist", default=None
)
argparser.add_argument(
    "-e", "--end", type=int, help="End index of the playlist", default=None
)
argparser.add_argument(
    "-r",
    "--refresh_folder_mode",
    action="store_true",
    help=(
        "Refresh all mp3 folders in the folder, default is False.\n"
        "In this mode, work through all sub folders with .mp3 inside, and download all new videos"
    ),
)
argparser.add_argument(
    "-m",
    "--mp3",
    type=bool,
    help="Convert mp4 files to mp3 files in the folder (WIP)",
    default=True,
)

description = """
Download youtube video or playlist, convert to mp3, store into a folder.

If folder not exists, creates a folder.
Otherwise, uses the folder, and will only download new videos from the playlist.

If webpath is provided, creates a .dmp3 file in the folder to store the webpath for future use.
If not provided, uses the webpath in the .dmp3 file in the folder stored previously.
If not provided and no .dmp3 file is found in the folder, exits.

If start and/or end are provided, download only the subset of the playlist.
But will not download the videos that are already downloaded.
"""

epilog = """
Example:

Entire playlist:
dmp3 /mnt/d/media/music/game_theme/starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy
Part of playlist:
dmp3 /mnt/d/media/music/game_theme/starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy -s 1 -e 2

Refresh entire playlist:
dmp3 /mnt/d/media/music/game_theme/starcraft_terran
Refresh part of playlist:
dmp3 /mnt/d/media/music/game_theme/starcraft_terran -e 3

Refresh all folders:
dmp3 /mnt/d/media/music/game_theme -r
"""
epilog2 = """asdf"""

argparser.description = description
argparser.epilog = epilog


# main process
def process_folder_and_webpath(
    folder: Path, webpath: str, start: int, end: int, mp3: bool
):
    if not folder.exists():
        folder.mkdir(parents=True)
        existing_ids = []
    else:
        existing_ids = already_downloaded_ids(folder)

    if webpath:
        with open(folder / ".dmp3", "w") as f:
            f.write(webpath)
    else:
        try:
            with open(folder / ".dmp3", "r") as f:
                webpath = f.read()
        except FileNotFoundError:
            print(
                f"No webpath provided and no .dmp3 file found in the folder: {folder}"
            )
            return

    is_playlist: bool = "playlist" in webpath

    if len(existing_ids) > 0 and is_playlist:
        target_urls = fetch_items_from_list(webpath, start, end)
        target_ids = ids_from_list(target_urls)
        new_ids = list(set(target_ids) - set(existing_ids))
        download_ids_and_convert_to_mp3(new_ids, folder)
    else:
        download_list_subset_and_convert_to_mp3(webpath, folder, start, end)


def dmp3(
    folder: Path,
    webpath: str = None,
    start: int = None,
    end: int = None,
    refresh_folder_mode: bool = False,
    mp3: bool = True,
):
    # refresh all folders mode
    if refresh_folder_mode:
        for sub_folder in folder.iterdir():
            if sub_folder.is_dir() and (sub_folder / ".dmp3").exists():
                process_folder_and_webpath(
                    folder=sub_folder,
                    webpath=None,
                    start=None,
                    end=None,
                    mp3=mp3,
                )
    else:
        # vanilla mode
        process_folder_and_webpath(
            folder=folder,
            webpath=webpath,
            start=start,
            end=end,
            mp3=mp3,
        )


def cli():
    args = argparser.parse_args()
    folder = args.folder
    webpath = args.webpath
    start = args.start
    end = args.end
    refresh_folder_mode = args.refresh_folder_mode
    mp3 = args.mp3

    dmp3(folder, webpath, start, end, refresh_folder_mode, mp3)


if __name__ == "__main__":
    cli()
