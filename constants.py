#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
constants.py
"""
# Configuration parameters
API_KEY = \
    '0effe79116d37cc227be6a361bd8d2e9d685abba78fab531b3040b0c7eed58d3'
API_URL = 'https://api.unsplash.com/photos/random'
DEFAULT_PHOTO_SUBJECT = 'sunset'
FILENAME_LENGTH = 10

# Info strings
DESCRIPTION = ('Command line tool to automatically set a beautiful photograph '
               'as desktop background.')
SUBJECT_DESCRIPTION = 'The subject of the photograph'

# Text message constants
TEXT_ERROR_CONNECT = 'Error connecting to Unsplash.'
TEXT_ERROR_DOWNLOAD = 'Error getting photo.'
TEXT_ERROR_OS_UNSUPPORTED = 'System {} is not supported.'
TEXT_ERROR_PING = 'Error while pinging download location.'
TEXT_INFO_ATTRIBUTION = 'Photograph by {} on Unsplash.'
TEXT_INFO_DOWNLOADING = 'Downloading photo...'
TEXT_INFO_PICTURE_SET = 'Set photo as desktop background.'
TEXT_INFO_SAVE_PATH = 'Saved the photo to {}.'

# Literals for setting background
BACKGROUND_SET_LINUX = \
    'gsettings set org.gnome.desktop.background picture-uri {}'
BACKGROUND_SET_DARWIN = \
    """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

# General logic constants
ARG_SUBJECT = 'subject'
STATUS_CODE_OK = 200
SYSTEM_LINUX = 'Linux'
SYSTEM_OS_X = 'Darwin'
SYSTEM_WINDOWS = 'Windows'
WIN_SPI_SETBG = 20  # Parameter for setting desktop background in Windows
