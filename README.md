# Manzana Apple Music Downloader

A python program to download albums and songs with `AAC` codec in `.m4a` container format and music-videos upto 4K in `AVC` or `HEVC` codec in `.mp4` format from Apple Music. This python program uses the module called pywidevine that is a python implementation of Google's Widevine DRM (Digital Rights Management) CDM (Content Decryption Module). This doesn't support to download spatial audios (Dolby Atmos) and Apple Lossless audios (ALAC) because those are not protected with Widevine. They are protected with the FairPlay. [FairPlay](https://en.wikipedia.org/wiki/FairPlay) is a digital rights management (DRM) technology developed by Apple Inc.


<center>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/darkmode.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/lightmode.png">
    <img alt="Apple Music" src="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/lightmode.png">
  </picture>
</center>

# ! DISCLAIMER

- __THIS REPOSITORY IS ONLY FOR EDUCATIONAL PURPOSES.__

This will help you to understand how the Apple Music API works and how to deal with python scripts. You can use the source code to run and test this program or you can also use the compiled binary files from the [releases](https://github.com/dropcreations/Manzana-Apple-Music-Downloader/releases).

## Features

- Can download __album__ urls.
- Can download __song__ urls.
- Can download __music-video__ urls.
- Can download __playlist__ urls.
- Can download __artist__ urls (all albums, singles, music-videos).
- Can download __animated-cover__.
- Can download __time-synced lyrics__ as `.lrc`.

## Required

Make sure you have installed below in your PC or have added into the PATH.

- MP4Box
- mp4decrypt (bento4)
- ccextractor

## Usage

First of all you have to clone this project to your pc. If you're using git, you can do it simply by following command.

```
git clone https://github.com/dropcreations/Manzana-Apple-Music-Downloader.git
```

or you're not using git, just download the source code as a `.zip` file and extract it. Then go to the project directory.

This is a python program. So, you have to install `python` first (Recommended python version is `3.9`). Then you have to install all dependancies that need to run this program. You can approach this using below command.

```
pip install -r requirements.txt
```

__NOTE:__ Use `python3` or `pip3` if `python` or `pip` doesn't work for you.

Now you can run the program. In first run it will create all directories that need to deal inside the program. You have to fill the things that it will ask for. Firstly, it will ask to put your Widevine device files into `device` directory.

So, copy your widevine device directory to it. it should contain `device_client_id_blob` and  `device_private_key` files. Example for the file structure inside the `device` directory given below.

```
.
.
|--config
|--device
|  |--{device_name}
|      |--device_client_id_blob
|      |--device_private_key
|--keys
.
.
```

Then it will also ask for your `mediaUserToken`. Get it from cookies and add it to the program. You can get help page using below command.

```
python manzana.py -h
```

it will show you the help page.

```
usage: manzana [-h] [-v] [-a] [-s] [-ln] [-tn] [-cn] url [url ...]

Manzana: Apple Music Downloader

positional arguments:
  url               Apple Music URL(s) for artist, album, song, playlist or music-video

optional arguments:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit
  -a, --anim-cover  save animated artwork. [default: False]
  -s, --skip-video  skip music-videos inside albums. [default: False]
  -ln, --no-lrc     don't save time-synced lyrics. [default: False]
  -tn, --no-tags    don't add credits info. [default: False]
  -cn, --no-cover   don't save album artwork. [default: False]
```

Now you can start.

```
python manzana.py {url(s)},...
```

You can input multiple urls at one time. Just add `url_01 url_02 url_03...` with a `space` separator. You also can add text files that have urls. Just like `url_01 txt_file_path_01 url_02...`. If you're going to use a text file, urls must be in line by line as below.

```
https://music.apple.com/url_01
https://music.apple.com/url_02
https://music.apple.com/url_03
https://music.apple.com/url_04
.
.
```

__NOTE:__ When you're downloading an artist, if you want all items, just type `all` keyword when it ask for an ID.

__THIS IS FOR PRIVATE USE ONLY. TAKE YOUR OWN RISK AND USE IT!__

### Demo

- `MusicVideo` : [DJ Snake - Taki Taki](https://music.apple.com/lk/music-video/taki-taki-feat-selena-gomez-ozuna-cardi-b/1438473545)

![musicVideo](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/demo_musicVideo.gif)

- `Album` : [Doja Cat - Planet Her](https://music.apple.com/lk/album/planet-her-deluxe/1574004234)

![album](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/demo_album.gif)

- `Artist` : [Taylor Swift](https://music.apple.com/lk/artist/taylor-swift/159260351)

![artist](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/demo_artist.gif)

### Note

- Use the Windows Terminal app for better experience
- Inspired by the [script](https://github.com/loveyoursupport/AppleMusic-Downloader) by [loveyoursupport](https://github.com/loveyoursupport)
