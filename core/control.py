import os
import m3u8
import requests

from rich.console import Console

from core import parse
from core.api import AppleMusic

from core.process import download
from core.process import decrypt
from core.process import muxhls
from core.process import muxmv
from core.process import tag
from core.process import cc

from core.content import get_video
from core.content import get_audio
from core.content import get_animartwork

from utils import logger
from utils import keys
from utils import stats
from utils.stats import TEMPDIR
from utils.stats import OUTPUTDIR

cons = Console()

def run(args):
    try:
        aplm = AppleMusic()
        logger.info("Checking passed urls...")

        urls = parse.input_urls(args.url)
        urls = aplm.get_urls(urls)
        
        logger.info("Starting download process...")

        for url in urls:
            cons.print(f"\n\t[italic bold]URL: {url}[/]\n")
            data = aplm.get_info(url)

            for sub_data in data:
                dn = sub_data.get("dir")
                if not dn: dn = ""

                out_dir = os.path.join(OUTPUTDIR, dn)
                os.makedirs(out_dir, exist_ok=True)

                if aplm.kind != "playlist":
                    cover_data = requests.get(sub_data.get("coverUrl"), stream=True).content

                if args.anim:
                    __anh_fp = os.path.join(
                        TEMPDIR,
                        "hlsCover.mp4"
                    )

                    __ano_fp = os.path.join(
                        out_dir,
                        "Cover.mp4"
                    )
                    
                    if not os.path.exists(__ano_fp):
                        anim = get_animartwork(sub_data)
                        if anim:
                            uri = m3u8.load(anim.get("uri"))
                            uri = uri.base_uri + uri.segment_map[0].uri
                            
                            logger.info(f'Downloading "{anim["resolution"]}" artwork...')
                            download(uri, __anh_fp)

                            logger.info("Muxing animated artwork...")
                            rt = muxhls(__anh_fp, __ano_fp)
                            if rt == 0:
                                os.remove(__anh_fp)
                            else: logger.error("Muxing failed!")
                    else:
                        logger.info("Cover animation is already exists! skipping...")

                for track in sub_data["tracks"]:
                    if aplm.songId:
                        if track["id"] != aplm.songId:
                            continue

                    if track.get("coverUrl"):
                        cover_data = requests.get(track.get("coverUrl"), stream=True).content
                    
                    cons.print(f"[dim]{'-'*35}[/]")

                    if track["type"] == 1:
                        __enc_fp = os.path.join(
                            TEMPDIR,
                            "enc_aud_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __dec_fp = os.path.join(
                            TEMPDIR,
                            "dec_aud_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __mux_fp = os.path.join(
                            TEMPDIR,
                            "mux_aud_{}.m4a".format(
                                track["id"]
                            )
                        )

                        __out_fp = os.path.join(
                            out_dir,
                            f'{track["file"]}.m4a'
                        )

                        if os.path.exists(__out_fp):
                            logger.info(f'"{track["file"]}.m4a" is already exists! skipping...')
                            continue
                        
                    else:
                        __enc_v_fp = os.path.join(
                            TEMPDIR,
                            "enc_mv_vid_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __enc_a_fp = os.path.join(
                            TEMPDIR,
                            "enc_mv_aud_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __dec_v_fp = os.path.join(
                            TEMPDIR,
                            "dec_mv_vid_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __dec_a_fp = os.path.join(
                            TEMPDIR,
                            "dec_mv_aud_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __sub_fp = os.path.join(
                            TEMPDIR,
                            "sub_mv_{}.srt".format(
                                track["id"]
                            )
                        )

                        __mux_fp = os.path.join(
                            TEMPDIR,
                            "mux_mv_{}.mp4".format(
                                track["id"]
                            )
                        )

                        __out_fp = os.path.join(
                            out_dir,
                            f'{track["file"]}.mp4'
                        )

                        if args.skip:
                            if "album" in track:
                                logger.info(f'Skipping "{track["song"]}" music-video...')
                                continue

                        if os.path.exists(__out_fp):
                            logger.info(f'"{track["file"]}.mp4" is already exists! skipping...')
                            continue

                    gc = aplm.get_content(track)
                    if not gc: continue

                    if track["type"] == 1:
                        st = stats.get(track["id"])
                        if not st:
                            st = {
                                "isDownloaded": False,
                                "isDecrypted": False,
                                "isMuxed": False,
                                "isTagged": False
                            }
                        
                        if not st["isDownloaded"]:
                            if os.path.exists(__enc_fp):
                                os.remove(__enc_fp)

                            logger.info(f'Downloading "{track["file"]}"...')

                            download(
                                track["streams"]["uri"],
                                __enc_fp
                            )
                            
                            st["isDownloaded"] = True
                            stats.set(track["id"], st)
                        else: logger.info("Audio is already downloaded!")

                        if not st["isDecrypted"]:
                            if os.path.exists(__dec_fp):
                                os.remove(__dec_fp)

                            logger.info("Decrypting audio...")
                            __ky = keys.get(track["streams"]["pssh"])

                            rt = decrypt(
                                __enc_fp,
                                __dec_fp,
                                __ky
                            )

                            if rt == 0:
                                st["isDecrypted"] = True
                                stats.set(track["id"], st)
                                os.remove(__enc_fp)
                            else:
                                logger.error("Decryption failed!", 1)
                        else: logger.info("Audio is already decrypted!")

                        if not st["isMuxed"]:
                            if os.path.exists(__mux_fp):
                                os.remove(__mux_fp)

                            logger.info("Muxing audio...")

                            rt = muxhls(
                                __dec_fp,
                                __mux_fp
                            )

                            if rt == 0:
                                st["isMuxed"] = True
                                stats.set(track["id"], st)
                                os.remove(__dec_fp)
                            else:
                                logger.error("Muxing failed!", 1)
                        else: logger.info("Audio is already muxed!")

                        if not args.noTags:
                            if not st["isTagged"]:
                                logger.info("Tagging audio...")
                                
                                tag(
                                    __mux_fp,
                                    track,
                                    cover_data,
                                    [OUTPUTDIR, out_dir],
                                    args.noCover,
                                    args.noLrc
                                )
                                
                                st["isTagged"] = True
                                stats.set(track["id"], st)
                            else: logger.info("Audio is already tagged!")

                        if os.path.exists(__mux_fp):
                            os.renames(__mux_fp, __out_fp)

                    else:
                        st = stats.get(track["id"])
                        if not st:
                            st = {
                                "isVideoDownloaded": False,
                                "isAudioDownloaded": False,
                                "isVideoDecrypted": False,
                                "isAudioDecrypted": False,
                                "isMuxed": False,
                                "isTagged": False,
                                "vt": None,
                                "at": None
                            }

                        if st["vt"]: vt = st["vt"]
                        else:
                            vt = get_video(track.get("streams"))
                            st["vt"] = vt
                            stats.set(track["id"], st)


                        if not st["isVideoDownloaded"]:
                            if os.path.exists(__enc_v_fp):
                                os.remove(__enc_v_fp)

                            logger.info(f'Downloading "{track["file"]}" video...')

                            download(
                                vt["uri"],
                                __enc_v_fp
                            )
                            
                            st["isVideoDownloaded"] = True
                            stats.set(track["id"], st)
                        else: logger.info("Music-video's video stream is already downloaded!")

                        if not st["isVideoDecrypted"]:
                            if os.path.exists(__dec_v_fp):
                                os.remove(__dec_v_fp)

                            logger.info("Decrypting video...")
                            __ky = keys.get(vt["pssh"])

                            rt = decrypt(
                                __enc_v_fp,
                                __dec_v_fp,
                                __ky
                            )

                            if rt == 0:
                                st["isVideoDecrypted"] = True
                                stats.set(track["id"], st)
                                os.remove(__enc_v_fp)
                            else:
                                logger.error("Decryption failed!", 1)
                        else: logger.info("Music-video's video stream is already decrypted!")

                        if st["at"]: at = st["at"]
                        else:
                            at = get_audio(track.get("streams"))
                            st["at"] = at
                            stats.set(track["id"], st)

                        if not st["isAudioDownloaded"]:
                            if os.path.exists(__enc_a_fp):
                                os.remove(__enc_a_fp)

                            logger.info(f'Downloading "{track["file"]}" audio...')

                            download(
                                at["uri"],
                                __enc_a_fp
                            )
                            
                            st["isAudioDownloaded"] = True
                            stats.set(track["id"], st)
                        else: logger.info("Music-video's audio stream is already downloaded!")

                        if not st["isAudioDecrypted"]:
                            if os.path.exists(__dec_a_fp):
                                os.remove(__dec_a_fp)

                            logger.info("Decrypting audio...")
                            __ky = keys.get(at["pssh"])

                            rt = decrypt(
                                __enc_a_fp,
                                __dec_a_fp,
                                __ky
                            )

                            if rt == 0:
                                st["isAudioDecrypted"] = True
                                stats.set(track["id"], st)
                                os.remove(__enc_a_fp)
                            else:
                                logger.error("Decryption failed!", 1)
                        else: logger.info("Music-video's audio stream is already decrypted!")

                        if not st["isMuxed"]:
                            if os.path.exists(__mux_fp):
                                os.remove(__mux_fp)

                            logger.info("Extracting closed-captions...")
                            cc(__dec_v_fp, __sub_fp)
                            if os.path.getsize(__sub_fp) == 0:
                                logger.info("No closed-captions available!")
                                __sub_fp = None

                            logger.info("Muxing music-video...")
                            rt = muxmv(
                                __dec_v_fp,
                                __dec_a_fp,
                                __mux_fp,
                                at,
                                __sub_fp
                            )

                            if rt == 0:
                                st["isMuxed"] = True
                                stats.set(track["id"], st)
                                os.remove(__dec_v_fp)
                                os.remove(__dec_a_fp)
                                if __sub_fp:
                                    os.remove(__sub_fp)
                            else:
                                logger.error("Muxing failed!", 1)
                        else: logger.info("Music-video is already muxed!")

                        if not args.noTags:
                            if not st["isTagged"]:
                                logger.info("Tagging music-video...")
                                
                                tag(
                                    __mux_fp,
                                    track,
                                    cover_data,
                                    [OUTPUTDIR, out_dir],
                                    args.noCover,
                                    args.noLrc
                                )
                                
                                st["isTagged"] = True
                                stats.set(track["id"], st)
                            else: logger.info("Music-video is already tagged!")

                        if os.path.exists(__mux_fp):
                            os.renames(__mux_fp, __out_fp)

                if not args.noCover:
                    if aplm.kind != "music-video" and aplm.kind != "playlist":
                        with open(os.path.join(out_dir, 'Cover.jpg'), 'wb') as fp:
                            fp.write(cover_data)
        
        cons.print(f"[dim]{'-'*35}[/]")

        logger.info("Cleaning temp...")
        for t in os.listdir(TEMPDIR):
            os.remove(
                os.path.join(TEMPDIR, t)
            )

        logger.info("Done.")
        
    except KeyboardInterrupt:
        logger.error("Interrupted by user!")