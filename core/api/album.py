import m3u8
from m3u8 import M3U8
from core import parse

from . import lyrics

def parse_anim(data: M3U8):
    streamList = []
    for i, variants in enumerate(data.playlists):
        streamList.append(
            {
                "id": i,
                "fps": variants.stream_info.frame_rate,
                "codec": "AVC" if "avc" in variants.stream_info.codecs else "HEVC",
                "range": variants.stream_info.video_range,
                "bitrate": f'{round((variants.stream_info.average_bandwidth)/1000000, 2)} Mb/s',
                "resolution": f'{variants.stream_info.resolution[0]}x{variants.stream_info.resolution[1]}',
                "uri": variants.uri
            }
        )
    return streamList

def parse_data(data):
    media = {}
    media_list = []

    attr = data["attributes"]

    media["coverUrl"] = attr["artwork"]["url"].format(
        w=attr["artwork"].get("width"),
        h=attr["artwork"].get("height")
    )

    if "editorialVideo" in attr:
        animdata = {}
        if "motionDetailSquare" in attr["editorialVideo"]:
            __data = m3u8.load(attr["editorialVideo"]["motionDetailSquare"].get("video"))
            animdata['square'] = parse_anim(__data)
        if "motionDetailTall" in attr["editorialVideo"]:
            __data = m3u8.load(attr["editorialVideo"]["motionDetailTall"].get("video"))
            animdata['tall'] = parse_anim(__data)
        media["animartwork"] = animdata

    dirname = parse.sanitize(
        "{} - {} [{}]{}{}{}".format(
            attr.get("artistName"),
            attr.get("name"),
            data["id"],
            " [S]" if "Single" in attr.get("name") else "",
            " [EP]" if "EP" in attr.get("name") else "",
            " [E]" if attr.get("contentRating") == "explicit" else ""
        )
    )

    media["dir"] = dirname.replace(' - Single', '').replace(' - EP', '')

    a = {
        "copyright": attr.get("copyright"),
        "upc": attr.get("upc"),
        "recordlabel": attr.get("recordLabel"),
        "trackcount": attr.get("trackCount"),
        "album": attr.get("name"),
        "albumartist": attr.get("artistName")
    }

    for item in data["relationships"]["tracks"]["data"]:
        attr = item.get("attributes")

        filename = parse.sanitize(
            "{} - {}{}".format(
                str(attr.get("trackNumber")).zfill(2),
                attr.get("name"),
                " [E]" if attr.get("contentRating") == "explicit" else ""
            )
        )

        s = {
            "id": item.get("id"),
            "genre": attr.get("genreNames"),
            "releasedate": attr.get("releaseDate"),
            "trackno": attr.get("trackNumber"),
            "isrc": attr.get("isrc"),
            "composer": attr.get("composerName"),
            "discno": attr.get("discNumber"),
            "song": attr.get("name"),
            "songartist": attr.get("artistName"),
            "rating": 4 if attr.get("contentRating") == "explicit" else 0,
            "file": filename
        }

        rela = item.get("relationships")
        if not rela: rela = {}

        if "credits" in rela:
            credits = rela["credits"].get("data")
            if credits:

                roles = []
                creds = {}

                for catagory in credits:
                    for credit in catagory["relationships"]["credit-artists"]["data"]:
                        for role in credit["attributes"]["roleNames"]:
                            if not role in roles:
                                roles.append(role)
                                creds[role] = [credit["attributes"]["name"]]
                            else:
                                roleArtist: list = creds[role]
                                roleArtist.append(credit["attributes"]["name"])
                                creds[role] = roleArtist

                s["credits"] = creds

        if "lyrics" in rela:
            if rela["lyrics"].get("data"):
                if rela["lyrics"]["data"][0].get("attributes"):
                    s.update(
                        lyrics.parse(
                            rela["lyrics"]["data"][0]["attributes"]["ttml"]
                        )
                    )

        if item.get("type") == "songs":
            s["type"] = 1
        elif item.get("type") == "music-videos":
            s["type"] = 6

        s.update(a)
        media_list.append(
            parse.opt(s)
        )
    
    media["tracks"] = media_list
    return media
