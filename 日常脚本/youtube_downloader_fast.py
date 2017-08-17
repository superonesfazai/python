# Requirements:
#   youtube-dl
#   aria2c

import subprocess
import sys

video_link, threads = sys.argv[1], sys.argv[2]
subprocess.call([
    "youtube-dl",
    video_link,
    "--external-downloader",
    "aria2c",
    "--external-downloader-args",
    "-x"+threads
])
