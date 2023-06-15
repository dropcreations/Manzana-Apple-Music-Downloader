import m3u8
from api.lyrics import getLyrics

def song(data, syncpoints, animartwork=False):
    info = {}
    attr = data["data"][0]["relationships"]["albums"]["data"][0]["attributes"]

    name = attr["name"]

    if " - EP" in name:
        name = name.replace(" - EP", "") + " [EP]"
    if " - Single" in name:
        name = name.replace(" - Single", "") + " [S]"

    __dir = "{0} - {1} [{2}]".format(
        attr["artistName"],
        name,
        data["data"][0]["relationships"]["albums"]["data"][0]["id"]
    )

    if "contentRating" in attr:
        if attr["contentRating"] == "explicit":
            __dir += " [E]"

    info["dir"] = __dir

    if "artwork" in attr:
        info["coverUrl"] = attr["artwork"].get("url").format(
            w=attr["artwork"].get("width"),
            h=attr["artwork"].get("height")
        )

    if animartwork:
        if "editorialVideo" in attr:
            if "motionDetailSquare" in attr["editorialVideo"]:
                m3u8Url = attr["editorialVideo"]["motionDetailSquare"].get("video")
                m3u8data = m3u8.load(m3u8Url).data

                streamList = []

                for i, variants in enumerate(m3u8data["playlists"]):
                    codec = variants["stream_info"].get("codecs")

                    if "avc" in codec: codec = "AVC"
                    elif "hvc" in codec: codec = "HEVC"

                    streamList.append(
                        {
                            "id": i,
                            "fps": variants["stream_info"].get("frame_rate"),
                            "codec": codec,
                            "range": variants["stream_info"].get("video_range"),
                            "bitrate": f'{round((variants["stream_info"].get("average_bandwidth"))/1000000, 2)} Mb/s',
                            "resolution": variants["stream_info"].get("resolution"),
                            "uri": variants.get("uri")
                        }
                    )

                info["animartwork"] = streamList

    trackList = []
    tracks = data["data"]

    for track in tracks:
        __info = {}
        __info["id"] = track.get("id")
        
        attr = track["attributes"]

        if "albumName" in attr: __info["album"] = attr.get("albumName")
        if "genreNames" in attr: __info["genre"] = ', '.join(attr.get("genreNames"))
        if "trackNumber" in attr: __info["tracknumber"] = attr.get("trackNumber")
        if "releaseDate" in attr: __info["releasedate"] = attr.get("releaseDate")
        if "isrc" in attr: __info["isrc"] = attr.get("isrc")
        if "audioLocale" in attr: __info["language"] = attr.get("audioLocale")
        if "composerName" in attr: __info["composer"] = attr.get("composerName")
        if "discNumber" in attr: __info["discnumber"] = attr.get("discNumber")
        if "name" in attr: __info["track"] = attr.get("name")
        if "artistName" in attr: __info["trackartist"] = attr.get("artistName")

        __file = "{0} - {1}".format(
            str(attr.get("trackNumber")).zfill(2),
            attr.get("name")
        )

        if "contentRating" in attr:
            __info["rating"] = attr.get("contentRating")
            if attr.get("contentRating") == "explicit":
                __file += " [E]"

        __info["file"] = __file

        attr = track["relationships"]["albums"]["data"][0]["attributes"]

        if "copyright" in attr: __info["copyright"] = attr.get("copyright")
        if "upc" in attr: __info["upc"] = attr.get("upc")
        if "recordLabel" in attr: __info["recordlabel"] = attr.get("recordLabel")
        if "trackCount" in attr: __info["trackcount"] = attr.get("trackCount")
        if "artistName" in attr: __info["albumartist"] = attr.get("artistName")

        if "lyrics" in track["relationships"]:
            if len(track["relationships"]["lyrics"].get("data")) > 0:
                __info.update(getLyrics(track["relationships"]["lyrics"]["data"][0]["attributes"].get("ttml"), syncpoints))

        __info["type"] = 1

        trackList.append(__info)
        
    info["tracks"] = trackList
    return info