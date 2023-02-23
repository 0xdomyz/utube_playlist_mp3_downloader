@echo off

pushd %~dp0

if "%1"=="" goto help
if "%1"=="h" goto help
if "%1"=="help" goto help
goto start

:help
echo.
echo.Download youtube video or playlist into mp3 in a playlist folder
echo.
echo.usage: folder path start end
echo.   folder: folder(create if not exist) to download into
echo.   path: path to video, often need to be quoted
echo.   start: playlist start number, optional
echo.   end: playlist end number, optional
echo.
echo.For example:
echo.    dmp3 starcraft_themes "https://www.youtube.com/playlist?list=PL82284CFB34DC70F3"
goto end

:start
set folder=%1
if not exist %folder%\ (mkdir %folder%)
cd %folder%
if [%3]==[] (goto case_no_start_end) else (goto case_start_end)

:case_no_start_end
yt-dlp -i -x --audio-format mp3 %2
goto end

:case_start_end
yt-dlp -i -x --audio-format mp3 --playlist-start %3 --playlist-end %4 %2
goto end

:end
popd
