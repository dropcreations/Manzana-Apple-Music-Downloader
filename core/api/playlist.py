from core import parse

from . import lyrics

def parse_data(data):
    media = {}
    media_list = []

    id        = data["data"][0]["id"]
    resources = data["resources"]
    playlist  = resources["library-playlists"][id]
    library   = resources["library-songs"]
    attr      = playlist["attributes"]
    relations = playlist["relationships"]["tracks"]["data"]

    media["dir"] = parse.sanitize(
        "{} [{}]".format(
            attr["name"],
            id
        )
    )

    for relation in relations:
        lib_entry = library[relation["id"]]
        lib_rel = lib_entry["relationships"]["catalog"]["data"][0]
        item_type = lib_rel["type"]
        song_id = lib_rel["id"]

        song_entry = resources[item_type][song_id]
        song_rels = song_entry["relationships"]
        song_attr = song_entry["attributes"]

        album_id = song_rels["albums"]["data"][0]["id"]
        album_attr = resources["albums"][album_id]["attributes"]

        filename = parse.sanitize(
            "{} - {}{}".format(
                str(song_attr.get("trackNumber")).zfill(2),
                song_attr.get("name"),
                " [E]" if song_attr.get("contentRating") == "explicit" else ""
            )
        )

        artwork = song_attr["artwork"]
        cover = artwork["url"].format(
            w=artwork["width"],
            h=artwork["height"],
            f="jpg"
        )

        s = {
            "id": song_id,
            "genre": song_attr.get("genreNames"),
            "releasedate": song_attr.get("releaseDate"),
            "trackno": song_attr.get("trackNumber"),
            "isrc": song_attr.get("isrc"),
            "composer": song_attr.get("composerName"),
            "discno": song_attr.get("discNumber"),
            "song": song_attr.get("name"),
            "songartist": song_attr.get("artistName"),
            "rating": 4 if song_attr.get("contentRating") == "explicit" else 0,
            "file": filename,
            "coverUrl": cover,

            "copyright": album_attr.get("copyright"),
            "upc": album_attr.get("upc"),
            "recordlabel": album_attr.get("recordLabel"),
            "trackcount": album_attr.get("trackCount"),
            "album": album_attr.get("name"),
            "albumartist": album_attr.get("artistName"),
        }

        # -- TODO parse song credits

        if song_attr.get('hasLyrics') and song_attr['hasLyrics'] and "lyrics" in song_rels:
            if song_rels["lyrics"].get("data"):
                lyrics_rel = song_rels["lyrics"]["data"][0]
                lyrics_array = resources.get(lyrics_rel["type"])

                if lyrics_array:
                    lyrics_entry = lyrics_array[lyrics_rel["id"]]

                    if lyrics_entry and lyrics_entry.get("attributes"):
                        s.update(
                            lyrics.parse(
                                lyrics_entry["attributes"]["ttml"]
                            )
                        )

        if item_type == "songs":
            s["type"] = 1
        elif item_type == "music-videos":
            s["type"] = 6

        media_list.append(
            parse.opt(s)
        )

    media["tracks"] = media_list
    return media
