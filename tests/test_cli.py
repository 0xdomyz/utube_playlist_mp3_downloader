from pathlib import Path

from terminal import run_cmd_on_path

# from dmp3 import dmp3

# set up
_dir = Path("/home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir")

_playlist = "https://www.youtube.com/playlist?list=PLmXDcu9yx4WCHiLoBFvaXqC9ytNfTxvki"
_folder = Path(_dir / "starcraft_terran")

_playlist2 = "https://www.youtube.com/playlist?list=PLmXDcu9yx4WDVK_u65DLeqAzmLkqfdhA3"
_folder2 = Path(_dir / "diablo1")

_video = "https://www.youtube.com/watch?v=mD4GbGmvNRc&list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy&index=2&ab_channel=Katrulzin"
_video2 = "https://www.youtube.com/watch?v=zAS8KivZX5s&ab_channel=nudl3r"
_video_folder = Path(_dir / "various")

_channel = "https://www.youtube.com/@Diablo/videos"
_channel_folder = Path(_dir / "diablo")


# __file__ = "test_wsl.py"
_tool_dir = Path(__file__).resolve().parents[1]


# iterate over all files and folders and delete them
def kill_dir(path: Path):
    if Path(path).exists():
        for file in Path(path).glob("*"):
            if file.is_dir():
                kill_dir(file)
            else:
                file.unlink()
        Path(path).rmdir()


def kill_mp3(path: Path, n: int = None):
    # remove all if n None
    i = 0
    for file in Path(path).glob("*.mp3"):
        file.unlink()
        i += 1
        if n is not None and i >= n:
            break


def number_of_mp3_files(path: Path):
    return len(list(Path(path).glob("*.mp3")))


def run(cmd: str):
    run_cmd_on_path(f"echo {cmd} >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"echo '' >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"echo '' >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"{cmd} >> tests/test.log", _tool_dir)
    # run_cmd_on_path(cmd, _tool_dir)


# test
# todo better fixtures, no sequence dependency


def test_video():
    kill_dir(_video_folder)
    run(
        f"dmp3 {_video_folder} -w '{_video}'",
    )
    run(
        f"dmp3 {_video_folder} -w '{_video2}'",
    )

    # dmp3(
    #     folder=_video_folder,
    #     webpath=_video,
    # )
    # dmp3(
    #     folder=_video_folder,
    #     webpath=_video2,
    # )

    assert Path(_video_folder).exists()
    assert Path(_video_folder / ".dmp3").exists()
    assert number_of_mp3_files(_video_folder) == 2


# channel
def test_channel():
    kill_dir(_channel_folder)
    run(
        f"dmp3 {_channel_folder} -w {_channel} -e 1",
    )

    # dmp3(
    #     folder=_channel_folder,
    #     webpath=_channel,
    #     end=1,
    # )

    assert Path(_channel_folder).exists()
    assert Path(_channel_folder / ".dmp3").exists()
    assert number_of_mp3_files(_channel_folder) == 1


def test_refresh_channel():
    run(
        f"dmp3 {_channel_folder}",
    )

    # dmp3(folder=_channel_folder,)

    assert Path(_channel_folder).exists()
    assert Path(_channel_folder / ".dmp3").exists()
    assert number_of_mp3_files(_channel_folder) == 1


# playlist


def test_part_of_playlist():
    kill_dir(_folder)
    run(
        f"dmp3 {_folder} -w {_playlist} -s 1 -e 2",
    )

    # dmp3(
    #     folder=_folder,
    #     webpath=_playlist,
    #     start=1,
    #     end=2,
    # )

    assert Path(_folder).exists()
    assert Path(_folder / ".dmp3").exists()
    assert number_of_mp3_files(_folder) == 2


def test_entire_playlist():
    kill_dir(_folder)
    run(
        f"dmp3 {_folder} -w {_playlist}",
    )

    assert Path(_folder).exists()
    assert Path(_folder / ".dmp3").exists()
    assert number_of_mp3_files(_folder) >= 3


def test_refresh_part_of_playlist():
    n = number_of_mp3_files(_folder)
    kill_mp3(_folder, 2)
    run(
        f"dmp3 {_folder} -s 1 -e {n}",
    )
    assert number_of_mp3_files(_folder) == n


def test_refresh_entire_playlist():
    n = number_of_mp3_files(_folder)
    kill_mp3(_folder, 2)
    run(
        f"dmp3 {_folder}",
    )

    assert number_of_mp3_files(_folder) == n


def test_refresh_all_folders():
    kill_dir(_folder2)
    run(
        f"dmp3 {_folder2} -w {_playlist2}",
    )

    n = number_of_mp3_files(_folder)
    n2 = number_of_mp3_files(_folder2)
    n3 = number_of_mp3_files(_video_folder)
    n4 = number_of_mp3_files(_channel_folder)

    kill_mp3(_folder, 2)
    kill_mp3(_folder2, 2)
    # kill_dir(_video_folder)
    # kill_dir(_channel_folder)

    run(
        f"dmp3 {_folder.parent} -r",
    )

    assert number_of_mp3_files(_folder) == n
    assert number_of_mp3_files(_folder2) == n2
    assert number_of_mp3_files(_video_folder) == n3
    assert number_of_mp3_files(_channel_folder) == n4
