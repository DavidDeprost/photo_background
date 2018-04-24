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
        print('Error getting wallpaper.')
        return 1
    ext = resp.headers['content-type'].split('/')[1]
    filename = string_gen() + '.' + ext

    i = Image.open(BytesIO(resp.content))
    i.save(filename, ext)
    filepath = os.path.realpath(filename)
    print('Saved the wallpaper to', filepath)
    set_background(filepath)


def set_background(filepath):
    opsys = platform.system()
    if opsys == 'Windows':
        import ctypes
        ctypes.windll.user32.SystemParametersInfoA(20, 0, filepath, 0)
        print('Set wallpaper as desktop background.')
    elif opsys == 'Linux':
        command = 'gsettings set org.gnome.desktop.background picture-uri {}'.format(filepath)
        os.system(command)
        print('Set wallpaper as desktop background.')
    elif opsys == 'Darwin':
        print('Mac OS is not yet supported.')
    else:
        print('OS not supported.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line tool to automatically set a beautiful wallpaper as background.')
    parser.add_argument('subject', help='The subject of the wallpaper', nargs='?', default='sunset')
    args = parser.parse_args()
    
    main(args.subject)