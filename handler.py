import os
import sys

from sanitize_filename import sanitize

from api import AppleMusic
from utils import Logger
from core import getAnimArtwork, getAudios, getVideos, tag
from core import download, muxhls, decrypt, cc, muxmv

logger = Logger()

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

CACHE = os.path.join(__get_path(), "cache")
CONFIG = os.path.join(__get_path(), "config")

def __temp():
    if os.path.exists("__encrypted.mp4"):
        os.remove("__encrypted.mp4")
    if os.path.exists("__decrypted.mp4"):
        os.remove("__decrypted.mp4")
    if os.path.exists("__muxed.m4a"):
        os.remove("__muxed.m4a")
    if os.path.exists("__encrypted_video.mp4"):
        os.remove("__encrypted_video.mp4")
    if os.path.exists("__decrypted_video.mp4"):
        os.remove("__decrypted_video.mp4")
    if os.path.exists("__encrypted_audio.mp4"):
        os.remove("__encrypted_audio.mp4")
    if os.path.exists("__decrypted_audio.mp4"):
        os.remove("__decrypted_audio.mp4")
    if os.path.exists("__decrypted_video.srt"):
        os.remove("__decrypted_video.srt")
    if os.path.exists("__sub.srt"):
        os.remove("__sub.srt")
    if os.path.exists("Cover.jpg"):
        os.remove("Cover.jpg")
    if os.path.exists("Cover.mp4"):
        os.remove("Cover.mp4")

def __sanitize(path):
    if path != "":
        return sanitize(path)
    return path

def arguments(args):
    __temp()

    syncMsPointCount = 2
    if args.sync: syncMsPointCount = 3

    applemusic = AppleMusic(CACHE, CONFIG, syncMsPointCount, args.anim)
    data = applemusic.getInfo(args.url)

    __dir = data.get("dir")

    if os.path.exists(
        os.path.join(__sanitize(__dir), "Cover.jpg")
    ):
        logger.warning('"Cover.jpg" is already exists!')
    else:
        if not args.no_cover:
            if "coverUrl" in data:
                if os.path.exists("Cover.jpg"): os.remove("Cover.jpg")
                download(
                    data.get("coverUrl"),
                    os.getcwd(),
                    "Cover.jpg",
                    "Downloading album artwork..."
                )

    if os.path.exists(
        os.path.join(__sanitize(__dir), "Cover.mp4")
    ):
        logger.warning('"Cover.mp4" is already exists!')
    else:
        if args.anim:
            anim = getAnimArtwork(data)
            if anim:
                if os.path.exists("Cover.mp4"): os.remove("Cover.mp4")
                download(
                    anim,
                    os.getcwd(),
                    "Cover.mp4",
                    "Downloading animated artwork..."
                )
                if os.path.exists("Cover.mp4"):
                    logger.info("Muxing animated artwork...")
                    if muxhls("Cover.mp4", "_Cover.mp4") == 0:
                        os.remove("Cover.mp4")
                        os.rename("_Cover.mp4", "Cover.mp4")
                    else:
                        logger.error("Muxing failed! Ignoring muxing...")
                        if os.path.exists("_Cover.mp4"): os.remove("_Cover.mp4")

    for track in data["tracks"]:
        content = applemusic.getStreamInfo(
            track.get("id"),
            track.get("type")
        )

        __file = track.get("file")

        if "streamUrl" in content:
            if os.path.exists(
                os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.m4a")
            ):
                logger.warning(f'"{__file}.m4a" is already exists!')
            else:
                download(
                    content.get("streamUrl"),
                    os.getcwd(),
                    "__encrypted.mp4",
                    f'Downloading "{__file}.m4a"...'
                )
                logger.info("Decrypting audio...")
                if decrypt(
                    "__encrypted.mp4",
                    "__decrypted.mp4",
                    content.get("decryptKey")
                ) == 0:
                    os.remove("__encrypted.mp4")
                    logger.info("Muxing audio...")
                    if muxhls(
                        "__decrypted.mp4",
                        "__muxed.m4a"
                    ) == 0:
                        os.remove("__decrypted.mp4")
                        if os.path.exists("Cover.jpg"):
                            try:
                                os.renames(
                                    "Cover.jpg",
                                    os.path.join(__sanitize(__dir), "Cover.jpg")
                                )
                            except FileExistsError:
                                logger.warning('"Cover.jpg" is already exists!')
                        if os.path.exists("Cover.mp4"):
                            try:
                                os.renames(
                                    "Cover.mp4",
                                    os.path.join(__sanitize(__dir), "Cover.mp4")
                                )
                            except FileExistsError:
                                logger.warning('"Cover.mp4" is already exists!')
                        logger.info("Tagging audio...")
                        tag(
                            "__muxed.m4a",
                            track,
                            os.path.join(__sanitize(__dir), "Cover.jpg"),
                            "__muxed.lrc",
                            nocover=args.no_cover,
                            nolrc=args.no_lrc
                        )
                        os.renames(
                            "__muxed.m4a",
                            os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.m4a")
                        )
                        if not args.no_lrc: os.renames(
                            "__muxed.lrc",
                            os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.lrc")
                        )
                    else:
                        if os.path.exists("__decrypted.mp4"): os.remove("__decrypted.mp4")
                        if os.path.exists("__muxed.m4a"): os.remove("__muxed.m4a")
                        logger.error("Muxing failed!", 1)
                else:
                    if os.path.exists("__encrypted.mp4"): os.remove("__encrypted.mp4")
                    if os.path.exists("__decrypted.mp4"): os.remove("__decrypted.mp4")
                    logger.error("Decryption failed!", 1)
        else:
            if os.path.exists(
                os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.mp4")
            ):
                logger.warning(f'"{__file}.mp4" is already exists!')
            else:
                videoUrl, decryptKey = getVideos(content)
                download(
                    videoUrl,
                    os.getcwd(),
                    "__encrypted_video.mp4",
                    f'Downloading "{__file}" video...'
                )
                logger.info("Decrypting video...")
                if decrypt(
                    "__encrypted_video.mp4",
                    "__decrypted_video.mp4",
                    decryptKey
                ) == 0:
                    os.remove("__encrypted_video.mp4")
                else:
                    if os.path.exists("__encrypted_video.mp4"): os.remove("__encrypted_video.mp4")
                    if os.path.exists("__decrypted_video.mp4"): os.remove("__decrypted_video.mp4")
                    logger.error("Decryption failed!", 1)

                audioUrl, decryptKey = getAudios(content)
                download(
                    audioUrl,
                    os.getcwd(),
                    "__encrypted_audio.mp4",
                    f'Downloading "{__file}" audio...'
                )
                logger.info("Decrypting audio...")
                if decrypt(
                    "__encrypted_audio.mp4",
                    "__decrypted_audio.mp4",
                    decryptKey
                ) == 0:
                    os.remove("__encrypted_audio.mp4")
                else:
                    if os.path.exists("__encrypted_audio.mp4"): os.remove("__encrypted_audio.mp4")
                    if os.path.exists("__decrypted_audio.mp4"): os.remove("__decrypted_audio.mp4")
                    if os.path.exists("__decrypted_video.mp4"): os.remove("__decrypted_video.mp4")
                    logger.error("Decryption failed!", 1)

                sub = None

                if content.get("closed-captions") != []:
                    logger.info("Extracting Closed-Captions...")
                    if cc(
                        "__decrypted_video.mp4"
                    ) == 0:
                        os.rename(
                            "__decrypted_video.srt",
                            "__sub.srt"
                        )
                        sub = "__sub.srt"
                    else:
                        if os.path.exists("__decrypted_video.srt"): os.remove("__decrypted_video.srt")
                        logger.error("Closed-Captions extraction failed!")
                else: logger.info("No Closed-Captions available!")

                logger.info("Muxing music-video...")
                if muxmv(
                    "__decrypted_video.mp4",
                    "__decrypted_audio.mp4",
                    "__output.mp4",
                    sub
                ) == 0:
                    os.remove("__decrypted_video.mp4")
                    os.remove("__decrypted_audio.mp4")
                    if sub: os.remove(sub)
                    logger.info("Tagging music-video...")
                    tag(
                        "__output.mp4",
                        track,
                        "",
                        "",
                        nocover=args.no_cover,
                        nolrc=args.no_lrc
                    )
                    os.renames(
                        "__output.mp4",
                        os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.mp4")
                    )
                else:
                    if os.path.exists("__decrypted_video.mp4"): os.remove("__decrypted_video.mp4")
                    if os.path.exists("__decrypted_audio.mp4"): os.remove("__decrypted_audio.mp4")
                    if sub:
                        if os.path.exists(sub): os.remove(sub)
                    if os.path.exists("__output.mp4"): os.remove("__output.mp4")
                    logger.error("Muxing music-video failed!", 1)
    logger.info("Done.")
