===============================
DMP3
===============================

Download youtube video or playlist or channel, convert to mp3, store into a folder.

Features:

- Download all or subset of playlist
- Download all or most recent n videos from channel
- Download only additional items, once local storage folder is created
- Refresh local storage folder with saved parameters
- Refresh multiple local storage folders

Installation
------------

#. Install Python 3.9, 3.10, or 3.11.

#. Install package from pypi.

    .. code-block:: console

        pip install -U dmp3

#. Install `FFMPEG <https://ffmpeg.org/>`_, it converts media formats. 

    Linux

    .. code-block:: console

        sudo apt install ffmpeg

    Windows
    
    #. Install from `ffmpeg download page <https://ffmpeg.org/download.html>`_,
       most likely use `windows installer <https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip>`_.
    #. Add the bin folder that contains ``ffmpeg.exe`` to system path,
       so that it is available on command line.

Simple Usage
--------------

Linux:

.. code-block:: console

    cd /home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir
    dmp3 starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy

Windows:

.. code-block:: console

    dmp3 "D:\media\music\game_theme\starcraft_terran" -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy

Example results:

.. code-block:: text

    mp3_dir/
    ├── diablo1
    │   ├── .dmp3
    │   ├── Diablo 1 [OST] - 01 - Intro-Y7P7vrvEQYc.mp3
    │   ├── Diablo 1 [OST] - 02 - Town-SEpydfXj87M.mp3
    │   ├── Diablo 1 [OST] - 03 - Dungeon-yQCg-uHOrZk.mp3
    │   ├── Diablo 1 [OST] - 04 - Catacombs-FPQPJwVX-60.mp3
    │   ├── Diablo 1 [OST] - 05 - Caves-J9OIyH21ZKo.mp3
    │   └── Diablo 1 [OST] - 06 - Hell-5PBG92gkL7I.mp3
    └── starcraft_terran
        ├── .dmp3
        ├── StarCraft - Terran Theme 1-mD4GbGmvNRc.mp3
        ├── Starcraft 2 Soundtrack - Terran 01-zAS8KivZX5s.mp3
        ├── Starcraft 2 Soundtrack - Terran 02-sNbTg0Li36k.mp3
        ├── Starcraft 2 Soundtrack - Terran 03-dssNa11htIM.mp3
        ├── Starcraft 2 Soundtrack - Terran 04-4YfQjho2IOk.mp3
        ├── Starcraft 2 Soundtrack - Terran 05-fQluJBSXM5I.mp3
        ├── Terran Theme 2 - Starcraft Soundtrack-_R1QLIo16DY.mp3
        ├── Terran Theme 3 - Starcraft Soundtrack-xcEHDqji74A.mp3
        └── Terran Theme 4 (Brood War) - Starcraft Soundtrack-l9XSZw67QpY.mp3

Refresh multiple local storage folders, each tracking a playlist or a channel:

.. code-block:: console

    cd /home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir
    dmp3 . -r

Usage in python script:

.. code-block:: Python

        from dmp3.dmp3 import dmp3
        from pathlib import Path

        folder = Path("/home/user/Projects/utube_playlist_mp3_downloader/tests/mp3_dir/starcraft_terran")
        webpath = "https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy"

        dmp3(folder=folder)
        dmp3(folder=folder, webpath=webpath, start=1, end=3, refresh_folder_mode=False, mp3=True)

API
-------

   .. code-block:: console
   
        usage: dmp3 [-h] [-w WEBPATH] [-s START] [-e END] [-r] [-m MP3] folder

        Download youtube video or playlist or channel, convert to mp3, store into a folder.

        Creates folder if not exists.
        Otherwise only download additional mp3 into the folder.

        If webpath is provided, creates a .dmp3 file in the folder to store parameters.
        If not provided, uses saved parameter.

        If start and/or end are provided, download only the subset in addition to already downloaded.
        If not provided, uses saved parameters if any.

        positional arguments:
        folder                Folder to store mp3 files

        options:
        -h, --help            show this help message and exit
        -w WEBPATH, --webpath WEBPATH
                                Webpath to download from, creates a .dmp3 file insdie folder to store parameters
        -s START, --start START
                                Start index of the playlist
        -e END, --end END     End index of the playlist
        -r, --refresh_folder_mode
                                Refresh all mp3 folders in the folder, default is False
        -m MP3, --mp3 MP3     Convert video to mp3 files in the folder, default is True (WIP)

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
