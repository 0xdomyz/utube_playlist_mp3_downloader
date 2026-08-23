import time
from pathlib import Path

from terminal import run_cmd_on_path

# from dmp3 import dmp3

# set up
_dir = Path(__file__).resolve().parent / "mp3_dir"

_video = "https://www.youtube.com/watch?v=zAS8KivZX5s"
_video_folder = Path(_dir / "various")

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


def number_of_files(path: Path):
    return len(list(Path(path).glob("*")))


def run(cmd: str):
    run_cmd_on_path(f'echo "{cmd}" >> tests/test.log', _tool_dir)
    run_cmd_on_path(f"echo '' >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"echo '' >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"{cmd}  >> tests/test.log", _tool_dir)
    time.sleep(1)  # Add 1 second cooldown after each command
    # run_cmd_on_path(cmd, _tool_dir)


# test
# todo better fixtures, no sequence dependency


def test_video():
    kill_dir(_video_folder)
    run(
        f"dmp3 {_video_folder} -w {_video}",
    )

    assert Path(_video_folder).exists()
    assert Path(_video_folder / ".dmp3").exists()
    assert number_of_mp3_files(_video_folder) == 1
    assert number_of_files(_video_folder) == 2

def test_video2():
    kill_dir(_video_folder)
    run(
        f"dmp3 {_video_folder} -w {_video} -v",
    )

    assert Path(_video_folder).exists()
    assert Path(_video_folder / ".dmp3").exists()
    assert number_of_mp3_files(_video_folder) == 0
    assert len(list(Path(_video_folder).glob("*.webm"))) == 1
    assert number_of_files(_video_folder) == 2

