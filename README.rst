===============================
Youtube Playlist MP3 Downloader
===============================

Download youtube video or playlist into mp3 in a playlist folder. Also serve as a batch script example.

Installation
------------

Youtube-dl python package
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    pip install youtube-dl

This does all the work. Details:
https://github.com/ytdl-org/youtube-dl

Example direct usage:
https://gist.github.com/0xdomyz/8e906350b913a8e61ec1fd87a801d25f

FFMPEG
^^^^^^

1. Install from https://www.gyan.dev/ffmpeg/builds/
2. Add the bin folder that contains ``ffmpeg.exe`` to system path, so that it is available on cmd.

It converts medio formats, in this case to mp3. Details: https://ffmpeg.org/

Usage
-----

1. Get this batch script and put it into a folder called something like: ``music``.
2. Think of the folder to put the playlist, for example: ``starcraft_themes``.
3. Navigate to this location via command line, and run:

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

4. Results:

   .. code-block:: text
   
           music
           ├── dmp3.bat
           └── starcraft_themes
               ├── Starcraft Main Menu-J0lPR-XAW3g.mp3
               ├── Starcraft Brood War Intro-f80wJqOtirI.mp3
               ├── Terran Briefing Room - Starcraft Soundtrack-eINBamhiMVw.mp3
               └── ...

5. Help:

   .. code-block:: console
   
       dmp3
       dmp3 -h
       dmp3 -help
