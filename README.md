# photo_background
Simple script that downloads a random photo from Unsplash, and sets it as the desktop background.

I was loosely inspired by [this Rust code](https://github.com/faebser/beautiful-wallpaper-every-day/blob/master/src/main.rs);
finding it hard to follow, I decided to rewrite it in Python.

## Dependencies
pip install requests pillow

## Usage
photo_background.py [-h] [subject]

positional arguments:
  subject     The subject of the photograph

optional arguments:
  -h, --help  show this help message and exit

## Problems
### Linux
* Only Gnome based distro's are supported.
* When using Python from Anaconda, you might run into the following notification:
"GLib-GIO-Message: Using the 'memory' GSettings backend.  Your settings will not be saved or shared with other applications."
If this occurs, settings are not saved, and the background will not be changed. There is an easy fix though:
Add "export GIO_EXTRA_MODULES=/usr/lib/x86_64-linux-gnu/gio/modules/" to your .bashrc or .zshrc.
