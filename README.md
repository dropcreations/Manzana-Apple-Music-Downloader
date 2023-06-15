# Manzana Apple Music Downloader

A python program to download albums and songs with `AAC` codec in `.m4a` container format and music-videos upto 4K in `AVC` or `HEVC` codec in `.mp4` format from Apple Music. This python program uses the module called pywidevine that is a python implementation of Google's Widevine DRM (Digital Rights Management) CDM (Content Decryption Module). This doesn't support to download spatial audios (Dolby Atmos) and Apple Lossless audios (Apple ALAC) because those are not protected with Widevine. They are protected with the FairPlay. [FairPlay](https://en.wikipedia.org/wiki/FairPlay) is a digital rights management (DRM) technology developed by Apple Inc.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/darkmode.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/lightmode.png">
  <img alt="Apple Music" src="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/lightmode.png">
</picture>

# ⚠ DISCLAIMER

- __THIS REPOSITORY IS ONLY FOR EDUCATIONAL PURPOSES.__

This will help you to understand how the Apple Music API works and how to deal with python scripts. This is basically created for Windows OS. If you want you can change the binaries and the script to work with Linux, MacOS...etc. To use this repository you need to find some stuff. see the code.

### Demo

- `MusicVideo` : [DJ Snake - Taki Taki](https://music.apple.com/lk/music-video/taki-taki-feat-selena-gomez-ozuna-cardi-b/1438473545)

![musicVideo](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/demo_musicVideo.gif)

- `Album` : [Doja Cat - Planet Her](https://music.apple.com/lk/album/planet-her-deluxe/1574004234)

![album](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Downloader/main/assets/demo_album.gif)

### Mediainfo

- `MusicVideo`: [DJ Snake - Taki Taki](https://music.apple.com/lk/music-video/taki-taki-feat-selena-gomez-ozuna-cardi-b/1438473545)

```
Format                      : MPEG-4
Format profile              : Base Media
Codec ID                    : isom (isom/iso2/mp41)
File size                   : 342 MiB
Duration                    : 3 min 51 s
Overall bit rate mode       : Variable
Overall bit rate            : 12.4 Mb/s
Frame rate                  : 23.976 FPS
Movie name                  : Taki Taki (feat. Selena Gomez, Ozuna & Cardi B)
Performer                   : DJ Snake
Genre                       : Dance
ContentType                 : Music Video
Recorded date               : 2018-10-09
ISRC                        : USUMV1801044
Rating                      : Explicit

Video
ID                          : 1
Format                      : HEVC
Format/Info                 : High Efficiency Video Coding
Format profile              : Main 10@L5@High
Codec ID                    : hvc1
Codec ID/Info               : High Efficiency Video Coding
Duration                    : 3 min 51 s
Source duration             : 3 min 51 s
Bit rate                    : 12.1 Mb/s
Width                       : 3 832 pixels
Height                      : 1 434 pixels
Display aspect ratio        : 2.672
Frame rate mode             : Variable
Frame rate                  : 23.976 FPS
Minimum frame rate          : 23.976 FPS
Maximum frame rate          : 24.768 FPS
Color space                 : YUV
Chroma subsampling          : 4:2:0
Bit depth                   : 10 bits
Scan type                   : Progressive
Bits/(Pixel*Frame)          : 0.092
Stream size                 : 334 MiB (98%)
Source stream size          : 334 MiB (98%)
Title                       : Core Media Video
Language                    : English
Color range                 : Limited
Color primaries             : BT.709
Transfer characteristics    : BT.709
Matrix coefficients         : BT.709
mdhd_Duration               : 231606
Codec configuration box     : hvcC

Audio
ID                          : 2
Format                      : AAC LC
Format/Info                 : Advanced Audio Codec Low Complexity
Codec ID                    : mp4a-40-2
Duration                    : 3 min 51 s
Bit rate mode               : Constant
Bit rate                    : 248 kb/s
Channel(s)                  : 2 channels
Channel layout              : L R
Sampling rate               : 48.0 kHz
Frame rate                  : 46.875 FPS (1024 SPF)
Compression mode            : Lossy
Stream size                 : 6.85 MiB (2%)
Title                       : Core Media Audio
Default                     : Yes
Alternate group             : 1

Text
ID                          : 3
Format                      : Timed Text
Muxing mode                 : sbtl
Codec ID                    : tx3g
Duration                    : 3 min 45 s
Bit rate mode               : Variable
Bit rate                    : 126 b/s
Frame rate                  : 0.749 FPS
Stream size                 : 3.47 KiB (0%)
Default                     : Yes
Forced                      : No
Alternate group             : 3
Count of events             : 84
```

- `Album`: [Doja Cat - Planet Her](https://music.apple.com/lk/album/planet-her-deluxe/1574004234)

```
Format                      : MPEG-4
Format profile              : Apple audio with iTunes info
Codec ID                    : M4A  (isom/M4A /mp42)
File size                   : 9.69 MiB
Duration                    : 2 min 52 s
Overall bit rate mode       : Variable
Overall bit rate            : 471 kb/s
Album                       : Planet Her (Deluxe)
Album/Performer             : Doja Cat
Part/Position               : 1
Part/Total                  : 1
Track name                  : Woman
Track name/Position         : 1
Track name/Total            : 19
Performer                   : Doja Cat
Composer                    : Amala Zandile Dlamini / David Sprecher / Aaron Horn / Aynzli Jones / Linden Jay / Lydia Asrat / Jidenna
Lyricist                    : Aaron Horn / Amala Zandile Dlamini / Aynzli Jones / David Sprecher / Jidenna / Linden Jay / Lydia Asrat
Label                       : Kemosabe Records/RCA Records
Genre                       : Pop / Music
ContentType                 : Music
Recorded date               : 2021-06-25
Encoded date                : 2023-03-26 19:26:20 UTC
Tagged date                 : 2023-03-26 19:26:20 UTC
ISRC                        : USRC12101532
Copyright                   : ℗ 2021 Kemosabe Records/RCA Records
Cover                       : Yes
Lyrics                      : Hey, woman / Woman / Let me be your woman / Woman, woman, woman / I can be your woman / Woman, woman, woman / Let me be your woman / Woman, woman, woman / I can be your woman / Woman, woman, woman / What you need / She give tenfold, come here, papa, plant your seed / She can grow it from her womb, a family / Provide lovin' overlooked and unappreciated, you see / You can't reciprocate / I got delicious taste, you need a woman's touch in your place / Just protect her and keep her safe / Baby, worship my hips and waist / So feminine with grace / I touch your soul when you hear me say, "Boy" / Let me be your woman / Woman / Let me be your woman / Woman, woman, woman / I can be your woman / Woman, woman, woman / Let me be your woman / Woman, woman, woman (Ay) / I can be your woman / Woman, woman, woman / I can't be your lady, I'm a / Woman, I'm a motherfucker, but they got a problem / Put some babies in your life and take away the drama / Put that paper in the picture like a diorama / Gotta face a lot of people love the opposite / 'Cause the world told me, "We ain't got that common sense" / Gotta prove it to myself that I'm on top of shit / And you will never know a god without the goddesses / Honest, it's fuckin' honest, kiddin' / I could be on everything / I mean, I could be the leader, head of all the states / I could smile and jiggle it till his pockets empty / I could be the CEO just like a Robyn Fenty / And I'ma be there for you 'cause you on my team, girl / Don't ever think you ain't 'head of these n*****, dream girl / They wanna pit us against each other when we succeed / And for no reasons, they wanna see us end up like we Regina on Mean Girls / Princess or queen, tomboy or king (Yeah) / You've heard a lot, you've never seen (Nah) / Mother Earth, Mother Mary rise to the top / Divine feminine, I'm feminine (Why?) / Woman (Daddy) / Let me be your woman (Let me be your) / Woman, woman, woman (Let me be, let me be your) / I can be your woman / Woman, woman, woman (Daddy) / Let me be your woman (I know) / Woman, woman, woman (Daddy) / I can be your woman / Woman, woman, woman / Hey, woman / Hey, woman / Hey, woman / Hey, woman
Rating                      : Explicit
UPC                         : 886449410538

Audio
ID                          : 1
Format                      : AAC LC
Format/Info                 : Advanced Audio Codec Low Complexity
Codec ID                    : mp4a-40-2
Duration                    : 2 min 52 s
Bit rate mode               : Variable
Bit rate                    : 265 kb/s
Maximum bit rate            : 369 kb/s
Channel(s)                  : 2 channels
Channel layout              : L R
Sampling rate               : 44.1 kHz
Frame rate                  : 43.066 FPS (1024 SPF)
Compression mode            : Lossy
Stream size                 : 5.48 MiB (57%)
Encoded date                : 2022-08-13 13:39:59 UTC
Tagged date                 : 2023-03-26 19:26:20 UTC
```

- Samples [here](https://drive.google.com/drive/folders/191ZdiG6Rfv23ivfIwSGBAuyrVgcBUsYv)

### Note

- Use the Windows Terminal app for better experience
- Inspired by the [script](https://github.com/loveyoursupport/AppleMusic-Downloader) by [loveyoursupport](https://github.com/loveyoursupport)
