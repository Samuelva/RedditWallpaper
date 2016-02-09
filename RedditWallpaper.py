import imghdr
import os
import praw
from pprint import pprint
import struct
import sys
import urllib.request
from time import sleep

directory = "/media/samuel/Data/Afbeeldingen/Wallpapers/"
subreddits = ["earthporn", "animalporn", ""]

def main():
    user_agent = "python:RedditWallpapers:v2.0 (by /u/suryoye)"
    r = praw.Reddit(user_agent=user_agent)

    subreddit = r.get_subreddit("animalporn")

    for submission in subreddit.get_top_from_day():
        image_name = submission.url.split("/")[-1]

        if not validate_submission(image_name):
            continue

        urllib.request.urlretrieve(submission.url, directory+image_name)
        resolution = get_image_size(directory+image_name)

        if validate_resolution(resolution):
            os.system("gsettings set org.gnome.desktop.background picture-uri file://%(path)s" % {'path':directory+image_name})
            os.system("gsettings set org.gnome.desktop.background picture-options wallpaper")
            break
        else:
            os.system("rm %s" % directory+image_name)


def validate_submission(image_name):
    print(image_name.split(".")[-1])
    if image_name.split(".")[-1] in ["jpg", "png", "gif"]:
        return True
    else:
        False


def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                fhandle.seek(1, 1)
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:
                return
        else:
            return
        return width, height

def validate_resolution(resolution):
    if resolution[0] >= 1920 and resolution[1] >= 1080:
        return True
    else:
        return False


main()