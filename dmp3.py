# after import, use it to fetch items list from a youtube play list

import yt_dlp

playlist_url = "https://www.youtube.com/playlist?list=<playlist_id>"
with yt_dlp.YoutubeDL({"flat_playlist": True}) as ydl:
    playlist = ydl.extract_info(playlist_url, download=False)
    for video in playlist["entries"]:
        print(video["title"])

# list out files from a location in python, compare to that list

import os

path1 = "/path/to/directory1"
path2 = "/path/to/directory2"

files1 = set(os.listdir(path1))
files2 = set(os.listdir(path2))

common_files = files1 & files2
unique_files = files1 ^ files2

print("Common Files:")
for file in common_files:
    print(file)

print("Unique Files:")
for file in unique_files:
    print(file)


# download the ones that are not already in the local list

import os

path = "/path/to/directory"
local_files = set(os.listdir(path))

remote_files = ["file1.txt", "file2.txt", "file3.txt"]

for file in remote_files:
    if file not in local_files:
        with yt_dlp.YoutubeDL({"outtmpl": os.path.join(path, file)}) as ydl:
            ydl.download(["https://www.youtube.com/watch?v=<video_id>"])
