"""
Entire playlist:
python3.11 dmp3.py /mnt/d/media/music/starcraft_themes -w https://www.youtube.com/playlist?list=PL82284CFB34DC70F3
Part of playlist:
python3.11 dmp3.py /mnt/d/media/music/starcraft_themes -w https://www.youtube.com/playlist?list=PL82284CFB34DC70F3 -s 1 -e 10

Refresh entire playlist:
python3.11 dmp3.py /mnt/d/media/music/starcraft_themes
Refresh part of playlist:
python3.11 dmp3.py /mnt/d/media/music/starcraft_themes -s 1 -e 3

Refresh all folders:
python3.11 dmp3.py /mnt/d/media/music -r
"""

from pathlib import Path

from terminal import run_cmd_on_path

_playlist = "https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy"
_folder = Path("/mnt/d/media/music/game_theme/starcraft_terran")
# __file__ = "test_wsl.py"
_tool_dir = Path(__file__).resolve().parents[1]


def kill_folder():
    try:
        run_cmd_on_path(f"rm -rf {_folder.name}", _folder.parent)
        run_cmd_on_path(f"echo {_folder.name} killed >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
    except Exception:
        pass


def kill_mp3():
    try:
        run_cmd_on_path(f"rm -rf *.mp3", _folder)
        run_cmd_on_path(f"echo {_folder.name} mp3 killed >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
        run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
    except Exception:
        pass


def run(cmd: str):
    run_cmd_on_path(f"echo {cmd} >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"echo >> tests/test.log", _tool_dir)
    run_cmd_on_path(f"{cmd} >> tests/test.log", _tool_dir)


def test_entire_playlist():
    kill_folder()
    run(
        f"python3.11 dmp3.py {_folder} -w {_playlist}",
    )


def test_part_of_playlist():
    kill_folder()
    run(
        f"python3.11 dmp3.py {_folder} -w {_playlist} -s 1 -e 2",
    )


def test_refresh_entire_playlist():
    kill_mp3()
    run(
        f"python3.11 dmp3.py {_folder}",
    )


def test_refresh_part_of_playlist():
    kill_mp3()
    run(
        f"python3.11 dmp3.py {_folder} -s 1 -e 2",
    )


def test_refresh_all_folders():
    run(
        f"python3.11 dmp3.py {_folder.parent} -r",
    )
