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
    help="Webpath to download from, creates a .dmp3 file insdie folder to store parameters",
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
    help=("Refresh all mp3 folders in the folder, default is False"),
)
argparser.add_argument(
    "-m",
    "--mp3",
    type=bool,
    help="Convert video to mp3 files in the folder, default is True (WIP)",
    default=True,
)

description = """
Download youtube video, playlist, channel. Convert to mp3, store into folder. Efficiently refresh mutiple storage folders.

Creates folder if not exists.
Otherwise only download additional mp3 into the folder.

If webpath is provided, creates a .dmp3 file in the folder to store parameters.
If not provided, uses saved parameter.

If start and/or end are provided, download only the subset in addition to already downloaded.
If not provided, uses saved parameters if any.
"""

epilog = """
Examples:

Entire playlist:
cd /home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir
dmp3 starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy

Part of playlist:
dmp3 starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy -s 1 -e 2

Most recent 5 videos from channel:
dmp3 diablo -w https://www.youtube.com/@Diablo/videos -e 5

Refresh entire or part of playlist:
dmp3 starcraft_terran
dmp3 starcraft_terran -s 5

Refresh channel using saved parameters:
dmp3 diablo

Refresh all storage folders, each with saved parameters:
cd /home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir
dmp3 . -r

"""

argparser.description = description
argparser.epilog = epilog


# main process
def process_folder_and_webpath(
    **kwargs,
):
    # breakpoint()

    folder = kwargs["folder"]
    webpath = kwargs["webpath"]
    start = kwargs["start"]
    end = kwargs["end"]
    mp3 = kwargs["mp3"]

    # folder
    if not folder.exists():
        print(f"Creating folder: {folder}")
        folder.mkdir(parents=True)
    existing_ids = already_downloaded_ids(folder)
    print(f"No. of existing mp3 files: {len(existing_ids)}")

    # webpath
    if webpath is None:
        try:
            print(f"Reading webpath from .dmp3 file in the folder: {folder}")
            info = read_saved_info(folder / ".dmp3")
            webpath = info["webpath"]
            start = info["start"] if "start" in info and start is None else start
            end = info["end"] if "end" in info and end is None else end
        except FileNotFoundError:
            raise Exception(
                f"No webpath provided and no .dmp3 file found in the folder: {folder}"
            )
    else:
        info = kwargs.copy()
        info["folder"] = str(folder)
        print(f"Saving webpath to .dmp3 file in the folder: {folder}")
        save_info(info=info, path=folder / ".dmp3")

    # logics
    webpath_type = parse_webpath(webpath)
    print(f"Webpath type recognized as: {webpath_type}")

    if webpath_type == "video":
        id = id_from_video_webpath(webpath)
        if id not in existing_ids:
            download_ids_and_convert_to_mp3([id], folder)
    elif webpath_type in ["playlist", "channel"]:
        if len(existing_ids) > 0:
            if webpath_type == "playlist":
                print(f"Fetcing playlist items: {webpath}")
                target_urls = fetch_items_from_list(webpath, start, end)
            else:
                print(f"Fetcing channel items: {webpath}")
                target_urls = fetch_items_from_channel(webpath, start, end)
            target_ids = ids_from_list(target_urls)
            new_ids = list(set(target_ids) - set(existing_ids))
            print(f"No. of new mp3 files to download: {len(new_ids)}")
            download_ids_and_convert_to_mp3(new_ids, folder)
        else:
            download_list_subset_and_convert_to_mp3(webpath, folder, start, end)
    else:
        raise ValueError(f"Unknown webpath type: {webpath_type}")


def dmp3(
    folder: Path,
    webpath: str = None,
    start: int = None,
    end: int = None,
    refresh_folder_mode: bool = False,
    mp3: bool = True,
):
    if refresh_folder_mode:
        print("Refresh all folders mode")
        for sub_folder in folder.iterdir():
            if sub_folder.is_dir() and (sub_folder / ".dmp3").exists():
                print(f"Processing folder: {sub_folder}")
                process_folder_and_webpath(
                    folder=sub_folder,
                    webpath=None,
                    start=None,
                    end=None,
                    mp3=mp3,
                )
    else:
        print("Single folder mode")
        process_folder_and_webpath(
            folder=folder,
            webpath=webpath,
            start=start,
            end=end,
            mp3=mp3,
        )


def cli():
    args = argparser.parse_args()
    dmp3(**vars(args))


if __name__ == "__main__":
    cli()
