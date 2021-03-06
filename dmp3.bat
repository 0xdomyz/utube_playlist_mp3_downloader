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
echo.   path: path to video
echo.   start: playlist start number, optional
echo.   end: playlist end number, optional
echo.
goto end

:start
set folder=%1
if not exist %folder%\ (mkdir %folder%)
cd %folder%
if [%3]==[] (goto case_no_start_end) else (goto case_start_end)

:case_no_start_end
youtube-dl -i -x --audio-format mp3 %2
goto end

:case_start_end
youtube-dl -i -x --audio-format mp3 --playlist-start %3 --playlist-end %4 %2
goto end

:end
popd
