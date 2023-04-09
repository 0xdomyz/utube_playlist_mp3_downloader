from pathlib import Path

from dmp3 import dmp3

# set up
_dir = Path("/home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir")

_playlist = "https://www.youtube.com/playlist?list=PLmXDcu9yx4WCHiLoBFvaXqC9ytNfTxvki"
_folder = Path(_dir / "starcraft_terran")


# iterate over all files and folders and delete them
def kill_dir(path: Path):
    if Path(path).exists():
        for file in Path(path).glob("*"):
            if file.is_dir():
                kill_dir(file)
            else:
                file.unlink()
        Path(path).rmdir()


def number_of_mp3_files(path: Path):
    return len(list(Path(path).glob("*.mp3")))


# test
# todo better fixtures, no sequence dependency

# playlist


def test_part_of_playlist():
    kill_dir(_folder)

    dmp3(
        folder=_folder,
        webpath=_playlist,
        start=1,
        end=2,
    )

    assert Path(_folder).exists()
    assert Path(_folder / ".dmp3").exists()
    assert number_of_mp3_files(_folder) == 2
