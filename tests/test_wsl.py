from pathlib import Path

from terminal import run_cmd_on_path

_playlist = "https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy"
_folder = Path(
    "/home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir/starcraft_terran"
)
_folder2 = Path(
    "/home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir/diablo1"
)
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


# todo better fixtures
# no sequence dependency


def test_part_of_playlist():
    kill_dir(_folder)
    run(
        f"dmp3 {_folder} -w {_playlist} -s 1 -e 2",
    )

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
    kill_mp3(_folder)
    run(
        f"dmp3 {_folder} -e 2",
    )
    assert number_of_mp3_files(_folder) == 2


def test_refresh_entire_playlist():
    kill_mp3(_folder)
    run(
        f"dmp3 {_folder}",
    )

    assert number_of_mp3_files(_folder) >= 3


def test_refresh_all_folders():
    n = number_of_mp3_files(_folder)
    n2 = number_of_mp3_files(_folder2)

    kill_mp3(_folder, 2)
    kill_mp3(_folder2, 2)

    run(
        f"dmp3 {_folder.parent} -r",
    )

    assert number_of_mp3_files(_folder) == n
    assert number_of_mp3_files(_folder2) == n2
