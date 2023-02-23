===============================
Youtube Playlist MP3 Downloader
===============================

Download youtube video or playlist into mp3 in a playlist folder.

Installation
------------

#. Install yt-dlp python package

    .. code-block:: console

        pip install yt-dlp

    Details see `pypi link <https://pypi.org/project/yt-dlp/>`_

#. Install FFMPEG

    #. Install from `ffmpeg download page <https://ffmpeg.org/download.html>`_
    #. In case of windows, can use `installer <https://www.gyan.dev/ffmpeg/builds/>`_
    #. Add the bin folder that contains ``ffmpeg.exe`` to system path, so that it is available on command line.

    It converts medio formats, in this case to mp3. `Details <https://ffmpeg.org/>`_

Usage
-----

#. Download the ``dmp3.bat`` file and put it into a folder. For example inside ``E:\\music``.
#. Think of a name for the folder to put the playlist, for example: ``starcraft_themes``.
#. Navigate to this location via command line, and run:

   .. code-block:: console
   
       cd /d E:\music

   .. code-block:: console
   
       dmp3 starcraft_themes "https://www.youtube.com/playlist?list=PL82284CFB34DC70F3"
   
   Alternatively, only download a continuous subset in the list, say from 2nd to 3rd:
   
   .. code-block:: console
   
       dmp3 starcraft_themes "https://www.youtube.com/playlist?list=PL82284CFB34DC70F3" 2 3
   
   Alternatively, just a song:
   
   .. code-block:: console
   
       dmp3 starcraft_themes "https://www.youtube.com/watch?v=J0lPR-XAW3g"

#. Results:

   .. code-block:: text
   
           music
           ├── dmp3.bat
           └── starcraft_themes
               ├── Starcraft Main Menu-J0lPR-XAW3g.mp3
               ├── Starcraft Brood War Intro-f80wJqOtirI.mp3
               ├── Terran Briefing Room - Starcraft Soundtrack-eINBamhiMVw.mp3
               └── ...

#. Help:

   .. code-block:: console
   
       dmp3
       dmp3 -h
       dmp3 -help
