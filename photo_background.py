#!/usr/bin/env python3

import argparse
import requests
from PIL import Image
from io import BytesIO

import os
import platform
import random
import string

def string_gen(size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main(subject):
    print('Downloading photo ...')
    url = 'https://api.unsplash.com/photos/random'
    params = {'orientation': 'landscape', 'query': subject}
    headers = {'Authorization': 'Client-ID 0effe79116d37cc227be6a361bd8d2e9d685abba78fab531b3040b0c7eed58d3',
                'Accept-Version': 'v1'}

    resp = requests.get(url, params=params, headers=headers)
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


def set_background(filepath):
    opsys = platform.system()
    if opsys == 'Windows':
        import ctypes
        ctypes.windll.user32.SystemParametersInfoA(20, 0, filepath, 0)
        print('Set photo as desktop background.')
    elif opsys == 'Linux':
        command = 'gsettings set org.gnome.desktop.background picture-uri {}'.format(filepath)
        os.system(command)
        print('Set photo as desktop background.')
    elif opsys == 'Darwin':
        import subprocess
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
    parser = argparse.ArgumentParser(description='Command line tool to automatically set a beautiful photo as desktop background.')
    parser.add_argument('subject', help='The subject of the photo', nargs='?', default='sunset')
    args = parser.parse_args()
    
    main(args.subject)