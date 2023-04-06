===============================
DMP3
===============================

Download youtube video or playlist, convert to mp3, store into a folder.

Features:

- Download all or subset of playlist
- Download only new playlist additions, once local storage folder is created
- Refresh local storage folder without respecifying link to playlist
- Refresh multiple local storage folders

Installation
------------

#. Install Python >= 3.9

#. Install dmp3 package from pypi

    .. code-block:: console

        pip install dmp3

#. Install `FFMPEG <https://ffmpeg.org/>`_, it converts medio formats. 

    - Linux

        .. code-block:: console

            sudo apt install ffmpeg

    - Windows
    
        #. Install from `ffmpeg download page <https://ffmpeg.org/download.html>`_, or `windows installer <https://www.gyan.dev/ffmpeg/builds/>`_.
        #. Add the bin folder that contains ``ffmpeg.exe`` to system path, so that it is available on command line.

Simple Usage
--------------

Linux:

.. code-block:: console

    dmp3 /mnt/d/media/music/game_theme/starcraft_terran -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy

Windows:

.. code-block:: console

    dmp3 "D:\media\music\game_theme\starcraft_terran" -w https://www.youtube.com/playlist?list=PLEtYTVnkBVuZWJ4Gsxtt80tWbiiyy1bcy


API
-------

   .. code-block:: console
   
        usage: dmp3 [-h] [-w WEBPATH] [-s START] [-e END] [-r] [-m MP3] folder

        Download youtube video or playlist, convert to mp3, store into a folder.

        If folder not exists, creates a folder.
        Otherwise, uses the folder, and will only download new videos from the playlist.

        If webpath is provided, creates a .dmp3 file in the folder to store the webpath for future use.
        If not provided, uses the webpath in the .dmp3 file in the folder stored previously.
        If not provided and no .dmp3 file is found in the folder, exits.

        If start and/or end are provided, download only the subset of the playlist.
        But will not download the videos that are already downloaded.

        positional arguments:
        folder                Folder to store mp3 files

        options:
        -h, --help            show this help message and exit
        -w WEBPATH, --webpath WEBPATH
                                Webpath to download from, creates a .dmp3 file insdie folder to store webpath
        -s START, --start START
                                Start index of the playlist
        -e END, --end END     End index of the playlist
        -r, --refresh_folder_mode
                                Refresh all mp3 folders in the folder, default is False.
                                In this mode, work through all sub folders with .mp3 inside, and download all new videos
        -m MP3, --mp3 MP3     Convert mp4 files to mp3 files in the folder (WIP)

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