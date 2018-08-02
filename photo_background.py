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
    print(constants.TEXT_INFO_DOWNLOADING)

    params = {'orientation': 'landscape', 'query': subject}
    headers = {'Authorization': 'Client-ID ' + constants.API_KEY,
                'Accept-Version': 'v1'}

    resp = requests.get(constants.API_URL, params=params, headers=headers)
    if not resp.status_code == constants.STATUS_CODE_OK:
        print(constants.TEXT_ERROR_CONNECT)
        return 1
    json = resp.json()
    # from pprint import pprint; pprint(json)

    pic_url = json['urls']['full']
    resp = requests.get(pic_url)
    if not resp.status_code == constants.STATUS_CODE_OK:
        print(constants.TEXT_ERROR_DOWNLOAD)
        return 1
    ext = resp.headers['content-type'].split('/')[1]
    filename = string_gen() + '.' + ext

    # Save the returned image to disk:
    i = Image.open(BytesIO(resp.content))
    i.save(filename, ext)
    filepath = os.path.realpath(filename)
    print(constants.TEXT_INFO_SAVE_PATH.format(filepath))
    set_background(filepath)

    resp = requests.get(url, headers=headers)
    if not resp.status_code == constants.STATUS_CODE_OK:
        print(constants.TEXT_ERROR_PING)
        return 1
    # print('Pinged download location per api guidelines.')

    username = json['user']['name']
    print(constants.TEXT_INFO_ATTRIBUTION.format(username))

    return 0


def set_background(filepath):
    opsys = platform.system()
    if opsys == constants.SYSTEM_WINDOWS:
        ctypes.windll.user32.SystemParametersInfoW(constants.WIN_SPI_SETBG, 0, filepath, 0)
        print(constants.TEXT_INFO_PICTURE_SET)
    elif opsys == constants.SYSTEM_LINUX:
        os.system(constants.BACKGROUND_SET_LINUX.format(filepath))
        print(constants.TEXT_INFO_PICTURE_SET)
    elif opsys == constants.SYSTEM_OS_X:
        subprocess.Popen(constants.BACKGROUND_SET_DARWIN % filepath,
                         shell=True)
        print(constants.TEXT_INFO_PICTURE_SET)
    else:
        print(constants.TEXT_ERROR_OS_UNSUPPORTED.format(opsys))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=constants.DESCRIPTION)
    parser.add_argument(constants.ARG_SUBJECT, help=constants.SUBJECT_DESCRIPTION, nargs='?', default=constants.DEFAULT_PHOTO_SUBJECT)
    args = parser.parse_args()

    main(args.subject)
