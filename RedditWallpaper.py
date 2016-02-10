import os
import praw
from PIL import Image
import random
import sys
import urllib.request

directory = "/home/samuel/Pictures/Wallpapers/"
subreddits = ["earthporn", "animalporn", "wallpaper", "topwalls", "wallpapers", "cats"]

def main(subredditChoice):
    user_agent = "python:RedditWallpapers:v2.0 (by /u/suryoye)"
    r = praw.Reddit(user_agent=user_agent)

    subreddit = r.get_subreddit(subredditChoice)

    for submission in subreddit.get_top_from_day():
        image_name = submission.url.split("/")[-1]

        print(submission.url)

        if not allowed_extension(image_name):
            continue

        try:
            urllib.request.urlretrieve(submission.url, directory+image_name)
        except urllib.error.HTTPError:
            continue

        if allowed_resolution(directory+image_name):
            os.system("gsettings set org.gnome.desktop.background picture-uri file://%(path)s" % {'path':directory+image_name})
            os.system("gsettings set org.gnome.desktop.background picture-options wallpaper")
            break
        else:
            os.system("rm %s" % directory+image_name)


def allowed_extension(image):
    if image.split(".")[-1] in ["jpg", "png"]:
        return True
    else:
        False

def allowed_resolution(image):
    with Image.open(image) as img:
        if img.size[0] >= 1920 and img.size[1] >= 1080:
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(random.choice(subreddits))