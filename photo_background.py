#!/usr/bin/env python3

import argparse
import requests
from PIL import Image
from io import BytesIO

import ctypes
import subprocess
import os
import platform
import random
import string

import constants

def string_gen(size=constants.FILENAME_LENGTH, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main(subject):
    print('Downloading photo ...')
    params = {'orientation': 'landscape', 'query': subject}
    headers = {'Authorization': 'Client-ID ' + constants.API_KEY,
                'Accept-Version': 'v1'}

    resp = requests.get(constants.API_URL, params=params, headers=headers)
    if not resp.status_code == 200:
        print('Error connecting to unsplash.')
        return 1
    json = resp.json()
    # from pprint import pprint; pprint(json)

    pic_url = json['urls']['full']
    resp = requests.get(pic_url)
    if not resp.status_code == 200:
        print('Error getting photo.')
        return 1
    ext = resp.headers['content-type'].split('/')[1]
    filename = string_gen() + '.' + ext

    # Save the returned image to disk:
    i = Image.open(BytesIO(resp.content))
    i.save(filename, ext)
    filepath = os.path.realpath(filename)
    print('Saved the photo to', filepath)
    set_background(filepath)

    resp = requests.get(url, headers=headers)
    if not resp.status_code == 200:
        print('Error while pinging download location.')
        return 1
    # print('Pinged download location per api guidelines.')

    username = json['user']['name']
    attribution = "Photograph by {} on Unsplash.".format(username)
    print(attribution)

    return 0


def set_background(filepath):
    opsys = platform.system()
    if opsys == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)
        print('Set photo as desktop background.')
    elif opsys == 'Linux':
        command = 'gsettings set org.gnome.desktop.background picture-uri {}'.format(filepath)
        os.system(command)
        print('Set photo as desktop background.')
    elif opsys == 'Darwin':
        SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""
        subprocess.Popen(SCRIPT%filepath, shell=True)
        print('Set photo as desktop background.')
    else:
        print('OS not supported.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line tool to automatically set a beautiful photograph as desktop background.')
    parser.add_argument('subject', help='The subject of the photograph', nargs='?', default=constants.DEFAULT_PHOTO_SUBJECT)
    args = parser.parse_args()

    main(args.subject)
