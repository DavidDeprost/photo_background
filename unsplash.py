#!/usr/bin/env python3

import argparse
import requests
import shutil
from pprint import pprint
from PIL import Image
from io import BytesIO

def main(subject):
    url = 'https://api.unsplash.com/photos/random'
    params = {'orientation': 'landscape', 'query': subject}
    headers = {'Authorization': 'Client-ID 0effe79116d37cc227be6a361bd8d2e9d685abba78fab531b3040b0c7eed58d3',
                'Accept-Version': 'v1'}

    json = requests.get(url, params=params, headers=headers).json()
    # pprint(json)

    pic_url = json['urls']['full']
    resp = requests.get(pic_url)
    if resp.status_code == 200:
        ext = resp.headers['content-type'].split('/')[1]
        print(ext)
        i = Image.open(BytesIO(resp.content))
        i.save('surprise2', ext)
    # resp = requests.get(pic_url, stream=True)
    # if resp.status_code == 200:
    #     with open('surprise', 'wb') as f:
    #         resp.raw.decode_content = True
    #         shutil.copyfileobj(resp.raw, f)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line tool to automatically set a beautiful wallpaper as background.')
    parser.add_argument('subject', help='The subject of the wallpaper')
    args = parser.parse_args()
    
    main(args.subject)